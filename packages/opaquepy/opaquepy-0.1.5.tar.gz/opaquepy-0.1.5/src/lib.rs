use argon2::Argon2;
use curve25519_dalek;
use curve25519_dalek::ristretto::RistrettoPoint;
use opaque_ke::ciphersuite::CipherSuite;
use sha2;
use rand::{rngs::OsRng};
use opaque_ke::{CredentialFinalization, CredentialRequest,
                RegistrationRequest, RegistrationUpload, ServerLogin, ServerLoginFinishResult,
                ServerLoginStartParameters, ServerLoginStartResult, ServerRegistration,
                ServerRegistrationStartResult};
use opaque_ke::keypair::{Key, KeyPair};
use pyo3::prelude::*;
use base64;
use base64::DecodeError;
use digest::Digest;
use digest::generic_array::GenericArray;
use digest::generic_array::typenum::Unsigned;
use opaque_ke::errors::{InternalPakeError, PakeError, ProtocolError};
use opaque_ke::hash::Hash;
use opaque_ke::slow_hash::SlowHash;
use pyo3::exceptions::PyValueError;

struct DefaultCipher;
impl CipherSuite for DefaultCipher {
    type Group = curve25519_dalek::ristretto::RistrettoPoint;
    type KeyExchange = opaque_ke::key_exchange::tripledh::TripleDH;
    type Hash = sha2::Sha512;
    type SlowHash = ArgonWrapper;
}

pub struct ArgonWrapper(Argon2<'static>);

impl<D: Hash> SlowHash<D> for ArgonWrapper {
    fn hash(
        input: GenericArray<u8, <D as Digest>::OutputSize>,
    ) -> Result<Vec<u8>, InternalPakeError> {
        let params = Argon2::default();
        let mut output = vec![0u8; <D as Digest>::OutputSize::to_usize()];
        params
            .hash_password_into(
                &input,
                &[0; argon2::MIN_SALT_LEN],
                &mut output,
            )
            .map_err(|_| InternalPakeError::SlowHashError)?;
        Ok(output)
    }
}

#[pymodule]
fn opaquepy(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    let opqrust = PyModule::new(py, "_opqrust")?;
    opqrust.add_function(wrap_pyfunction!(generate_keys_py, opqrust)?)?;
    opqrust.add_function(wrap_pyfunction!(register_server_py, opqrust)?)?;
    opqrust.add_function(wrap_pyfunction!(register_server_finish_py, opqrust)?)?;
    opqrust.add_function(wrap_pyfunction!(login_server_py, opqrust)?)?;
    opqrust.add_function(wrap_pyfunction!(login_server_finish_py, opqrust)?)?;

    m.add_submodule(opqrust)?;

    Ok(())
}

#[pyfunction]
fn generate_keys_py() -> (String, String) {
    let keypair = generate();
    let private_key = keypair.private().to_vec();
    let public_key = keypair.public().to_vec();

    let private_encoded = base64::encode_config(private_key, base64::URL_SAFE_NO_PAD);
    let public_encoded = base64::encode_config(public_key, base64::URL_SAFE_NO_PAD);

    (private_encoded, public_encoded)
}

trait ToPyErr {
    fn to_pyerr(self) -> PyErr;
}

impl ToPyErr for ProtocolError {
    fn to_pyerr(self) -> PyErr {
        PyValueError::new_err(format!("{:?}", self))
    }
}

impl ToPyErr for PakeError {
    fn to_pyerr(self) -> PyErr {
        PyValueError::new_err(format!("{:?}", self))
    }
}

impl ToPyErr for DecodeError {
    fn to_pyerr(self) -> PyErr {
        PyValueError::new_err(self.to_string())
    }
}

#[pyfunction]
fn register_server_py(client_request: String, public_key: String) -> PyResult<(String, String)> {
    let request_bytes = base64::decode_config(client_request, base64::URL_SAFE_NO_PAD)
        .map_err(ToPyErr::to_pyerr)?;
    let client_request: RegistrationRequest<DefaultCipher> = RegistrationRequest::deserialize(&request_bytes)
        .map_err(ToPyErr::to_pyerr)?;
    let key_bytes = base64::decode_config(public_key, base64::URL_SAFE_NO_PAD)
        .map_err(ToPyErr::to_pyerr)?;
    let public_key = Key::from_bytes(&key_bytes)
        .map_err(ToPyErr::to_pyerr)?;

    let s = server_register(client_request, &public_key)
        .map_err(ToPyErr::to_pyerr)?;

    let response_bytes = s.message.serialize();
    let state_bytes = s.state.serialize();

    let response_encoded = base64::encode_config(response_bytes, base64::URL_SAFE_NO_PAD);
    let state_encoded = base64::encode_config(state_bytes, base64::URL_SAFE_NO_PAD);

    Ok((response_encoded, state_encoded))
}

#[pyfunction]
fn register_server_finish_py(client_request_finish: String, registration_state: String) -> PyResult<String> {
    let request_bytes = base64::decode_config(client_request_finish, base64::URL_SAFE_NO_PAD)
        .map_err(ToPyErr::to_pyerr)?;
    let client_request_finish: RegistrationUpload<DefaultCipher> = RegistrationUpload::deserialize(&request_bytes)
        .map_err(ToPyErr::to_pyerr)?;

    let state_bytes = base64::decode_config(registration_state, base64::URL_SAFE_NO_PAD)
        .map_err(ToPyErr::to_pyerr)?;
    let registration_state: ServerRegistration<DefaultCipher> = ServerRegistration::deserialize(&state_bytes)
        .map_err(ToPyErr::to_pyerr)?;

    let s = server_register_finish(client_request_finish, registration_state)
        .map_err(ToPyErr::to_pyerr)?;

    let password_file_bytes = s.serialize();

    let password_file_encoded = base64::encode_config(password_file_bytes, base64::URL_SAFE_NO_PAD);

    Ok(password_file_encoded)
}

#[pyfunction]
fn login_server_py(password_file: String, client_request: String, private_key: String) -> PyResult<(String, String)> {
    let password_file_bytes = base64::decode_config(password_file, base64::URL_SAFE_NO_PAD)
        .map_err(ToPyErr::to_pyerr)?;
    let password_file= ServerRegistration::<DefaultCipher>::deserialize(&password_file_bytes)
        .map_err(ToPyErr::to_pyerr)?;

    let request_bytes = base64::decode_config(client_request, base64::URL_SAFE_NO_PAD)
        .map_err(ToPyErr::to_pyerr)?;
    let client_request: CredentialRequest<DefaultCipher> = CredentialRequest::deserialize(&request_bytes)
        .map_err(ToPyErr::to_pyerr)?;

    let key_bytes = base64::decode_config(private_key, base64::URL_SAFE_NO_PAD)
        .map_err(ToPyErr::to_pyerr)?;
    let private_key = Key::from_bytes(&key_bytes)
        .map_err(ToPyErr::to_pyerr)?;

    let s = server_login(password_file, &private_key, client_request)
        .map_err(ToPyErr::to_pyerr)?;

    let response_bytes = s.message.serialize()
        .map_err(ToPyErr::to_pyerr)?;
    let state_bytes = s.state.serialize()
        .map_err(ToPyErr::to_pyerr)?;

    let response_encoded = base64::encode_config(response_bytes, base64::URL_SAFE_NO_PAD);
    let state_encoded = base64::encode_config(state_bytes, base64::URL_SAFE_NO_PAD);

    Ok((response_encoded, state_encoded))
}

#[pyfunction]
fn login_server_finish_py(client_request_finish: String, login_state: String) -> PyResult<String> {
    let request_bytes = base64::decode_config(client_request_finish, base64::URL_SAFE_NO_PAD)
        .map_err(ToPyErr::to_pyerr)?;
    let client_request_finish: CredentialFinalization<DefaultCipher> = CredentialFinalization::deserialize(&request_bytes)
        .map_err(ToPyErr::to_pyerr)?;

    let state_bytes = base64::decode_config(login_state, base64::URL_SAFE_NO_PAD)
        .map_err(ToPyErr::to_pyerr)?;
    let login_state: ServerLogin<DefaultCipher> = ServerLogin::deserialize(&state_bytes)
        .map_err(ToPyErr::to_pyerr)?;

    let s = server_login_finish(client_request_finish, login_state)
        .map_err(ToPyErr::to_pyerr)?;

    let session_key_bytes = s.session_key;

    let session_key_encoded = base64::encode_config(session_key_bytes, base64::URL_SAFE_NO_PAD);

    Ok(session_key_encoded)
}

fn generate() -> KeyPair<RistrettoPoint> {
    let mut rng = OsRng;
    DefaultCipher::generate_random_keypair(&mut rng)
}

fn server_register(client_request: RegistrationRequest<DefaultCipher>, public_key: &Key) -> Result<ServerRegistrationStartResult<DefaultCipher>, ProtocolError> {

    let mut server_rng = OsRng;
    ServerRegistration::<DefaultCipher>::start(
        &mut server_rng,
        client_request,
        public_key,
    )
}

fn server_register_finish(client_request_finish: RegistrationUpload<DefaultCipher>, registration_state: ServerRegistration<DefaultCipher>)
    -> Result<ServerRegistration<DefaultCipher>, ProtocolError> {

    registration_state.finish(
        client_request_finish
    )
}

fn server_login(password_file: ServerRegistration<DefaultCipher>, private_key: &Key, client_request: CredentialRequest<DefaultCipher>)
    -> Result<ServerLoginStartResult<DefaultCipher>, ProtocolError> {

    let mut server_rng = OsRng;
    ServerLogin::start(
        &mut server_rng,
        password_file,
        private_key,
        client_request,
        ServerLoginStartParameters::default(),
    )
}

fn server_login_finish(client_request_finish: CredentialFinalization<DefaultCipher>, login_state: ServerLogin<DefaultCipher>)
    -> Result<ServerLoginFinishResult<DefaultCipher>, ProtocolError> {
    login_state.finish(
        client_request_finish
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn gen_test() {
        let (privt, publ) = generate_keys_py();
        println!("{}", privt);
        println!("{}", publ);
    }

    #[test]
    fn server_register() {
        //password 'garbage'
        let message = "Pj8bFY58CZoyi9Rsp2KyS4HhA2vXcSEAFH7BViwxRzw".to_string();
        let pub_string = "OhKbj6rzdot9c9y_RCcFcIKYozF2OaOHW7A6-UhveQo".to_string();

        let (response, state) = register_server_py(message, pub_string).unwrap();
        println!("{}", response);
        println!("{}", state);
    }

    #[test]
    fn server_register_finish() {
        let client_message = "WiiA158EDDe0lHHfg0C8HrhAnAh3AUfqanzVbsajm0IBmDAbxVcbUp5MVFm759dCz5YvNYlpZw5NQoaQFAJHkPmufK3_FFdV87nQ7bfp7BZ5BURZgLp6O_b0FlE80IKksTQFXN2mo8QqrVlIQPJ1DiAtr5FGuXqaSkduYkJyGRLXy_RzSmkME8Fs1zYqTPM-fAzzRjbRJBfOKdcuiJSzyFU".to_string();
        let server_state = "bdbAbu6_ZGoJUShySB6qx8oQrpNXz3CCWd_7qC1J2ws".to_string();
        let password_file = register_server_finish_py(client_message, server_state).unwrap();
        println!("{}", password_file)

        // example file:
        // bdbAbu6_ZGoJUShySB6qx8oQrpNXz3CCWd_7qC1J2wtaKIDXnwQMN7SUcd-DQLweuECcCHcBR-pqfNVuxqObQgGYMBvFVxtSnkxUWbvn10LPli81iWlnDk1ChpAUAkeQ-a58rf8UV1XzudDtt-nsFnkFRFmAuno79vQWUTzQgqSxNAVc3aajxCqtWUhA8nUOIC2vkUa5eppKR25iQnIZEtfL9HNKaQwTwWzXNipM8z58DPNGNtEkF84p1y6IlLPIVQ
    }

    #[test]
    fn server_login() {
        let client_message = "UD06GXLMCcJr-EaYonw0zKGQ9FMeMJ55Mh_H5yJ2S1AuF_sQmykFADMj9vdgA1Umw2SwtH0Tai0lOdF1WAM0TAAA_gVx9nSVv9YgIw5aMsrg67LJTZBm7DDQG4O6XpK9Rlw".to_string();
        // password 'abc'
        let password_file = "bdbAbu6_ZGoJUShySB6qx8oQrpNXz3CCWd_7qC1J2wtaKIDXnwQMN7SUcd-DQLweuECcCHcBR-pqfNVuxqObQgGYMBvFVxtSnkxUWbvn10LPli81iWlnDk1ChpAUAkeQ-a58rf8UV1XzudDtt-nsFnkFRFmAuno79vQWUTzQgqSxNAVc3aajxCqtWUhA8nUOIC2vkUa5eppKR25iQnIZEtfL9HNKaQwTwWzXNipM8z58DPNGNtEkF84p1y6IlLPIVQ".to_string();
        let private_key = "QNxnQ_c-rx2nmuLAOTln5Ul60XYqNz_yws_WG8BoAAc".to_string();

        let (response, state) = login_server_py(password_file, client_message, private_key).unwrap();

        println!("{}", response);
        println!("{}", state);
    }

    #[test]
    fn server_login_finish() {
        // correspond to above
        let client_message = "YHLmz1dB6XXkFabmzSctR53HskpKEWcZVvXEcswegia2OVbC4NezY1jqhzGN-z7trO8SCe_IbEyeg1n04UkJXw".to_string();
        let state = "3soQ8dLh007sMpOUvyBM4o0FDp-sHHXMu-WU1rtofMtjT5veRMmrv3KmZDTaAzGTxP442NYS-0_XpjPyLN_O9_UKQV92Cv6YvpFWwrNJlye_XfrwUV9fm9JCCA5R0CHCN9PVcrarW_1-GmSd5KitAr57LeS0Ne6fWZsYtI6yM6GkphmMAcxzykJxtyqicpmF3gjesD-Nbgktp7A3d066kHUZ4DRredc9NaF-gdVg76PtE8dVuL9aVEN2reciq54U".to_string();

        let session = login_server_finish_py(client_message, state).unwrap();

        println!("{}", session)
    }
}
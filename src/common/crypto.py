# standard imports
import os

# lib imports
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from datetime import datetime, timedelta, UTC

# local imports
from common import definitions
from common import logger

log = logger.get_logger(name=__name__)

CERT_FILE = os.path.join(definitions.Paths.CONFIG_DIR, "cert.pem")
KEY_FILE = os.path.join(definitions.Paths.CONFIG_DIR, "key.pem")


def check_expiration(cert_path: str) -> int:
    with open(cert_path, "rb") as cert_file:
        cert_data = cert_file.read()
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    expiry_date = cert.not_valid_after_utc
    return (expiry_date - datetime.now(UTC)).days


def generate_certificate():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    subject = issuer = x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, u"localhost"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(UTC)
    ).not_valid_after(
        datetime.now(UTC) + timedelta(days=365)
    ).sign(private_key, hashes.SHA256())

    with open(KEY_FILE, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption(),
        ))

    with open(CERT_FILE, "wb") as f:
        f.write(cert.public_bytes(Encoding.PEM))


def initialize_certificate() -> tuple[str, str]:
    log.info("Initializing SSL certificate")
    if os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE):
        cert_expires_in = check_expiration(CERT_FILE)
        log.info(f"Certificate expires in {cert_expires_in} days.")
        if cert_expires_in >= 90:
            return CERT_FILE, KEY_FILE
    log.info("Generating new certificate")
    generate_certificate()
    return CERT_FILE, KEY_FILE

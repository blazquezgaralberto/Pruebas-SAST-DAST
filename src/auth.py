"""
Módulo de autenticación — Demo GitHub Advanced Security
ADVERTENCIA: Contiene patrones inseguros INTENCIONALES para demostrar Secret Scanning y CodeQL.
"""

import hashlib
import hmac
import os

# [SECRET-1] Hardcoded credentials — Secret Scanning lo detecta
# GitHub Advanced Security bloqueará el push si Push Protection está activo.
# NUNCA hardcodear credenciales en código fuente.
DATABASE_URL = "postgresql://admin:SuperSecret123!@db.internal.example.com:5432/appdb"
JWT_SECRET = "my-super-secret-jwt-key-do-not-share"
STRIPE_SECRET_KEY = "sk_live_EXAMPLE_FAKE_KEY_1234567890abcdef"  # noqa: S105 (fake key for demo)

# La forma correcta es leer de variables de entorno:
# DATABASE_URL = os.environ.get("DATABASE_URL")
# JWT_SECRET = os.environ.get("JWT_SECRET")


# [VULN-6] Weak hashing — CodeQL: py/weak-cryptographic-algorithm
# MD5 no es apto para hashear contraseñas.
def hash_password_insecure(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


# La forma correcta con bcrypt o argon2:
def hash_password_secure(password: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return salt.hex() + ":" + key.hex()


# [VULN-7] Timing attack en comparación de tokens — CodeQL: py/timing-attack
def verify_token_insecure(user_token: str, expected_token: str) -> bool:
    # VULNERABLE: la comparación directa es susceptible a timing attacks
    return user_token == expected_token


# La forma correcta con hmac.compare_digest:
def verify_token_secure(user_token: str, expected_token: str) -> bool:
    return hmac.compare_digest(user_token.encode(), expected_token.encode())


# [VULN-8] Hardcoded secret usado en lógica de negocio
ADMIN_BYPASS_TOKEN = "bypass_token_abc123xyz"  # noqa: S105 (fake for demo)


def is_admin(token: str) -> bool:
    # VULNERABLE: token hardcodeado en el código
    return token == ADMIN_BYPASS_TOKEN

"""
Utilidades — Demo GitHub Advanced Security
ADVERTENCIA: Contiene vulnerabilidades INTENCIONALES para fines educativos.
"""

import pickle
import yaml
import subprocess
import tempfile
import os


# [VULN-9] Insecure Deserialization — CodeQL: py/unsafe-deserialization
# pickle.loads con datos no confiables permite Remote Code Execution.
def deserialize_user_data(raw_bytes: bytes) -> dict:
    # VULNERABLE: nunca deserializar datos del usuario con pickle
    return pickle.loads(raw_bytes)


# La forma correcta: usar json.loads
import json

def deserialize_user_data_safe(raw_bytes: bytes) -> dict:
    return json.loads(raw_bytes)


# [VULN-10] YAML injection — CodeQL: py/yaml-injection
# yaml.load sin Loader permite ejecución de código arbitrario.
def load_config(config_str: str) -> dict:
    # VULNERABLE: yaml.load sin Loader=yaml.SafeLoader
    return yaml.load(config_str)


# La forma correcta:
def load_config_safe(config_str: str) -> dict:
    return yaml.safe_load(config_str)


# [VULN-11] Temporary file race condition — CodeQL: py/insecure-temporary-file
def write_temp_file_insecure(content: str) -> str:
    # VULNERABLE: tempfile.mktemp crea un nombre pero no el archivo (TOCTOU)
    tmp_path = tempfile.mktemp(suffix=".txt")
    with open(tmp_path, "w") as f:
        f.write(content)
    return tmp_path


# La forma correcta:
def write_temp_file_secure(content: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(content)
        return f.name


# [VULN-12] Log injection — CodeQL: py/log-injection
import logging

logger = logging.getLogger(__name__)


def log_user_action_insecure(username: str, action: str) -> None:
    # VULNERABLE: input del usuario insertado directamente en logs
    # Permite inyectar entradas falsas en los logs
    logger.info(f"User {username} performed: {action}")


def log_user_action_secure(username: str, action: str) -> None:
    sanitized_username = username.replace("\n", "").replace("\r", "")
    sanitized_action = action.replace("\n", "").replace("\r", "")
    logger.info("User %s performed: %s", sanitized_username, sanitized_action)

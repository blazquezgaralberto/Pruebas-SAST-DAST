# GitHub Advanced Security — Demo Project

Este proyecto demuestra las tres capacidades principales de **GitHub Advanced Security (GHAS)**
usando una aplicación web Python/Node.js deliberadamente vulnerable con fines educativos.

---

## Estructura del Proyecto

```
.
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # CodeQL analysis workflow
│   │   ├── dependency-review.yml   # Dependency review on PRs
│   │   └── secret-scanning.yml     # Secret scanning push protection
│   ├── codeql/
│   │   └── codeql-config.yml       # CodeQL custom configuration
│   └── dependabot.yml              # Dependabot auto-update config
├── src/
│   ├── app.py                      # Flask app con vulnerabilidades demo
│   ├── auth.py                     # Módulo de autenticación inseguro
│   └── utils.py                    # Utilidades con path traversal
├── frontend/
│   ├── index.html                  # Frontend con XSS vulnerability
│   └── app.js                      # JS con prototype pollution
├── docs/
│   ├── 01-secret-scanning.md       # Guía: Secret Scanning
│   ├── 02-code-scanning.md         # Guía: Code Scanning (CodeQL)
│   └── 03-dependency-scanning.md   # Guía: Dependabot
├── requirements.txt                # Python deps (con versiones vulnerables)
└── package.json                    # Node deps (con versiones vulnerables)
```

---

## Las 3 Partes de GHAS

### 1. Secret Scanning
Detecta automáticamente secretos (API keys, tokens, contraseñas) commiteados al repositorio.
Ver [`docs/01-secret-scanning.md`](docs/01-secret-scanning.md)

### 2. Code Scanning (CodeQL)
Analiza el código fuente buscando vulnerabilidades como SQLi, XSS, path traversal, etc.
Ver [`docs/02-code-scanning.md`](docs/02-code-scanning.md)

### 3. Dependency Scanning (Dependabot)
Detecta librerías y paquetes con versiones vulnerables o desactualizadas.
Ver [`docs/03-dependency-scanning.md`](docs/03-dependency-scanning.md)

---

## Setup Rapido

```bash
# Instalar dependencias Python
pip install -r requirements.txt

# Instalar dependencias Node
npm install

# Ejecutar la app
python src/app.py
```

> **ADVERTENCIA:** Este código contiene vulnerabilidades intencionales para fines educativos.
> **NO usar en producción.**

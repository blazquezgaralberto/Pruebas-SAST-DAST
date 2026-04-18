# Parte 2 — Code Scanning (CodeQL)

## ¿Qué es?

**Code Scanning** con **CodeQL** es el motor de análisis estático de GitHub Advanced Security.
Trata el código como datos y ejecuta queries para encontrar patrones de vulnerabilidades.

CodeQL soporta: Python, JavaScript/TypeScript, Java, C/C++, C#, Go, Ruby, Swift, Kotlin.

---

## Cómo funciona

```
Push / PR / Schedule
        │
        ▼
    CodeQL init
    (crea la base de datos del código)
        │
        ▼
    Build / Autobuild
    (para lenguajes compilados)
        │
        ▼
    CodeQL analyze
    (ejecuta queries contra la BD)
        │
        ▼
    Genera SARIF
        │
        ▼
    GitHub procesa el SARIF
        │
        ▼
    Security tab → Code scanning alerts
```

---

## Vulnerabilidades detectadas en este proyecto

### Python (`src/app.py`)

| ID | Vulnerabilidad | Regla CodeQL | Línea |
|----|---------------|-------------|-------|
| VULN-1 | SQL Injection | `py/sql-injection` | 47 |
| VULN-2 | Reflected XSS | `py/reflected-xss` | 60 |
| VULN-3 | Command Injection | `py/command-injection` | 70 |
| VULN-4 | Path Traversal | `py/path-injection` | 81 |
| VULN-5 | Open Redirect | `py/url-redirection` | 92 |

### Python (`src/auth.py`)

| ID | Vulnerabilidad | Regla CodeQL | Línea |
|----|---------------|-------------|-------|
| VULN-6 | Weak Hashing (MD5) | `py/weak-cryptographic-algorithm` | 29 |
| VULN-7 | Timing Attack | `py/timing-attack` | 37 |

### Python (`src/utils.py`)

| ID | Vulnerabilidad | Regla CodeQL | Línea |
|----|---------------|-------------|-------|
| VULN-9 | Insecure Deserialization | `py/unsafe-deserialization` | 18 |
| VULN-10 | YAML Injection | `py/yaml-injection` | 27 |
| VULN-11 | Temp File Race (TOCTOU) | `py/insecure-temporary-file` | 33 |
| VULN-12 | Log Injection | `py/log-injection` | 50 |

### JavaScript (`frontend/app.js`)

| ID | Vulnerabilidad | Regla CodeQL | Línea |
|----|---------------|-------------|-------|
| VULN-15 | Prototype Pollution | `js/prototype-pollution` | 12 |
| VULN-16 | DOM XSS (document.write) | `js/xss` | 36 |
| VULN-17 | Code Injection (eval) | `js/code-injection` | 44 |
| VULN-18 | Missing Origin Check | `js/missing-origin-check` | 50 |

---

## Workflow configurado

El archivo `.github/workflows/codeql.yml` configura:

- **Triggers**: push a `main`/`develop`, PRs a `main`, schedule semanal
- **Lenguajes**: Python + JavaScript/TypeScript
- **Query suites**: `security-extended` + `security-and-quality`
- **Config**: `.github/codeql/codeql-config.yml`

```yaml
# Fragmento clave del workflow
- name: Initialize CodeQL
  uses: github/codeql-action/init@v3
  with:
    languages: python
    queries: security-extended,security-and-quality
```

---

## Query Suites disponibles

| Suite | Descripción |
|-------|-------------|
| `security-extended` | Vulnerabilidades de seguridad (OWASP, CWE) |
| `security-and-quality` | Seguridad + calidad de código |
| `security-experimental` | Queries experimentales de alta severidad |

---

## Ejemplo: SQL Injection detectado

CodeQL rastrea el **flujo de datos** (taint tracking) desde la fuente hasta el sink:

```
Source: request.form.get("username")  ← entrada del usuario
         │
         ▼ (flujo sin sanitizar)
Sink:   conn.execute(f"...{username}...")  ← query SQL
         │
         ▼
Alert: SQL injection [HIGH / CWE-89]
```

### Fix correcto

```python
# VULNERABLE
query = f"SELECT * FROM users WHERE username='{username}'"
cursor = conn.execute(query)

# CORRECTO — usar parámetros
cursor = conn.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (username, password)
)
```

---

## Interpretar los resultados

Los resultados aparecen en:
- `Security` tab → `Code scanning`
- Como comentarios en el PR (si el trigger es pull_request)
- En el archivo SARIF descargable

Cada alerta incluye:
- **Severidad**: Critical / High / Medium / Low
- **CWE**: Common Weakness Enumeration
- **Data flow**: ruta completa de source a sink
- **Fix sugerido**: a veces incluye un parche automático

---

## Referencias

- [CodeQL documentation](https://codeql.github.com/docs/)
- [CodeQL query libraries](https://codeql.github.com/codeql-query-help/)
- [SARIF format](https://docs.oasis-open.org/sarif/sarif/v2.0/sarif-v2.0.html)
- [CWE Top 25](https://cwe.mitre.org/top25/)

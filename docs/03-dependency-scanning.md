# Parte 3 — Dependency Scanning (Dependabot)

## ¿Qué es?

**Dependabot** es el sistema de GitHub para detectar y actualizar automáticamente
dependencias vulnerables u obsoletas en tu proyecto.

Tiene tres componentes:

| Componente | Función |
|-----------|---------|
| **Dependabot Alerts** | Avisa cuando una dependencia tiene una CVE conocida |
| **Dependabot Security Updates** | Crea PRs automáticos para parchear vulnerabilidades |
| **Dependabot Version Updates** | Crea PRs para mantener las dependencias al día |

---

## Ecosistemas soportados

Dependabot soporta más de **20 ecosistemas**:

| Ecosistema | Archivo de manifiesto |
|------------|----------------------|
| pip | `requirements.txt`, `Pipfile`, `pyproject.toml` |
| npm | `package.json`, `package-lock.json` |
| Maven | `pom.xml` |
| NuGet | `*.csproj`, `packages.config` |
| Docker | `Dockerfile` |
| GitHub Actions | `.github/workflows/*.yml` |
| Composer | `composer.json` |
| Cargo | `Cargo.toml` |
| Go modules | `go.mod` |
| Gradle | `build.gradle` |

---

## Vulnerabilidades en este proyecto

### Python (`requirements.txt`)

| Paquete | Versión actual | Versión segura | CVE | CVSS |
|---------|---------------|---------------|-----|------|
| Flask | 1.0.2 | >=2.3.0 | CVE-2018-1000656 | 7.5 (High) |
| Jinja2 | 2.10 | >=3.1.3 | CVE-2019-10906 | 8.1 (High) |
| Werkzeug | 0.15.3 | >=3.0.3 | CVE-2019-14806 | 7.5 (High) |
| requests | 2.18.4 | >=2.32.0 | CVE-2018-18074 | 6.5 (Medium) |
| PyYAML | 3.13 | >=6.0.1 | CVE-2019-20477 | 9.8 (Critical) |
| cryptography | 2.1.4 | >=42.0.0 | Múltiples CVEs | Critical |
| Pillow | 5.0.0 | >=10.3.0 | CVE-2019-16865 | 7.5 (High) |
| SQLAlchemy | 1.1.18 | >=2.0.0 | Sin mantenimiento | N/A |

### Node.js (`package.json`)

| Paquete | Versión actual | Versión segura | CVE | CVSS |
|---------|---------------|---------------|-----|------|
| express | 4.17.1 | >=4.18.2 | CVE-2022-24999 | 7.5 (High) |
| lodash | 4.17.15 | >=4.17.21 | CVE-2020-8203 | 7.4 (High) |
| axios | 0.18.1 | >=1.7.0 | CVE-2019-10742 | 7.5 (High) |
| marked | 0.6.3 | >=4.0.10 | CVE-2022-21681 | 7.5 (High) |
| handlebars | 4.1.2 | >=4.7.7 | CVE-2019-19919 | 9.8 (Critical) |
| jquery | 3.3.1 | >=3.5.0 | CVE-2019-11358 | 6.1 (Medium) |

---

## Cómo funciona Dependabot

```
GitHub Advisory Database (GHSA)
  + National Vulnerability Database (NVD)
  + npm advisory, PyPI advisory...
            │
            ▼
  Dependabot escanea tus manifiestos
  (requirements.txt, package.json...)
            │
        ┌───┴───┐
        │       │
   Alerta     Alerta
   +           +
   Security    Version
   Update PR   Update PR
```

### Dependabot Alerts
Aparecen en `Security` → `Dependabot` del repositorio.
GitHub también envía notificaciones por email.

### Security Update PRs
Dependabot crea PRs automáticos:
```
Title: Bump lodash from 4.17.15 to 4.17.21
Body:
  Bumps lodash from 4.17.15 to 4.17.21.

  Vulnerabilities fixed:
  - CVE-2020-8203: Prototype Pollution (CVSS 7.4)

  Release notes / Changelog / Commits included.
```

---

## Configuración en este proyecto

El archivo `.github/dependabot.yml` configura:

1. **pip** — actualizaciones semanales los lunes, agrupadas por tipo
2. **npm** — actualizaciones semanales los lunes, agrupadas
3. **github-actions** — actualizaciones semanales los martes

### Estrategia de agrupación (Dependabot Groups)

```yaml
groups:
  production-dependencies:
    dependency-type: "production"
  development-dependencies:
    dependency-type: "development"
```

Esto agrupa múltiples actualizaciones en un solo PR, reduciendo el ruido.

---

## Dependency Review en Pull Requests

El workflow `.github/workflows/dependency-review.yml` bloquea PRs que:
- Introduzcan dependencias con vulnerabilidades **HIGH** o **CRITICAL**
- Usen licencias no permitidas (GPL-3.0, AGPL-3.0)

```
PR abierto con package.json actualizado
              │
              ▼
   Dependency Review Action ejecuta
              │
        ┌─────┴─────┐
        │           │
    Sin vulns    Vuln HIGH/CRITICAL
        │           │
   PR pasa      PR bloqueado
              + Comentario en PR con detalles
```

---

## Ejemplo de alerta Dependabot

```
⚠️ Dependabot alert #1

Package: PyYAML
Installed version: 3.13
Fixed in: 6.0.1

Vulnerability: Arbitrary code execution
Severity: CRITICAL (CVSS 9.8)
CVE: CVE-2019-20477

PyYAML 5.1 through 5.1.2 has a "FullLoader" class
that is unsafe by default. An attacker could execute
arbitrary code via the yaml.load() function.

Affected function in this repo:
  src/utils.py:27 — yaml.load(config_str)
```

---

## Buenas prácticas

### 1. Pinear versiones en producción
```txt
# Mal — rango amplio
Flask>=1.0

# Bien — versión exacta con hash
Flask==2.3.3 \
    --hash=sha256:f69080bb...
```

### 2. Auditar manualmente con herramientas CLI
```bash
# Python
pip-audit --requirement requirements.txt

# Node.js
npm audit
npm audit fix

# Node.js — solo producción
npm audit --omit=dev
```

### 3. Verificar transitivas
```bash
# Ver árbol de dependencias con vulnerabilidades
pip-audit --desc --format=json | jq '.dependencies[] | select(.vulns | length > 0)'

# Node.js
npm audit --json | jq '.vulnerabilities'
```

### 4. Software Bill of Materials (SBOM)
GitHub genera un SBOM automáticamente:
`Insights` → `Dependency graph` → `Export SBOM`

---

## Métricas de exposición de este proyecto

```
Total dependencias vulnerables: 16
  ├── CRITICAL: 3  (PyYAML, cryptography, handlebars)
  ├── HIGH: 10
  └── MEDIUM: 3

Dependencias sin mantenimiento activo: 2
  ├── SQLAlchemy 1.1.x (branch EOL)
  └── Flask 1.0.x (branch EOL)

CVSS score promedio: 7.8 / 10
```

---

## Referencias

- [Dependabot docs](https://docs.github.com/en/code-security/dependabot)
- [GitHub Advisory Database](https://github.com/advisories)
- [GHSA format](https://github.com/github/advisory-database)
- [pip-audit](https://pypi.org/project/pip-audit/)
- [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)

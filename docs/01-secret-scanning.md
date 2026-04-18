# Parte 1 — Secret Scanning

## ¿Qué es?

**Secret Scanning** es la capacidad de GitHub Advanced Security que detecta automáticamente
credenciales, tokens y secretos commiteados en el repositorio — tanto en el historial
como en tiempo real cuando se hace un push.

GitHub mantiene una lista de más de **200 patrones** de proveedores (AWS, Azure, GCP,
Stripe, Slack, etc.) y escanea cada commit en busca de coincidencias.

---

## Cómo funciona

```
Developer pushes code
        │
        ▼
  GitHub recibe el push
        │
        ▼
Secret Scanning analiza cada archivo y commit
        │
    ┌───┴───┐
    │       │
Detecta   No detecta
    │
    ▼
Push Protection (si está activo):
  → Bloquea el push
  → Notifica al developer
  → Abre un Security Alert
```

### Push Protection
Cuando está activo, **bloquea el push antes de que llegue al repositorio**.
El desarrollador recibe un error y debe eliminar el secreto antes de poder hacer push.

```bash
$ git push origin main
remote: Push rejected.
remote: GitHub Secret Scanning found a secret in your push.
remote: Secret: Stripe API Key
remote: Location: src/auth.py:12
remote: To bypass this block, visit: https://github.com/...
```

---

## Patrones detectados en este proyecto

### `src/auth.py`
| Línea | Secreto detectado | Proveedor |
|-------|------------------|-----------|
| 17 | `DATABASE_URL` con credenciales | PostgreSQL |
| 18 | `JWT_SECRET` hardcodeado | Generic |
| 19 | `sk_live_...` | Stripe API Key |
| 40 | `ADMIN_BYPASS_TOKEN` | Generic Token |

### `frontend/index.html`
| Línea | Secreto detectado | Proveedor |
|-------|------------------|-----------|
| 36 | `AIzaSy...` | Google API Key |

---

## Configuración en el repositorio

### Habilitar Secret Scanning
1. `Settings` → `Code security and analysis`
2. Activar **Secret scanning**
3. Activar **Push protection**

### Configurar alertas
- `Settings` → `Security` → `Secret scanning`
- Configurar notificaciones por email o webhook

### Archivo de configuración (opcional)
Para excluir rutas específicas, crear `.github/secret_scanning.yml`:

```yaml
paths-ignore:
  - "docs/examples/**"
  - "**/*.test.*"
  - "**/fixtures/**"
```

---

## Remediation

Cuando se detecta un secreto:

1. **Revocar inmediatamente** el secreto en el proveedor (aunque no haya sido explotado)
2. **Eliminar** el secreto del código
3. **Usar variables de entorno** o un secret manager

### Antes (VULNERABLE)
```python
# src/auth.py
STRIPE_SECRET_KEY = "sk_live_abc123..."
DATABASE_URL = "postgresql://user:pass@host/db"
```

### Después (CORRECTO)
```python
# src/auth.py
import os

STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]
```

### Con GitHub Actions Secrets
```yaml
# .github/workflows/deploy.yml
env:
  STRIPE_SECRET_KEY: ${{ secrets.STRIPE_SECRET_KEY }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

---

## Herramientas complementarias

| Herramienta | Uso | En este proyecto |
|-------------|-----|-----------------|
| **TruffleHog** | Escanea historial Git | `.github/workflows/secret-scanning.yml` |
| **Gitleaks** | Detecta secretos con regex | `.github/gitleaks.toml` |
| **detect-secrets** | Pre-commit hook | Integrable como pre-commit |

---

## Referencias

- [GitHub Secret Scanning docs](https://docs.github.com/en/code-security/secret-scanning)
- [Lista de patrones soportados](https://docs.github.com/en/code-security/secret-scanning/secret-scanning-patterns)
- [Push Protection](https://docs.github.com/en/code-security/secret-scanning/push-protection-for-repositories-and-organizations)

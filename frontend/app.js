/**
 * Demo Frontend JS — GitHub Advanced Security
 * ADVERTENCIA: Contiene vulnerabilidades INTENCIONALES para fines educativos.
 * CodeQL debería detectar los problemas marcados con [VULN].
 */

// [VULN-15] Prototype Pollution — CodeQL: js/prototype-pollution
// Mezclar objetos sin validar las claves permite contaminar Object.prototype.
function mergeObjects(target, source) {
  // VULNERABLE: no se comprueba si la clave es "__proto__" o "constructor"
  for (const key in source) {
    if (typeof source[key] === "object" && source[key] !== null) {
      target[key] = target[key] || {};
      mergeObjects(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

// La forma correcta: usar Object.assign o structuredClone con whitelist de claves
function mergeObjectsSafe(target, source) {
  const BANNED_KEYS = new Set(["__proto__", "constructor", "prototype"]);
  for (const key of Object.keys(source)) {
    if (BANNED_KEYS.has(key)) continue;
    target[key] = source[key];
  }
  return target;
}


// [VULN-16] DOM-based XSS via document.write — CodeQL: js/xss
// El hash de la URL se inserta como HTML sin sanitizar.
function renderFromHash() {
  const hash = decodeURIComponent(window.location.hash.slice(1));
  // VULNERABLE: document.write con input del usuario
  if (hash) {
    document.write("<p>Sección: " + hash + "</p>");
  }
}


// [VULN-17] Eval de input del usuario — CodeQL: js/code-injection
function calculateExpression(expr) {
  // VULNERABLE: eval ejecuta código arbitrario
  return eval(expr);
}

// La forma correcta: parsear la expresión manualmente o usar una librería segura


// [VULN-18] postMessage sin validar origen — CodeQL: js/missing-origin-check
window.addEventListener("message", function (event) {
  // VULNERABLE: no se valida event.origin antes de procesar el mensaje
  const data = JSON.parse(event.data);
  if (data.action === "redirect") {
    window.location.href = data.url;
  }
});

// La forma correcta:
// window.addEventListener("message", function(event) {
//   if (event.origin !== "https://trusted-origin.example.com") return;
//   ...
// });


// [VULN-19] localStorage para datos sensibles — Secret Scanning / best practice
function storeUserSession(token) {
  // VULNERABLE: JWT en localStorage es accesible por cualquier script (XSS)
  localStorage.setItem("auth_token", token);
  localStorage.setItem("user_role", "admin");
}

// La forma correcta: usar httpOnly cookies gestionadas por el servidor


// Inicialización de la página
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("search-form");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const query = document.getElementById("search-input").value;
      // VULNERABLE: innerHTML con input del usuario (refuerza VULN-13)
      document.getElementById("search-results").innerHTML =
        "<p>Buscando: " + query + "</p>";
    });
  }

  renderFromHash();
});

/**
 * TecnoPlace · Validación ligera del lado del cliente.
 * Reduce viajes innecesarios al servidor (objetivo arquitectónico).
 */
(function () {
  "use strict";

  // Auto-cerrar mensajes flash después de 6s
  document.querySelectorAll(".flash").forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity .4s, transform .4s";
      el.style.opacity = "0";
      el.style.transform = "translateY(-8px)";
      setTimeout(() => el.remove(), 400);
    }, 6000);
  });

  // Validación de contraseñas coincidentes en registro
  const formRegistro = document.querySelector('form[action*="registro"], form input[name="password2"]');
  if (formRegistro) {
    const form = formRegistro.form || formRegistro;
    form.addEventListener("submit", (e) => {
      const p1 = form.querySelector('input[name="password"]');
      const p2 = form.querySelector('input[name="password2"]');
      if (p1 && p2 && p1.value !== p2.value) {
        e.preventDefault();
        alert("Las contraseñas no coinciden.");
        p2.focus();
      }
    });
  }

  // Validación de tamaño de archivos (8 MB)
  document.querySelectorAll('input[type="file"]').forEach((input) => {
    input.addEventListener("change", () => {
      for (const f of input.files) {
        if (f.size > 8 * 1024 * 1024) {
          alert(`El archivo "${f.name}" supera los 8 MB.`);
          input.value = "";
          return;
        }
      }
    });
  });

  // Validar precio positivo en formulario de producto
  const precio = document.querySelector('input[name="precio"]');
  if (precio) {
    precio.addEventListener("input", () => {
      if (parseFloat(precio.value) <= 0) {
        precio.setCustomValidity("El precio debe ser mayor que cero.");
      } else {
        precio.setCustomValidity("");
      }
    });
  }
})();

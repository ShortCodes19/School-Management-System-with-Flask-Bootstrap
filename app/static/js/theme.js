// static/js/theme.js
document.addEventListener("DOMContentLoaded", () => {
  const storageKey = "theme"; // stored values: "light" or "dark"
  const btn = document.getElementById("theme-toggle");
  const icon = document.getElementById("theme-icon");
  if (!btn || !icon) return;

  // Determine initial theme: saved -> system preference -> light
  const saved = (function () {
    try {
      return localStorage.getItem(storageKey);
    } catch (e) {
      return null;
    }
  })();

  const prefersDark =
    window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  let theme = saved || (prefersDark ? "dark" : "light");

  // Apply theme and update icon
  function applyTheme(t) {
    // For Bootstrap 5.3, set data-bs-theme to "light" or "dark"
    if (t === "dark") {
      document.documentElement.setAttribute("data-bs-theme", "dark");
    } else {
      document.documentElement.setAttribute("data-bs-theme", "light");
    }

    // Icon: moon means switch to dark, sun means currently dark (so show sun)
    // We'll show sun when dark, moon when light
    if (t === "dark") {
      icon.classList.remove("fa-moon");
      icon.classList.add("fa-sun");
    } else {
      icon.classList.remove("fa-sun");
      icon.classList.add("fa-moon");
    }
  }

  function saveTheme(t) {
    try {
      localStorage.setItem(storageKey, t);
    } catch (e) {
      // ignore write errors (private mode)
    }
  }

  // Toggle handler
  btn.addEventListener("click", () => {
    theme = theme === "dark" ? "light" : "dark";
    applyTheme(theme);
    saveTheme(theme);
  });

  // Watch for system preference changes and adapt only if user has not set a theme
  try {
    if (window.matchMedia) {
      window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
        const stored = localStorage.getItem(storageKey);
        if (!stored) {
          theme = e.matches ? "dark" : "light";
          applyTheme(theme);
        }
      });
    }
  } catch (e) {
    // ignore if browser doesn't support matchMedia event
  }

  // Finally apply the initial theme
  applyTheme(theme);
});

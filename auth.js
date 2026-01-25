// auth.js
(function () {
  const KEY = "pm_auth_ok";

  function isAuthed() {
    return localStorage.getItem(KEY) === "1";
  }

  const path = location.pathname.toLowerCase();

  // Protegemos SOLO estas carpetas
  const isProtected = path.includes("/dpi/") || path.includes("/dr/");

  if (isProtected && !isAuthed()) {
    const next = encodeURIComponent(location.pathname + location.search + location.hash);
    // desde /dpi/ o /dr/ subimos 1 nivel para ir al login
    location.replace(`../login.html?next=${next}`);
  }

  // Logout opcional
  window.pmLogout = function () {
    localStorage.removeItem(KEY);
    location.replace("../index.html");
  };
})();

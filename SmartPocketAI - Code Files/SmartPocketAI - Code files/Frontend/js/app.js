const PS = (() => {
  const API_BASE = window.SMARTPOCKET_API_BASE || "http://127.0.0.1:8000";
  const SESSION_KEY = "ps_api_session";

  const getSession = () => JSON.parse(localStorage.getItem(SESSION_KEY) || "null");
  const setSession = (payload) => localStorage.setItem(SESSION_KEY, JSON.stringify({
    token: payload.token,
    ...payload.user,
    initials: initials(payload.user.name)
  }));
  const initials = (name) => name.trim().split(/\s+/).slice(0, 2).map(w => w[0].toUpperCase()).join("");

  async function api(path, options = {}) {
    const session = getSession();
    const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
    if (session?.token) headers.Authorization = `Bearer ${session.token}`;
    const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
    let body = null;
    try { body = await response.json(); } catch (_) {}
    if (response.status === 401 && path !== "/login") localStorage.removeItem(SESSION_KEY);
    if (!response.ok) throw new Error(body?.detail || body?.message || `Request failed (${response.status})`);
    return body;
  }

  async function register(name, username, email, password) {
    try {
      const data = await api("/register", { method: "POST", body: JSON.stringify({ name, username, email, password }) });
      setSession(data);
      return { ok: true, user: data.user };
    } catch (error) { return { ok: false, message: error.message }; }
  }

  async function login(identifier, password) {
    try {
      const data = await api("/login", { method: "POST", body: JSON.stringify({ identifier, password }) });
      setSession(data);
      return { ok: true, user: data.user };
    } catch (error) { return { ok: false, message: error.message }; }
  }

  function logout() {
    localStorage.removeItem(SESSION_KEY);
    window.location.href = "login.html";
  }

  function requireAuth() {
    const session = getSession();
    if (!session?.token) { window.location.href = "login.html"; return null; }
    return session;
  }

  function currentUser() { return getSession(); }

  async function getSessionInfo() {
    const data = await api("/session-info");
    return { ...data, login_time: new Date(data.login_time) };
  }

  async function getHistory() { return api("/history"); }
  async function saveHistory(entry) { return api("/history", { method: "POST", body: JSON.stringify(entry) }); }
  async function deleteHistory(id) { return api(`/history/${encodeURIComponent(id)}`, { method: "DELETE" }); }
  async function clearAllHistory() { return api("/history", { method: "DELETE" }); }

  function stashReuse(entry) { sessionStorage.setItem("ps_reuse", JSON.stringify(entry)); }
  function popReuse() {
    const raw = sessionStorage.getItem("ps_reuse");
    if (!raw) return null;
    sessionStorage.removeItem("ps_reuse");
    return JSON.parse(raw);
  }

  function toast(msg, type = "default") {
    let el = document.querySelector(".toast");
    if (!el) { el = document.createElement("div"); el.className = "toast"; document.body.appendChild(el); }
    el.className = "toast " + type; el.textContent = msg;
    requestAnimationFrame(() => el.classList.add("show"));
    clearTimeout(el._t); el._t = setTimeout(() => el.classList.remove("show"), 3200);
  }
  function fmtINR(n) { return "₹" + Math.round(n || 0).toLocaleString("en-IN"); }
  function fmtDate(iso) { return new Date(iso).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }); }
  function initSidebarToggle() {
    const btn = document.querySelector(".hamburger"), sidebar = document.querySelector(".sidebar");
    if (!btn || !sidebar) return;
    btn.addEventListener("click", () => sidebar.classList.toggle("open"));
    document.addEventListener("click", e => {
      if (sidebar.classList.contains("open") && !sidebar.contains(e.target) && e.target !== btn && !btn.contains(e.target)) sidebar.classList.remove("open");
    });
  }
  function initNavToggle() {
    const btn = document.querySelector(".nav-toggle"), links = document.querySelector(".nav-links");
    if (btn && links) btn.addEventListener("click", () => links.classList.toggle("open"));
  }
  function renderUserWidgets() {
    const s = currentUser(); if (!s) return;
    document.querySelectorAll("[data-user-name]").forEach(el => el.textContent = s.name);
    document.querySelectorAll("[data-user-username]").forEach(el => el.textContent = s.username);
    document.querySelectorAll("[data-user-email]").forEach(el => el.textContent = s.email);
    document.querySelectorAll("[data-user-initials]").forEach(el => el.textContent = s.initials);
    document.querySelectorAll("[data-user-firstname]").forEach(el => el.textContent = s.name.split(" ")[0]);
  }
  function markActiveNav() {
    const page = window.location.pathname.split("/").pop() || "dashboard.html";
    document.querySelectorAll(".side-link").forEach(a => { if (a.getAttribute("href") === page) a.classList.add("active"); });
  }

  return { register, login, logout, requireAuth, currentUser, getSessionInfo, getHistory, saveHistory, deleteHistory, clearAllHistory, stashReuse, popReuse, toast, fmtINR, fmtDate, initSidebarToggle, initNavToggle, renderUserWidgets, markActiveNav };
})();

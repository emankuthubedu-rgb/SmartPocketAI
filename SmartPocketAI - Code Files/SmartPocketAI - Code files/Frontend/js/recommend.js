const PSRecommend = (() => {
  const API_BASE = window.SMARTPOCKET_API_BASE || "http://127.0.0.1:8000";
  async function request(path, input) {
    const session = PS.currentUser();
    if (!session?.token) throw new Error("Please sign in again.");
    const response = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${session.token}` },
      body: JSON.stringify(input)
    });
    let data = null;
    try { data = await response.json(); } catch (_) {}
    if (!response.ok) throw new Error(data?.detail || `Recommendation request failed (${response.status})`);
    return data;
  }
  return {
    generateHomeRecommendations: input => request("/recommend/home", input),
    generatePartyRecommendations: input => request("/recommend/party", input),
    generateJewelryRecommendations: input => request("/recommend/jewelry", input)
  };
})();

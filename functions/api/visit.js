export async function onRequestGet() {
  return new Response(JSON.stringify({
    totalVisits: 28,
    formatted: "28"
  }), {
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "no-cache"
    }
  });
}

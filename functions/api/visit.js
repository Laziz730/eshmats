export async function onRequestGet() {
  const baseCount = 3485;
  return new Response(JSON.stringify({
    totalVisits: baseCount,
    formatted: baseCount.toLocaleString()
  }), {
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "no-cache"
    }
  });
}

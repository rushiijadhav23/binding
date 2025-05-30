export async function fetchMetadataFromGemini(product) {
  try {
    const response = await fetch("http://localhost:5000/enrich", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(product),
    });
    return await response.json();
  } catch (error) {
    console.error("Error fetching metadata:", error);
    return null;
  }
}

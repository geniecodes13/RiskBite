export async function scanProduct(image, conditions) {
  if (!image) {
    return {
      ok: false,
      error: "No image provided"
    };
  }

  const formData = new FormData();
  formData.append("image", image);
  formData.append("conditions", JSON.stringify(conditions));

  try {
    const response = await fetch("http://localhost:8000/scan", {
      method: "POST",
      body: formData,
      headers: {
        // Don't set Content-Type, browser will set it with boundary for multipart/form-data
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return {
        ok: false,
        error: errorData.detail || `Server error: ${response.statusText}`
      };
    }

    const data = await response.json();
    return {
      ok: true,
      ...data
    };
  } catch (error) {
    return {
      ok: false,
      error: error.message || "Network error - please check your connection"
    };
  }
}

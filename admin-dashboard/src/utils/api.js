export function normalizeBackendUrl(url) {
  return String(url || "").trim().replace(/\/$/, "");
}

export async function apiGet(path, { backendUrl, adminKey, isCsv = false } = {}) {
  const base = normalizeBackendUrl(backendUrl);
  if (!base) throw new Error("Backend URL is required.");
  const response = await fetch(`${base}${path}`, {
    method: "GET",
    headers: adminKey ? { "x-admin-key": adminKey } : {},
  });
  if (!response.ok) {
    const text = await response.text().catch(() => "");
    throw new Error(`Request failed (${response.status}): ${text || response.statusText}`);
  }
  return isCsv ? response.blob() : response.json();
}

export async function apiPatch(path, body, { backendUrl, adminKey } = {}) {
  const base = normalizeBackendUrl(backendUrl);
  if (!base) throw new Error("Backend URL is required.");
  const response = await fetch(`${base}${path}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      ...(adminKey ? { "x-admin-key": adminKey } : {}),
    },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const text = await response.text().catch(() => "");
    throw new Error(`Request failed (${response.status}): ${text || response.statusText}`);
  }
  return response.json();
}

export function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

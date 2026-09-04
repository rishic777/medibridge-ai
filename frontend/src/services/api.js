/**
 * Single point of contact with the backend. No component should call
 * fetch() directly -- everything goes through here, so the frontend
 * stays independent of where/how the backend is hosted.
 */
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"; 
const API_PREFIX = "/api/v1";

async function request(path, { method = "GET", body, params } = {}) {
  let url = `${API_URL}${API_PREFIX}${path}`;
  if (params) {
    const query = new URLSearchParams(params).toString();
    url += `?${query}`;
  }

  const response = await fetch(url, {
    method,
    headers: body instanceof FormData ? undefined : { "Content-Type": "application/json" },
    body: body ? (body instanceof FormData ? body : JSON.stringify(body)) : undefined,
  });

  const payload = await response.json().catch(() => null);

  if (!response.ok || (payload && payload.success === false)) {
    const message = payload?.error?.message || "Something went wrong. Please try again.";
    throw new Error(message);
  }

  return payload?.data ?? payload;
}

// ---- Patients ----
export const createPatient = (data) => request("/patients", { method: "POST", body: data });
export const getPatient = (id) => request(`/patients/${id}`);
export const listPatients = () => request("/patients");
export const getPatientAlerts = (id) => request(`/patients/${id}/alerts`);

// ---- Conversations ----
export const startConversation = (patientId) => request("/conversations", { method: "POST", body: { patient_id: patientId } });
export const getConversation = (id) => request(`/conversations/${id}`);
export const postMessage = (conversationId, text, inputMode = "text") =>
  request(`/conversations/${conversationId}/message`, { method: "POST", body: { text, input_mode: inputMode } });

// ---- AI ----
export const aiExtract = (text) => request("/ai/extract", { method: "POST", body: { text } });
export const aiNextQuestion = (condition, answeredIds = []) =>
  request("/ai/question", { method: "POST", body: { condition, answered_ids: answeredIds } });
export const aiSummary = (patientData) => request("/ai/summary", { method: "POST", body: { patient_data: patientData } });

// ---- Reports ----
export const uploadReport = (patientId, file) => {
  const form = new FormData();
  form.append("file", file);
  return request(`/reports/upload?patient_id=${patientId}`, { method: "POST", body: form });
};
export const processReport = (reportId) => request(`/reports/${reportId}/process`, { method: "POST" });
export const getReport = (reportId) => request(`/reports/${reportId}`);

// ---- Safety ----
export const safetyCheck = (symptomTags) => request("/safety/check", { method: "POST", body: { symptom_tags: symptomTags } });

// ---- History / verification ----
export const getHistory = (patientId) => request(`/history/${patientId}`);
export const verifyHistoryItem = (patientId, payload) => request(`/history/${patientId}/verify`, { method: "POST", body: payload });

// ---- Doctors ----
export const getDoctorDashboard = () => request("/doctors/dashboard");
export const listAlerts = () => request("/alerts");
export const acknowledgeAlert = (alertId) => request(`/alerts/${alertId}/acknowledge`, { method: "PATCH" });

import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const saveAttentionEvent = async (event) => {
  return axios.post(`${API_BASE}/reports/attention/`, event);
};

export const getComplianceReport = async () => {
  return axios.get(`${API_BASE}/reports/compliance/`);
};

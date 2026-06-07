import axios from 'axios';
import { API_BASE } from './api';

export const saveAttentionEvent = async (event) => {
  return axios.post(`${API_BASE}/reports/attention/`, event);
};

export const getComplianceReport = async () => {
  return axios.get(`${API_BASE}/reports/compliance/`);
};

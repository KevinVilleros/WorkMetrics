const defaultApiBase =
  process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000/api';

export const API_BASE = (process.env.REACT_APP_API_URL || defaultApiBase).replace(/\/+$/, '');

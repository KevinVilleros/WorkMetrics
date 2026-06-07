const defaultApiBase = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const API_BASE = defaultApiBase.replace(/\/+$/g, '');

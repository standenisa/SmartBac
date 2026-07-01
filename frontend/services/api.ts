/**
 * API Service Layer — centralizat fetch cu auth headers
 */
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_BASE_URL } from '@/constants/api';

const TOKEN_KEY = 'bac_prep_token';

async function getToken(): Promise<string | null> {
  return AsyncStorage.getItem(TOKEN_KEY);
}

interface RequestOptions extends Omit<RequestInit, 'body'> {
  body?: any;
}

/**
 * Fetch wrapper care adaugă automat:
 * - Authorization header cu token
 * - Content-Type: application/json
 * - Error handling consistent
 */
export async function apiFetch<T = any>(
  endpoint: string,
  options: RequestOptions = {},
): Promise<T> {
  const token = await getToken();

  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Nu setăm Content-Type pentru FormData (upload fișiere)
  if (options.body && !(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
    body:
      options.body instanceof FormData
        ? options.body
        : options.body
          ? JSON.stringify(options.body)
          : undefined,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Eroare de server' }));
    throw new Error(error.detail || `Eroare ${res.status}`);
  }

  return res.json();
}

/** GET request */
export const apiGet = <T = any>(endpoint: string) =>
  apiFetch<T>(endpoint, { method: 'GET' });

/** POST request */
export const apiPost = <T = any>(endpoint: string, body?: any) =>
  apiFetch<T>(endpoint, { method: 'POST', body });

/** PUT request */
export const apiPut = <T = any>(endpoint: string, body?: any) =>
  apiFetch<T>(endpoint, { method: 'PUT', body });

/** POST cu FormData (pentru upload fișiere) */
export const apiUpload = <T = any>(endpoint: string, formData: FormData) =>
  apiFetch<T>(endpoint, { method: 'POST', body: formData });

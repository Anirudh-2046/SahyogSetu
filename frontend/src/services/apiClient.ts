/**
 * SahyogSetu Centralized API Client
 *
 * Provides a unified, resilient HTTP communication layer:
 * 1. Centralized base URL resolution (VITE_API_URL, user runtime settings, dev defaults)
 * 2. In-flight GET request deduplication to prevent redundant network traffic
 * 3. Configurable timeouts with AbortController
 * 4. Citizen-safe error sanitization (strips raw stack traces and technical jargon)
 * 5. Type-safe generic request methods: get, post, patch, delete
 * 6. Health and connectivity inspection
 */

export interface RequestOptions {
  timeoutMs?: number;
  headers?: Record<string, string>;
  signal?: AbortSignal;
  skipDeduplication?: boolean;
}

export class ApiError extends Error {
  public status: number;
  public userMessage: string;
  public isNetworkError: boolean;

  constructor(status: number, userMessage: string, isNetworkError: boolean = false) {
    super(userMessage);
    this.name = 'ApiError';
    this.status = status;
    this.userMessage = userMessage;
    this.isNetworkError = isNetworkError;
  }
}

class ApiClient {
  private inFlightRequests: Map<string, Promise<any>> = new Map();
  private defaultTimeoutMs: number = 8000;

  /**
   * Resolves the authoritative backend base URL
   */
  public getBaseUrl(): string {
    // 1. Environment variable (Vite build/dev)
    const envUrl = (import.meta as any).env?.VITE_API_URL;
    if (envUrl && typeof envUrl === 'string' && envUrl.trim()) {
      return envUrl.trim().replace(/\/+$/, '');
    }

    // 2. User runtime override in localStorage
    if (typeof window !== 'undefined' && window.localStorage) {
      const runtimeUrl =
        localStorage.getItem('sahyog_setu_api_url') ||
        localStorage.getItem('sanjha_sahayak_api_url');
      if (runtimeUrl && runtimeUrl.trim()) {
        return runtimeUrl.trim().replace(/\/+$/, '');
      }

      // 3. Dev environment fallback when running on standard Vite ports
      const port = window.location?.port;
      if (port === '5173' || port === '3000' || port === '4173') {
        return 'http://127.0.0.1:8000';
      }
    }

    // 4. Default relative origin for same-host deployments
    return '';
  }

  /**
   * Builds full absolute or relative URL
   */
  public buildUrl(path: string): string {
    const cleanPath = path.startsWith('/') ? path : `/${path}`;
    const baseUrl = this.getBaseUrl();
    return baseUrl ? `${baseUrl}${cleanPath}` : cleanPath;
  }

  /**
   * Performs connectivity health check
   */
  public async checkHealth(): Promise<{ isConnected: boolean; message: string; details?: any }> {
    try {
      const res = await this.get<{ status: string; components?: any }>('/health', {
        timeoutMs: 4000,
        skipDeduplication: true,
      });
      return {
        isConnected: true,
        message: 'Connected to live SahyogSetu backend service.',
        details: res,
      };
    } catch (err: any) {
      return {
        isConnected: false,
        message: err.userMessage || 'Could not reach backend service.',
      };
    }
  }

  /**
   * Centralized HTTP Request Handler
   */
  public async request<T = any>(
    endpoint: string,
    method: 'GET' | 'POST' | 'PATCH' | 'DELETE' = 'GET',
    body?: any,
    options: RequestOptions = {}
  ): Promise<T> {
    const fullUrl = this.buildUrl(endpoint);
    const timeoutMs = options.timeoutMs ?? this.defaultTimeoutMs;

    // In-flight GET request deduplication
    const dedupeKey = method === 'GET' && !options.skipDeduplication ? fullUrl : null;
    if (dedupeKey && this.inFlightRequests.has(dedupeKey)) {
      return this.inFlightRequests.get(dedupeKey) as Promise<T>;
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    // Combine caller signal if provided
    if (options.signal) {
      options.signal.addEventListener('abort', () => controller.abort());
    }

    const headers: Record<string, string> = {
      Accept: 'application/json',
      ...options.headers,
    };

    let fetchBody: any = undefined;
    if (body !== undefined) {
      if (body instanceof FormData) {
        fetchBody = body; // Browser sets multipart boundary automatically
      } else {
        headers['Content-Type'] = 'application/json';
        fetchBody = JSON.stringify(body);
      }
    }

    const execute = async (): Promise<T> => {
      try {
        const response = await fetch(fullUrl, {
          method,
          headers,
          body: fetchBody,
          signal: controller.signal,
        });
        clearTimeout(timeoutId);

        if (!response.ok) {
          let userMsg = `Server returned status ${response.status}.`;
          try {
            const errData = await response.json();
            if (errData?.detail) {
              userMsg = typeof errData.detail === 'string' ? errData.detail : JSON.stringify(errData.detail);
            } else if (errData?.message) {
              userMsg = errData.message;
            }
          } catch {
            // Non-JSON error response
          }

          // Citizen-safe error messages
          if (response.status === 404) {
            userMsg = 'Requested resource or legal document not found.';
          } else if (response.status >= 500) {
            userMsg = 'The legal service encountered an issue. Operating in verified offline corpus mode.';
          }

          throw new ApiError(response.status, userMsg);
        }

        // Parse JSON response
        const contentType = response.headers.get('content-type') || '';
        if (contentType.includes('application/json')) {
          return (await response.json()) as T;
        }
        return (await response.text()) as unknown as T;
      } catch (err: any) {
        clearTimeout(timeoutId);

        if (err instanceof ApiError) {
          throw err;
        }

        if (err.name === 'AbortError') {
          throw new ApiError(408, 'Request timed out while waiting for government service.', true);
        }

        // Network connectivity error
        throw new ApiError(
          0,
          'Unable to reach SahyogSetu backend. Offline statutory knowledge remains accessible.',
          true
        );
      } finally {
        if (dedupeKey) {
          this.inFlightRequests.delete(dedupeKey);
        }
      }
    };

    const promise = execute();
    if (dedupeKey) {
      this.inFlightRequests.set(dedupeKey, promise);
    }

    return promise;
  }

  public get<T = any>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, 'GET', undefined, options);
  }

  public post<T = any>(endpoint: string, body?: any, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, 'POST', body, options);
  }

  public patch<T = any>(endpoint: string, body?: any, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, 'PATCH', body, options);
  }

  public delete<T = any>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, 'DELETE', undefined, options);
  }
}

export const apiClient = new ApiClient();
export default apiClient;

import { Injectable, signal } from '@angular/core';

export interface Toast {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  title?: string;
  message: string;
}

@Injectable({
  providedIn: 'root',
})
export class ToastService {
  readonly toasts = signal<Toast[]>([]);

  show(message: string, type: 'success' | 'error' | 'info' | 'warning' = 'info', title?: string, durationMs: number = 4500): void {
    const id = `toast_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    const toast: Toast = { id, type, title, message };

    this.toasts.update((current) => [...current, toast]);

    if (durationMs > 0) {
      setTimeout(() => {
        this.remove(id);
      }, durationMs);
    }
  }

  success(message: string, title: string = 'Success'): void {
    this.show(message, 'success', title);
  }

  error(message: string, title: string = 'Error'): void {
    this.show(message, 'error', title);
  }

  info(message: string, title: string = 'Info'): void {
    this.show(message, 'info', title);
  }

  warning(message: string, title: string = 'Warning'): void {
    this.show(message, 'warning', title);
  }

  remove(id: string): void {
    this.toasts.update((current) => current.filter((t) => t.id !== id));
  }

  /**
   * Parse RFC 9457 / RFC 7807 problem+json response to extract human-readable error detail.
   */
  extractProblemDetail(error: any): string {
    if (!error) return 'An unexpected error occurred.';

    const body = error.error || error;

    // RFC 9457 detail field
    if (body?.detail) {
      if (typeof body.detail === 'string') {
        return body.detail;
      }
      if (Array.isArray(body.detail)) {
        // FastAPI / Pydantic validation error array
        return body.detail
          .map((item: any) => {
            const loc = Array.isArray(item?.loc) ? item.loc.join('.') : '';
            const msg = item?.msg || item?.message || JSON.stringify(item);
            return loc ? `${loc}: ${msg}` : msg;
          })
          .join('; ');
      }
    }

    if (body?.title) return body.title;
    if (body?.message) return body.message;
    if (error?.statusText && error.statusText !== 'OK') return error.statusText;
    if (error?.message) return error.message;

    return 'Network request failed. Please check connectivity or server status.';
  }

  showProblemError(error: any, fallbackTitle: string = 'Request Failed'): void {
    const detail = this.extractProblemDetail(error);
    this.error(detail, fallbackTitle);
  }
}

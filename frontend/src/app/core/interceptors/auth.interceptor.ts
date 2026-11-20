import { HttpErrorResponse, HttpHandlerFn, HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { BehaviorSubject, catchError, filter, switchMap, take, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { ToastService } from '../services/toast.service';

let isRefreshing = false;
const refreshTokenSubject = new BehaviorSubject<string | null>(null);

function addTokenHeader(req: HttpRequest<unknown>, token: string): HttpRequest<unknown> {
  return req.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const toastService = inject(ToastService);
  const token = authService.accessToken();

  let modifiedReq = req;
  if (token && (req.url.startsWith('/api') || req.url.startsWith('http://') || req.url.startsWith('https://'))) {
    modifiedReq = addTokenHeader(req, token);
  }

  return next(modifiedReq).pipe(
    catchError((error: HttpErrorResponse) => {
      // On 401: call /auth/refresh once, queue concurrent requests, retry
      if (
        error.status === 401 &&
        !req.url.includes('/auth/login') &&
        !req.url.includes('/auth/refresh')
      ) {
        if (!isRefreshing) {
          isRefreshing = true;
          refreshTokenSubject.next(null);

          return authService.rotateTokens().pipe(
            switchMap((refreshRes) => {
              isRefreshing = false;
              refreshTokenSubject.next(refreshRes.access_token);
              return next(addTokenHeader(req, refreshRes.access_token));
            }),
            catchError((refreshErr) => {
              isRefreshing = false;
              authService.logout();
              toastService.showProblemError(refreshErr, 'Session Expired');
              return throwError(() => refreshErr);
            })
          );
        } else {
          // Another refresh is already in-flight: wait for new token and retry
          return refreshTokenSubject.pipe(
            filter((t): t is string => t !== null),
            take(1),
            switchMap((newToken) => next(addTokenHeader(req, newToken)))
          );
        }
      }

      // Parse RFC 9457 errors and display detail in toasts for user awareness
      if (error.status !== 401 && error.status !== 0) {
        toastService.showProblemError(error);
      }

      return throwError(() => error);
    })
  );
};

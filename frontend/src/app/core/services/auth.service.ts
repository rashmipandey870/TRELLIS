import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, catchError, map, of, tap, throwError } from 'rxjs';

export interface CurrentUser {
  id: string;
  email: string;
  fullName: string;
  roles: string[];
  orgId: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user_id: string;
  email: string;
  roles: string[];
  org_id: string;
  requires_mfa?: boolean;
  mfa_ticket?: string;
}

export interface RefreshResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);

  // In-memory token storage (XSS prevention invariant: NEVER in localStorage/sessionStorage)
  readonly accessToken = signal<string | null>(null);
  private refreshToken: string | null = null;

  readonly currentUser = signal<CurrentUser | null>(null);
  readonly isAuthenticated = computed(() => !!this.accessToken());

  /**
   * Perform standard employee / admin login.
   * Access token is held strictly in-memory.
   */
  login(email: string, password: string): Observable<LoginResponse> {
    return this.http
      .post<LoginResponse>('/api/v1/auth/login', {
        email,
        password,
      })
      .pipe(
        tap((res) => {
          this.accessToken.set(res.access_token);
          this.refreshToken = res.refresh_token;
          this.currentUser.set({
            id: res.user_id,
            email: res.email,
            fullName: res.email.split('@')[0].replace('.', ' '),
            roles: res.roles || [],
            orgId: res.org_id,
          });
        })
      );
  }

  /**
   * Rotate refresh token and update in-memory access token.
   */
  rotateTokens(): Observable<RefreshResponse> {
    if (!this.refreshToken) {
      return throwError(() => new Error('NO_REFRESH_TOKEN'));
    }

    return this.http
      .post<RefreshResponse>('/api/v1/auth/refresh', {
        refresh_token: this.refreshToken,
      })
      .pipe(
        tap((res) => {
          this.accessToken.set(res.access_token);
          this.refreshToken = res.refresh_token;
        }),
        catchError((err) => {
          this.logout();
          return throwError(() => err);
        })
      );
  }

  /**
   * Invalidate session and clear in-memory state.
   */
  logout(): void {
    if (this.refreshToken) {
      this.http
        .post('/api/v1/auth/logout', { refresh_token: this.refreshToken })
        .pipe(catchError(() => of(null)))
        .subscribe();
    }
    this.accessToken.set(null);
    this.refreshToken = null;
    this.currentUser.set(null);
    this.router.navigate(['/login']);
  }
}

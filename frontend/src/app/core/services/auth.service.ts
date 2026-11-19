import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, catchError, map, of, switchMap, tap, throwError } from 'rxjs';

export interface CurrentUser {
  id: string;
  email: string;
  fullName: string;
  roles: string[];
  role: 'ADMIN' | 'MENTOR' | 'LEARNER' | string;
  orgId: string;
  avatarUrl?: string | null;
}

export interface LoginResponse {
  mfa_required: boolean;
  mfa_enrolment_required: boolean;
  mfa_ticket: string | null;
  tokens: (RefreshResponse & { user_id: string; roles: string[] }) | null;
  message: string | null;
}

export interface UserProfileResponse {
  id: string;
  org_id: string;
  email: string;
  full_name: string;
  avatar_url?: string | null;
  roles: string[];
  role: string;
  preferences_json?: Record<string, unknown> | null;
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

  readonly primaryRole = computed(() => {
    const user = this.currentUser();
    if (!user) return null;
    return (user.role || user.roles?.[0] || 'LEARNER').toUpperCase();
  });

  readonly isAdmin = computed(() => this.primaryRole() === 'ADMIN');
  readonly isMentor = computed(() => this.primaryRole() === 'MENTOR');
  readonly isLearner = computed(() => this.primaryRole() === 'LEARNER');

  /**
   * Determine the target landing route based on user role.
   */
  getRoleRedirectPath(): string {
    const role = this.primaryRole();
    if (role === 'ADMIN') return '/admin';
    if (role === 'MENTOR') return '/mentor';
    return '/learner';
  }

  hasRole(role: string): boolean {
    const primary = this.primaryRole();
    if (primary === role.toUpperCase()) return true;
    return this.currentUser()?.roles?.includes(role) ?? false;
  }

  /**
   * Perform standard employee / admin login.
   * Access token is held strictly in-memory.
   */
  login(email: string, password: string): Observable<UserProfileResponse> {
    return this.http
      .post<LoginResponse>('/api/v1/auth/login', {
        email,
        password,
      })
      .pipe(
        switchMap((res) => {
          if (res.mfa_required || !res.tokens) {
            return throwError(
              () => new Error(res.message || 'Multi-factor authentication is required.')
            );
          }

          this.accessToken.set(res.tokens.access_token);
          this.refreshToken = res.tokens.refresh_token;

          return this.http.get<UserProfileResponse>('/api/v1/auth/me').pipe(
            tap((user) => {
              const roleNormalized = (user.role || user.roles?.[0] || 'LEARNER').toUpperCase();
              this.currentUser.set({
                id: user.id,
                email: user.email,
                fullName: user.full_name,
                roles: user.roles || [roleNormalized],
                role: roleNormalized,
                orgId: user.org_id,
                avatarUrl: user.avatar_url,
              });
            })
          );
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

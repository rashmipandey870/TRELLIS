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

const REFRESH_TOKEN_KEY = 'trellis_refresh_token';

/**
 * Security Architecture Trade-Off:
 * --------------------------------
 * Access tokens are stored strictly in-memory (Angular signals) to prevent unauthorized exfiltration
 * via persistent browser storage. To support seamless session persistence across browser reloads,
 * the rotation-capable refresh token is persisted in sessionStorage.
 * On application start, `initSession()` performs a silent refresh to re-acquire a fresh in-memory
 * access token and user profile. If token reuse or tampering is detected by the server, the token family
 * is revoked and the session is cleared.
 */
@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);

  // In-memory access token (XSS mitigation)
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

  constructor() {
    // Attempt to recover refresh token from sessionStorage
    try {
      this.refreshToken = sessionStorage.getItem(REFRESH_TOKEN_KEY);
    } catch {
      this.refreshToken = null;
    }
  }

  getRefreshToken(): string | null {
    return this.refreshToken;
  }

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
          this.setRefreshToken(res.tokens.refresh_token);

          return this.fetchUserProfile();
        })
      );
  }

  /**
   * Fetch current user profile.
   */
  fetchUserProfile(): Observable<UserProfileResponse> {
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
  }

  /**
   * Rotate refresh token and update in-memory access token.
   */
  rotateTokens(): Observable<RefreshResponse> {
    const token = this.refreshToken;
    if (!token) {
      return throwError(() => new Error('NO_REFRESH_TOKEN'));
    }

    return this.http
      .post<RefreshResponse>('/api/v1/auth/refresh', {
        refresh_token: token,
      })
      .pipe(
        tap((res) => {
          this.accessToken.set(res.access_token);
          this.setRefreshToken(res.refresh_token);
        }),
        catchError((err) => {
          this.logout();
          return throwError(() => err);
        })
      );
  }

  /**
   * Silent refresh on application startup to restore session.
   */
  initSession(): Observable<boolean> {
    if (!this.refreshToken) {
      return of(false);
    }

    return this.rotateTokens().pipe(
      switchMap(() => this.fetchUserProfile()),
      map(() => true),
      catchError(() => {
        this.logout();
        return of(false);
      })
    );
  }

  private setRefreshToken(token: string | null): void {
    this.refreshToken = token;
    try {
      if (token) {
        sessionStorage.setItem(REFRESH_TOKEN_KEY, token);
      } else {
        sessionStorage.removeItem(REFRESH_TOKEN_KEY);
      }
    } catch {
      // Ignore sessionStorage exceptions
    }
  }

  /**
   * Invalidate session and clear in-memory state.
   */
  logout(): void {
    const token = this.refreshToken;
    this.accessToken.set(null);
    this.setRefreshToken(null);
    this.currentUser.set(null);

    if (token) {
      this.http
        .post('/api/v1/auth/logout', { refresh_token: token })
        .pipe(catchError(() => of(null)))
        .subscribe();
    }
    this.router.navigate(['/login']);
  }
}

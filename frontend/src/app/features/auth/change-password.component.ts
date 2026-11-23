import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-change-password',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="min-h-screen flex flex-col justify-center items-center py-12 px-4 sm:px-6 lg:px-8 bg-slate-50">
      <div class="absolute inset-0 bg-gradient-to-tr from-amber-100/30 via-sky-100/30 to-rose-100/20 pointer-events-none"></div>

      <div class="relative w-full max-w-md space-y-6 bg-white border border-slate-200 p-8 rounded-2xl shadow-xl">
        <!-- Header -->
        <div class="text-center space-y-2">
          <div class="inline-flex items-center justify-center gap-2 mb-1">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#FAA634] to-[#D7182A] flex items-center justify-center shadow-md">
              <span class="text-white font-black text-xl tracking-tight">T</span>
            </div>
            <span class="text-2xl font-black tracking-tight text-slate-900">TRELLIS</span>
          </div>
          <h2 class="text-lg font-bold text-slate-900">Mandatory Password Update</h2>
          <p class="text-xs text-slate-500">
            For security compliance, you must set a new strong personal password before proceeding.
          </p>
        </div>

        @if (errorMessage()) {
          <div role="alert" class="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs">
            <p class="font-bold">Update Failed</p>
            <p>{{ errorMessage() }}</p>
          </div>
        }

        @if (successMessage()) {
          <div role="alert" class="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs">
            <p class="font-bold">Password Updated</p>
            <p>{{ successMessage() }}</p>
          </div>
        }

        <form (ngSubmit)="handleChangePassword()" class="space-y-4" novalidate>
          <div>
            <label for="currentPassword" class="block text-xs font-semibold uppercase tracking-wider text-slate-700 mb-1">
              Current / Temporary Password
            </label>
            <input
              id="currentPassword"
              name="currentPassword"
              type="password"
              required
              [(ngModel)]="currentPassword"
              placeholder="••••••••••••"
              class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-[#008FBB] transition" />
          </div>

          <div>
            <label for="newPassword" class="block text-xs font-semibold uppercase tracking-wider text-slate-700 mb-1">
              New Password
            </label>
            <input
              id="newPassword"
              name="newPassword"
              type="password"
              required
              [(ngModel)]="newPassword"
              placeholder="Minimum 8 characters"
              class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-[#008FBB] transition" />
            
            <!-- Password Strength Indicator -->
            <div class="mt-2 space-y-1">
              <div class="flex items-center justify-between text-[11px]">
                <span class="text-slate-500">Strength:</span>
                <span class="font-bold" [ngClass]="strengthTextColor()">{{ strengthLabel() }}</span>
              </div>
              <div class="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                <div class="h-full transition-all duration-300" [ngClass]="strengthBarColor()" [style.width.%]="strengthScore() * 25"></div>
              </div>
            </div>
          </div>

          <div>
            <label for="confirmPassword" class="block text-xs font-semibold uppercase tracking-wider text-slate-700 mb-1">
              Confirm New Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              required
              [(ngModel)]="confirmPassword"
              placeholder="Re-enter new password"
              class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-[#008FBB] transition" />
          </div>

          <button
            type="submit"
            [disabled]="loading() || !canSubmit()"
            class="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-[#008FBB] to-[#007499] hover:from-[#007499] hover:to-[#005e7c] disabled:opacity-50 disabled:cursor-not-allowed font-bold text-white text-sm tracking-wide shadow-md transition focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#008FBB]">
            @if (loading()) {
              <span>Updating Password...</span>
            } @else {
              Update Password & Continue
            }
          </button>
        </form>
      </div>
    </div>
  `,
})
export class ChangePasswordComponent {
  private readonly http = inject(HttpClient);
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  currentPassword = '';
  newPassword = '';
  confirmPassword = '';

  readonly loading = signal<boolean>(false);
  readonly errorMessage = signal<string | null>(null);
  readonly successMessage = signal<string | null>(null);

  readonly strengthScore = computed(() => {
    const p = this.newPassword;
    if (!p) return 0;
    let score = 0;
    if (p.length >= 8) score++;
    if (/[A-Z]/.test(p)) score++;
    if (/[0-9]/.test(p)) score++;
    if (/[^A-Za-z0-9]/.test(p)) score++;
    return score;
  });

  readonly strengthLabel = computed(() => {
    const s = this.strengthScore();
    if (s === 0) return 'Too short';
    if (s === 1) return 'Weak';
    if (s === 2) return 'Fair';
    if (s === 3) return 'Good';
    return 'Strong';
  });

  readonly strengthTextColor = computed(() => {
    const s = this.strengthScore();
    if (s <= 1) return 'text-rose-500';
    if (s === 2) return 'text-amber-500';
    if (s === 3) return 'text-sky-500';
    return 'text-emerald-500';
  });

  readonly strengthBarColor = computed(() => {
    const s = this.strengthScore();
    if (s <= 1) return 'bg-rose-500';
    if (s === 2) return 'bg-amber-500';
    if (s === 3) return 'bg-sky-500';
    return 'bg-emerald-500';
  });

  canSubmit(): boolean {
    return (
      !!this.currentPassword &&
      this.newPassword.length >= 8 &&
      this.newPassword === this.confirmPassword &&
      this.newPassword !== this.currentPassword
    );
  }

  handleChangePassword(): void {
    if (!this.canSubmit()) return;

    this.loading.set(true);
    this.errorMessage.set(null);
    this.successMessage.set(null);

    this.http
      .post('/api/v1/auth/change-password', {
        current_password: this.currentPassword,
        new_password: this.newPassword,
      })
      .subscribe({
        next: () => {
          this.loading.set(false);
          this.successMessage.set('Password successfully updated. Redirecting to workspace...');
          // Refresh user profile and redirect to landing
          this.authService.fetchUserProfile().subscribe({
            next: () => {
              const target = this.authService.getRoleRedirectPath();
              setTimeout(() => this.router.navigate([target]), 1000);
            },
            error: () => {
              setTimeout(() => this.router.navigate(['/login']), 1000);
            },
          });
        },
        error: (err) => {
          this.loading.set(false);
          this.errorMessage.set(
            err.error?.detail || err.message || 'Failed to update password. Please check your current password.'
          );
        },
      });
  }
}

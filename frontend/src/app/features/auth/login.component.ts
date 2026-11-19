import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="min-h-screen flex flex-col justify-center items-center py-12 px-4 sm:px-6 lg:px-8 bg-slate-50 dark:bg-slate-950">
      <!-- Background subtle gradient decorative flare -->
      <div class="absolute inset-0 bg-gradient-to-tr from-orange-100/30 via-sky-100/30 to-rose-100/20 dark:from-slate-900 dark:via-slate-950 dark:to-slate-900 pointer-events-none"></div>

      <div class="relative w-full max-w-md space-y-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl shadow-xl">
        
        <!-- CSM Header Brand & Logo -->
        <div class="text-center space-y-2">
          <div class="inline-flex items-center justify-center gap-2 mb-1">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#FAA634] to-[#D7182A] flex items-center justify-center shadow-md">
              <span class="text-white font-black text-xl tracking-tight">T</span>
            </div>
            <span class="text-2xl font-black tracking-tight text-slate-900 dark:text-white">TRELLIS</span>
          </div>
          <p class="text-xs font-semibold text-[#008FBB] uppercase tracking-wider">
            CSM Technologies &bull; Learning &amp; Knowledge Portal
          </p>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Secure Role-Governed Access (Admin &bull; Mentor &bull; Learner)
          </p>
        </div>

        <!-- Accessible Error Alert -->
        @if (errorMessage()) {
          <div 
            role="alert" 
            aria-live="assertive"
            class="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/80 border border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-200 text-xs flex items-start gap-3">
            <svg class="w-4 h-4 text-rose-500 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div class="space-y-1">
              <p class="font-bold">Authentication Failed</p>
              <p>{{ errorMessage() }}</p>
            </div>
          </div>
        }

        <!-- Login Form -->
        <form (ngSubmit)="handleLogin()" class="space-y-4" novalidate>
          <div>
            <label for="email" class="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1">
              Corporate Email Address
            </label>
            <input 
              id="email" 
              name="email" 
              type="email" 
              autocomplete="email" 
              required 
              [(ngModel)]="email"
              placeholder="e.g. admin@csmtech.internal"
              class="w-full px-4 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#008FBB] transition" />
          </div>

          <div>
            <label for="password" class="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1">
              Password
            </label>
            <input 
              id="password" 
              name="password" 
              type="password" 
              autocomplete="current-password" 
              required 
              [(ngModel)]="password"
              placeholder="••••••••••••"
              class="w-full px-4 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#008FBB] transition" />
          </div>

          <button 
            type="submit" 
            [disabled]="loading() || !email || !password"
            class="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-[#008FBB] to-[#007499] hover:from-[#007499] hover:to-[#005e7c] disabled:opacity-50 disabled:cursor-not-allowed font-bold text-white text-sm tracking-wide shadow-md transition focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#008FBB]">
            @if (loading()) {
              <span class="inline-flex items-center gap-2">
                <svg class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Authenticating...
              </span>
            } @else {
              Sign In
            }
          </button>
        </form>

        <!-- Quick Demo Fill Personas (Step 1 requirement & seeded users) -->
        <div class="pt-5 border-t border-slate-200 dark:border-slate-800 space-y-2">
          <p class="text-[11px] font-bold uppercase tracking-wider text-slate-500 text-center">
            One-Click Demo Personas (Argon2 Pre-Seeded)
          </p>
          <div class="grid grid-cols-1 gap-2">
            <!-- Learner Persona -->
            <button 
              type="button" 
              (click)="fillCredentials('learner1@csmtech.internal', 'CSMTrellis2026!')"
              class="w-full text-left px-3 py-2 rounded-lg bg-sky-50 dark:bg-slate-800/80 hover:bg-sky-100 dark:hover:bg-slate-800 border border-sky-200 dark:border-slate-700 text-xs text-slate-900 dark:text-slate-100 flex items-center justify-between transition group">
              <div>
                <span class="font-bold text-[#008FBB]">Learner:</span>
                <span class="ml-1 text-slate-700 dark:text-slate-300">Priya Sharma</span>
                <span class="block text-[10px] text-slate-400">learner1&#64;csmtech.internal &bull; Batch Alpha</span>
              </div>
              <span class="text-[10px] font-mono font-bold text-[#008FBB] bg-white dark:bg-slate-900 px-2 py-1 rounded border border-sky-300 group-hover:scale-105 transition">
                Load &rarr;
              </span>
            </button>

            <!-- Mentor Persona -->
            <button 
              type="button" 
              (click)="fillCredentials('mentor1@csmtech.internal', 'CSMTrellis2026!')"
              class="w-full text-left px-3 py-2 rounded-lg bg-amber-50 dark:bg-slate-800/80 hover:bg-amber-100 dark:hover:bg-slate-800 border border-amber-200 dark:border-slate-700 text-xs text-slate-900 dark:text-slate-100 flex items-center justify-between transition group">
              <div>
                <span class="font-bold text-[#FAA634]">Mentor:</span>
                <span class="ml-1 text-slate-700 dark:text-slate-300">Ananya Rao</span>
                <span class="block text-[10px] text-slate-400">mentor1&#64;csmtech.internal &bull; Lead Cloud Architect</span>
              </div>
              <span class="text-[10px] font-mono font-bold text-[#FAA634] bg-white dark:bg-slate-900 px-2 py-1 rounded border border-amber-300 group-hover:scale-105 transition">
                Load &rarr;
              </span>
            </button>

            <!-- Admin Persona -->
            <button 
              type="button" 
              (click)="fillCredentials('admin@csmtech.internal', 'CSMTrellis2026!')"
              class="w-full text-left px-3 py-2 rounded-lg bg-rose-50 dark:bg-slate-800/80 hover:bg-rose-100 dark:hover:bg-slate-800 border border-rose-200 dark:border-slate-700 text-xs text-slate-900 dark:text-slate-100 flex items-center justify-between transition group">
              <div>
                <span class="font-bold text-[#D7182A]">Admin:</span>
                <span class="ml-1 text-slate-700 dark:text-slate-300">Rajesh Mohanty</span>
                <span class="block text-[10px] text-slate-400">admin&#64;csmtech.internal &bull; L&amp;K Governance</span>
              </div>
              <span class="text-[10px] font-mono font-bold text-[#D7182A] bg-white dark:bg-slate-900 px-2 py-1 rounded border border-rose-300 group-hover:scale-105 transition">
                Load &rarr;
              </span>
            </button>
          </div>
        </div>

      </div>
    </div>
  `,
})
export class LoginComponent {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  email = '';
  password = '';
  readonly loading = signal<boolean>(false);
  readonly errorMessage = signal<string | null>(null);

  fillCredentials(email: string, pass: string): void {
    this.email = email;
    this.password = pass;
    this.errorMessage.set(null);
  }

  handleLogin(): void {
    if (!this.email || !this.password) return;

    this.loading.set(true);
    this.errorMessage.set(null);

    this.authService.login(this.email, this.password).subscribe({
      next: () => {
        this.loading.set(false);
        // Role-aware redirect (Step 1): /admin, /mentor, or /learner
        const targetPath = this.authService.getRoleRedirectPath();
        this.router.navigate([targetPath]);
      },
      error: (err) => {
        this.loading.set(false);
        this.errorMessage.set(
          err.error?.detail || err.message || 'Invalid email or password. Please verify credentials.'
        );
      },
    });
  }
}

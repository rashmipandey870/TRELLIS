import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

interface DemoAccount {
  role: string;
  name: string;
  email: string;
  password?: string;
  description?: string;
}

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="min-h-screen flex flex-col justify-center items-center py-12 px-4 sm:px-6 lg:px-8 bg-slate-50">
      <!-- Background subtle gradient decorative flare -->
      <div class="absolute inset-0 bg-gradient-to-tr from-orange-100/30 via-sky-100/30 to-rose-100/20 pointer-events-none"></div>

      <div class="relative w-full max-w-md space-y-6 bg-white border border-slate-200 p-8 rounded-2xl shadow-xl">
        
        <!-- CSM Header Brand & Logo -->
        <div class="text-center space-y-2">
          <div class="inline-flex items-center justify-center gap-2 mb-1">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#FAA634] to-[#D7182A] flex items-center justify-center shadow-md">
              <span class="text-white font-black text-xl tracking-tight">T</span>
            </div>
            <span class="text-2xl font-black tracking-tight text-slate-900">TRELLIS</span>
          </div>
          <p class="text-xs font-semibold text-[#008FBB] uppercase tracking-wider">
            CSM Technologies &bull; Learning &amp; Knowledge Portal
          </p>
          <p class="text-xs text-slate-500">
            Secure Role-Governed Access (Admin &bull; Mentor &bull; Learner)
          </p>
        </div>

        <!-- Accessible Error Alert -->
        @if (errorMessage()) {
          <div 
            role="alert" 
            aria-live="assertive"
            class="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-3">
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
            <label for="email" class="block text-xs font-semibold uppercase tracking-wider text-slate-700 mb-1">
              Corporate Email Address
            </label>
            <input 
              id="email" 
              name="email" 
              type="email" 
              autocomplete="email" 
              required 
              [(ngModel)]="email"
              placeholder="name@company.com"
              class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#008FBB] transition" />
          </div>

          <div>
            <div class="flex items-center justify-between mb-1">
              <label for="password" class="block text-xs font-semibold uppercase tracking-wider text-slate-700">
                Password
              </label>
              <span class="text-[10px] text-slate-400 font-mono font-medium">Demo: CSMTrellis2026!</span>
            </div>
            <input 
              id="password" 
              name="password" 
              type="password" 
              autocomplete="current-password" 
              required 
              [(ngModel)]="password"
              placeholder="••••••••••••"
              class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#008FBB] transition" />
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

        <!-- Optional Demo Convenience Panel (Phase A3: disabled unless backend DEMO_MODE=True) -->
        @if (demoMode() && demoAccounts().length > 0) {
          <div class="pt-5 border-t border-slate-200 space-y-2">
            <div class="flex items-center justify-between">
              <p class="text-[11px] font-bold uppercase tracking-wider text-slate-500">
                Demo Accounts
              </p>
              <span class="text-[10px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                DEMO_MODE
              </span>
            </div>
            <div class="grid grid-cols-1 gap-2">
              @for (acc of demoAccounts(); track acc.email) {
                <button 
                  type="button" 
                  (click)="fillCredentials(acc.email, acc.password || '')"
                  class="w-full text-left px-3 py-2 rounded-lg bg-slate-50 hover:bg-slate-100 border border-slate-200 text-xs text-slate-900 flex items-center justify-between transition group">
                  <div>
                    <span class="font-bold" [ngClass]="{
                      'text-[#008FBB]': acc.role === 'LEARNER',
                      'text-[#FAA634]': acc.role === 'MENTOR',
                      'text-[#D7182A]': acc.role === 'ADMIN'
                    }">{{ acc.role }}:</span>
                    <span class="ml-1 text-slate-700 font-medium">{{ acc.name }}</span>
                    <span class="block text-[10px] text-slate-400">{{ acc.email }} @if (acc.description) { &bull; {{ acc.description }} }</span>
                  </div>
                  <span class="text-[10px] font-mono font-bold text-[#008FBB] bg-white px-2 py-1 rounded border border-slate-300 group-hover:scale-105 transition">
                    Load &rarr;
                  </span>
                </button>
              }
            </div>
          </div>
        }

      </div>
    </div>
  `,
})
export class LoginComponent implements OnInit {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  email = '';
  password = '';
  readonly loading = signal<boolean>(false);
  readonly errorMessage = signal<string | null>(null);

  readonly demoMode = signal<boolean>(false);
  readonly demoAccounts = signal<DemoAccount[]>([]);

  ngOnInit(): void {
    this.authService.getDemoAccounts().subscribe((res) => {
      if (res && res.enabled && res.accounts?.length) {
        this.demoMode.set(true);
        this.demoAccounts.set(res.accounts);
      }
    });
  }

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
        // Role-based portal redirect (Phase A2): role decides portal
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

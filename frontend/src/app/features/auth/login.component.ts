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
    <div class="min-h-[80vh] flex flex-col justify-center items-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="w-full max-w-md space-y-8 bg-slate-900/90 border border-slate-800 p-8 rounded-2xl shadow-2xl backdrop-blur">
        
        <!-- Header -->
        <div class="text-center space-y-2">
          <div class="inline-flex w-12 h-12 rounded-2xl bg-gradient-to-br from-cyan-500 to-cyan-700 items-center justify-center font-black text-slate-950 text-2xl shadow-lg shadow-cyan-950/60" aria-hidden="true">
            T
          </div>
          <h1 class="text-2xl font-black tracking-tight text-white">Sign in to TRELLIS</h1>
          <p class="text-xs text-slate-400">Enterprise Learning &amp; Knowledge Platform &bull; CSM Technology</p>
        </div>

        <!-- Accessible Error Alert -->
        @if (errorMessage()) {
          <div 
            role="alert" 
            aria-live="assertive"
            class="p-4 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 text-xs flex items-start gap-3">
            <svg class="w-4 h-4 text-rose-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div class="space-y-1">
              <p class="font-bold">Authentication Failed</p>
              <p>{{ errorMessage() }}</p>
            </div>
          </div>
        }

        <!-- Login Form -->
        <form (ngSubmit)="handleLogin()" class="mt-6 space-y-6" novalidate>
          <div class="space-y-4">
            <div>
              <label for="email" class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">
                Corporate Email Address
              </label>
              <input 
                id="email" 
                name="email" 
                type="email" 
                autocomplete="email" 
                required 
                [(ngModel)]="email"
                placeholder="name@csmtech.internal"
                class="w-full px-4 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-cyan-400 transition" />
            </div>

            <div>
              <label for="password" class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">
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
                class="w-full px-4 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-cyan-400 transition" />
            </div>
          </div>

          <button 
            type="submit" 
            [disabled]="loading() || !email || !password"
            class="w-full py-3 px-4 rounded-xl bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed font-bold text-slate-950 text-sm tracking-wide shadow-lg shadow-cyan-950/50 transition focus:outline-none focus:ring-2 focus:ring-cyan-300">
            @if (loading()) {
              <span class="inline-flex items-center gap-2">
                <svg class="animate-spin h-4 w-4 text-slate-950" fill="none" viewBox="0 0 24 24">
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

        <!-- Quick Demo Fill Section -->
        <div class="pt-6 border-t border-slate-800 space-y-3">
          <p class="text-[11px] font-semibold uppercase tracking-wider text-slate-400 text-center">
            Demo Personas (Pre-Seeded)
          </p>
          <div class="grid grid-cols-1 gap-2">
            <button 
              type="button" 
              (click)="fillCredentials('demo.learner01@csmtech.internal', 'DemoPassword123!')"
              class="w-full text-left px-3 py-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 border border-slate-700/80 text-xs text-slate-200 flex items-center justify-between transition focus:outline-none focus:ring-1 focus:ring-cyan-400">
              <span class="font-medium">Demo Learner 01 <span class="text-slate-400 text-[10px]">(Associate Engineer)</span></span>
              <span class="text-[10px] font-mono text-cyan-400 bg-cyan-950/80 px-1.5 py-0.5 rounded border border-cyan-800">Fill</span>
            </button>
            <button 
              type="button" 
              (click)="fillCredentials('demo.trainer01@csmtech.internal', 'DemoPassword123!')"
              class="w-full text-left px-3 py-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 border border-slate-700/80 text-xs text-slate-200 flex items-center justify-between transition focus:outline-none focus:ring-1 focus:ring-cyan-400">
              <span class="font-medium">Demo Trainer 01 <span class="text-slate-400 text-[10px]">(Principal Architect)</span></span>
              <span class="text-[10px] font-mono text-cyan-400 bg-cyan-950/80 px-1.5 py-0.5 rounded border border-cyan-800">Fill</span>
            </button>
            <button 
              type="button" 
              (click)="fillCredentials('demo.admin01@csmtech.internal', 'DemoPassword123!')"
              class="w-full text-left px-3 py-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 border border-slate-700/80 text-xs text-slate-200 flex items-center justify-between transition focus:outline-none focus:ring-1 focus:ring-cyan-400">
              <span class="font-medium">Demo Admin 01 <span class="text-slate-400 text-[10px]">(Platform Admin)</span></span>
              <span class="text-[10px] font-mono text-cyan-400 bg-cyan-950/80 px-1.5 py-0.5 rounded border border-cyan-800">Fill</span>
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
        this.router.navigate(['/home']);
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

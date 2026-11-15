import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AuthService } from './core/services/auth.service';
import { HomeStore } from './core/store/home.store';
import { DemoBannerComponent } from './features/home/components/demo-banner/demo-banner.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, DemoBannerComponent],
  template: `
    <!-- Skip Link for Keyboard Accessibility (WCAG 2.4.1) -->
    <a href="#main-content" class="skip-link">Skip to main content</a>

    <!-- Persistent Synthetic Demo Banner & Accessibility Bar -->
    <app-demo-banner />

    <!-- Primary Navigation Landmark -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-30 px-6 py-4">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-500 to-cyan-700 flex items-center justify-center font-black text-slate-950 text-xl shadow-lg shadow-cyan-900/50" aria-hidden="true">
            T
          </div>
          <div>
            <h1 class="text-lg font-black tracking-tight text-white flex items-center gap-2">
              TRELLIS
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-300 border border-cyan-800 font-mono">v0.1.0-alpha</span>
            </h1>
            <p class="text-[11px] text-slate-400 font-medium">Where every Tendril climbs &bull; CSM Technology</p>
          </div>
        </div>

        <nav aria-label="Primary Navigation" class="flex items-center gap-4 text-sm font-medium text-slate-300">
          @if (auth.isAuthenticated()) {
            <a href="#home" class="text-cyan-400 font-bold border-b-2 border-cyan-400 py-1 px-2">Home</a>
            <a href="#pathways" class="hover:text-white py-1 px-2 rounded transition">Pathways</a>
            <a href="#growth-ring" class="hover:text-white py-1 px-2 rounded transition">Growth Ring</a>
            <a href="#greenhouse" class="hover:text-white py-1 px-2 rounded transition">Greenhouse</a>

            <div class="h-4 w-px bg-slate-700 hidden sm:block" aria-hidden="true"></div>

            <!-- User Badge & Sign Out -->
            <div class="flex items-center gap-2">
              <span class="text-xs text-slate-300 font-medium hidden md:inline">
                {{ auth.currentUser()?.email }}
              </span>
              <button 
                type="button" 
                (click)="auth.logout()"
                class="text-xs px-2.5 py-1 rounded-lg border border-slate-700 bg-slate-800/80 text-rose-300 hover:text-rose-200 hover:border-rose-700 transition focus:outline-none focus:ring-1 focus:ring-rose-400">
                Sign Out
              </button>
            </div>
          } @else {
            <span class="text-xs text-slate-400 font-medium">Sign In to access platform</span>
          }
        </nav>
      </div>
    </header>

    <!-- Main Content Landmark with Dynamic Dyslexia & High-Contrast Classes -->
    <main 
      id="main-content" 
      class="max-w-7xl mx-auto px-6 py-8"
      [class.dyslexia-mode]="store.preferences().dyslexiaFont"
      [class.high-contrast]="store.preferences().highContrast"
      [class.calm-mode]="store.preferences().calmMode">
      
      <router-outlet />

    </main>

    <!-- Footer Landmark -->
    <footer class="border-t border-slate-800/80 py-8 text-center text-xs text-slate-500 space-y-1">
      <p>TRELLIS Enterprise Learning &amp; Knowledge Platform &mdash; CSM Technology</p>
      <p class="text-[11px] text-slate-600 font-mono">
        Cryptographic Evidence Ledger &bull; Default-Deny RBAC &bull; WCAG 2.2 Level AA Verified
      </p>
    </footer>
  `,
})
export class AppComponent {
  readonly store = inject(HomeStore);
  readonly auth = inject(AuthService);
}

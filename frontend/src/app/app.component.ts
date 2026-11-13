import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  template: `
    <!-- Skip Link for Keyboard Accessibility (WCAG 2.4.1) -->
    <a href="#main-content" class="skip-link">Skip to main content</a>

    <!-- Labelled Placeholder Branding Banner (Q1 Assumption) -->
    <div class="bg-amber-950/80 border-b border-amber-500/40 text-amber-200 px-4 py-1.5 text-xs font-mono flex items-center justify-between" role="region" aria-label="Branding Notice">
      <div class="flex items-center gap-2">
        <span class="inline-block w-2 h-2 rounded-full bg-amber-400 animate-pulse" aria-hidden="true"></span>
        <span><strong>[PLACEHOLDER BRANDING]</strong> Official CSM Technology brand assets pending delivery. Design tokens active.</span>
      </div>
      <button 
        type="button"
        (click)="toggleDyslexiaMode()"
        [attr.aria-pressed]="dyslexiaMode()"
        class="underline hover:text-white focus:outline-none focus:ring-2 focus:ring-cyan-400 px-2 py-0.5 rounded text-xs">
        {{ dyslexiaMode() ? 'Standard Font' : 'Dyslexia-Friendly Font' }}
      </button>
    </div>

    <!-- Navigation Landmark -->
    <header class="border-b border-slate-800 bg-slate-900/60 backdrop-blur px-6 py-4">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-cyan-600 flex items-center justify-center font-bold text-slate-950 text-lg shadow-lg shadow-cyan-900/50" aria-hidden="true">
            T
          </div>
          <div>
            <h1 class="text-lg font-bold tracking-tight text-white flex items-center gap-2">
              TRELLIS
              <span class="text-xs px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 font-normal">v0.1.0</span>
            </h1>
            <p class="text-xs text-slate-400 font-medium">Where every Tendril climbs</p>
          </div>
        </div>

        <nav aria-label="Primary Navigation" class="flex items-center gap-4 text-sm font-medium text-slate-300">
          <a href="#home" class="text-cyan-400 hover:text-cyan-300 py-1 px-2 rounded">Home</a>
          <a href="#pathways" class="hover:text-white py-1 px-2 rounded">Pathways</a>
          <a href="#growth-ring" class="hover:text-white py-1 px-2 rounded">Growth Ring</a>
          <div class="h-4 w-px bg-slate-700" aria-hidden="true"></div>
          <button 
            type="button" 
            class="text-xs px-3 py-1.5 rounded-md border border-slate-700 bg-slate-800/80 text-slate-300 hover:border-slate-500 flex items-center gap-2">
            <span>Search</span>
            <kbd class="px-1 py-0.5 rounded bg-slate-900 border border-slate-700 text-[10px] font-mono text-slate-400">Ctrl+K</kbd>
          </button>
        </nav>
      </div>
    </header>

    <!-- Main Content Landmark -->
    <main id="main-content" class="max-w-7xl mx-auto px-6 py-8" [class.dyslexia-mode]="dyslexiaMode()">
      <section aria-labelledby="ci-status-heading" class="rounded-xl border border-slate-800 bg-slate-900/40 p-8 shadow-2xl">
        <div class="flex items-center justify-between mb-6 pb-6 border-b border-slate-800">
          <div>
            <h2 id="ci-status-heading" class="text-2xl font-bold text-white mb-1">CI Quality Pipeline &amp; Foundation</h2>
            <p class="text-sm text-slate-400">Phase 1 / Slice 1.1 Automated Quality Gate Active</p>
          </div>
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800">
            <span class="w-2 h-2 rounded-full bg-emerald-400" aria-hidden="true"></span>
            Pipeline Configured
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="rounded-lg border border-slate-800 bg-slate-950/60 p-5">
            <h3 class="text-sm font-semibold text-slate-200 mb-2">Backend Quality Gate</h3>
            <p class="text-xs text-slate-400 mb-3">FastAPI 0.162.5, Ruff linting, Mypy strict static typing, and Pytest test suite.</p>
            <div class="text-[11px] font-mono text-cyan-400 bg-cyan-950/40 p-2 rounded border border-cyan-900/40">
              ruff check backend/ && mypy --strict backend/
            </div>
          </div>

          <div class="rounded-lg border border-slate-800 bg-slate-950/60 p-5">
            <h3 class="text-sm font-semibold text-slate-200 mb-2">Permission Matrix Gate</h3>
            <p class="text-xs text-slate-400 mb-3">20 resources x 15 actions x 12 roles (3,600 tuples) evaluated under Default-Deny.</p>
            <div class="text-[11px] font-mono text-cyan-400 bg-cyan-950/40 p-2 rounded border border-cyan-900/40">
              python docs/security/coverage_report.py
            </div>
          </div>

          <div class="rounded-lg border border-slate-800 bg-slate-950/60 p-5">
            <h3 class="text-sm font-semibold text-slate-200 mb-2">Accessibility &amp; Vulnerabilities</h3>
            <p class="text-xs text-slate-400 mb-3">DOMPurify 3.4.17 override (0 critical), WCAG 2.2 AA Axe-core automated scan.</p>
            <div class="text-[11px] font-mono text-cyan-400 bg-cyan-950/40 p-2 rounded border border-cyan-900/40">
              npm audit && npm run test:axe
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer Landmark -->
    <footer class="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
      <p>TRELLIS &mdash; CSM Technology Enterprise Learning &amp; Knowledge Platform</p>
    </footer>
  `,
  styles: []
})
export class AppComponent {
  title = 'trellis-frontend';
  dyslexiaMode = signal<boolean>(false);

  toggleDyslexiaMode(): void {
    this.dyslexiaMode.update(mode => !mode);
  }
}

import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { HomeStore } from '../../../../core/store/home.store';

@Component({
  selector: 'app-demo-banner',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (store.isDemoEnv()) {
      <aside 
        class="bg-amber-950/90 border-b border-amber-500/40 text-amber-200 px-4 py-2 text-xs font-mono"
        role="region" 
        aria-label="Synthetic Demo Environment and Accessibility Notice">
        <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
          <div class="flex items-center gap-2">
            <span class="inline-block w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse" aria-hidden="true"></span>
            <span>
              <strong>[SYNTHETIC DEMO ENVIRONMENT]</strong>
              Simulated persona: <em>{{ store.profile()?.name }} ({{ store.profile()?.role }})</em>. Official CSM Technology brand assets pending delivery.
            </span>
          </div>

          <div class="flex items-center gap-2 flex-wrap" role="group" aria-label="Accessibility & Demo State Toggles">
            <!-- Dyslexia Font Toggle -->
            <button
              type="button"
              id="btn-toggle-dyslexia"
              (click)="store.toggleDyslexiaFont()"
              [attr.aria-pressed]="store.preferences().dyslexiaFont"
              class="px-2.5 py-1 rounded border border-amber-500/50 hover:bg-amber-900/60 transition focus:outline-none focus:ring-2 focus:ring-cyan-400 text-xs">
              {{ store.preferences().dyslexiaFont ? 'Standard Font' : 'Dyslexia-Friendly' }}
            </button>

            <!-- Calm Mode Toggle -->
            <button
              type="button"
              id="btn-toggle-calm"
              (click)="store.toggleCalmMode()"
              [attr.aria-pressed]="store.preferences().calmMode"
              class="px-2.5 py-1 rounded border border-amber-500/50 hover:bg-amber-900/60 transition focus:outline-none focus:ring-2 focus:ring-cyan-400 text-xs">
              {{ store.preferences().calmMode ? 'Calm Mode: ON' : 'Calm Mode: OFF' }}
            </button>

            <!-- High Contrast Toggle -->
            <button
              type="button"
              id="btn-toggle-contrast"
              (click)="store.toggleHighContrast()"
              [attr.aria-pressed]="store.preferences().highContrast"
              class="px-2.5 py-1 rounded border border-amber-500/50 hover:bg-amber-900/60 transition focus:outline-none focus:ring-2 focus:ring-cyan-400 text-xs">
              {{ store.preferences().highContrast ? 'High Contrast: ON' : 'High Contrast: OFF' }}
            </button>

            <!-- Interactive State Previews for Reviewer -->
            <span class="text-amber-500/60 font-bold" aria-hidden="true">|</span>
            <button
              type="button"
              (click)="toggleLoadingPreview()"
              class="px-2 py-0.5 rounded text-[11px] bg-amber-900/40 hover:bg-amber-900/80 border border-amber-700/50 text-amber-300">
              Preview Skeleton
            </button>
            <button
              type="button"
              (click)="store.triggerErrorState()"
              class="px-2 py-0.5 rounded text-[11px] bg-red-950/60 hover:bg-red-900/80 border border-red-700/50 text-red-300">
              Trigger Error State
            </button>
            <button
              type="button"
              (click)="store.triggerEmptyState()"
              class="px-2 py-0.5 rounded text-[11px] bg-slate-900/60 hover:bg-slate-800 border border-slate-700 text-slate-300">
              Trigger Empty State
            </button>
            <button
              type="button"
              (click)="store.retry()"
              class="px-2 py-0.5 rounded text-[11px] bg-cyan-950/60 hover:bg-cyan-900/80 border border-cyan-700 text-cyan-300 font-bold">
              Reset Demo
            </button>
          </div>
        </div>
      </aside>
    }
  `,
})
export class DemoBannerComponent {
  readonly store = inject(HomeStore);

  toggleLoadingPreview(): void {
    this.store.setLoading(true);
    setTimeout(() => {
      this.store.setLoading(false);
    }, 2500);
  }
}

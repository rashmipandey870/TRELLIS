import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { HomeStore } from '../../../../core/store/home.store';

@Component({
  selector: 'app-demo-banner',
  standalone: true,
  imports: [CommonModule],
  template: `
    <aside 
      class="bg-amber-950/90 border-b border-amber-500/40 text-amber-200 px-4 py-2 text-xs font-mono"
      role="region" 
      aria-label="Synthetic Demo Environment and Accessibility Notice">
      <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-2">
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse" aria-hidden="true"></span>
          <span>
            <strong>[SYNTHETIC DEMO ENVIRONMENT]</strong>
            Active persona: <em>{{ store.profile()?.name || 'Demo Learner 01' }} ({{ store.profile()?.role || 'Associate Platform Engineer' }})</em>. Official CSM Technology brand assets pending delivery.
          </span>
        </div>

        <div class="flex items-center gap-2 flex-wrap" role="group" aria-label="Accessibility Mode Toggles">
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
        </div>
      </div>
    </aside>
  `,
})
export class DemoBannerComponent {
  readonly store = inject(HomeStore);
}

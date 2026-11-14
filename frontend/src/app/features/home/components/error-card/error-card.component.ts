import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { HomeStore } from '../../../../core/store/home.store';

@Component({
  selector: 'app-error-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (store.error(); as err) {
      <div 
        role="alert" 
        aria-live="assertive"
        class="rounded-2xl border border-rose-700/60 bg-rose-950/40 p-6 md:p-8 shadow-2xl">
        <div class="flex items-start gap-4">
          <div class="w-10 h-10 rounded-xl bg-rose-900/60 border border-rose-600/60 flex items-center justify-center text-rose-300 shrink-0" aria-hidden="true">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>

          <div class="flex-1 space-y-2">
            <h3 class="text-lg font-bold text-rose-100">
              Synchronisation Error Encountered
            </h3>
            <p class="text-sm text-rose-200/90 leading-relaxed">
              {{ err }}
            </p>

            <div class="pt-3 flex items-center gap-3">
              <button
                type="button"
                (click)="store.retry()"
                class="px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs shadow-md transition focus:outline-none focus:ring-2 focus:ring-rose-300">
                Retry Telemetry Synchronisation
              </button>
            </div>
          </div>
        </div>
      </div>
    }
  `,
})
export class ErrorCardComponent {
  readonly store = inject(HomeStore);
}

import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ToastService } from './core/services/toast.service';
import { CommandPaletteComponent } from './shared/components/command-palette.component';
import { AssistantComponent } from './shared/assistant/assistant.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, CommandPaletteComponent, AssistantComponent],
  template: `
    <!-- Skip Link for Keyboard Accessibility (WCAG 2.4.1) -->
    <a href="#main-content" class="skip-link sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:p-2 focus:bg-white focus:text-slate-900 focus:shadow-md focus:rounded-md">
      Skip to main content
    </a>

    <!-- Command Palette (Ctrl+K or Cmd+K) -->
    <app-command-palette />

    <!-- Role-Governed AI Assistant Floating Action Widget -->
    <app-assistant />

    <!-- Toast Notifications Region (WCAG 4.1.3 Live Region) -->
    <div aria-live="polite" aria-atomic="true" class="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none">
      @for (toast of toastService.toasts(); track toast.id) {
        <div
          role="alert"
          class="pointer-events-auto p-4 rounded-xl shadow-lg border transition-all duration-300 flex items-start gap-3"
          [ngClass]="{
            'bg-emerald-50 dark:bg-emerald-950/90 border-emerald-200 text-emerald-900 dark:text-emerald-100': toast.type === 'success',
            'bg-rose-50 dark:bg-rose-950/90 border-rose-200 text-rose-900 dark:text-rose-100': toast.type === 'error',
            'bg-amber-50 dark:bg-amber-950/90 border-amber-200 text-amber-900 dark:text-amber-100': toast.type === 'warning',
            'bg-sky-50 dark:bg-sky-950/90 border-sky-200 text-sky-900 dark:text-sky-100': toast.type === 'info'
          }">
          <div class="flex-1 text-xs">
            @if (toast.title) {
              <div class="font-bold text-sm mb-0.5">{{ toast.title }}</div>
            }
            <div class="leading-relaxed whitespace-pre-wrap">{{ toast.message }}</div>
          </div>
          <button
            type="button"
            (click)="toastService.remove(toast.id)"
            class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 text-sm font-bold"
            aria-label="Close notification">
            &times;
          </button>
        </div>
      }
    </div>

    <div id="main-content" class="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      <router-outlet />
    </div>
  `,
})
export class AppComponent {
  readonly toastService = inject(ToastService);
}

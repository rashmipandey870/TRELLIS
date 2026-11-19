import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  template: `
    <!-- Skip Link for Keyboard Accessibility (WCAG 2.4.1) -->
    <a href="#main-content" class="skip-link sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:p-2 focus:bg-white focus:text-slate-900 focus:shadow-md focus:rounded-md">
      Skip to main content
    </a>
    <div id="main-content" class="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      <router-outlet />
    </div>
  `,
})
export class AppComponent {}

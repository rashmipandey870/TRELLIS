import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { HomeStore } from '../../core/store/home.store';
import { AssignedSessionsComponent } from './components/assigned-sessions/assigned-sessions.component';
import { ErrorCardComponent } from './components/error-card/error-card.component';
import { GreenhouseCardComponent } from './components/greenhouse-card/greenhouse-card.component';
import { HeroClimbingComponent } from './components/hero-climbing/hero-climbing.component';
import { LoadingSkeletonComponent } from './components/loading-skeleton/loading-skeleton.component';
import { SkillGapsCardComponent } from './components/skill-gaps-card/skill-gaps-card.component';
import { StreakCounterComponent } from './components/streak-counter/streak-counter.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    HeroClimbingComponent,
    SkillGapsCardComponent,
    StreakCounterComponent,
    AssignedSessionsComponent,
    GreenhouseCardComponent,
    LoadingSkeletonComponent,
    ErrorCardComponent,
  ],
  template: `
    <div class="space-y-8" [class.calm-mode]="store.preferences().calmMode" [class.high-contrast]="store.preferences().highContrast">
      <!-- Welcome Header -->
      <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <h1 class="text-3xl font-black text-white tracking-tight">
            Welcome back, {{ store.profile()?.name }}
          </h1>
          <p class="text-sm text-slate-400 mt-1">
            {{ store.profile()?.role }} &bull; CSM Technology Cloud Platform Tendril
          </p>
        </div>

        <div class="flex items-center gap-3">
          <div class="text-right hidden sm:block">
            <span class="text-xs text-slate-400 block font-mono">Evidence Ledger ID</span>
            <span class="text-xs font-semibold text-cyan-400 font-mono">pse-7a9f...c28b</span>
          </div>
          <div class="w-10 h-10 rounded-full bg-cyan-900 border border-cyan-500/50 flex items-center justify-center font-bold text-white text-sm shadow-md" aria-hidden="true">
            PS
          </div>
        </div>
      </header>

      <!-- Conditional Error Card -->
      <app-error-card />

      <!-- Conditional Loading State vs Telemetry Content -->
      @if (store.loading()) {
        <app-loading-skeleton />
      } @else {
        <!-- Main Hero Card: Continue Climbing -->
        <app-hero-climbing />

        <!-- 2x2 Responsive Telemetry & Social Learning Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Growth Ring Skill Gaps -->
          <app-skill-gaps-card />

          <!-- 14-Day Climbing Streak Counter -->
          <app-streak-counter />

          <!-- Upcoming Cohort Sessions -->
          <app-assigned-sessions />

          <!-- Greenhouse Innovation of the Month -->
          <app-greenhouse-card />
        </div>
      }
    </div>
  `,
})
export class HomeComponent {
  readonly store = inject(HomeStore);
}

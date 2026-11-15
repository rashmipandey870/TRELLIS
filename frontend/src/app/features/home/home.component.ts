import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
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
            Welcome back, {{ store.profile()?.name || 'Learner' }}
          </h1>
          <p class="text-sm text-slate-400 mt-1">
            {{ store.profile()?.role || 'Associate Platform Engineer' }} &bull; CSM Technology
          </p>
        </div>

        <div class="flex items-center gap-3">
          <div class="text-right hidden sm:block">
            <span class="text-xs text-slate-400 block font-mono">Evidence Ledger Pseudonym</span>
            <span class="text-xs font-semibold text-cyan-400 font-mono">
              {{ store.profile()?.id ? ('pse-' + store.profile()!.id.slice(0, 8) + '...') : 'pse-unlinked' }}
            </span>
          </div>
          <div class="w-10 h-10 rounded-full bg-cyan-900 border border-cyan-500/50 flex items-center justify-center font-bold text-white text-sm shadow-md" aria-hidden="true">
            {{ getInitials(store.profile()?.name) }}
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
          <!-- Growth Ring Skill Gaps with Evidence Labels & Why this? -->
          <app-skill-gaps-card />

          <!-- Climbing Streak Counter & Audited Freeze -->
          <app-streak-counter />

          <!-- Upcoming Cohort Sessions -->
          <app-assigned-sessions />

          <!-- Greenhouse Innovation of the Month (Phase 3 Upcoming) -->
          <app-greenhouse-card />
        </div>
      }
    </div>
  `,
})
export class HomeComponent implements OnInit {
  readonly store = inject(HomeStore);

  ngOnInit(): void {
    this.store.loadHomeData();
  }

  getInitials(name?: string): string {
    if (!name) return 'DL';
    const parts = name.trim().split(/\s+/);
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }
}

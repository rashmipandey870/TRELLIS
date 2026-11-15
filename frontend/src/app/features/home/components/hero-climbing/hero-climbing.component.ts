import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { HomeStore } from '../../../../core/store/home.store';

@Component({
  selector: 'app-hero-climbing',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (store.enrolment(); as enr) {
      <article
        class="relative overflow-hidden rounded-2xl border border-cyan-800/40 bg-gradient-to-br from-slate-900/90 via-slate-900/70 to-slate-950/90 p-6 md:p-8 shadow-xl shadow-cyan-950/20"
        aria-labelledby="hero-climbing-heading">
        <!-- Background subtle glow -->
        <div class="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-cyan-600/10 blur-3xl" aria-hidden="true"></div>

        <div class="relative z-10 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div class="flex-1 space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-cyan-950/70 text-cyan-300 border border-cyan-700/50">
              <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" aria-hidden="true"></span>
              <span>Active Pathway &bull; First 90 Days</span>
            </div>

            <h2 id="hero-climbing-heading" class="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
              Continue Climbing: {{ enr.pathwayTitle }}
            </h2>

            <p class="text-sm text-slate-300 max-w-2xl leading-relaxed">
              Current focus: <span class="font-semibold text-cyan-200">{{ enr.currentModuleName }}</span>
              <br class="hidden sm:inline" />
              <span class="text-xs text-slate-400">
                Course: {{ enr.currentCourseTitle }} &bull; {{ enr.completedModules }} of {{ enr.totalModules }} modules verified
              </span>
            </p>

            <div class="pt-2 flex flex-wrap items-center gap-4">
              <a
                [href]="'#pathways/' + enr.pathwayId + '/modules/' + enr.currentModuleId"
                class="inline-flex items-center gap-2.5 px-6 py-3 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-sm shadow-lg shadow-cyan-900/40 transition transform active:scale-95 focus:outline-none focus:ring-2 focus:ring-cyan-300 focus:ring-offset-2 focus:ring-offset-slate-900"
                [attr.aria-label]="'Resume learning: ' + enr.currentModuleName">
                <svg class="w-5 h-5 text-slate-950 fill-current" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M8 5v14l11-7z" />
                </svg>
                <span>Resume Learning</span>
              </a>

              <div class="text-xs text-slate-400 flex items-center gap-2">
                <svg class="w-4 h-4 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>~{{ enr.estimatedMinutesRemaining }} mins to complete module</span>
              </div>
            </div>
          </div>

          <!-- Circular SVG Progress Ring -->
          <div class="flex flex-col items-center justify-center p-2 self-center lg:self-auto">
            <div 
              class="relative flex items-center justify-center"
              role="progressbar"
              [attr.aria-valuenow]="enr.progressPct"
              aria-valuemin="0"
              aria-valuemax="100"
              [attr.aria-label]="enr.pathwayTitle + ' progress: ' + enr.progressPct + ' percent'">
              
              <svg class="w-32 h-32 transform -rotate-90" viewBox="0 0 100 100" aria-hidden="true">
                <!-- Track circle -->
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  stroke-width="10"
                  class="stroke-slate-800"
                  fill="transparent"
                />
                <!-- Progress ring -->
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  stroke-width="10"
                  stroke-linecap="round"
                  class="stroke-cyan-500 transition-all duration-700 ease-out"
                  fill="transparent"
                  stroke-dasharray="263.89"
                  [attr.stroke-dashoffset]="getStrokeDashoffset(enr.progressPct)"
                />
              </svg>

              <!-- Center label -->
              <div class="absolute flex flex-col items-center justify-center text-center">
                <span class="text-2xl font-black tracking-tight text-white">
                  {{ enr.progressPct }}%
                </span>
                <span class="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                  Completed
                </span>
              </div>
            </div>

            <p class="mt-2 text-xs text-slate-400 text-center">
              Target Role: <strong class="text-slate-200">{{ enr.targetRoleCode || 'PLATFORM_ENG_L2' }}</strong>
            </p>
          </div>
        </div>
      </article>
    } @else {
      <!-- Empty State Card (WCAG accessible) -->
      <article
        class="rounded-2xl border border-slate-800 bg-slate-900/60 p-8 text-center"
        aria-labelledby="empty-climbing-heading">
        <div class="mx-auto w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 mb-4" aria-hidden="true">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <h2 id="empty-climbing-heading" class="text-xl font-bold text-white mb-2">No Active Pathway Enrolment</h2>
        <p class="text-sm text-slate-400 max-w-md mx-auto mb-6">
          You are not currently enrolled in an active learning pathway. Explore the curriculum catalog or contact your trainer to start your onboarding pathway.
        </p>
        <button
          type="button"
          (click)="store.retry()"
          class="px-5 py-2.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-sm shadow-md transition focus:outline-none focus:ring-2 focus:ring-cyan-300">
          Synchronise Enrolment Status
        </button>
      </article>
    }
  `,
})
export class HeroClimbingComponent {
  readonly store = inject(HomeStore);

  getStrokeDashoffset(progressPct: number): number {
    const circumference = 263.89;
    return circumference * (1 - progressPct / 100);
  }
}

import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { RouterModule } from '@angular/router';
import { LearnerDashboardData, LearnerService } from '../../core/services/learner.service';

@Component({
  selector: 'app-learner-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="space-y-6">
      <!-- Title & Streak Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">Learner Portal</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Welcome back! Track your meetings, pending assessments, and continuous practice streak.
          </p>
        </div>
        <div class="flex items-center gap-2">
          <!-- Streak Indicator Pill -->
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-50 dark:bg-amber-950/60 border border-amber-300 dark:border-amber-800 text-[#FAA634] font-black text-xs shadow-sm">
            <span>🔥</span>
            <span>{{ data()?.streak_days ?? 14 }} Day Streak!</span>
          </div>
        </div>
      </div>

      <!-- Quick Highlights Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#008FBB]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Assigned Assessments</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">{{ data()?.assigned_assessments?.length ?? 1 }}</span>
            <span class="text-xs font-semibold text-[#008FBB]">Ready to Take</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Full-Stack Foundation</p>
        </div>

        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#FAA634]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Upcoming Mentoring</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">{{ data()?.upcoming_meetings?.length ?? 1 }}</span>
            <span class="text-xs font-semibold text-[#FAA634]">Today</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">16:00 IST &bull; Teams</p>
        </div>

        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-emerald-500"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Average Performance</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">92%</span>
            <span class="text-xs font-semibold text-emerald-500">Top 15%</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Batch Alpha Percentile</p>
        </div>

        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-purple-500"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">AI Practice Track</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">92/100</span>
            <span class="text-xs font-semibold text-purple-600">Dedication</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">18 Problems Attempted</p>
        </div>
      </div>

      <!-- Actionable Cards: Mentor Feedback & Live Assessments -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Assigned Assessment Action Card -->
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#008FBB] animate-pulse"></span>
              Assigned Assessments
            </h3>
            <a routerLink="/learner/assessments" class="text-xs text-[#008FBB] font-bold hover:underline">
              View All &rarr;
            </a>
          </div>

          <div class="p-4 rounded-xl bg-sky-50/70 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800 space-y-3">
            <div class="flex items-start justify-between">
              <div>
                <span class="text-[10px] font-mono font-bold uppercase text-[#008FBB] bg-white dark:bg-slate-900 px-2 py-0.5 rounded border border-sky-300">
                  Full-Stack Architecture
                </span>
                <h4 class="text-sm font-bold text-slate-900 dark:text-white mt-1">Full-Stack Foundation Assessment</h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">MCQ questions + Sandboxed coding challenge</p>
              </div>
              <span class="text-xs font-mono font-bold text-slate-700 dark:text-slate-300">60 mins</span>
            </div>

            <div class="flex items-center justify-between pt-1">
              <span class="text-xs text-slate-500 font-semibold">Proctored &bull; Tab switch tracking</span>
              <a routerLink="/learner/assessments" class="px-4 py-2 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-white text-xs font-bold transition shadow-sm">
                Launch Assessment &rarr;
              </a>
            </div>
          </div>
        </div>

        <!-- Mentor Feedback & Remarks -->
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#FAA634]"></span>
              Advisor Remarks &amp; Feedback
            </h3>
            <span class="text-[11px] text-slate-400">Lead Cloud Architect</span>
          </div>

          <div class="p-4 rounded-xl bg-amber-50/70 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/40 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-900 dark:text-white">Ananya Rao (Mentor)</span>
              <span class="text-[10px] text-slate-400">Yesterday</span>
            </div>
            <p class="text-xs text-slate-700 dark:text-slate-300 italic">
              "Strong architectural thinking on Docker sandboxes. Keep refining test case boundary handling in the Coding Lab!"
            </p>
          </div>
        </div>

      </div>

      <!-- Quick Launch Strip -->
      <div class="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-[#005e7c] text-white flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xl">
        <div class="space-y-1">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-[#FAA634]"></span>
            <span class="text-[11px] font-bold uppercase tracking-wider text-sky-200">Continuous AI Practice Track</span>
          </div>
          <h3 class="text-base font-black">Sharpen your problem solving in our sandboxed lab</h3>
          <p class="text-xs text-slate-300">Generate adaptive Python, SQL, Java, or DSA challenges verified by LLM reasoning.</p>
        </div>
        <a routerLink="/learner/practice" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#FAA634] to-[#e09228] text-white text-xs font-bold shadow-lg hover:scale-105 transition whitespace-nowrap">
          Open AI Practice &rarr;
        </a>
      </div>
    </div>
  `,
})
export class LearnerDashboardComponent {
  private readonly learnerService = inject(LearnerService);
  readonly data = signal<LearnerDashboardData | null>(null);

  ngOnInit(): void {
    this.learnerService.getDashboard().subscribe({
      next: (res) => this.data.set(res),
      error: () => {},
    });
  }
}

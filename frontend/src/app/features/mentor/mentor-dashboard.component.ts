import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MentorDashboardData, MentorService } from '../../core/services/mentor.service';

@Component({
  selector: 'app-mentor-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="space-y-6">
      <!-- Title & Role Badge -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">Mentor Command Center</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Advisory oversight for your assigned engineering cohorts at CSM Technology.
          </p>
        </div>
        <div class="flex items-center gap-2">
          <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-amber-50 text-[#FAA634] border border-amber-200">
            MENTOR ACTIVE
          </span>
        </div>
      </div>

      <!-- Quick Metrics -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#FAA634]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Assigned Learners</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">{{ data()?.assigned_learners_count ?? 3 }}</span>
            <span class="text-xs font-semibold text-emerald-500">Engineers</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Batch Alpha</p>
        </div>

        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#008FBB]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Upcoming Meetings</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">{{ data()?.upcoming_meetings?.length ?? 1 }}</span>
            <span class="text-xs font-semibold text-[#008FBB]">Scheduled</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Next: System Architecture Standup</p>
        </div>

        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-purple-500"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Live Assessments</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">{{ data()?.live_assessments?.length ?? 1 }}</span>
            <span class="text-xs font-semibold text-purple-600">Active</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">MCQ &bull; Coding Tests</p>
        </div>

        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#D7182A]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Talent Alerts</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">{{ data()?.new_practice_alerts?.length ?? 1 }}</span>
            <span class="text-xs font-semibold text-[#D7182A]">Pending Action</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Practice Threshold Qualified</p>
        </div>
      </div>

      <!-- Actionable Dashboard Sections -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Talent Spotlight Attention Card -->
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-[#FAA634] animate-ping"></span>
              <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">
                Talent Spotlight AI Practice Alert
              </h3>
            </div>
            <a routerLink="/mentor/spotlight" class="text-xs text-[#FAA634] font-bold hover:underline">
              Review &amp; Act &rarr;
            </a>
          </div>

          <div class="p-4 rounded-xl bg-amber-50/70 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/50 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-900 dark:text-white">Priya Sharma &bull; Python Practice Track</span>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-[#FAA634]">14d Streak</span>
            </div>
            <p class="text-xs text-slate-600 dark:text-slate-300">
              Crossed criteria: 14 active days in 30d window, 88% weighted accuracy across 18 problems.
            </p>
            <div class="pt-2 flex gap-2">
              <a routerLink="/mentor/spotlight" class="px-3 py-1.5 rounded-lg bg-[#FAA634] text-white text-xs font-bold hover:bg-[#e09228] transition">
                Triage Alert
              </a>
            </div>
          </div>
        </div>

        <!-- Upcoming Meeting Schedule -->
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Upcoming Mentoring Sessions
            </h3>
            <a routerLink="/mentor/meetings" class="text-xs text-[#008FBB] font-bold hover:underline">
              Schedule New &rarr;
            </a>
          </div>

          <div class="space-y-2.5">
            <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-between">
              <div>
                <p class="text-xs font-bold text-slate-900 dark:text-white">Architecture &amp; Clean Code Review</p>
                <p class="text-[11px] text-slate-400 mt-0.5">Today &bull; 16:00 - 17:00 IST &bull; Batch Alpha</p>
              </div>
              <a href="https://teams.microsoft.com/l/meetup-join/sample" target="_blank" class="px-3 py-1.5 rounded-lg bg-[#008FBB] hover:bg-[#007499] text-white text-xs font-bold transition">
                Launch Link
              </a>
            </div>
          </div>
        </div>

      </div>
    </div>
  `,
})
export class MentorDashboardComponent {
  private readonly mentorService = inject(MentorService);
  readonly data = signal<MentorDashboardData | null>(null);

  ngOnInit(): void {
    this.mentorService.getDashboard().subscribe({
      next: (res) => this.data.set(res),
      error: () => {},
    });
  }
}

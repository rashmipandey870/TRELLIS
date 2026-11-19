import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AdminDashboardData, AdminService } from '../../core/services/admin.service';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="space-y-6">
      <!-- Title & Intro -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">Department Dashboard</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            CSM Technology Learning &amp; Knowledge Governance Overview
          </p>
        </div>
        <div class="flex items-center gap-2">
          <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-rose-50 text-[#D7182A] border border-rose-200">
            ADMIN OVERSIGHT
          </span>
        </div>
      </div>

      <!-- KPI Summary Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Learners -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden group">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#008FBB]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Total Enrolled Learners</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">{{ data()?.total_learners ?? 6 }}</span>
            <span class="text-xs font-semibold text-emerald-500">Active</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Assigned across cohorts</p>
        </div>

        <!-- Mentors -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden group">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#FAA634]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Active Mentors</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">{{ data()?.total_mentors ?? 2 }}</span>
            <span class="text-xs font-semibold text-[#FAA634]">Advisors</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Leading curriculum &amp; reviews</p>
        </div>

        <!-- Average Score -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden group">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#D7182A]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Org Average Score</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">{{ data()?.average_score ?? 84.5 }}%</span>
            <span class="text-xs font-semibold text-emerald-500">&uarr; 3.2% MoM</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Across MCQ &amp; coding tests</p>
        </div>

        <!-- Batches -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden group">
          <div class="absolute top-0 left-0 right-0 h-1 bg-purple-500"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Active Batches</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900 dark:text-white">{{ data()?.total_batches ?? 2 }}</span>
            <span class="text-xs font-semibold text-purple-600">Cohorts</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Batch Alpha &amp; Batch Beta</p>
        </div>
      </div>

      <!-- Two-Column Operational Details -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Top Performers -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
              Top Performers
            </h3>
            <a routerLink="/admin/learners" class="text-xs text-[#008FBB] font-bold hover:underline">View All &rarr;</a>
          </div>

          <div class="space-y-2.5">
            @for (p of data()?.top_performers ?? fallbackPerformers; track p.id) {
              <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/60">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 font-bold text-xs flex items-center justify-center">
                    #{{ $index + 1 }}
                  </div>
                  <div>
                    <p class="text-xs font-bold text-slate-900 dark:text-white">{{ p.full_name }}</p>
                    <p class="text-[10px] text-slate-400">{{ p.email }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <span class="text-xs font-bold text-slate-900 dark:text-white">{{ p.score }}%</span>
                  <span class="block text-[10px] text-amber-500 font-semibold">{{ p.streak_days }}d streak</span>
                </div>
              </div>
            }
          </div>
        </div>

        <!-- Learners Needing Attention -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#D7182A]"></span>
              Learners Needing Attention
            </h3>
            <span class="text-xs text-rose-500 font-bold">Action Suggested</span>
          </div>

          <div class="space-y-2.5">
            @for (l of data()?.learners_needing_attention ?? fallbackAttention; track l.id) {
              <div class="flex items-center justify-between p-3 rounded-xl bg-rose-50/50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/40">
                <div>
                  <p class="text-xs font-bold text-slate-900 dark:text-white">{{ l.full_name }}</p>
                  <p class="text-[10px] text-slate-400">{{ l.email }}</p>
                </div>
                <div class="text-right">
                  <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-[#D7182A] border border-rose-300">
                    {{ l.reason }}
                  </span>
                </div>
              </div>
            }
          </div>
        </div>

      </div>

      <!-- Mentor Workload & Practice Engagement Overview -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Mentor Overview -->
        <div class="lg:col-span-2 p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">
            Mentor Performance &amp; Assignment Overview
          </h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="text-[10px] font-bold uppercase tracking-wider text-slate-400 border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th class="py-2">Mentor Name</th>
                  <th class="py-2 text-center">Assigned Batches</th>
                  <th class="py-2 text-center">Assigned Learners</th>
                  <th class="py-2 text-center">Assessments Published</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
                @for (m of data()?.mentor_metrics ?? fallbackMentorMetrics; track m.mentor_id) {
                  <tr>
                    <td class="py-3 font-semibold text-slate-900 dark:text-white">{{ m.name }}</td>
                    <td class="py-3 text-center font-mono font-bold">{{ m.batches_count }}</td>
                    <td class="py-3 text-center font-mono font-bold">{{ m.learners_count }}</td>
                    <td class="py-3 text-center font-mono font-bold text-[#008FBB]">{{ m.assessments_count }}</td>
                  </tr>
                }
              </tbody>
            </table>
          </div>
        </div>

        <!-- Practice & AI Engagement -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">
            Practice Engagement
          </h3>
          <div class="space-y-4 text-xs">
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-1">
              <span class="text-slate-400 text-[11px] uppercase font-bold">Total Practice Attempts</span>
              <p class="text-2xl font-black text-slate-900 dark:text-white">
                {{ data()?.practice_engagement?.total_attempts ?? 42 }}
              </p>
              <p class="text-[10px] text-emerald-500 font-semibold">&uarr; 18% weekly increase</p>
            </div>

            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-1">
              <span class="text-slate-400 text-[11px] uppercase font-bold">Active 30d Learners</span>
              <p class="text-2xl font-black text-slate-900 dark:text-white">
                {{ data()?.practice_engagement?.active_learners_30d ?? 6 }} / 6
              </p>
              <p class="text-[10px] text-[#008FBB] font-semibold">100% platform adoption</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  `,
})
export class AdminDashboardComponent {
  private readonly adminService = inject(AdminService);
  readonly data = signal<AdminDashboardData | null>(null);

  readonly fallbackPerformers = [
    { id: '1', full_name: 'Sneha Mukherjee', email: 'learner3@csmtech.internal', streak_days: 19, score: 96 },
    { id: '2', full_name: 'Priya Sharma', email: 'learner1@csmtech.internal', streak_days: 14, score: 92 },
    { id: '3', full_name: 'Deepika Iyer', email: 'learner5@csmtech.internal', streak_days: 12, score: 88 },
  ];

  readonly fallbackAttention = [
    { id: '4', full_name: 'Rohan Verma', email: 'learner4@csmtech.internal', reason: 'Score < 70% in 2 tests' },
    { id: '6', full_name: 'Kavita Reddy', email: 'learner6@csmtech.internal', reason: 'Missed last meeting' },
  ];

  readonly fallbackMentorMetrics = [
    { mentor_id: 'm1', name: 'Ananya Rao (Lead Cloud Architect)', batches_count: 1, learners_count: 3, assessments_count: 2 },
    { mentor_id: 'm2', name: 'Vikram Patel (Principal Systems Engineer)', batches_count: 1, learners_count: 3, assessments_count: 1 },
  ];

  ngOnInit(): void {
    this.adminService.getDashboard().subscribe({
      next: (res) => this.data.set(res),
      error: () => {},
    });
  }
}

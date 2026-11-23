import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AdminDashboardData, AdminService, AIHealthData } from '../../core/services/admin.service';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="space-y-6">
      <!-- Title & Intro -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">Department Dashboard</h1>
          <p class="text-xs text-slate-500">
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
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden group">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#008FBB]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Total Enrolled Learners</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ data()?.total_learners ?? 0 }}</span>
            <span class="text-xs font-semibold text-emerald-500">Active</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Assigned across cohorts</p>
        </div>

        <!-- Mentors -->
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden group">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#FAA634]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Active Mentors</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ data()?.total_mentors ?? 0 }}</span>
            <span class="text-xs font-semibold text-[#FAA634]">Advisors</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Leading curriculum &amp; reviews</p>
        </div>

        <!-- Average Score -->
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden group">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#D7182A]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Org Average Score</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ data()?.average_score ?? 0 }}%</span>
            <span class="text-xs font-semibold text-emerald-500">&uarr; 3.2% MoM</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Across MCQ &amp; coding tests</p>
        </div>

        <!-- Total Batches -->
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden group">
          <div class="absolute top-0 left-0 right-0 h-1 bg-slate-400"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Training Batches</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ data()?.total_batches ?? 0 }}</span>
            <span class="text-xs font-semibold text-slate-400">Running</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Active enterprise batches</p>
        </div>
      </div>

      <!-- AI Health & Service Governance Panel (WS2) -->
      <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
          <div>
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full"
                    [ngClass]="{
                      'bg-emerald-500': aiHealth()?.status === 'HEALTHY',
                      'bg-amber-500': aiHealth()?.status === 'DEGRADED',
                      'bg-rose-500': aiHealth()?.status === 'DOWN'
                    }"></span>
              TRELLIS AI Gateway &amp; Model Governance
            </h3>
            <p class="text-[11px] text-slate-400 mt-0.5">
              Provider: <span class="font-bold text-slate-700">{{ aiHealth()?.primary_provider ?? 'Detecting...' }}</span> |
              Instruct Model: <span class="font-mono text-slate-700">{{ aiHealth()?.active_instruct_model ?? 'N/A' }}</span> |
              Code Model: <span class="font-mono text-slate-700">{{ aiHealth()?.active_code_model ?? 'N/A' }}</span>
            </p>
          </div>

          <div class="flex items-center gap-2">
            <span class="px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider"
                  [ngClass]="{
                    'bg-emerald-50 text-emerald-700 border border-emerald-200': aiHealth()?.circuit_breaker_state === 'CLOSED',
                    'bg-rose-50 text-rose-700 border border-rose-200': aiHealth()?.circuit_breaker_state === 'OPEN',
                    'bg-amber-50 text-amber-700 border border-amber-200': aiHealth()?.circuit_breaker_state === 'HALF_OPEN'
                  }">
              Circuit: {{ aiHealth()?.circuit_breaker_state ?? 'CLOSED' }}
            </span>

            @if (aiHealth()?.circuit_breaker_state === 'CLOSED') {
              <button (click)="toggleCircuitBreaker('trip')"
                      class="px-2.5 py-1 text-[11px] font-bold rounded-lg border border-rose-200 text-rose-600 hover:bg-rose-50 transition-colors">
                Trip Circuit
              </button>
            } @else {
              <button (click)="toggleCircuitBreaker('reset')"
                      class="px-2.5 py-1 text-[11px] font-bold rounded-lg border border-emerald-200 text-emerald-600 hover:bg-emerald-50 transition-colors">
                Reset Circuit
              </button>
            }

            <button (click)="refillPool()"
                    class="px-2.5 py-1 text-[11px] font-bold rounded-lg bg-slate-900 text-white hover:bg-slate-800 transition-colors">
              Refill Pools
            </button>
          </div>
        </div>

        <!-- AI Metrics Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-1">
          <div class="p-3 rounded-xl bg-slate-50 border border-slate-200/60">
            <span class="text-[10px] font-bold uppercase text-slate-400">p50 Latency</span>
            <p class="text-xl font-black text-slate-900 mt-1">{{ aiHealth()?.p50_latency_ms ?? 0 }} ms</p>
            <span class="text-[10px] text-slate-400">Median generation</span>
          </div>

          <div class="p-3 rounded-xl bg-slate-50 border border-slate-200/60">
            <span class="text-[10px] font-bold uppercase text-slate-400">p95 Latency</span>
            <p class="text-xl font-black text-slate-900 mt-1">{{ aiHealth()?.p95_latency_ms ?? 0 }} ms</p>
            <span class="text-[10px] text-slate-400">95th percentile</span>
          </div>

          <div class="p-3 rounded-xl bg-slate-50 border border-slate-200/60">
            <span class="text-[10px] font-bold uppercase text-slate-400">Validation Pass Rate</span>
            <p class="text-xl font-black text-emerald-600 mt-1">{{ aiHealth()?.validation_pass_rate_percent ?? 100 }}%</p>
            <span class="text-[10px] text-slate-400">Quality gate success</span>
          </div>

          <div class="p-3 rounded-xl bg-slate-50 border border-slate-200/60">
            <span class="text-[10px] font-bold uppercase text-slate-400">Verified Pool Items</span>
            <p class="text-xl font-black text-[#008FBB] mt-1">{{ getPoolTotal() }}</p>
            <span class="text-[10px] text-slate-400">Ready in memory</span>
          </div>
        </div>
      </div>

      <!-- Detail Panels: Top Performers & Attention -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

        <!-- Top Performers -->
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
              Top Performing Learners
            </h3>
            <a routerLink="/admin/learners" class="text-xs text-[#008FBB] font-bold hover:underline">View All &rarr;</a>
          </div>

          <div class="space-y-2.5">
            @if (data()?.top_performers?.length) {
              @for (p of data()?.top_performers; track p.id) {
                <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200/60">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-800 font-bold text-xs flex items-center justify-center">
                      #{{ $index + 1 }}
                    </div>
                    <div>
                      <p class="text-xs font-bold text-slate-900">{{ p.full_name }}</p>
                      <p class="text-[10px] text-slate-400">{{ p.email }}</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <span class="text-sm font-black text-emerald-600">{{ p.score }}%</span>
                    <span class="block text-[10px] text-amber-500 font-semibold">{{ p.streak_days }}d streak</span>
                  </div>
                </div>
              }
            } @else {
              <div class="py-8 text-center text-xs text-slate-400">No completed assessment scores recorded yet.</div>
            }
          </div>
        </div>

        <!-- Learners Needing Attention -->
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#D7182A]"></span>
              Learners Needing Attention
            </h3>
            <span class="text-xs text-rose-500 font-bold">Action Suggested</span>
          </div>

          <div class="space-y-2.5">
            @if (data()?.learners_needing_attention?.length) {
              @for (l of data()?.learners_needing_attention; track l.id) {
                <div class="flex items-center justify-between p-3 rounded-xl bg-rose-50/50 border border-rose-200">
                  <div>
                    <p class="text-xs font-bold text-slate-900">{{ l.full_name }}</p>
                    <p class="text-[10px] text-slate-400">{{ l.email }}</p>
                  </div>
                  <div class="text-right">
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-[#D7182A] border border-rose-300">
                      {{ l.reason }}
                    </span>
                  </div>
                </div>
              }
            } @else {
              <div class="py-8 text-center text-xs text-slate-400">All enrolled learners are meeting progress milestones.</div>
            }
          </div>
        </div>

      </div>

      <!-- Mentor Workload & Practice Engagement Overview -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Mentor Overview -->
        <div class="lg:col-span-2 p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
            Mentor Performance &amp; Assignment Overview
          </h3>
          <div class="overflow-x-auto">
            @if (data()?.mentor_metrics?.length) {
              <table class="w-full text-left text-xs">
                <thead class="text-[10px] font-bold uppercase tracking-wider text-slate-400 border-b border-slate-200">
                  <tr>
                    <th class="py-2">Mentor Name</th>
                    <th class="py-2 text-center">Assigned Batches</th>
                    <th class="py-2 text-center">Assigned Learners</th>
                    <th class="py-2 text-center">Assessments Published</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  @for (m of data()?.mentor_metrics; track m.mentor_id) {
                    <tr>
                      <td class="py-3 font-semibold text-slate-900">{{ m.name }}</td>
                      <td class="py-3 text-center font-mono font-bold">{{ m.batches_count }}</td>
                      <td class="py-3 text-center font-mono font-bold">{{ m.learners_count }}</td>
                      <td class="py-3 text-center font-mono font-bold text-[#008FBB]">{{ m.assessments_count }}</td>
                    </tr>
                  }
                </tbody>
              </table>
            } @else {
              <div class="py-8 text-center text-xs text-slate-400">No active mentors currently assigned to batches.</div>
            }
          </div>
        </div>

        <!-- Practice & AI Engagement -->
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
            Practice Engagement
          </h3>
          <div class="space-y-4 text-xs">
            <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span class="text-slate-400 text-[11px] uppercase font-bold">Total Practice Attempts</span>
              <p class="text-2xl font-black text-slate-900">
                {{ data()?.practice_engagement?.total_attempts ?? 0 }}
              </p>
              <p class="text-[10px] text-emerald-500 font-semibold">Self-directed practice</p>
            </div>

            <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span class="text-slate-400 text-[11px] uppercase font-bold">Active 30d Learners</span>
              <p class="text-2xl font-black text-slate-900">
                {{ data()?.practice_engagement?.active_learners_30d ?? 0 }}
              </p>
              <p class="text-[10px] text-[#008FBB] font-semibold">Active in last 30 days</p>
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
  readonly aiHealth = signal<AIHealthData | null>(null);

  ngOnInit(): void {
    this.adminService.getDashboard().subscribe({
      next: (res) => this.data.set(res),
      error: () => {},
    });

    this.refreshAIHealth();
  }

  refreshAIHealth(): void {
    this.adminService.getAIHealth().subscribe({
      next: (res) => this.aiHealth.set(res),
      error: () => {},
    });
  }

  toggleCircuitBreaker(action: 'trip' | 'reset'): void {
    this.adminService.manageCircuitBreaker(action).subscribe({
      next: () => this.refreshAIHealth(),
      error: () => {},
    });
  }

  refillPool(): void {
    this.adminService.refillAIPool().subscribe({
      next: () => this.refreshAIHealth(),
      error: () => {},
    });
  }

  getPoolTotal(): number {
    const counts = this.aiHealth()?.pool_counts;
    if (!counts) return 0;
    return Object.values(counts).reduce((acc, curr) => acc + curr, 0);
  }
}

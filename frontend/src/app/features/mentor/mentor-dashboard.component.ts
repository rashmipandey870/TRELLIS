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
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">Mentor Command Center</h1>
          <p class="text-xs text-slate-500">
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
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#FAA634]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Assigned Learners</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ data()?.assigned_learners_count ?? 0 }}</span>
            <span class="text-xs font-semibold text-emerald-500">Engineers</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Assigned Cohorts</p>
        </div>

        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#008FBB]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Upcoming Meetings</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ data()?.upcoming_meetings?.length ?? 0 }}</span>
            <span class="text-xs font-semibold text-[#008FBB]">Scheduled</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Scheduled syncs</p>
        </div>

        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-purple-500"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Live Assessments</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ data()?.live_assessments?.length ?? 0 }}</span>
            <span class="text-xs font-semibold text-purple-600">Active</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">MCQ &bull; Coding Tests</p>
        </div>

        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#D7182A]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Talent Alerts</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ data()?.new_practice_alerts?.length ?? 0 }}</span>
            <span class="text-xs font-semibold text-[#D7182A]">Pending Action</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Practice Threshold Qualified</p>
        </div>
      </div>

      <!-- Actionable Dashboard Sections -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Talent Spotlight Attention Card -->
        <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-[#FAA634] animate-ping"></span>
              <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
                Talent Spotlight AI Practice Alert
              </h3>
            </div>
            <a routerLink="/mentor/spotlight" class="text-xs text-[#FAA634] font-bold hover:underline">
              Review &amp; Act &rarr;
            </a>
          </div>

          @if (data()?.new_practice_alerts && (data()?.new_practice_alerts)!.length > 0) {
            <div class="p-4 rounded-xl bg-amber-50/70 border border-amber-200 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-slate-900">{{ (data()?.new_practice_alerts)![0].learner_name }} &bull; {{ (data()?.new_practice_alerts)![0].field }} Track</span>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-[#FAA634]">{{ (data()?.new_practice_alerts)![0].active_days || (data()?.new_practice_alerts)![0].streak || 14 }}d Active</span>
              </div>
              <p class="text-xs text-slate-600">
                {{ (data()?.new_practice_alerts)![0].message }}
              </p>
              <div class="pt-2 flex gap-2">
                <a routerLink="/mentor/spotlight" class="px-3 py-1.5 rounded-lg bg-[#FAA634] text-white text-xs font-bold hover:bg-[#e09228] transition">
                  Triage Alert
                </a>
              </div>
            </div>
          } @else {
            <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-500">
              No pending Talent Spotlight alerts across your assigned cohorts.
            </div>
          }
        </div>

        <!-- Upcoming Meeting Schedule -->
        <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
              Upcoming Mentoring Sessions
            </h3>
            <a routerLink="/mentor/meetings" class="text-xs text-[#008FBB] font-bold hover:underline">
              Schedule New &rarr;
            </a>
          </div>

          <div class="space-y-2.5">
            @for (m of data()?.upcoming_meetings; track m.id) {
              <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                <div>
                  <p class="text-xs font-bold text-slate-900">{{ m.title }}</p>
                  <p class="text-[11px] text-slate-400 mt-0.5">{{ m.meeting_date || m.start_time | date:'short' }} &bull; {{ m.batch_name || 'Assigned Cohort' }}</p>
                </div>
                <a [href]="m.meeting_link" target="_blank" class="px-3 py-1.5 rounded-lg bg-[#008FBB] hover:bg-[#007499] text-white text-xs font-bold transition">
                  Launch Link
                </a>
              </div>
            } @empty {
              <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-500 text-center">
                No upcoming sessions scheduled.
              </div>
            }
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

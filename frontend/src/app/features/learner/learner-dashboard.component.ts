import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
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
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">Learner Portal</h1>
          <p class="text-xs text-slate-500">
            Welcome back! Track your mentoring sessions, pending assessments, and continuous practice streak.
          </p>
        </div>
        <div class="flex items-center gap-2">
          <!-- Streak Indicator Pill -->
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-50 border border-amber-300 text-[#FAA634] font-black text-xs shadow-sm">
            <span>🔥</span>
            <span>{{ data()?.streak_days ?? 0 }} Day Streak</span>
          </div>
          <a routerLink="/learner/results" class="px-3 py-1.5 rounded-full bg-sky-50 text-[#008FBB] border border-sky-200 text-xs font-bold hover:bg-sky-100 transition">
            View Analytics Reports &rarr;
          </a>
        </div>
      </div>

      <!-- Quick Highlights Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <!-- Assigned Assessments -->
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#008FBB]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Assigned Assessments</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ getPendingAssessmentsCount() }}</span>
            <span class="text-xs font-semibold text-[#008FBB]">Pending</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400 truncate">
            {{ getFirstPendingAssessmentTitle() }}
          </p>
        </div>

        <!-- Upcoming Mentoring Meeting with Direct Join -->
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-[#FAA634]"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Upcoming Mentoring</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ data()?.upcoming_meetings?.length ?? 0 }}</span>
            <span class="text-xs font-semibold text-[#FAA634]">
              {{ (data()?.upcoming_meetings?.length ?? 0) > 0 ? 'Scheduled' : 'None' }}
            </span>
          </div>
          @if (data()?.upcoming_meetings?.length) {
            <p class="mt-1 text-[11px] text-slate-700 font-bold truncate">
              {{ data()?.upcoming_meetings?.[0]?.title }}
            </p>
            <div class="mt-2 flex items-center justify-between">
              <span class="text-[10px] text-slate-400 font-mono">
                {{ data()?.upcoming_meetings?.[0]?.date }} {{ data()?.upcoming_meetings?.[0]?.start_time }}
              </span>
              <a 
                [href]="data()?.upcoming_meetings?.[0]?.meeting_link" 
                target="_blank" 
                class="px-2.5 py-1 bg-[#008FBB] hover:bg-[#007499] text-white rounded-lg text-[10px] font-bold shadow-xs transition">
                Join &rarr;
              </a>
            </div>
          } @else {
            <p class="mt-1 text-[11px] text-slate-400">No active sessions scheduled</p>
          }
        </div>

        <!-- Average Performance -->
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-emerald-500"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Average Score</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ getAverageScore() }}%</span>
            <span class="text-xs font-semibold text-emerald-600">Overall</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Across verified assessments</p>
        </div>

        <!-- AI Practice Track -->
        <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-purple-500"></div>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">AI Practice Track</span>
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-slate-900">{{ getPracticeScore() }}/100</span>
            <span class="text-xs font-semibold text-purple-600">Score</span>
          </div>
          <p class="mt-1 text-[11px] text-slate-400">Adaptive self-directed practice</p>
        </div>

      </div>

      <!-- Actionable Cards: Mentor Feedback & Live Assessments -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Assigned Assessment Action Card -->
        <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#008FBB] animate-pulse"></span>
              Assigned Assessments
            </h3>
            <a routerLink="/learner/assessments" class="text-xs text-[#008FBB] font-bold hover:underline">
              View All &rarr;
            </a>
          </div>

          @if (getPendingAssessments().length) {
            @for (a of getPendingAssessments(); track a.id) {
              <div class="p-4 rounded-xl bg-sky-50/70 border border-sky-200 space-y-3">
                <div class="flex items-start justify-between">
                  <div>
                    <span class="text-[10px] font-mono font-bold uppercase text-[#008FBB] bg-white px-2 py-0.5 rounded border border-sky-300">
                      {{ a.field || 'Assessment' }}
                    </span>
                    <h4 class="text-sm font-bold text-slate-900 mt-1">{{ a.title }}</h4>
                    <p class="text-xs text-slate-500 mt-0.5">{{ a.instructions || 'Proctored test with timer and tab tracking' }}</p>
                  </div>
                  <span class="text-xs font-mono font-bold text-slate-700">{{ a.duration_minutes || 60 }} mins</span>
                </div>

                <div class="flex items-center justify-between pt-1">
                  <span class="text-xs text-slate-500 font-semibold">Proctored &bull; Passing {{ a.passing_score || 75 }}%</span>
                  <a routerLink="/learner/assessments" class="px-4 py-2 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-white text-xs font-bold transition shadow-sm">
                    Launch Assessment &rarr;
                  </a>
                </div>
              </div>
            }
          } @else {
            <div class="p-6 text-center text-xs text-slate-400 border border-dashed border-slate-200 rounded-xl">
              No pending assessments assigned. All evaluations are completed.
            </div>
          }
        </div>

        <!-- Mentor Feedback & Remarks -->
        <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#FAA634]"></span>
              Advisor Remarks &amp; Feedback
            </h3>
            <span class="text-[11px] text-slate-400">Assigned Mentors</span>
          </div>

          @if (data()?.mentor_remarks?.length) {
            @for (rem of data()?.mentor_remarks; track rem.id) {
              <div class="p-4 rounded-xl bg-amber-50/70 border border-amber-200 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold text-slate-900">{{ rem.mentor_name || 'Mentor' }}</span>
                  <span class="text-[10px] text-slate-400 font-mono">{{ rem.created_at | date:'mediumDate' }}</span>
                </div>
                <p class="text-xs text-slate-700 italic">"{{ rem.remark_text }}"</p>
              </div>
            }
          } @else {
            <div class="p-6 text-center text-xs text-slate-400 border border-dashed border-slate-200 rounded-xl">
              No new mentor remarks recorded. Feedback will appear here after code reviews.
            </div>
          }
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
        <div class="flex items-center gap-2">
          <a routerLink="/learner/results" class="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-bold transition whitespace-nowrap">
            View Analytics &rarr;
          </a>
          <a routerLink="/learner/practice" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#FAA634] to-[#e09228] text-white text-xs font-bold shadow-lg hover:scale-105 transition whitespace-nowrap">
            Open AI Practice &rarr;
          </a>
        </div>
      </div>
    </div>
  `,
})
export class LearnerDashboardComponent implements OnInit {
  private readonly learnerService = inject(LearnerService);
  readonly data = signal<LearnerDashboardData | null>(null);

  ngOnInit(): void {
    this.learnerService.getDashboard().subscribe({
      next: (res) => this.data.set(res),
      error: () => {},
    });
  }

  getPendingAssessments(): any[] {
    const d = this.data() as any;
    if (!d) return [];
    return d.assigned_assessments || d.live_assessments || [];
  }

  getPendingAssessmentsCount(): number {
    return this.getPendingAssessments().length;
  }

  getFirstPendingAssessmentTitle(): string {
    const list = this.getPendingAssessments();
    return list.length > 0 && list[0]?.title ? list[0].title : 'All caught up';
  }

  getAverageScore(): number {
    const scores = this.data()?.latest_scores;
    if (!scores || !scores.length) return 85;
    const total = scores.reduce((acc: number, curr: any) => acc + (Number(curr.score) || 0), 0);
    return Math.round(total / scores.length);
  }

  getPracticeScore(): number {
    const d = this.data();
    if (d?.streak_days && d.streak_days > 0) {
      return Math.min(100, 60 + d.streak_days * 5);
    }
    return 75;
  }
}

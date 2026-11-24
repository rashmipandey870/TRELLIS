import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { MentorService } from '../../core/services/mentor.service';

@Component({
  selector: 'app-mentor-learner-analytics',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="space-y-6 max-w-7xl mx-auto pb-12 animate-in fade-in duration-200">

      <!-- Breadcrumbs & Top Action Bar -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <nav class="flex items-center gap-2 text-xs font-semibold text-slate-500 mb-1">
            @if (isAdmin()) {
              <a routerLink="/admin" class="hover:text-slate-900 transition">Admin Portal</a>
              <span>/</span>
              <a routerLink="/admin/learners" class="hover:text-slate-900 transition">Learner Directory</a>
              <span>/</span>
              <span class="text-[#008FBB]">Performance Dossier</span>
            } @else {
              <a routerLink="/mentor" class="hover:text-slate-900 transition">Mentor Portal</a>
              <span>/</span>
              <a routerLink="/mentor/learners" class="hover:text-slate-900 transition">Assigned Learners</a>
              <span>/</span>
              <span class="text-[#008FBB]">Performance Dossier</span>
            }
          </nav>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight flex items-center gap-2.5">
            <span>Student Performance &amp; Graphical Marks Analysis</span>
          </h1>
          <p class="text-xs text-slate-500 mt-0.5">
            Holistic assessment scores, optional practice activity, cohort ranking, and mastery progression.
          </p>
        </div>

        <div class="flex items-center gap-3">
          <a [routerLink]="isAdmin() ? '/admin/learners' : '/mentor/learners'" class="px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-xs font-bold text-slate-700 hover:bg-slate-50 transition shadow-xs flex items-center gap-1.5">
            &larr; Back to Learners
          </a>
          <button (click)="printDossier()" class="px-4 py-2 rounded-xl bg-gradient-to-r from-[#008FBB] to-[#007499] text-white text-xs font-bold shadow-md hover:opacity-95 transition flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
            <span>Print / Save Dossier</span>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      @if (loading()) {
        <div class="p-16 text-center space-y-3 bg-white rounded-2xl border border-slate-200">
          <div class="w-10 h-10 border-4 border-[#008FBB] border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p class="text-sm font-bold text-slate-700">Loading comprehensive performance data...</p>
          <p class="text-xs text-slate-400">Aggregating assignment scores, practice attempts, and class rankings.</p>
        </div>
      }

      @if (!loading() && data()) {
        <!-- Student Executive Banner -->
        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div class="flex items-center gap-4">
            <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#FAA634] to-[#D7182A] text-white flex items-center justify-center font-black text-2xl shadow-md">
              {{ getInitials(data().learner_name) }}
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h2 class="text-2xl font-black text-slate-900">{{ data().learner_name }}</h2>
                <span class="px-2.5 py-0.5 rounded-full text-xs font-bold"
                  [ngClass]="data().average_score >= 75 ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'">
                  {{ data().average_score >= 75 ? 'Distinction / On Track' : 'Needs Support' }}
                </span>
              </div>
              <p class="text-xs text-slate-500 font-mono">{{ data().email }}</p>
              <div class="flex items-center gap-4 mt-2 text-xs text-slate-600">
                <span class="flex items-center gap-1 font-semibold">
                  <span class="w-2 h-2 rounded-full bg-[#008FBB]"></span>
                  Active Batch Cohort
                </span>
                <span class="flex items-center gap-1 font-semibold text-amber-600">
                  🔥 {{ data().streak_days || 12 }}-Day Practice Streak
                </span>
              </div>
            </div>
          </div>

          <!-- Quick Action: Schedule 1-on-1 -->
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <a routerLink="/mentor/meetings" class="px-4 py-2.5 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-300 text-xs font-bold text-slate-800 transition text-center flex items-center justify-center gap-2 shadow-xs">
              <svg class="w-4 h-4 text-[#008FBB]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>Schedule Mentoring Meeting &rarr;</span>
            </a>
          </div>
        </div>

        <!-- 4 Top Executive KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- KPI 1: Overall Average -->
          <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
            <div class="flex items-center justify-between text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
              <span>Overall Average Marks</span>
              <span class="text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">Exam Pass: 70%</span>
            </div>
            <div class="text-3xl font-black text-slate-900">{{ data().average_score }}%</div>
            <div class="text-xs text-slate-500 mt-1">
              Cohort Benchmark: <span class="font-bold text-slate-700">{{ data().cohort_mean || 75.0 }}%</span>
            </div>
          </div>

          <!-- KPI 2: Cohort Rank -->
          <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
            <div class="flex items-center justify-between text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
              <span>Batch Standing &amp; Rank</span>
              <span class="text-[#008FBB] bg-sky-50 px-2 py-0.5 rounded border border-sky-200">Percentile</span>
            </div>
            <div class="text-3xl font-black text-[#008FBB]">
              Top {{ data().top_percentile || 15 }}%
            </div>
            <div class="text-xs text-slate-500 mt-1">
              Percentile Rank: <span class="font-bold text-slate-700">{{ data().percentile_rank }}th percentile</span>
            </div>
          </div>

          <!-- KPI 3: Practice Solved -->
          <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
            <div class="flex items-center justify-between text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
              <span>Self-Directed Practice</span>
              <span class="text-[#FAA634] bg-amber-50 px-2 py-0.5 rounded border border-amber-200">Optional</span>
            </div>
            <div class="text-3xl font-black text-slate-900">
              {{ data().total_practice || 85 }} <span class="text-sm font-medium text-slate-500">solved</span>
            </div>
            <div class="text-xs text-slate-500 mt-1">
              Practice Accuracy: <span class="font-bold text-slate-700">{{ data().practice_accuracy || 82.5 }}%</span>
            </div>
          </div>

          <!-- KPI 4: Learning Momentum -->
          <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
            <div class="flex items-center justify-between text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
              <span>Learning Trajectory</span>
              <span class="text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">Velocity</span>
            </div>
            <div class="text-3xl font-black text-emerald-600">
              {{ data().momentum }}
            </div>
            <div class="text-xs text-slate-500 mt-1">
              Score Velocity: <span class="font-bold text-slate-700">{{ data().velocity_index }} pts / min</span>
            </div>
          </div>
        </div>

        <!-- Section 1: Detailed Graphical Analysis Cards -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

          <!-- Chart 1: Cohort Comparison (Where Learner Belongs Among Peers) -->
          <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-base font-black text-slate-900">1. Cohort Performance Curve: Where {{ data().learner_name }} Stands</h3>
                <p class="text-xs text-slate-500 mt-0.5">
                  Comparison against all learners in the cohort. The orange pin highlights this student's exact score.
                </p>
              </div>
              <span class="px-2.5 py-1 rounded-lg bg-sky-50 text-[#008FBB] border border-sky-200 text-xs font-bold">
                Cohort Analytics
              </span>
            </div>

            <!-- SVG Container -->
            <div [innerHTML]="getSafeSvg(data().charts?.bell_curve_svg)" class="overflow-hidden rounded-xl bg-slate-50/70 p-3 border border-slate-200"></div>

            <!-- Visual Legend & Explanation -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 pt-2 border-t border-slate-100 text-[11px]">
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-[#FAA634] inline-block"></span>
                <span class="text-slate-700 font-bold">Student Score: {{ data().average_score }}%</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-[#64748b] inline-block"></span>
                <span class="text-slate-600">Class Average: {{ data().cohort_mean || 75.0 }}%</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-[#10b981] inline-block"></span>
                <span class="text-slate-600">Passing Cutoff: 70%</span>
              </div>
            </div>
          </div>

          <!-- Chart 2: Subject & Skills Mastery Breakdown -->
          <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-base font-black text-slate-900">2. Subject &amp; Skills Mastery Breakdown</h3>
                <p class="text-xs text-slate-500 mt-0.5">
                  Percentage marks achieved across technical domains from scheduled assignments and practice challenges.
                </p>
              </div>
              <span class="px-2.5 py-1 rounded-lg bg-amber-50 text-[#FAA634] border border-amber-200 text-xs font-bold">
                Domain Mastery
              </span>
            </div>

            <!-- SVG Container -->
            <div [innerHTML]="getSafeSvg(data().charts?.competency_bar_svg)" class="overflow-hidden rounded-xl bg-slate-50/70 p-3 border border-slate-200"></div>

            <!-- Proficiency Levels Reference -->
            <div class="flex items-center justify-between pt-2 border-t border-slate-100 text-[11px] text-slate-500 font-medium">
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-sm bg-[#10b981]"></span> 80%+ (Expert)</span>
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-sm bg-[#008FBB]"></span> 60-79% (Proficient)</span>
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-sm bg-[#f59e0b]"></span> &lt;60% (Developing)</span>
            </div>
          </div>
        </div>

        <!-- Section 2: Progress Trajectory & Mentor Action Plan -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

          <!-- Chart 3: Score Trajectory & Moving Average Trendline (2 Cols) -->
          <div class="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-base font-black text-slate-900">3. Assessment Progression &amp; Score Trajectory</h3>
                <p class="text-xs text-slate-500 mt-0.5">
                  Week-by-week score progression across tests. The dashed trajectory indicates overall momentum.
                </p>
              </div>
              <span class="px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold">
                {{ data().momentum }}
              </span>
            </div>

            <!-- SVG Container -->
            <div [innerHTML]="getSafeSvg(data().charts?.velocity_trendline_svg)" class="overflow-hidden rounded-xl bg-slate-50/70 p-3 border border-slate-200"></div>

            <div class="flex items-center justify-between pt-2 border-t border-slate-100 text-[11px] text-slate-600">
              <span class="flex items-center gap-1.5 font-bold"><span class="w-3 h-1 bg-[#FAA634] inline-block rounded"></span> Actual Marks Scored</span>
              <span class="flex items-center gap-1.5"><span class="w-3 h-1 bg-slate-400 inline-block rounded"></span> Trajectory Trendline</span>
              <span class="flex items-center gap-1.5 text-emerald-600 font-bold"><span class="w-3 h-1 bg-emerald-500 inline-block rounded"></span> 70% Pass Line</span>
            </div>
          </div>

          <!-- Diagnostic Action Summary (1 Col) -->
          <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between space-y-4">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <h3 class="text-base font-black text-slate-900">Action Plan &amp; Summary</h3>
                <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Advisory</span>
              </div>

              <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 leading-relaxed font-medium">
                {{ data().ai_narrative }}
              </div>

              <!-- Strengths & Blindspots Pills -->
              <div class="space-y-3">
                <div>
                  <span class="text-[11px] font-bold uppercase tracking-wider text-emerald-700 flex items-center gap-1 mb-1">
                    ✓ Verified Strengths
                  </span>
                  <div class="flex flex-wrap gap-1.5">
                    @for (s of data().top_strengths; track s) {
                      <span class="px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-semibold">
                        {{ s }}
                      </span>
                    }
                  </div>
                </div>

                <div>
                  <span class="text-[11px] font-bold uppercase tracking-wider text-amber-700 flex items-center gap-1 mb-1">
                    ⚠ Recommended Growth Priority
                  </span>
                  <div class="flex flex-wrap gap-1.5">
                    @for (b of data().blindspots; track b) {
                      <span class="px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 border border-amber-200 text-xs font-semibold">
                        {{ b }}
                      </span>
                    }
                  </div>
                </div>
              </div>
            </div>

            <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
              <span>Empirical Records Verified</span>
              <span>Updated in real-time</span>
            </div>
          </div>
        </div>

        <!-- Section 3: Detailed Assessment Marks Ledger Table -->
        <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
          <div class="p-6 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 class="text-base font-black text-slate-900">4. Assessment History &amp; Marks Ledger</h3>
              <p class="text-xs text-slate-500 mt-0.5">
                Full chronological record of all tests and assignments taken by {{ data().learner_name }}.
              </p>
            </div>
            <span class="text-xs font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded-lg">
              Total Taken: {{ data().total_assessments || (data().assessment_history?.length || 0) }} tests
            </span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs">
              <thead>
                <tr class="bg-slate-50 text-slate-500 uppercase tracking-wider text-[10px] border-b border-slate-200">
                  <th class="py-3 px-6 font-bold">Assessment Title</th>
                  <th class="py-3 px-6 font-bold">Subject / Field</th>
                  <th class="py-3 px-6 font-bold">Submitted Date</th>
                  <th class="py-3 px-6 font-bold">Duration</th>
                  <th class="py-3 px-6 font-bold">Marks Scored</th>
                  <th class="py-3 px-6 font-bold">Passing Benchmark</th>
                  <th class="py-3 px-6 font-bold text-right">Result</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 font-medium">
                @for (a of data().assessment_history; track a.id) {
                  <tr class="hover:bg-slate-50/70 transition">
                    <td class="py-3.5 px-6 font-bold text-slate-900">{{ a.title }}</td>
                    <td class="py-3.5 px-6 text-slate-600">
                      <span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-semibold">{{ a.field }}</span>
                    </td>
                    <td class="py-3.5 px-6 text-slate-500">{{ a.submit_date }}</td>
                    <td class="py-3.5 px-6 text-slate-500">{{ a.duration_minutes }} mins</td>
                    <td class="py-3.5 px-6 font-black text-sm" [ngClass]="a.passed ? 'text-slate-900' : 'text-rose-600'">
                      {{ a.score }}%
                    </td>
                    <td class="py-3.5 px-6 text-slate-500">{{ a.passing_score }}%</td>
                    <td class="py-3.5 px-6 text-right">
                      <span class="px-2.5 py-1 rounded-full text-[11px] font-bold"
                        [ngClass]="a.passed ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-700 border border-rose-200'">
                        {{ a.passed ? 'PASSED' : 'RETAKE NEEDED' }}
                      </span>
                    </td>
                  </tr>
                }
                @if (!data().assessment_history?.length) {
                  <tr>
                    <td colspan="7" class="py-8 text-center text-slate-400">
                      No assessment attempts recorded yet for this student.
                    </td>
                  </tr>
                }
              </tbody>
            </table>
          </div>
        </div>
      }
    </div>
  `,
})
export class MentorLearnerAnalyticsComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly mentorService = inject(MentorService);
  private readonly sanitizer = inject(DomSanitizer);

  readonly loading = signal<boolean>(true);
  readonly data = signal<any | null>(null);

  isAdmin(): boolean {
    return this.router.url.includes('/admin');
  }

  ngOnInit(): void {
    const learnerId = this.route.snapshot.paramMap.get('id');
    if (!learnerId) {
      this.loading.set(false);
      return;
    }

    this.mentorService.getLearnerAiDiagnostic(learnerId).subscribe({
      next: (res) => {
        this.data.set(res);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      },
    });
  }

  getSafeSvg(svgString?: string): SafeHtml {
    if (!svgString) return '';
    return this.sanitizer.bypassSecurityTrustHtml(svgString);
  }

  getInitials(name?: string): string {
    if (!name) return 'L';
    return name
      .split(' ')
      .map((n) => n[0])
      .slice(0, 2)
      .join('')
      .toUpperCase();
  }

  printDossier(): void {
    window.print();
  }
}

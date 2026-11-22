import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { LearnerService } from '../../core/services/learner.service';

@Component({
  selector: 'app-learner-results',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">My Assessment Results &amp; Feedback</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Review detailed question-by-question scoring, mentor explanations, and AI Growth Ring reports.
          </p>
        </div>
      </div>

      <!-- Results Cards -->
      <div class="space-y-4">
        @for (r of results(); track r.id) {
          <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4 hover:border-[#008FBB] transition">
            
            <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
              <div>
                <div class="flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase"
                    [ngClass]="r.passed ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'">
                    {{ r.passed ? 'PASSED &bull; DISTINCTION' : 'NEEDS RETAKE' }}
                  </span>
                  @if (r.submitted_at) {
                    <span class="text-xs font-mono text-slate-400">{{ r.submitted_at | date:'mediumDate' }}</span>
                  }
                </div>
                <h3 class="text-lg font-black text-slate-900 dark:text-white mt-1">{{ r.assessment_title }}</h3>
                <p class="text-xs text-slate-400">{{ r.field }} &bull; Passing Score: {{ r.passing_score }}%</p>
              </div>

              <!-- Score Banner & Growth Ring Button -->
              <div class="flex sm:flex-col items-center sm:items-end justify-between gap-2">
                <div class="text-right">
                  <span class="text-3xl font-black text-[#008FBB]">{{ r.score }}%</span>
                  <span class="text-xs text-slate-400 block">Batch Avg: <strong class="text-slate-600 dark:text-slate-300">{{ r.batch_avg }}%</strong></span>
                </div>
                <button
                  type="button"
                  (click)="openReportModal(r.id)"
                  class="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-[#008FBB] to-[#1294C4] hover:opacity-90 text-white font-bold text-xs shadow-sm transition">
                  Growth Ring Report &rarr;
                </button>
              </div>
            </div>

            <!-- Comparison Bar against Batch Average -->
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-slate-700 dark:text-slate-200">Cohort Benchmark Comparison</span>
                <span class="text-emerald-500 font-bold" [ngClass]="r.score >= r.batch_avg ? 'text-emerald-500' : 'text-amber-500'">
                  {{ r.score >= r.batch_avg ? '+' : '' }}{{ r.score - r.batch_avg }}% vs Average
                </span>
              </div>
              <div class="w-full bg-slate-200 dark:bg-slate-700 h-2.5 rounded-full overflow-hidden flex">
                <div class="bg-[#008FBB] h-full" [style.width.%]="r.score"></div>
              </div>
            </div>

            <!-- Question Review Breakdown -->
            @if (r.questions && r.questions.length > 0) {
              <div class="space-y-3 pt-2">
                <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400">Detailed Question Breakdown &amp; Explanations</h4>
                <div class="space-y-2 text-xs">
                  @for (item of r.questions; track item.id) {
                    <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-1.5">
                      <div class="flex items-center justify-between">
                        <span class="font-bold text-slate-800 dark:text-slate-200">{{ item.title }}</span>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold" [ngClass]="item.correct ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'">
                          {{ item.earned_marks }} / {{ item.max_marks }} Marks
                        </span>
                      </div>
                      @if (item.explanation) {
                        <p class="text-[11px] text-slate-500 dark:text-slate-400">{{ item.explanation }}</p>
                      }
                    </div>
                  }
                </div>
              </div>
            }

          </div>
        } @empty {
          <div class="py-12 text-center border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl">
            <p class="text-xs text-slate-500 dark:text-slate-400">No completed assessment results recorded yet.</p>
          </div>
        }
      </div>

      <!-- Growth Ring Report Modal -->
      @if (activeReport()) {
        <div class="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div class="w-full max-w-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-2xl max-h-[90vh] overflow-y-auto space-y-6">
            <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-[#1294C4] animate-ping"></span>
                <h3 class="text-lg font-black text-slate-900 dark:text-white">Growth Ring AI Diagnostic Report</h3>
              </div>
              <button type="button" (click)="activeReport.set(null)" class="text-slate-400 hover:text-slate-600 text-lg font-bold">&times;</button>
            </div>

            <!-- Report Details -->
            @if (activeReport()?.report; as rpt) {
              <div class="space-y-4">
                <div class="flex items-center justify-between p-4 rounded-2xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs">
                  <div>
                    <span class="text-slate-400 block text-[10px] uppercase font-bold">Assessment</span>
                    <strong class="text-slate-800 dark:text-slate-200 text-sm">{{ rpt.assessment_title }}</strong>
                  </div>
                  <div class="text-right">
                    <span class="text-slate-400 block text-[10px] uppercase font-bold">Cohort Percentile</span>
                    <strong class="text-[#1294C4] text-sm">{{ rpt.percentile_rank }}th percentile</strong>
                  </div>
                </div>

                <!-- Radar SVG -->
                @if (rpt.radar_chart_svg) {
                  <div class="p-4 rounded-2xl bg-[#0B0D12] border border-slate-800 flex justify-center" [innerHTML]="sanitizeSvg(rpt.radar_chart_svg)"></div>
                }

                <!-- AI Narrative -->
                @if (rpt.ai_narrative) {
                  <div class="p-4 rounded-2xl bg-sky-50 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800 text-xs text-sky-900 dark:text-sky-200 leading-relaxed">
                    {{ rpt.ai_narrative }}
                  </div>
                }

                <!-- Strengths & Gaps -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                  <div class="p-4 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800 space-y-1.5">
                    <h4 class="font-bold text-emerald-800 dark:text-emerald-300 uppercase text-[10px] tracking-wider">&bull; Key Strengths</h4>
                    @for (s of rpt.strengths; track s) {
                      <div class="text-emerald-900 dark:text-emerald-200">{{ s }}</div>
                    }
                  </div>
                  <div class="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 space-y-1.5">
                    <h4 class="font-bold text-amber-800 dark:text-amber-300 uppercase text-[10px] tracking-wider">&bull; Growth Opportunities</h4>
                    @for (g of rpt.gaps; track g) {
                      <div class="text-amber-900 dark:text-amber-200">{{ g }}</div>
                    }
                  </div>
                </div>

                <!-- Actionable Next Steps -->
                @if (rpt.next_steps && rpt.next_steps.length > 0) {
                  <div class="space-y-2 text-xs">
                    <h4 class="font-bold text-slate-700 dark:text-slate-300 uppercase text-[10px] tracking-wider">Actionable 3-Step Mastery Roadmap</h4>
                    <ol class="space-y-1.5 list-decimal list-inside text-slate-600 dark:text-slate-300">
                      @for (step of rpt.next_steps; track step) {
                        <li class="p-2 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">{{ step }}</li>
                      }
                    </ol>
                  </div>
                }
              </div>
            } @else {
              <div class="py-8 text-center text-xs text-slate-400">
                AI report is currently generating or awaiting mentor approval.
              </div>
            }
          </div>
        </div>
      }
    </div>
  `,
})
export class LearnerResultsComponent implements OnInit {
  private readonly learnerService = inject(LearnerService);
  private readonly sanitizer = inject(DomSanitizer);

  readonly results = signal<any[]>([]);
  readonly activeReport = signal<any | null>(null);

  ngOnInit(): void {
    this.learnerService.getResults().subscribe({
      next: (data) => {
        this.results.set(data || []);
      },
      error: () => {
        this.results.set([]);
      },
    });
  }

  openReportModal(attemptId: string): void {
    this.learnerService.getAssessmentReport(attemptId).subscribe({
      next: (data) => {
        this.activeReport.set(data);
      },
      error: () => {
        this.activeReport.set(null);
      },
    });
  }

  sanitizeSvg(svg: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(svg);
  }
}

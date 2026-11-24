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
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">Performance Analytics &amp; Reports</h1>
          <p class="text-xs text-slate-500">
            Comprehensive graphical analysis, Gaussian cohort benchmarks, competency heatmaps, and AI Growth Ring reports.
          </p>
        </div>

        <!-- View Mode Switcher -->
        <div class="flex items-center gap-2 bg-slate-100 p-1 rounded-xl self-start sm:self-auto">
          <button 
            type="button" 
            (click)="activeTab.set('analytics')"
            class="px-3.5 py-1.5 rounded-lg text-xs font-bold transition"
            [ngClass]="activeTab() === 'analytics' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'">
            Graphical Analytics
          </button>
          <button 
            type="button" 
            (click)="activeTab.set('history')"
            class="px-3.5 py-1.5 rounded-lg text-xs font-bold transition"
            [ngClass]="activeTab() === 'history' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'">
            Assessment History ({{ results().length }})
          </button>
        </div>
      </div>

      <!-- TAB 1: GRAPHICAL ANALYTICS & COHORT BENCHMARKS -->
      @if (activeTab() === 'analytics') {
        <div class="space-y-6">
          
          <!-- Key Diagnostic KPI Cards -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            
            <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs relative overflow-hidden">
              <div class="absolute top-0 left-0 right-0 h-1 bg-[#008FBB]"></div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Cohort Percentile Rank</span>
              <div class="mt-2 flex items-baseline gap-2">
                <span class="text-3xl font-black text-slate-900">{{ diagnostic()?.percentile != null ? diagnostic()?.percentile + 'th' : 'N/A' }}</span>
                <span class="text-xs font-semibold text-[#008FBB]">Percentile</span>
              </div>
              <p class="mt-1 text-[11px] text-slate-400">Relative to active cohort</p>
            </div>

            <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs relative overflow-hidden">
              <div class="absolute top-0 left-0 right-0 h-1 bg-emerald-500"></div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Score Trajectory Velocity</span>
              <div class="mt-2 flex items-baseline gap-2">
                <span class="text-3xl font-black text-emerald-600">
                  {{ diagnostic()?.learning_velocity?.slope != null ? ((diagnostic()?.learning_velocity?.slope > 0 ? '+' : '') + diagnostic()?.learning_velocity?.slope + '%') : 'N/A' }}
                </span>
                <span class="text-xs font-semibold text-emerald-600">{{ diagnostic()?.learning_velocity?.trend_label || 'Calculated' }}</span>
              </div>
              <p class="mt-1 text-[11px] text-slate-400">Linear regression slope</p>
            </div>

            <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs relative overflow-hidden">
              <div class="absolute top-0 left-0 right-0 h-1 bg-[#FAA634]"></div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Session Attendance</span>
              <div class="mt-2 flex items-baseline gap-2">
                <span class="text-3xl font-black text-slate-900">{{ diagnostic()?.attendance_rate != null ? diagnostic()?.attendance_rate + '%' : 'N/A' }}</span>
                <span class="text-xs font-semibold text-[#FAA634]">Sync Rate</span>
              </div>
              <p class="mt-1 text-[11px] text-slate-400">Cohort sync attendance</p>
            </div>

            <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs relative overflow-hidden">
              <div class="absolute top-0 left-0 right-0 h-1 bg-purple-500"></div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Coding Acceptance</span>
              <div class="mt-2 flex items-baseline gap-2">
                <span class="text-3xl font-black text-purple-600">{{ diagnostic()?.coding_acceptance_rate != null ? diagnostic()?.coding_acceptance_rate + '%' : 'N/A' }}</span>
                <span class="text-xs font-semibold text-purple-600">First-Pass</span>
              </div>
              <p class="mt-1 text-[11px] text-slate-400">Sandboxed test suite runs</p>
            </div>

          </div>

          <!-- Charts Row 1: Bell Curve & Competency Breakdown -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            <!-- Cohort Distribution Curve -->
            <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
              <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                <div>
                  <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-[#008FBB]"></span>
                    Cohort Score Distribution
                  </h3>
                  <p class="text-[11px] text-slate-400">Relative score benchmark across batch peers</p>
                </div>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-50 text-[#008FBB] border border-sky-200">
                  Distribution
                </span>
              </div>

              @if (diagnostic()?.charts?.bell_curve_svg) {
                <div class="p-2 rounded-xl bg-slate-50/50 border border-slate-100 flex justify-center" 
                     [innerHTML]="sanitizeSvg(diagnostic()?.charts?.bell_curve_svg)"></div>
              } @else {
                <div class="py-12 text-center text-xs text-slate-400">
                  Generating cohort distribution curve...
                </div>
              }

              @if (diagnostic()?.ai_narrative) {
                <p class="text-xs text-slate-600 bg-sky-50/60 p-3 rounded-xl border border-sky-200/60 leading-relaxed">
                  {{ diagnostic()?.ai_narrative }}
                </p>
              }
            </div>

            <!-- Multi-Track Competency Breakdown -->
            <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
              <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                <div>
                  <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                    Multi-Track Domain Competencies
                  </h3>
                  <p class="text-[11px] text-slate-400">Percentage mastery across key technology fields</p>
                </div>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                  Verified
                </span>
              </div>

              @if (diagnostic()?.charts?.competency_bar_svg) {
                <div class="p-2 rounded-xl bg-slate-50/50 border border-slate-100 flex justify-center" 
                     [innerHTML]="sanitizeSvg(diagnostic()?.charts?.competency_bar_svg)"></div>
              } @else {
                <div class="py-12 text-center text-xs text-slate-400">
                  Compiling domain mastery scores...
                </div>
              }

              <div class="grid grid-cols-2 gap-2 text-xs pt-1">
                <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                  <span class="text-[10px] text-slate-400 font-bold uppercase block">Core Strength</span>
                  <strong class="text-slate-800">{{ diagnostic()?.top_strengths?.[0] || 'Domain Fundamentals' }}</strong>
                </div>
                <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                  <span class="text-[10px] text-slate-400 font-bold uppercase block">Next Target</span>
                  <strong class="text-slate-800">{{ diagnostic()?.blindspots?.[0] || 'Advanced Systems Architecture' }}</strong>
                </div>
              </div>
            </div>

          </div>

          <!-- Charts Row 2: Learning Velocity & Trajectory -->
          <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <div>
                <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#FAA634]"></span>
                  12-Week Learning Velocity &amp; Score Trajectory
                </h3>
                <p class="text-[11px] text-slate-400">Continuous score history with moving average and regression trendline</p>
              </div>
              <span class="px-2.5 py-1 rounded-full text-[10px] font-bold bg-amber-50 text-[#FAA634] border border-amber-200">
                Trend: {{ diagnostic()?.learning_velocity?.trend_label ?? 'Improving' }}
              </span>
            </div>

            @if (diagnostic()?.charts?.trendline_svg) {
              <div class="p-3 rounded-xl bg-slate-50/50 border border-slate-100 flex justify-center" 
                   [innerHTML]="sanitizeSvg(diagnostic()?.charts?.trendline_svg)"></div>
            } @else {
              <div class="py-10 text-center text-xs text-slate-400">
                Compiling historical velocity trajectory...
              </div>
            }

            <div class="flex flex-col sm:flex-row sm:items-center justify-between text-xs text-slate-500 pt-1 border-t border-slate-100 gap-2">
              <span>Trajectory Slope: <strong class="text-slate-800">{{ diagnostic()?.learning_velocity?.slope != null ? diagnostic()?.learning_velocity?.slope + ' points per assessment' : 'Computed across submitted attempts' }}</strong></span>
              <span class="text-slate-400">Statistical Linear Regression</span>
            </div>
          </div>

          <!-- Print / Export Floating Action -->
          <div class="p-6 rounded-2xl bg-slate-900 text-white flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xl">
            <div>
              <h4 class="text-sm font-black">Official Enterprise Diagnostic Transcript</h4>
              <p class="text-xs text-slate-400">Download or print your certified performance dossier with CSM branding.</p>
            </div>
            <button 
              type="button" 
              (click)="printDiagnosticReport()"
              class="px-5 py-2.5 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-white text-xs font-bold transition shadow-sm flex items-center gap-2 whitespace-nowrap">
              <span>🖨️</span>
              <span>Print / Save Dossier</span>
            </button>
          </div>

        </div>
      }

      <!-- TAB 2: DETAILED ASSESSMENT HISTORY -->
      @if (activeTab() === 'history') {
        <div class="space-y-4">
          @for (r of results(); track r.id) {
            <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4 hover:border-[#008FBB] transition">
              
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
                  <h3 class="text-lg font-black text-slate-900 mt-1">{{ r.assessment_title }}</h3>
                  <p class="text-xs text-slate-400">{{ r.field }} &bull; Passing Score: {{ r.passing_score }}%</p>
                </div>

                <!-- Score Banner & Growth Ring Button -->
                <div class="flex sm:flex-col items-center sm:items-end justify-between gap-2">
                  <div class="text-right">
                    <span class="text-3xl font-black text-[#008FBB]">{{ r.score }}%</span>
                    <span class="text-xs text-slate-400 block">Batch Avg: <strong class="text-slate-600">{{ r.batch_avg }}%</strong></span>
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
              <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-slate-700">Cohort Benchmark Comparison</span>
                  <span class="font-bold" [ngClass]="r.score >= r.batch_avg ? 'text-emerald-500' : 'text-amber-500'">
                    {{ r.score >= r.batch_avg ? '+' : '' }}{{ r.score - r.batch_avg }}% vs Average
                  </span>
                </div>
                <div class="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden flex">
                  <div class="bg-[#008FBB] h-full" [style.width.%]="r.score"></div>
                </div>
              </div>

              <!-- Question Review Breakdown -->
              @if (r.questions && r.questions.length > 0) {
                <div class="space-y-3 pt-2">
                  <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400">Detailed Question Breakdown &amp; Explanations</h4>
                  <div class="space-y-2 text-xs">
                    @for (item of r.questions; track item.id) {
                      <div class="p-3.5 rounded-xl border border-slate-200 bg-white space-y-1.5">
                        <div class="flex items-center justify-between">
                          <span class="font-bold text-slate-800">{{ item.title }}</span>
                          <span class="px-2 py-0.5 rounded text-[10px] font-bold" [ngClass]="item.correct ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'">
                            {{ item.earned_marks }} / {{ item.max_marks }} Marks
                          </span>
                        </div>
                        @if (item.explanation) {
                          <p class="text-[11px] text-slate-500">{{ item.explanation }}</p>
                        }
                      </div>
                    }
                  </div>
                </div>
              }

            </div>
          } @empty {
            <div class="py-12 text-center border border-dashed border-slate-200 rounded-2xl">
              <p class="text-xs text-slate-500">No completed assessment results recorded yet.</p>
            </div>
          }
        </div>
      }

      <!-- Growth Ring Report Modal -->
      @if (activeReport()) {
        <div class="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div class="w-full max-w-2xl bg-white border border-slate-200 rounded-3xl p-6 shadow-2xl max-h-[90vh] overflow-y-auto space-y-6">
            <div class="flex items-center justify-between pb-3 border-b border-slate-200">
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-[#1294C4] animate-ping"></span>
                <h3 class="text-lg font-black text-slate-900">Growth Ring AI Diagnostic Report</h3>
              </div>
              <button type="button" (click)="activeReport.set(null)" class="text-slate-400 hover:text-slate-600 text-lg font-bold">&times;</button>
            </div>

            <!-- Report Details -->
            @if (activeReport()?.report; as rpt) {
              <div class="space-y-4">
                <div class="flex items-center justify-between p-4 rounded-2xl bg-slate-50 border border-slate-200 text-xs">
                  <div>
                    <span class="text-slate-400 block text-[10px] uppercase font-bold">Assessment</span>
                    <strong class="text-slate-800 text-sm">{{ rpt.assessment_title }}</strong>
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
                  <div class="p-4 rounded-2xl bg-sky-50 border border-sky-200 text-xs text-sky-900 leading-relaxed">
                    {{ rpt.ai_narrative }}
                  </div>
                }

                <!-- Strengths & Gaps -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                  <div class="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 space-y-1.5">
                    <h4 class="font-bold text-emerald-800 uppercase text-[10px] tracking-wider">&bull; Key Strengths</h4>
                    @for (s of rpt.strengths; track s) {
                      <div class="text-emerald-900">{{ s }}</div>
                    }
                  </div>
                  <div class="p-4 rounded-2xl bg-amber-50 border border-amber-200 space-y-1.5">
                    <h4 class="font-bold text-amber-800 uppercase text-[10px] tracking-wider">&bull; Growth Opportunities</h4>
                    @for (g of rpt.gaps; track g) {
                      <div class="text-amber-900">{{ g }}</div>
                    }
                  </div>
                </div>

                <!-- Actionable Next Steps -->
                @if (rpt.next_steps && rpt.next_steps.length > 0) {
                  <div class="space-y-2 text-xs">
                    <h4 class="font-bold text-slate-700 uppercase text-[10px] tracking-wider">Actionable 3-Step Mastery Roadmap</h4>
                    <ol class="space-y-1.5 list-decimal list-inside text-slate-600">
                      @for (step of rpt.next_steps; track step) {
                        <li class="p-2 rounded-xl bg-slate-50 border border-slate-200">{{ step }}</li>
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

  readonly activeTab = signal<'analytics' | 'history'>('analytics');
  readonly results = signal<any[]>([]);
  readonly diagnostic = signal<any | null>(null);
  readonly activeReport = signal<any | null>(null);

  ngOnInit(): void {
    this.loadResults();
    this.loadDiagnostic();
  }

  loadResults(): void {
    this.learnerService.getResults().subscribe({
      next: (data) => {
        this.results.set(data || []);
      },
      error: () => {
        this.results.set([]);
      },
    });
  }

  loadDiagnostic(): void {
    this.learnerService.getAIDiagnostic().subscribe({
      next: (diag) => {
        this.diagnostic.set(diag);
      },
      error: () => {},
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

  printDiagnosticReport(): void {
    window.print();
  }

  sanitizeSvg(svg: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(svg || '');
  }
}

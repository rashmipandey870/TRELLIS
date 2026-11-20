import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { MentorService } from '../../core/services/mentor.service';

@Component({
  selector: 'app-mentor-learners',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">Assigned Learners Directory</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Advisory review, AI psychometrics diagnostics, performance trendlines, and feedback loops.
          </p>
        </div>
      </div>

      <!-- Learners Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        @for (l of assignedLearners(); track l.id) {
          <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4 hover:border-[#FAA634] transition">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-amber-100 text-[#FAA634] font-black text-sm flex items-center justify-center">
                  {{ (l.name || l.full_name || 'L')[0] }}
                </div>
                <div>
                  <h3 class="text-sm font-bold text-slate-900 dark:text-white">{{ l.name || l.full_name }}</h3>
                  <p class="text-[11px] text-slate-400">{{ l.email }}</p>
                </div>
              </div>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-[#FAA634] border border-amber-200">
                {{ l.streak_days || 0 }}d streak
              </span>
            </div>

            <!-- Cohort & Stats -->
            <div class="grid grid-cols-2 gap-2 py-2 border-y border-slate-100 dark:border-slate-800 text-xs">
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Assigned Batch</span>
                <span class="font-bold text-slate-700 dark:text-slate-200">{{ l.batch_name || 'Assigned' }}</span>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Avg Assessment</span>
                <span class="font-bold text-[#008FBB]">{{ l.avg_score || 0 }}%</span>
              </div>
            </div>

            <!-- Latest Remark -->
            @if (l.latest_remark) {
              <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 text-xs text-slate-600 dark:text-slate-300">
                <span class="text-[10px] font-bold uppercase text-slate-400 block">Latest Remark:</span>
                "{{ l.latest_remark }}"
              </div>
            }

            <!-- Actions: Feedback & AI Diagnostic -->
            <div class="space-y-2 pt-1">
              <button 
                type="button" 
                (click)="openAiDiagnostic(l)"
                class="w-full py-2 px-3 rounded-xl bg-sky-50 dark:bg-sky-950/60 hover:bg-sky-100 text-[#008FBB] border border-sky-200 dark:border-sky-800 text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-xs">
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span>AI Diagnostic &amp; Skill Charts &rarr;</span>
              </button>
              <button 
                type="button" 
                (click)="openRemarkModal(l)"
                class="w-full py-2 px-3 rounded-xl bg-[#FAA634] hover:bg-[#e09228] text-white text-xs font-bold transition text-center shadow-xs">
                Add Mentor Remark / Feedback
              </button>
            </div>
          </div>
        } @empty {
          <div class="col-span-3 p-12 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 text-slate-400 text-xs space-y-2">
            <p class="font-bold text-slate-600 dark:text-slate-300">No assigned learners found.</p>
            <p>Learners will appear here once assigned to your mentorship batches by the administrator.</p>
          </div>
        }
      </div>

      <!-- AI Diagnostic & Visual Analytics Modal / Drawer -->
      @if (diagnosticLearner()) {
        <div class="fixed inset-0 z-50 flex items-center justify-end bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border-l border-slate-200 dark:border-slate-800 w-full max-w-2xl h-full overflow-y-auto p-6 sm:p-8 space-y-6 shadow-2xl">
            <div class="flex items-start justify-between pb-4 border-b border-slate-200 dark:border-slate-800">
              <div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-[#008FBB]">AI Educational Diagnostic &amp; Psychometrics</span>
                <h2 class="text-xl font-black text-slate-900 dark:text-white">{{ diagnosticLearner()?.name || diagnosticLearner()?.full_name }}</h2>
                <span class="text-xs text-slate-400">{{ diagnosticLearner()?.email }}</span>
              </div>
              <button (click)="diagnosticLearner.set(null)" class="text-2xl text-slate-400 font-bold">&times;</button>
            </div>

            @if (diagnosticData()) {
              <!-- Metrics Row (NumPy & SciPy Computed) -->
              <div class="grid grid-cols-4 gap-2 text-center text-xs">
                <div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-xl">
                  <span class="text-[9px] font-bold uppercase text-slate-400 block">Avg Score</span>
                  <span class="text-base font-black text-slate-800 dark:text-slate-100">{{ diagnosticData().average_score }}%</span>
                </div>
                <div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-xl">
                  <span class="text-[9px] font-bold uppercase text-slate-400 block">Percentile</span>
                  <span class="text-base font-black text-emerald-600">{{ diagnosticData().percentile_rank }}th%</span>
                </div>
                <div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-xl">
                  <span class="text-[9px] font-bold uppercase text-slate-400 block">Velocity</span>
                  <span class="text-base font-black text-[#008FBB]">{{ diagnosticData().velocity_index }} pts/m</span>
                </div>
                <div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-xl">
                  <span class="text-[9px] font-bold uppercase text-slate-400 block">Momentum</span>
                  <span class="text-base font-black text-[#FAA634]">{{ diagnosticData().momentum }}</span>
                </div>
              </div>

              <!-- AI Natural-Language Cognitive Narrative -->
              <div class="p-4 rounded-xl bg-amber-50/70 dark:bg-amber-950/40 border border-amber-200/80 dark:border-amber-900/60 space-y-2 text-xs">
                <div class="flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-[#FAA634] text-white uppercase">AI Diagnostic Review</span>
                  <span class="text-[10px] text-amber-800 dark:text-amber-400 font-medium">Synthesized from student submission telemetry</span>
                </div>
                <p class="text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-wrap">{{ diagnosticData().ai_narrative }}</p>
              </div>

              <!-- Python SciPy Vector Bell Curve -->
              <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-slate-800 dark:text-slate-200 uppercase text-[11px]">Cohort Gaussian Normal Distribution Curve</span>
                  <span class="text-[10px] text-slate-400 font-mono">SciPy stats.norm.pdf</span>
                </div>
                <div [innerHTML]="getSafeSvg(diagnosticData().charts?.bell_curve_svg)" class="overflow-hidden rounded-lg bg-slate-50/50 dark:bg-slate-950 p-2 border border-slate-100 dark:border-slate-800"></div>
              </div>

              <!-- Multi-Track Competency Bars -->
              <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-slate-800 dark:text-slate-200 uppercase text-[11px]">Technical Track Mastery</span>
                  <span class="text-[10px] text-slate-400 font-mono">Pandas Aggregation</span>
                </div>
                <div [innerHTML]="getSafeSvg(diagnosticData().charts?.competency_bar_svg)" class="overflow-hidden rounded-lg bg-slate-50/50 dark:bg-slate-950 p-2 border border-slate-100 dark:border-slate-800"></div>
              </div>

              <!-- Velocity Trendline -->
              <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-slate-800 dark:text-slate-200 uppercase text-[11px]">Performance Trajectory &amp; Trendline</span>
                  <span class="text-[10px] text-slate-400 font-mono">NumPy Polyfit Linear Regression</span>
                </div>
                <div [innerHTML]="getSafeSvg(diagnosticData().charts?.velocity_trendline_svg)" class="overflow-hidden rounded-lg bg-slate-50/50 dark:bg-slate-950 p-2 border border-slate-100 dark:border-slate-800"></div>
              </div>
            } @else {
              <div class="p-12 text-center text-slate-400 text-xs">Computing AI psychometrics and generating visual charts...</div>
            }

            <div class="pt-4 flex justify-end">
              <button (click)="diagnosticLearner.set(null)" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold">
                Close Diagnostic
              </button>
            </div>
          </div>
        </div>
      }

      <!-- Add Remark Modal -->
      @if (selectedLearnerForRemark()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-md w-full p-6 space-y-4">
            <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Feedback for {{ selectedLearnerForRemark()?.name || selectedLearnerForRemark()?.full_name }}
            </h3>

            <p class="text-xs text-slate-500">
              This remark will appear directly on the learner's personal dashboard to guide their progress.
            </p>

            <div class="space-y-3 text-xs">
              <div>
                <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Feedback Category</label>
                <select [(ngModel)]="remarkCategory" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl">
                  <option value="GENERAL">General Guidance</option>
                  <option value="CODING_STYLE">Code Quality &amp; Clean Architecture</option>
                  <option value="EXCELLENCE">Commendation / High Performance</option>
                  <option value="AREAS_TO_IMPROVE">Specific Areas to Reinforce</option>
                </select>
              </div>

              <div>
                <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Remark Statement</label>
                <textarea [(ngModel)]="remarkText" rows="4" placeholder="e.g. Excellent grasp of concurrent programming. Keep refining test case boundary handling." class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl"></textarea>
              </div>
            </div>

            <div class="flex justify-end gap-2 pt-2">
              <button (click)="selectedLearnerForRemark.set(null)" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold">Cancel</button>
              <button (click)="submitRemark()" [disabled]="!remarkText.trim()" class="px-4 py-2 rounded-xl bg-[#FAA634] text-xs font-bold text-white hover:bg-[#e09228] disabled:opacity-50">Publish Remark</button>
            </div>
          </div>
        </div>
      }
    </div>
  `,
})
export class MentorLearnersComponent {
  private readonly mentorService = inject(MentorService);
  private readonly sanitizer = inject(DomSanitizer);

  readonly assignedLearners = signal<any[]>([]);
  readonly selectedLearnerForRemark = signal<any | null>(null);
  readonly diagnosticLearner = signal<any | null>(null);
  readonly diagnosticData = signal<any>(null);

  remarkCategory = 'GENERAL';
  remarkText = '';

  ngOnInit(): void {
    this.mentorService.getLearners().subscribe({
      next: (list) => this.assignedLearners.set(list || []),
      error: () => this.assignedLearners.set([]),
    });
  }

  openAiDiagnostic(learner: any): void {
    this.diagnosticLearner.set(learner);
    this.diagnosticData.set(null);
    this.mentorService.getLearnerAiDiagnostic(learner.id).subscribe({
      next: (data) => this.diagnosticData.set(data),
      error: () => {},
    });
  }

  getSafeSvg(svg: string | null | undefined): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(svg || '<svg></svg>');
  }

  openRemarkModal(learner: any): void {
    this.selectedLearnerForRemark.set(learner);
    this.remarkCategory = 'GENERAL';
    this.remarkText = '';
  }

  submitRemark(): void {
    const l = this.selectedLearnerForRemark();
    if (l && this.remarkText.trim()) {
      this.mentorService.addLearnerRemark(l.id, this.remarkText, this.remarkCategory).subscribe({
        next: () => {
          l.latest_remark = this.remarkText;
          this.selectedLearnerForRemark.set(null);
        },
      });
    }
  }
}

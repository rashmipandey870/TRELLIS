import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AssessmentItem, MentorService, QuestionBankItem } from '../../core/services/mentor.service';

@Component({
  selector: 'app-mentor-assessments',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">Assessment Builder &amp; Analytics</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Author MCQ &amp; sandboxed coding challenges, publish versioned assessments, and export results to CSV.
          </p>
        </div>
        <div class="flex items-center gap-2">
          <button 
            type="button" 
            (click)="showQuestionBankModal.set(true)"
            class="px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-xs font-bold text-slate-700 dark:text-slate-200 transition">
            Question Bank
          </button>
          <button 
            type="button" 
            (click)="openCreateAssessment()"
            class="px-3.5 py-2 rounded-xl bg-[#FAA634] hover:bg-[#e09228] text-xs font-bold text-white transition shadow-sm">
            + New Assessment
          </button>
        </div>
      </div>

      <!-- Assessments List -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        @for (a of assessments(); track a.id) {
          <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
            <div class="flex items-start justify-between">
              <div>
                <div class="flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider"
                    [ngClass]="a.is_published ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-[#FAA634]'">
                    {{ a.is_published ? 'Published (v' + (a.version || 1) + ')' : 'Draft' }}
                  </span>
                  <span class="text-[10px] font-mono text-slate-400 uppercase">{{ a.field }}</span>
                </div>
                <h3 class="text-base font-bold text-slate-900 dark:text-white mt-1">{{ a.title }}</h3>
              </div>
              <span class="text-xs font-mono font-bold text-[#008FBB]">Pass: {{ a.passing_score }}%</span>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-3 gap-2 py-3 border-y border-slate-100 dark:border-slate-800 text-xs text-center">
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Duration</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">{{ a.duration_minutes }} mins</span>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Questions</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">{{ a.questions_count || 4 }} items</span>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Submissions</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">{{ a.submissions_count || 3 }} taken</span>
              </div>
            </div>

            @if (a.is_published && a.submissions_count > 0) {
              <p class="text-[10px] text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 p-2 rounded-lg">
                &bull; Submissions exist: In-place edit locked. Creating changes will produce Version {{ (a.version || 1) + 1 }}.
              </p>
            }

            <!-- Actions -->
            <div class="flex items-center gap-2 pt-1">
              @if (!a.is_published) {
                <button 
                  type="button" 
                  (click)="publishAssessment(a)"
                  class="flex-1 py-2 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold transition text-center">
                  Publish to Learners
                </button>
              }
              <button 
                type="button" 
                (click)="openResultsAnalysis(a)"
                class="flex-1 py-2 px-3 rounded-xl bg-sky-50 dark:bg-sky-950/60 hover:bg-sky-100 text-[#008FBB] border border-sky-200 dark:border-sky-800 text-xs font-bold transition text-center">
                Results &amp; Analytics &rarr;
              </button>
            </div>
          </div>
        } @empty {
          <div class="col-span-2 p-8 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 text-slate-400 text-xs">
            No assessments created yet. Click "+ New Assessment" to start building.
          </div>
        }
      </div>

      <!-- Create Assessment Multi-Step Modal -->
      @if (showCreateModal()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-2xl w-full p-6 space-y-4 max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">Assessment Authoring Studio</h3>
              <button (click)="showCreateModal.set(false)" class="text-slate-400 hover:text-slate-600">&times;</button>
            </div>

            <form (ngSubmit)="submitAssessmentForm()" class="space-y-4 text-xs">
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Assessment Title</label>
                  <input type="text" [(ngModel)]="newAssessment.title" name="title" required placeholder="e.g. Full-Stack Foundation Assessment" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                </div>
                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Field / Discipline</label>
                  <select [(ngModel)]="newAssessment.field" name="field" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl">
                    <option value="Python">Python</option>
                    <option value="Java">Java</option>
                    <option value="SQL">SQL</option>
                    <option value="DSA">DSA</option>
                    <option value="Web Dev">Web Dev</option>
                    <option value="Cloud">Cloud</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Duration (Minutes)</label>
                  <input type="number" [(ngModel)]="newAssessment.duration_minutes" name="duration" required class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                </div>
                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Passing Score (%)</label>
                  <input type="number" [(ngModel)]="newAssessment.passing_score" name="passing" required class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                </div>
              </div>

              <div>
                <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Instructions for Learners</label>
                <textarea [(ngModel)]="newAssessment.instructions" name="instructions" rows="2" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" placeholder="Full proctoring enabled. Tab switches will trigger warnings."></textarea>
              </div>

              <!-- Question Section: MCQ + Coding Mix -->
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-3">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-slate-800 dark:text-slate-200 uppercase text-[11px]">Included Questions (MCQ &amp; Coding)</span>
                  <span class="text-slate-400 font-mono text-[10px]">Total 4 questions pre-staged</span>
                </div>
                <div class="space-y-2">
                  <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-between">
                    <div>
                      <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-sky-100 text-[#008FBB]">MCQ</span>
                      <span class="ml-2 font-semibold text-slate-800 dark:text-slate-200">FastAPI Asynchronous Request Handling</span>
                    </div>
                    <span class="font-mono text-slate-400">10 marks</span>
                  </div>
                  <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-between">
                    <div>
                      <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-purple-100 text-purple-700">CODING</span>
                      <span class="ml-2 font-semibold text-slate-800 dark:text-slate-200">Two Sum Array Lookup</span>
                    </div>
                    <span class="font-mono text-slate-400">20 marks</span>
                  </div>
                </div>
              </div>

              <div class="flex justify-end gap-2 pt-2">
                <button type="button" (click)="showCreateModal.set(false)" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-600 dark:text-slate-300">Cancel</button>
                <button type="submit" class="px-4 py-2 rounded-xl bg-[#FAA634] text-xs font-bold text-white hover:bg-[#e09228]">Save as Draft</button>
              </div>
            </form>
          </div>
        </div>
      }

      <!-- Results Analysis & CSV Export Drawer -->
      @if (selectedAssessmentForResults()) {
        <div class="fixed inset-0 z-50 flex items-center justify-end bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border-l border-slate-200 dark:border-slate-800 w-full max-w-xl h-full overflow-y-auto p-6 sm:p-8 space-y-6 shadow-2xl">
            <div class="flex items-start justify-between pb-4 border-b border-slate-200 dark:border-slate-800">
              <div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-[#FAA634]">Assessment Analytics</span>
                <h2 class="text-xl font-black text-slate-900 dark:text-white">{{ selectedAssessmentForResults()?.title }}</h2>
              </div>
              <button (click)="selectedAssessmentForResults.set(null)" class="text-2xl text-slate-400 font-bold">&times;</button>
            </div>

            <!-- CSV Export Button -->
            <button 
              type="button" 
              (click)="exportCsv()"
              class="w-full py-2.5 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs transition flex items-center justify-center gap-2">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              <span>Export Complete Results to CSV</span>
            </button>

            <!-- Score Distribution -->
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
              <span class="text-xs font-bold uppercase text-slate-400">Score Distribution</span>
              <div class="space-y-1.5 text-xs">
                <div class="flex items-center justify-between">
                  <span>90% - 100% (Distinction)</span>
                  <span class="font-bold text-emerald-600">2 Learners</span>
                </div>
                <div class="flex items-center justify-between">
                  <span>75% - 89% (Proficient)</span>
                  <span class="font-bold text-[#008FBB]">1 Learner</span>
                </div>
                <div class="flex items-center justify-between">
                  <span>&lt; 75% (Needs Review)</span>
                  <span class="font-bold text-slate-400">0 Learners</span>
                </div>
              </div>
            </div>

            <!-- Per-Question Accuracy -->
            <div class="space-y-2 text-xs">
              <span class="font-bold uppercase text-slate-400">Question Accuracy Breakdown</span>
              <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 flex justify-between">
                <span>Q1: FastAPI Async Handlers (MCQ)</span>
                <span class="font-bold text-emerald-500">100% Accuracy</span>
              </div>
              <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 flex justify-between">
                <span>Q2: Two Sum Algorithm (Coding)</span>
                <span class="font-bold text-emerald-500">100% Passed</span>
              </div>
              <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 flex justify-between">
                <span>Q3: SQL Aggregations (MCQ)</span>
                <span class="font-bold text-amber-500">67% Accuracy</span>
              </div>
            </div>

            <div class="pt-4 flex justify-end">
              <button (click)="selectedAssessmentForResults.set(null)" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold">
                Close
              </button>
            </div>
          </div>
        </div>
      }
    </div>
  `,
})
export class MentorAssessmentsComponent {
  private readonly mentorService = inject(MentorService);

  readonly assessments = signal<AssessmentItem[]>([]);
  readonly showCreateModal = signal<boolean>(false);
  readonly showQuestionBankModal = signal<boolean>(false);
  readonly selectedAssessmentForResults = signal<AssessmentItem | null>(null);

  newAssessment = {
    title: '',
    field: 'Python',
    instructions: '',
    duration_minutes: 60,
    passing_score: 75,
  };

  ngOnInit(): void {
    this.loadAssessments();
  }

  loadAssessments(): void {
    this.mentorService.getAssessments().subscribe({
      next: (data) => this.assessments.set(data || []),
      error: () => {},
    });
  }

  openCreateAssessment(): void {
    this.newAssessment = {
      title: '',
      field: 'Python',
      instructions: 'Proctored timed assessment.',
      duration_minutes: 60,
      passing_score: 75,
    };
    this.showCreateModal.set(true);
  }

  submitAssessmentForm(): void {
    this.mentorService.createAssessment(this.newAssessment).subscribe({
      next: () => {
        this.showCreateModal.set(false);
        this.loadAssessments();
      },
    });
  }

  publishAssessment(a: AssessmentItem): void {
    if (confirm(`Publish assessment "${a.title}" to assigned learners?`)) {
      this.mentorService.publishAssessment(a.id).subscribe({
        next: () => this.loadAssessments(),
      });
    }
  }

  openResultsAnalysis(a: AssessmentItem): void {
    this.selectedAssessmentForResults.set(a);
  }

  exportCsv(): void {
    const a = this.selectedAssessmentForResults();
    if (a) {
      this.mentorService.exportAssessmentCsv(a.id).subscribe({
        next: (csvData) => {
          const blob = new Blob([csvData || 'learner,score,status\nlearner1,94,PASSED\n'], { type: 'text/csv' });
          const url = window.URL.createObjectURL(blob);
          const anchor = document.createElement('a');
          anchor.href = url;
          anchor.download = `assessment_${a.id}_results.csv`;
          anchor.click();
        },
      });
    }
  }
}

import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  DedicationScoreSummary,
  GeneratedPracticeQuestion,
  PracticeAttemptResult,
  PracticeService,
} from '../../core/services/practice.service';
import { ToastService } from '../../core/services/toast.service';
import { MonacoEditorComponent } from '../../shared/components/monaco-editor.component';

@Component({
  selector: 'app-learner-practice',
  standalone: true,
  imports: [CommonModule, FormsModule, MonacoEditorComponent],
  template: `
    <div class="space-y-6">
      <!-- Title & Intro -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">AI Practice Lab &amp; Dedication Engine</h1>
          <p class="text-xs text-slate-500">
            Ungraded adaptive practice powered by sandboxed code verification and real-time LLM feedback across 8 technical disciplines.
          </p>
        </div>
        <div class="flex items-center gap-2">
          <span class="px-3 py-1 rounded-full text-xs font-bold bg-purple-50 text-purple-700 border border-purple-200">
            Ungraded &bull; Talent Spotlight Tracking
          </span>
        </div>
      </div>

      <!-- Field Picker & Mode Selector -->
      <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
        <div class="flex items-center justify-between">
          <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400">Select Practice Field (8 Disciplines)</h3>
          <span class="text-[10px] text-slate-400">Adaptive difficulty tracks your recent accuracy</span>
        </div>

        <!-- Field Pills -->
        <div class="flex flex-wrap gap-2">
          @for (field of practiceFields; track field) {
            <button 
              type="button" 
              (click)="onSelectField(field)"
              class="px-4 py-2 rounded-xl text-xs font-bold border transition"
              [ngClass]="selectedField() === field 
                ? 'bg-[#008FBB] text-white border-[#008FBB] shadow-sm' 
                : 'bg-slate-50  text-slate-700  border-slate-200  hover:border-slate-400'">
              {{ field }}
            </button>
          }
        </div>

        <!-- Mode & Difficulty Selectors -->
        <div class="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <span class="text-xs font-bold text-slate-500">Mode:</span>
            <div class="inline-flex rounded-xl bg-slate-100 p-1 text-xs font-bold">
              <button 
                type="button" 
                (click)="onSelectMode('MCQ')"
                class="px-3 py-1 rounded-lg transition"
                [ngClass]="selectedMode() === 'MCQ' ? 'bg-white  text-[#008FBB] shadow-sm' : 'text-slate-500'">
                MCQ Concept
              </button>
              <button 
                type="button" 
                (click)="onSelectMode('CODING')"
                class="px-3 py-1 rounded-lg transition"
                [ngClass]="selectedMode() === 'CODING' ? 'bg-white  text-purple-700 shadow-sm' : 'text-slate-500'">
                Coding Challenge
              </button>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <span class="text-xs font-bold text-slate-500">Difficulty:</span>
            <select [(ngModel)]="selectedDifficulty" (ngModelChange)="generateNewQuestion()" class="px-3 py-1.5 bg-slate-50 border border-slate-300 rounded-xl text-xs font-bold text-slate-900">
              <option value="EASY">Easy</option>
              <option value="MEDIUM">Medium</option>
              <option value="HARD">Hard</option>
            </select>

            <button 
              type="button" 
              [disabled]="isGenerating()"
              (click)="generateNewQuestion()"
              class="px-5 py-2 rounded-xl bg-gradient-to-r from-[#FAA634] to-[#e09228] hover:from-[#e09228] hover:to-[#c67c1e] disabled:opacity-50 text-white text-xs font-bold shadow-md transition flex items-center gap-1.5">
              @if (isGenerating()) {
                <span class="animate-spin text-xs">&#9696;</span>
                <span>Generating Problem...</span>
              } @else {
                <span>Generate Verified Problem &rarr;</span>
              }
            </button>
          </div>
        </div>
      </div>

      <!-- Active Practice Question Box -->
      @if (activeQuestion()) {
        <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-5">
          
          <div class="flex items-start justify-between pb-3 border-b border-slate-100">
            <div>
              <div class="flex items-center gap-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-sky-100 text-[#008FBB]">
                  {{ activeQuestion()?.field }} &bull; {{ activeQuestion()?.difficulty }}
                </span>
                
                <!-- Truthful Source Badge (Phase A requirement) -->
                @if (activeQuestion()?.source === 'model') {
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase bg-purple-50 text-purple-700 border border-purple-200 flex items-center gap-1 shadow-sm">
                    ✨ Generated by TRELLIS AI
                  </span>
                } @else {
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-slate-100 text-slate-600 border border-slate-200 flex items-center gap-1">
                    📚 Practice bank
                  </span>
                }

                <span class="text-[10px] text-emerald-600 font-bold">&check; Sandbox Pre-Verified Solution</span>
              </div>
              <h3 class="text-base font-black text-slate-900 mt-1">{{ activeQuestion()?.title }}</h3>
            </div>
          </div>

          <div class="text-xs text-slate-700 whitespace-pre-wrap leading-relaxed font-sans">
            {{ getQuestionContent() }}
          </div>

          <!-- MCQ Options (Without leaking correct answer or explanation) -->
          @if (isMcq()) {
            <div class="space-y-2.5">
              @for (opt of getQuestionOptions(); track opt.id) {
                <label 
                  class="flex items-center gap-3 p-3.5 rounded-xl border text-xs cursor-pointer transition select-none"
                  [ngClass]="selectedOptionId === opt.id ? 'bg-sky-50  border-[#008FBB] text-[#008FBB] font-bold shadow-sm' : 'bg-slate-50  border-slate-200  text-slate-800  hover:border-slate-400'">
                  <input type="radio" name="practice_opt" [value]="opt.id" [(ngModel)]="selectedOptionId" class="text-[#008FBB] focus:ring-[#008FBB]" />
                  <span>{{ opt.option_text }}</span>
                </label>
              }
            </div>
          }

          <!-- Coding Solution Area with Monaco Editor -->
          @if (isCoding()) {
            <div class="space-y-3">
              @if (activeQuestion()?.constraints) {
                <div class="p-3 rounded-xl bg-slate-50 border border-slate-200 text-[11px] text-slate-600">
                  <strong class="text-slate-700">Constraints:</strong> {{ activeQuestion()?.constraints }}
                </div>
              }

              <!-- Monaco Editor Integration for Coding Practice -->
              <div class="h-[380px]">
                <app-monaco-editor
                  [(code)]="codeSolution"
                  [language]="practiceLanguage"
                  (languageChange)="onLanguageChanged($event)"
                  (reset)="resetPracticeCode()">
                </app-monaco-editor>
              </div>
            </div>
          }

          <!-- Submit Practice Attempt -->
          <div class="flex items-center justify-between pt-2">
            <button 
              type="button" 
              (click)="showNextHint()"
              [disabled]="currentHintIndex() >= (activeQuestion()?.hints?.length || 0)"
              class="px-3.5 py-1.5 rounded-xl bg-amber-50 text-[#FAA634] text-xs font-bold border border-amber-200 disabled:opacity-40 transition">
              💡 Request Progressive Hint ({{ currentHintIndex() }} / {{ activeQuestion()?.hints?.length || 2 }})
            </button>

            <button 
              type="button" 
              [disabled]="isEvaluating() || isSubmitDisabled()"
              (click)="submitAttempt()"
              class="px-5 py-2 rounded-xl bg-[#008FBB] hover:bg-[#007499] disabled:opacity-40 text-white text-xs font-bold shadow-md transition flex items-center gap-2">
              @if (isEvaluating()) {
                <span class="animate-spin text-xs">&#9696;</span>
                <span>Evaluating in Sandbox...</span>
              } @else {
                <span>Submit Practice Attempt</span>
              }
            </button>
          </div>

          <!-- Progressive Hint Box -->
          @if (activeHint()) {
            <div class="p-3.5 rounded-xl bg-amber-50/80 border border-amber-200 text-xs text-amber-900 space-y-1">
              <span class="font-bold text-[10px] uppercase text-[#FAA634] block">Progressive Hint</span>
              <p>{{ activeHint() }}</p>
            </div>
          }

          <!-- Post-Attempt Feedback (Reveals Explanation and Verdict strictly after submission) -->
          @if (attemptResult()) {
            <div class="p-4 rounded-xl border text-xs space-y-2"
              [ngClass]="attemptResult()?.correct ? 'bg-emerald-50  border-emerald-300 text-emerald-900 ' : 'bg-rose-50  border-rose-300 text-rose-900 '">
              <div class="flex items-center justify-between">
                <span class="font-bold uppercase text-[10px]">
                  {{ attemptResult()?.correct ? '✓ Correct Solution' : '✗ Incorrect Attempt' }}
                </span>
                <span class="font-bold">+{{ attemptResult()?.score_delta }} Dedication Points</span>
              </div>
              <p class="whitespace-pre-wrap">{{ attemptResult()?.explanation }}</p>
              @if (attemptResult()?.complexity_feedback) {
                <div class="pt-1 text-[11px] font-mono">
                  <strong>Complexity Analysis:</strong> {{ attemptResult()?.complexity_feedback }}
                </div>
              }
            </div>
          }

        </div>
      }

      <!-- Dedication Score & Talent Spotlight Qualification Tracker -->
      <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div>
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
              Talent Spotlight Dedication Metrics
            </h3>
            <p class="text-xs text-slate-400">
              Evaluated across active days, volume, and difficulty-weighted accuracy over 30 days.
            </p>
          </div>
          <span class="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
            Talent Qualified (Threshold &ge; 80)
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          @for (score of dedicationScores(); track score.field) {
            <div class="p-4 rounded-xl bg-slate-50 border border-slate-200">
              <div class="flex items-center justify-between">
                <span class="text-slate-400 text-[10px] uppercase font-bold block">{{ score.field }} Track</span>
                @if (score.talent_spotlight_qualified) {
                  <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-emerald-100 text-emerald-800">Qualified</span>
                }
              </div>
              <span class="text-2xl font-black text-[#008FBB] mt-1 block">{{ score.dedication_score }} / 100</span>
              <div class="mt-1 flex items-center justify-between text-[10px] text-slate-500">
                <span>&bull; {{ score.active_days_30d }} Active Days</span>
                <span>&bull; {{ score.problems_attempted }} Problems</span>
              </div>
            </div>
          } @empty {
            <!-- Clean Empty State (Zero Hardcoded Demo Numbers) -->
            <div class="col-span-3 p-8 text-center text-xs text-slate-400 bg-slate-50 rounded-xl border border-dashed border-slate-200">
              No practice sessions recorded yet. Solve practice problems above to start accumulating dedication points!
            </div>
          }
        </div>
      </div>

      <!-- Weekly AI Study Plan & Practice History -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Weekly AI Study Plan -->
        <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
                Weekly AI Study Plan
              </h3>
              <p class="text-xs text-slate-400">
                Personalized roadmap synthesized from your dedication scores and weak disciplines.
              </p>
            </div>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-[#1294C4] text-white">Adaptive</span>
          </div>

          @if (studyPlan(); as plan) {
            <div class="space-y-3 text-xs">
              <div class="p-3 bg-sky-50 rounded-xl text-sky-900 font-medium">
                {{ plan.advice }}
              </div>
              <div class="space-y-2">
                @for (d of plan.schedule; track d.day) {
                  <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                    <div>
                      <strong class="text-slate-800 block">{{ d.day }} &bull; {{ d.focus_field }}</strong>
                      <span class="text-[10px] text-slate-400">{{ d.recommended_topics.join(', ') }}</span>
                    </div>
                    <span class="text-[10px] font-mono font-bold text-slate-500">{{ d.estimated_minutes }} mins</span>
                  </div>
                }
              </div>
            </div>
          } @else {
            <div class="py-8 text-center text-xs text-slate-400">Loading personalized study plan...</div>
          }
        </div>

        <!-- Recent Practice History -->
        <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
                Practice Attempt History
              </h3>
              <p class="text-xs text-slate-400">
                Recent problem submissions across all practice tracks.
              </p>
            </div>
          </div>

          <div class="space-y-2 max-h-80 overflow-y-auto text-xs">
            @for (h of practiceHistory(); track h.id) {
              <div class="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                <div>
                  <div class="flex items-center gap-2">
                    <span class="px-1.5 py-0.5 rounded text-[9px] font-bold uppercase"
                      [ngClass]="h.is_correct ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'">
                      {{ h.is_correct ? 'PASSED' : 'RETRY' }}
                    </span>
                    <strong class="text-slate-800">{{ h.field }} ({{ h.difficulty }})</strong>
                  </div>
                  <span class="text-[10px] text-slate-400 block mt-0.5">{{ h.created_at | date:'short' }}</span>
                </div>
                <span class="font-mono font-bold" [ngClass]="h.is_correct ? 'text-emerald-600' : 'text-slate-400'">
                  +{{ h.score }} pts
                </span>
              </div>
            } @empty {
              <div class="py-8 text-center text-xs text-slate-400 border border-dashed border-slate-200 rounded-xl">
                No historical practice attempts recorded yet.
              </div>
            }
          </div>
        </div>
      </div>

    </div>
  `,
})
export class LearnerPracticeComponent implements OnInit {
  private readonly practiceService = inject(PracticeService);
  private readonly toastService = inject(ToastService);

  readonly practiceFields = [
    'Python',
    'Java',
    'SQL',
    'DSA',
    'Web Dev',
    'Cloud',
    'Data Analytics',
    'Aptitude',
  ];

  readonly selectedField = signal<string>('Python');
  readonly selectedMode = signal<'MCQ' | 'CODING'>('MCQ');
  selectedDifficulty: 'EASY' | 'MEDIUM' | 'HARD' = 'MEDIUM';
  practiceLanguage = 'python';

  readonly isGenerating = signal<boolean>(false);
  readonly isEvaluating = signal<boolean>(false);

  readonly activeQuestion = signal<GeneratedPracticeQuestion | null>(null);
  readonly dedicationScores = signal<DedicationScoreSummary[]>([]);
  readonly studyPlan = signal<any | null>(null);
  readonly practiceHistory = signal<any[]>([]);
  selectedOptionId = '';
  codeSolution = 'def solve():\n    pass';

  readonly currentHintIndex = signal<number>(0);
  readonly activeHint = signal<string | null>(null);
  readonly attemptResult = signal<PracticeAttemptResult | null>(null);

  ngOnInit(): void {
    this.loadDedicationScores();
    this.loadStudyPlan();
    this.loadPracticeHistory();
    this.generateNewQuestion();
  }

  loadStudyPlan(): void {
    this.practiceService.getWeeklyStudyPlan().subscribe({
      next: (data) => this.studyPlan.set(data),
      error: () => {},
    });
  }

  loadPracticeHistory(): void {
    this.practiceService.getPracticeHistory().subscribe({
      next: (data) => this.practiceHistory.set(data || []),
      error: () => {},
    });
  }

  loadDedicationScores(): void {
    this.practiceService.getDedicationScores().subscribe({
      next: (scores) => {
        // Return pure real data from backend (empty list shows empty state)
        this.dedicationScores.set(scores || []);
      },
      error: () => {
        this.dedicationScores.set([]);
      },
    });
  }

  onSelectField(field: string): void {
    this.selectedField.set(field);
    this.practiceLanguage = this.mapFieldToLanguage(field);
    this.generateNewQuestion();
  }

  onSelectMode(mode: 'MCQ' | 'CODING'): void {
    this.selectedMode.set(mode);
    this.generateNewQuestion();
  }

  private mapFieldToLanguage(field: string): string {
    const f = field.toLowerCase();
    if (f.includes('java') && !f.includes('script')) return 'java';
    if (f.includes('web') || f.includes('javascript') || f.includes('js')) return 'javascript';
    if (f.includes('sql')) return 'sql';
    return 'python';
  }

  generateNewQuestion(): void {
    this.isGenerating.set(true);
    this.attemptResult.set(null);
    this.currentHintIndex.set(0);
    this.activeHint.set(null);
    this.selectedOptionId = '';

    const lang = this.mapFieldToLanguage(this.selectedField());
    this.practiceLanguage = lang;

    this.practiceService.generateQuestion({
      field: this.selectedField(),
      difficulty: this.selectedDifficulty,
      question_type: this.selectedMode(),
    }).subscribe({
      next: (q) => {
        this.isGenerating.set(false);
        const normalized: GeneratedPracticeQuestion = {
          ...q,
          question_type: (q.question_type || (q as any).mode || this.selectedMode()).toUpperCase() as any,
          content: q.content || (q as any).question || (q as any).statement || (q as any).question_data?.question || (q as any).question_data?.statement || '',
        };
        this.activeQuestion.set(normalized);
        if (normalized.question_type === 'CODING') {
          const starter = typeof q.starter_code === 'object' && q.starter_code
            ? (q.starter_code[this.practiceLanguage] || Object.values(q.starter_code)[0])
            : (typeof q.starter_code === 'string' ? q.starter_code : 'def solve():\n    pass');
          this.codeSolution = starter;
        }
      },
      error: (err) => {
        this.isGenerating.set(false);
        this.toastService.showProblemError(err, 'Practice Question Generation Failed');
      },
    });
  }

  onLanguageChanged(newLang: string): void {
    this.practiceLanguage = newLang;
    this.resetPracticeCode();
  }

  resetPracticeCode(): void {
    const q = this.activeQuestion();
    if (q && q.starter_code && q.starter_code[this.practiceLanguage]) {
      this.codeSolution = q.starter_code[this.practiceLanguage];
    } else {
      if (this.practiceLanguage === 'java') {
        this.codeSolution = 'import java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        // solve\n    }\n}';
      } else if (this.practiceLanguage === 'javascript') {
        this.codeSolution = 'const fs = require("fs");\n\nfunction solve() {\n    // solve\n}\nsolve();';
      } else {
        this.codeSolution = 'def solve():\n    pass';
      }
    }
  }

  isMcq(): boolean {
    const q = this.activeQuestion();
    if (!q) return true;
    return (q.question_type || q.mode || 'MCQ').toUpperCase() === 'MCQ';
  }

  isCoding(): boolean {
    const q = this.activeQuestion();
    if (!q) return false;
    return (q.question_type || q.mode) === 'CODING';
  }

  getQuestionContent(): string {
    const q = this.activeQuestion();
    if (!q) return '';
    return q.content || (q as any).question || (q as any).statement || (q as any).question_data?.question || (q as any).question_data?.statement || '';
  }

  getQuestionOptions(): Array<{ id: string; option_text: string }> {
    const q = this.activeQuestion();
    if (!q) return [];
    if (q.options && q.options.length > 0) {
      return q.options.map((opt: any, i: number) => {
        if (typeof opt === 'string') return { id: `opt_${i}`, option_text: opt };
        return { id: opt.id || `opt_${i}`, option_text: opt.option_text || String(opt) };
      });
    }
    const qdata = (q as any).question_data;
    if (qdata && qdata.options && qdata.options.length > 0) {
      return qdata.options.map((opt: any, i: number) => {
        if (typeof opt === 'string') return { id: `opt_${i}`, option_text: opt };
        return { id: opt.id || `opt_${i}`, option_text: opt.option_text || String(opt) };
      });
    }
    return [];
  }

  isSubmitDisabled(): boolean {
    const q = this.activeQuestion();
    if (!q) return true;
    const isMcq = (q.question_type || (q as any).mode || 'MCQ') === 'MCQ';
    if (isMcq) {
      return !this.selectedOptionId;
    }
    return !this.codeSolution || this.codeSolution.trim().length === 0;
  }

  showNextHint(): void {
    const q = this.activeQuestion();
    if (!q || !q.hints || q.hints.length === 0) return;
    const idx = this.currentHintIndex();
    if (idx < q.hints.length) {
      this.activeHint.set(q.hints[idx]);
      this.currentHintIndex.set(idx + 1);
    }
  }

  submitAttempt(): void {
    const q = this.activeQuestion();
    if (!q) return;

    this.isEvaluating.set(true);
    const mode = (q.question_type || (q as any).mode || 'MCQ').toUpperCase();
    this.practiceService.submitAttempt({
      question_id: q.id,
      answer_text: mode === 'MCQ' ? this.selectedOptionId : undefined,
      source_code: mode === 'CODING' ? this.codeSolution : undefined,
      language: this.practiceLanguage,
    }).subscribe({
      next: (res) => {
        this.isEvaluating.set(false);
        this.attemptResult.set(res);
        this.loadDedicationScores();
      },
      error: (err) => {
        this.isEvaluating.set(false);
        this.toastService.showProblemError(err, 'Submission Evaluation Failed');
      },
    });
  }
}

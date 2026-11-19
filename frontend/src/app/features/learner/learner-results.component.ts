import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
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
            Review detailed question-by-question scoring, mentor explanations, and batch average benchmark comparisons.
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
                  <span class="text-xs font-mono text-slate-400">{{ r.submitted_at | date:'mediumDate' }}</span>
                </div>
                <h3 class="text-lg font-black text-slate-900 dark:text-white mt-1">{{ r.assessment_title }}</h3>
                <p class="text-xs text-slate-400">{{ r.field }} &bull; Passing Score: {{ r.passing_score }}%</p>
              </div>

              <!-- Score Banner -->
              <div class="text-right sm:text-right flex items-baseline sm:flex-col gap-2 sm:gap-0">
                <span class="text-3xl font-black text-[#008FBB]">{{ r.score }}%</span>
                <span class="text-xs text-slate-400">Batch Avg: <strong class="text-slate-600 dark:text-slate-300">{{ r.batch_avg }}%</strong></span>
              </div>
            </div>

            <!-- Comparison Bar against Batch Average -->
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-slate-700 dark:text-slate-200">Cohort Benchmark Comparison</span>
                <span class="text-emerald-500 font-bold">+{{ r.score - r.batch_avg }}% Above Average</span>
              </div>
              <div class="w-full bg-slate-200 dark:bg-slate-700 h-2.5 rounded-full overflow-hidden flex">
                <div class="bg-[#008FBB] h-full" [style.width.%]="r.score"></div>
              </div>
            </div>

            <!-- Question Review Breakdown -->
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
                    <p class="text-[11px] text-slate-500 dark:text-slate-400">{{ item.explanation }}</p>
                  </div>
                }
              </div>
            </div>

          </div>
        }
      </div>
    </div>
  `,
})
export class LearnerResultsComponent {
  private readonly learnerService = inject(LearnerService);

  readonly results = signal<any[]>([
    {
      id: 'res1',
      assessment_title: 'Full-Stack Foundation Assessment',
      field: 'Python & Web Architecture',
      score: 94,
      batch_avg: 81,
      passing_score: 75,
      passed: true,
      submitted_at: '2026-11-16T10:30:00Z',
      questions: [
        {
          id: 'q1',
          title: 'Q1: FastAPI Concurrency Paradigms',
          correct: true,
          earned_marks: 10,
          max_marks: 10,
          explanation: 'Correct! Uvicorn running with Gunicorn worker processes handles asynchronous event loops via uvloop.',
        },
        {
          id: 'q2',
          title: 'Q2: Two Sum Algorithmic Lookup (Coding)',
          correct: true,
          earned_marks: 20,
          max_marks: 20,
          explanation: 'Optimal O(n) hash table solution accepted across all hidden test cases. Runtime: 34ms (94th percentile).',
        },
      ],
    },
  ]);

  ngOnInit(): void {
    this.learnerService.getResults().subscribe({
      next: (data) => {
        if (data && data.length > 0) {
          this.results.set(data);
        }
      },
      error: () => {},
    });
  }
}

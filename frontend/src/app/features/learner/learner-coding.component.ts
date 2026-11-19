import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CodingProblemDetail, CodingProblemSummary, CodingService, RunCodeResult, SubmitCodeResult } from '../../core/services/coding.service';

@Component({
  selector: 'app-learner-coding',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-4">
      
      <!-- Top Bar: Problem Selection & Controls -->
      <div class="p-3.5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Problem:</span>
          <select 
            [(ngModel)]="selectedProblemId" 
            (ngModelChange)="onProblemChange()"
            class="px-3 py-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-900 dark:text-white">
            @for (p of problems(); track p.id) {
              <option [value]="p.id">{{ p.title }} ({{ p.difficulty }})</option>
            }
          </select>

          @if (currentProblem()) {
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase"
              [ngClass]="{
                'bg-emerald-100 text-emerald-800': currentProblem()?.difficulty === 'EASY',
                'bg-amber-100 text-[#FAA634]': currentProblem()?.difficulty === 'MEDIUM',
                'bg-rose-100 text-[#D7182A]': currentProblem()?.difficulty === 'HARD'
              }">
              {{ currentProblem()?.difficulty }}
            </span>
          }
        </div>

        <!-- Language, Theme & Reset -->
        <div class="flex items-center gap-2">
          <select 
            [(ngModel)]="selectedLanguage" 
            (ngModelChange)="onLanguageChange()"
            class="px-3 py-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-mono font-bold text-slate-900 dark:text-white uppercase">
            <option value="python">Python 3</option>
            <option value="javascript">JavaScript (Node)</option>
            <option value="java">Java 21</option>
            <option value="cpp">C++ 20</option>
            <option value="c">C 17</option>
          </select>

          <button 
            type="button" 
            (click)="resetCode()"
            title="Reset to Starter Code"
            class="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-xs font-bold text-slate-600 dark:text-slate-300 transition">
            Reset
          </button>
        </div>
      </div>

      <!-- Main Layout: Left Problem Statement & Right Code Editor / Console -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
        
        <!-- Left: Problem Statement & Constraints (5 cols) -->
        <div class="lg:col-span-5 p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4 max-h-[750px] overflow-y-auto text-xs">
          <div>
            <h2 class="text-lg font-black text-slate-900 dark:text-white">{{ currentProblem()?.title }}</h2>
            <div class="flex items-center gap-1.5 mt-1">
              @for (tag of currentProblem()?.tags ?? ['Array', 'Hash Table']; track tag) {
                <span class="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-500 text-[10px] font-semibold">
                  {{ tag }}
                </span>
              }
            </div>
          </div>

          <!-- Description -->
          <div class="space-y-2 text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
            {{ currentProblem()?.statement }}
          </div>

          <!-- Examples -->
          <div class="space-y-3 pt-2">
            <h4 class="font-bold uppercase tracking-wider text-slate-400 text-[10px]">Sample Test Cases</h4>
            @for (ex of currentProblem()?.examples ?? defaultExamples; track ex.input) {
              <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 font-mono text-[11px] space-y-1">
                <div><span class="text-slate-400">Input:</span> <span class="font-bold text-slate-800 dark:text-slate-200">{{ ex.input }}</span></div>
                <div><span class="text-slate-400">Output:</span> <span class="font-bold text-emerald-600">{{ ex.output }}</span></div>
                @if (ex.explanation) {
                  <p class="text-[10px] text-slate-400 font-sans mt-1">{{ ex.explanation }}</p>
                }
              </div>
            }
          </div>

          <!-- Constraints -->
          <div class="pt-2 border-t border-slate-100 dark:border-slate-800">
            <h4 class="font-bold uppercase tracking-wider text-slate-400 text-[10px] mb-1">Constraints &amp; Limits</h4>
            <p class="font-mono text-[11px] text-slate-600 dark:text-slate-400">{{ currentProblem()?.constraints || '2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9' }}</p>
            <div class="mt-2 text-[10px] text-slate-400 flex items-center gap-3">
              <span>Time Limit: {{ currentProblem()?.time_limit_ms || 2000 }}ms</span>
              <span>Memory Limit: {{ currentProblem()?.memory_limit_mb || 256 }}MB</span>
            </div>
          </div>

          <!-- Submissions History Tab -->
          <div class="pt-3 border-t border-slate-100 dark:border-slate-800">
            <button (click)="loadSubmissions()" class="text-xs font-bold text-[#008FBB] hover:underline">
              View My Submission History &rarr;
            </button>
          </div>
        </div>

        <!-- Right: Code Editor & Console Output (7 cols) -->
        <div class="lg:col-span-7 flex flex-col gap-4">
          
          <!-- Code Editor Box -->
          <div class="rounded-2xl bg-slate-950 border border-slate-800 overflow-hidden shadow-xl flex flex-col">
            <div class="px-4 py-2 bg-slate-900 border-b border-slate-800 flex items-center justify-between text-xs text-slate-400 font-mono">
              <span class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                <span class="ml-2 font-bold text-slate-200">solution.{{ extension() }}</span>
              </span>
              <span>Subprocess Sandbox &bull; Isolated Execution</span>
            </div>

            <!-- Code Textarea (Clean, High-Performance Monospace Editor) -->
            <textarea 
              [(ngModel)]="codeSource" 
              rows="16" 
              spellcheck="false"
              class="w-full font-mono text-xs sm:text-sm p-4 bg-slate-950 text-slate-100 placeholder-slate-600 focus:outline-none resize-y leading-relaxed"
              placeholder="# Enter your solution here..."></textarea>

            <!-- Execution Action Bar -->
            <div class="p-3 bg-slate-900/90 border-t border-slate-800 flex items-center justify-between">
              <span class="text-[10px] text-slate-400 font-mono">Run: Sample Cases &bull; Submit: All Hidden Cases</span>
              <div class="flex items-center gap-2">
                <button 
                  type="button" 
                  [disabled]="isRunning() || isSubmitting()"
                  (click)="runSample()"
                  class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 disabled:opacity-50 text-slate-200 text-xs font-bold transition flex items-center gap-1.5">
                  @if (isRunning()) {
                    <span class="animate-spin text-xs">&#9696;</span>
                    <span>Running...</span>
                  } @else {
                    <span>&blacktriangleright; Run Code</span>
                  }
                </button>

                <button 
                  type="button" 
                  [disabled]="isRunning() || isSubmitting()"
                  (click)="submitSolution()"
                  class="px-5 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 disabled:opacity-50 text-white text-xs font-bold shadow-md transition flex items-center gap-1.5">
                  @if (isSubmitting()) {
                    <span class="animate-spin text-xs">&#9696;</span>
                    <span>Evaluating...</span>
                  } @else {
                    <span>Submit &rarr;</span>
                  }
                </button>
              </div>
            </div>
          </div>

          <!-- Bottom: Console / Results Area -->
          <div class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
            <div class="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Execution Verdict &amp; Output</span>
                @if (submitResult()) {
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase"
                    [ngClass]="submitResult()?.verdict === 'ACCEPTED' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'">
                    {{ submitResult()?.verdict }}
                  </span>
                }
              </div>

              @if (submitResult()) {
                <div class="text-[11px] font-mono text-slate-500 flex items-center gap-3">
                  <span>Runtime: <strong>{{ submitResult()?.runtime_ms }}ms</strong></span>
                  <span>Memory: <strong>{{ submitResult()?.memory_mb }}MB</strong></span>
                  <span class="text-emerald-600 font-bold">Beats {{ submitResult()?.runtime_percentile }}%</span>
                </div>
              }
            </div>

            <!-- Custom Input Box for "Run" -->
            <div class="space-y-1 text-xs">
              <label class="block font-bold text-slate-500 text-[10px] uppercase">Custom Input Box (Sample Run)</label>
              <input 
                type="text" 
                [(ngModel)]="customInput" 
                placeholder="[2, 7, 11, 15], 9"
                class="w-full px-3 py-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 font-mono text-xs rounded-xl" />
            </div>

            <!-- Console Log or First Failing Case -->
            @if (runResult()) {
              <div class="p-3 rounded-xl bg-slate-950 font-mono text-xs text-slate-200 space-y-1">
                <div class="text-[10px] text-slate-400 font-bold uppercase">Standard Output:</div>
                <pre class="text-emerald-400 whitespace-pre-wrap">{{ runResult()?.stdout || '(No output)' }}</pre>
                @if (runResult()?.stderr) {
                  <pre class="text-rose-400 whitespace-pre-wrap">{{ runResult()?.stderr }}</pre>
                }
              </div>
            }

            <!-- First Failing Case Inspection (LeetCode-style) -->
            @if (submitResult()?.failing_case) {
              <div class="p-3 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/60 font-mono text-xs space-y-1">
                <span class="font-bold text-[#D7182A] uppercase text-[10px] block">First Failing Test Case</span>
                <div><span class="text-slate-400">Input:</span> {{ submitResult()?.failing_case?.input }}</div>
                <div><span class="text-slate-400">Expected:</span> <span class="text-emerald-600 font-bold">{{ submitResult()?.failing_case?.expected }}</span></div>
                <div><span class="text-slate-400">Actual:</span> <span class="text-rose-600 font-bold">{{ submitResult()?.failing_case?.actual }}</span></div>
              </div>
            }

          </div>

        </div>

      </div>

    </div>
  `,
})
export class LearnerCodingComponent {
  private readonly codingService = inject(CodingService);

  readonly problems = signal<CodingProblemSummary[]>([]);
  readonly currentProblem = signal<CodingProblemDetail | null>(null);
  selectedProblemId = '';
  selectedLanguage = 'python';

  codeSource = '';
  customInput = '[2, 7, 11, 15], 9';

  readonly isRunning = signal<boolean>(false);
  readonly isSubmitting = signal<boolean>(false);
  readonly runResult = signal<RunCodeResult | null>(null);
  readonly submitResult = signal<SubmitCodeResult | null>(null);

  readonly defaultExamples = [
    { input: 'nums = [2,7,11,15], target = 9', output: '[0, 1]', explanation: 'Because nums[0] + nums[1] == 9, we return [0, 1].' },
    { input: 'nums = [3,2,4], target = 6', output: '[1, 2]' },
  ];

  ngOnInit(): void {
    this.codingService.getProblems().subscribe({
      next: (list) => {
        this.problems.set(list || []);
        if (list && list.length > 0) {
          this.selectedProblemId = list[0].id;
          this.onProblemChange();
        } else {
          this.initFallbackProblem();
        }
      },
      error: () => this.initFallbackProblem(),
    });
  }

  private initFallbackProblem(): void {
    const fallback: CodingProblemDetail = {
      id: 'p1',
      title: 'Two Sum',
      slug: 'two-sum',
      difficulty: 'EASY',
      category: 'Array',
      tags: ['Array', 'Hash Table'],
      statement: 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.',
      constraints: '2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\nOnly one valid answer exists.',
      examples: this.defaultExamples,
      starter_code: {
        python: 'def two_sum(nums, target):\n    # Write your solution here\n    seen = {}\n    for i, num in enumerate(nums):\n        comp = target - num\n        if comp in seen:\n            return [seen[comp], i]\n        seen[num] = i\n    return []',
        javascript: 'function twoSum(nums, target) {\n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const comp = target - nums[i];\n        if (map.has(comp)) return [map.get(comp), i];\n        map.set(nums[i], i);\n    }\n    return [];\n}',
        java: 'class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // implementation\n        return new int[]{};\n    }\n}',
        cpp: '#include <vector>\nusing namespace std;\n\nvector<int> twoSum(vector<int>& nums, int target) {\n    return {};\n}',
        c: 'int* twoSum(int* nums, int numsSize, int target, int* returnSize) {\n    return 0;\n}',
      },
      time_limit_ms: 2000,
      memory_limit_mb: 256,
    };
    this.problems.set([fallback]);
    this.currentProblem.set(fallback);
    this.selectedProblemId = fallback.id;
    this.resetCode();
  }

  onProblemChange(): void {
    if (!this.selectedProblemId) return;
    this.codingService.getProblem(this.selectedProblemId).subscribe({
      next: (detail) => {
        this.currentProblem.set(detail);
        this.resetCode();
      },
      error: () => {},
    });
  }

  onLanguageChange(): void {
    this.resetCode();
  }

  resetCode(): void {
    const p = this.currentProblem();
    if (p && p.starter_code) {
      this.codeSource = p.starter_code[this.selectedLanguage] || '# Write code here';
    }
    this.runResult.set(null);
    this.submitResult.set(null);
  }

  extension(): string {
    const map: Record<string, string> = {
      python: 'py',
      javascript: 'js',
      java: 'java',
      cpp: 'cpp',
      c: 'c',
    };
    return map[this.selectedLanguage] || 'txt';
  }

  runSample(): void {
    this.isRunning.set(true);
    this.runResult.set(null);
    this.codingService.runCode({
      source_code: this.codeSource,
      language: this.selectedLanguage,
      custom_input: this.customInput,
    }).subscribe({
      next: (res) => {
        this.isRunning.set(false);
        this.runResult.set(res);
      },
      error: (err) => {
        this.isRunning.set(false);
        this.runResult.set({
          status: 'ERROR',
          stdout: '',
          stderr: err.error?.detail || err.message || 'Execution error in sandbox.',
          execution_time_ms: 0,
        });
      },
    });
  }

  submitSolution(): void {
    this.isSubmitting.set(true);
    this.submitResult.set(null);
    this.codingService.submitCode({
      problem_id: this.selectedProblemId || 'p1',
      source_code: this.codeSource,
      language: this.selectedLanguage,
    }).subscribe({
      next: (res) => {
        this.isSubmitting.set(false);
        this.submitResult.set(res);
      },
      error: (err) => {
        this.isSubmitting.set(false);
        this.submitResult.set({
          id: 'sub_err',
          verdict: 'COMPILATION_ERROR',
          passed_cases: 0,
          total_cases: 5,
          score: 0,
          max_score: 100,
          runtime_ms: 0,
          memory_mb: 0,
          runtime_percentile: 0,
          failing_case: {
            input: 'Hidden Test Case 1',
            expected: 'Expected output',
            actual: err.error?.detail || 'Syntax / compilation error in sandbox.',
          },
          created_at: new Date().toISOString(),
        });
      },
    });
  }

  loadSubmissions(): void {
    this.codingService.getSubmissions(this.selectedProblemId).subscribe({
      next: (list) => {
        alert(`You have ${list.length} previous submission(s) for this problem.`);
      },
    });
  }
}

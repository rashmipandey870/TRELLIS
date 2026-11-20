import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  CodingProblemDetail,
  CodingProblemSummary,
  CodingService,
  RunCodeResult,
  SubmitCodeResult,
} from '../../core/services/coding.service';
import { MonacoEditorComponent } from '../../shared/components/monaco-editor.component';

@Component({
  selector: 'app-learner-coding',
  standalone: true,
  imports: [CommonModule, FormsModule, MonacoEditorComponent],
  template: `
    <div class="space-y-4">
      
      <!-- Top Bar: Problem Selection & Controls -->
      <div class="p-3.5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Problem:</span>
          @if (problems().length > 0) {
            <select 
              [(ngModel)]="selectedProblemId" 
              (ngModelChange)="onProblemChange()"
              class="px-3 py-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-900 dark:text-white">
              @for (p of problems(); track p.id) {
                <option [value]="p.id">{{ p.title }} ({{ p.difficulty }})</option>
              }
            </select>
          }

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

        <div class="flex items-center gap-2">
          <!-- Active Tab Selector (Editor vs History) -->
          <div class="inline-flex rounded-xl bg-slate-100 dark:bg-slate-800 p-1 text-xs font-bold">
            <button 
              type="button" 
              (click)="activeTab = 'editor'"
              class="px-3 py-1 rounded-lg transition"
              [ngClass]="activeTab === 'editor' ? 'bg-white dark:bg-slate-900 text-[#008FBB] shadow-sm' : 'text-slate-500'">
              Editor &amp; Output
            </button>
            <button 
              type="button" 
              (click)="openSubmissionHistory()"
              class="px-3 py-1 rounded-lg transition"
              [ngClass]="activeTab === 'history' ? 'bg-white dark:bg-slate-900 text-[#008FBB] shadow-sm' : 'text-slate-500'">
              Submissions ({{ submissionHistory().length }})
            </button>
          </div>
        </div>
      </div>

      <!-- Main Layout -->
      @if (problems().length === 0 && !currentProblem()) {
        <!-- Proper Empty State -->
        <div class="p-12 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-center space-y-3">
          <div class="w-12 h-12 mx-auto rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-xl text-slate-400">
            💻
          </div>
          <h3 class="text-base font-bold text-slate-800 dark:text-slate-200">No Coding Problems Available</h3>
          <p class="text-xs text-slate-500 max-w-md mx-auto">
            You do not currently have any active coding assessment or assigned problems. Check your assessments or practice lab!
          </p>
        </div>
      } @else {
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
          
          <!-- Left: Problem Statement & Constraints (5 cols) -->
          <div class="lg:col-span-5 p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4 max-h-[750px] overflow-y-auto text-xs">
            <div>
              <h2 class="text-lg font-black text-slate-900 dark:text-white">{{ currentProblem()?.title }}</h2>
              <div class="flex items-center gap-1.5 mt-1">
                @for (tag of currentProblem()?.tags ?? ['Algorithm', 'Data Structures']; track tag) {
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
              <p class="font-mono text-[11px] text-slate-600 dark:text-slate-400">{{ currentProblem()?.constraints || 'Standard execution limits apply.' }}</p>
              <div class="mt-2 text-[10px] text-slate-400 flex items-center gap-3">
                <span>Time Limit: {{ currentProblem()?.time_limit_ms || 3000 }}ms</span>
                <span>Memory Limit: {{ currentProblem()?.memory_limit_mb || 256 }}MB</span>
              </div>
            </div>
          </div>

          <!-- Right: Code Editor & Console Output OR Submission History (7 cols) -->
          <div class="lg:col-span-7 flex flex-col gap-4">
            
            @if (activeTab === 'editor') {
              <!-- Monaco Editor Integration -->
              <div class="h-[420px]">
                <app-monaco-editor
                  [(code)]="codeSource"
                  [language]="selectedLanguage"
                  (languageChange)="onLanguageChanged($event)"
                  (reset)="resetCode()">
                </app-monaco-editor>
              </div>

              <!-- Action Bar -->
              <div class="p-3.5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex items-center justify-between">
                <span class="text-[10px] text-slate-400 font-mono">Run: Custom / Sample Input &bull; Submit: All Hidden Cases</span>
                <div class="flex items-center gap-2">
                  <button 
                    type="button" 
                    [disabled]="isRunning() || isSubmitting()"
                    (click)="runSample()"
                    class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 disabled:opacity-50 text-slate-800 dark:text-slate-200 text-xs font-bold transition flex items-center gap-1.5">
                    @if (isRunning()) {
                      <span class="animate-spin text-xs">&#9696;</span>
                      <span>Executing...</span>
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
                      <span>Evaluating in Sandbox...</span>
                    } @else {
                      <span>Submit Solution &rarr;</span>
                    }
                  </button>
                </div>
              </div>

              <!-- Console / Results Area -->
              <div class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
                <div class="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Execution Output</span>
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
                      @if (submitResult()?.runtime_percentile !== null && submitResult()?.runtime_percentile !== undefined) {
                        <span class="text-emerald-600 font-bold">Beats {{ submitResult()?.runtime_percentile }}%</span>
                      }
                    </div>
                  }
                </div>

                <!-- Custom Input Box for "Run" -->
                <div class="space-y-1 text-xs">
                  <label class="block font-bold text-slate-500 text-[10px] uppercase">Custom Input (Standard Input)</label>
                  <input 
                    type="text" 
                    [(ngModel)]="customInput" 
                    placeholder="Enter standard input for your run..."
                    class="w-full px-3 py-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 font-mono text-xs rounded-xl" />
                </div>

                <!-- Run Standard Output -->
                @if (runResult()) {
                  <div class="p-3 rounded-xl bg-slate-950 font-mono text-xs text-slate-200 space-y-1">
                    <div class="text-[10px] text-slate-400 font-bold uppercase">Standard Output:</div>
                    <pre class="text-emerald-400 whitespace-pre-wrap">{{ runResult()?.stdout || '(No output)' }}</pre>
                    @if (runResult()?.stderr) {
                      <div class="text-[10px] text-rose-400 font-bold uppercase pt-1">Standard Error:</div>
                      <pre class="text-rose-400 whitespace-pre-wrap">{{ runResult()?.stderr }}</pre>
                    }
                  </div>
                }

                <!-- First Failing Case Inspection -->
                @if (submitResult()?.failing_case) {
                  <div class="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/60 font-mono text-xs space-y-1">
                    <span class="font-bold text-[#D7182A] uppercase text-[10px] block">First Failing Test Case</span>
                    <div><span class="text-slate-400">Input:</span> {{ submitResult()?.failing_case?.input }}</div>
                    <div><span class="text-slate-400">Expected:</span> <span class="text-emerald-600 font-bold">{{ submitResult()?.failing_case?.expected }}</span></div>
                    <div><span class="text-slate-400">Actual Output:</span> <span class="text-rose-600 font-bold">{{ submitResult()?.failing_case?.actual }}</span></div>
                  </div>
                }
              </div>
            } @else {
              <!-- Submissions History Tab -->
              <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
                <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
                  <h3 class="text-xs font-bold uppercase tracking-wider text-slate-500">My Submission History</h3>
                  <button (click)="activeTab = 'editor'" class="text-xs font-bold text-[#008FBB] hover:underline">
                    &larr; Back to Editor
                  </button>
                </div>

                @if (submissionHistory().length === 0) {
                  <div class="p-8 text-center text-xs text-slate-400">
                    No submissions recorded yet for this problem. Click "Submit Solution" to run all verification cases!
                  </div>
                } @else {
                  <div class="space-y-2">
                    @for (sub of submissionHistory(); track sub.id) {
                      <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 flex items-center justify-between text-xs font-mono">
                        <div class="flex items-center gap-3">
                          <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase"
                            [ngClass]="sub.verdict === 'ACCEPTED' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'">
                            {{ sub.verdict }}
                          </span>
                          <span class="text-slate-600 dark:text-slate-300">
                            Passed: <strong>{{ sub.passed_cases }}/{{ sub.total_cases }}</strong> (Score: {{ sub.score }})
                          </span>
                        </div>
                        <div class="text-[11px] text-slate-400 flex items-center gap-3">
                          <span>{{ sub.runtime_ms }}ms</span>
                          <span>{{ sub.memory_mb }}MB</span>
                          <span>{{ sub.created_at | date:'short' }}</span>
                        </div>
                      </div>
                    }
                  </div>
                }
              </div>
            }

          </div>

        </div>
      }

    </div>
  `,
})
export class LearnerCodingComponent implements OnInit {
  private readonly codingService = inject(CodingService);

  readonly problems = signal<CodingProblemSummary[]>([]);
  readonly currentProblem = signal<CodingProblemDetail | null>(null);
  readonly submissionHistory = signal<SubmitCodeResult[]>([]);

  selectedProblemId = '';
  selectedLanguage = 'python';
  activeTab: 'editor' | 'history' = 'editor';

  codeSource = '';
  customInput = 'racecar';

  readonly isRunning = signal<boolean>(false);
  readonly isSubmitting = signal<boolean>(false);
  readonly runResult = signal<RunCodeResult | null>(null);
  readonly submitResult = signal<SubmitCodeResult | null>(null);

  readonly defaultExamples = [
    { input: 'racecar', output: 'true', explanation: 'Reads identically forwards and backwards.' },
    { input: 'hello', output: 'false' },
  ];

  // Starter code templates per language
  readonly starterCodeTemplates: Record<string, string> = {
    python: 'import sys\n\ndef solve():\n    raw = sys.stdin.read().strip()\n    # Implement solution here\n    print(raw)\n\nif __name__ == "__main__":\n    solve()',
    javascript: 'const fs = require("fs");\n\nfunction solve() {\n    const input = fs.readFileSync(0, "utf-8").trim();\n    // Implement solution here\n    console.log(input);\n}\n\nsolve();',
    java: 'import java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextLine()) return;\n        String line = sc.nextLine();\n        // Implement solution here\n        System.out.println(line);\n    }\n}',
    cpp: '#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string s;\n    if (getline(cin, s)) {\n        // Implement solution here\n        cout << s << endl;\n    }\n    return 0;\n}',
    c: '#include <stdio.h>\n\nint main() {\n    char buffer[1024];\n    if (fgets(buffer, sizeof(buffer), stdin)) {\n        // Implement solution here\n        printf("%s", buffer);\n    }\n    return 0;\n}',
    sql: '-- Write your SQL query here\nSELECT * FROM employees;',
  };

  ngOnInit(): void {
    this.codingService.getProblems().subscribe({
      next: (list) => {
        this.problems.set(list || []);
        if (list && list.length > 0) {
          this.selectedProblemId = list[0].id;
          this.onProblemChange();
        }
      },
      error: () => {
        this.problems.set([]);
      },
    });
  }

  onProblemChange(): void {
    if (!this.selectedProblemId) return;
    this.codingService.getProblem(this.selectedProblemId).subscribe({
      next: (detail) => {
        this.currentProblem.set(detail);
        this.resetCode();
        this.loadSubmissions();
      },
      error: () => {},
    });
  }

  onLanguageChanged(newLang: string): void {
    this.selectedLanguage = newLang;
    this.resetCode();
  }

  resetCode(): void {
    const p = this.currentProblem();
    if (p && p.starter_code && p.starter_code[this.selectedLanguage]) {
      this.codeSource = p.starter_code[this.selectedLanguage];
    } else {
      this.codeSource = this.starterCodeTemplates[this.selectedLanguage] || '# Write code here';
    }
    this.runResult.set(null);
    this.submitResult.set(null);
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
      problem_id: this.selectedProblemId,
      source_code: this.codeSource,
      language: this.selectedLanguage,
    }).subscribe({
      next: (res) => {
        this.isSubmitting.set(false);
        this.submitResult.set(res);
        this.loadSubmissions();
      },
      error: (err) => {
        this.isSubmitting.set(false);
        this.submitResult.set({
          id: 'sub_err',
          verdict: 'COMPILATION_ERROR',
          passed_cases: 0,
          total_cases: 1,
          score: 0,
          max_score: 100,
          runtime_ms: 0,
          memory_mb: 0,
          runtime_percentile: 0,
          failing_case: {
            input: 'Verification Test Case',
            expected: 'Successful compilation',
            actual: err.error?.detail || 'Syntax / compilation error in sandbox.',
          },
          created_at: new Date().toISOString(),
        });
      },
    });
  }

  openSubmissionHistory(): void {
    this.activeTab = 'history';
    this.loadSubmissions();
  }

  loadSubmissions(): void {
    if (!this.selectedProblemId) return;
    this.codingService.getSubmissions(this.selectedProblemId).subscribe({
      next: (list) => {
        this.submissionHistory.set(list || []);
      },
      error: () => {
        this.submissionHistory.set([]);
      },
    });
  }
}

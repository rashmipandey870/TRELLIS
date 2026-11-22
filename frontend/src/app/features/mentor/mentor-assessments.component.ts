import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { AssessmentItem, MentorService, QuestionBankItem } from '../../core/services/mentor.service';

interface QuestionOption {
  option_id: string;
  option_text: string;
  is_correct: boolean;
}

interface TestCase {
  input_data: string;
  expected_output: string;
  is_hidden: boolean;
  explanation?: string;
}

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
            (click)="openQuestionBank()"
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

      <!-- Toast Feedback -->
      @if (actionToast()) {
        <div class="p-3 rounded-xl text-xs font-bold transition flex items-center justify-between"
          [ngClass]="actionToast()!.type === 'error' ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-emerald-50 text-emerald-800 border border-emerald-200'">
          <span>{{ actionToast()!.message }}</span>
          <button type="button" (click)="actionToast.set(null)" class="text-sm font-bold ml-2">&times;</button>
        </div>
      }

      <!-- Assessments List Grid -->
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

            <!-- Stats (Zero Fallbacks - Real Data Only) -->
            <div class="grid grid-cols-3 gap-2 py-3 border-y border-slate-100 dark:border-slate-800 text-xs text-center">
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Duration</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">{{ a.duration_minutes }} mins</span>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Questions</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">{{ a.questions_count }} items</span>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Submissions</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">{{ a.submissions_count }} taken</span>
              </div>
            </div>

            <div class="flex items-center justify-between text-[11px] text-slate-500">
              <span>Audience: <strong>{{ a.batch_name || 'Assigned Learners' }}</strong></span>
              <span>Total Marks: <strong>{{ a.total_marks || 0 }}</strong></span>
            </div>

            @if (a.is_published && a.submissions_count > 0) {
              <p class="text-[10px] text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 p-2 rounded-lg">
                &bull; Submissions exist: In-place edit locked. Adding or modifying questions will produce Version {{ (a.version || 1) + 1 }}.
              </p>
            }

            <!-- Actions -->
            <div class="flex items-center gap-2 pt-1">
              <button 
                type="button" 
                (click)="openEditAssessment(a)"
                class="flex-1 py-2 px-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-bold transition text-center">
                {{ a.is_published ? 'View / New Version' : 'Edit &amp; Add Questions' }}
              </button>
              @if (!a.is_published) {
                <button 
                  type="button" 
                  (click)="publishAssessment(a)"
                  class="flex-1 py-2 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold transition text-center">
                  Publish
                </button>
              }
              <button 
                type="button" 
                (click)="openResultsAnalysis(a)"
                class="flex-1 py-2 px-3 rounded-xl bg-sky-50 dark:bg-sky-950/60 hover:bg-sky-100 text-[#008FBB] border border-sky-200 dark:border-sky-800 text-xs font-bold transition text-center">
                Results &rarr;
              </button>
            </div>
          </div>
        } @empty {
          <div class="col-span-2 p-12 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 text-slate-400 text-xs space-y-2">
            <p class="font-bold text-slate-600 dark:text-slate-300">No assessments created yet.</p>
            <p>Click "+ New Assessment" to author your first MCQ or coding challenge assessment.</p>
          </div>
        }
      </div>

      <!-- Assessment Authoring Studio Modal -->
      @if (showStudioModal()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-4xl w-full p-6 space-y-5 max-h-[92vh] overflow-y-auto">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <div>
                <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">
                  {{ activeStudioAssessment() ? 'Assessment Authoring Studio (' + activeStudioAssessment()?.title + ')' : 'New Assessment Setup' }}
                </h3>
                <p class="text-xs text-slate-500">Configure parameters, audience, and author MCQ and coding challenges.</p>
              </div>
              <button (click)="closeStudioModal()" class="text-slate-400 hover:text-slate-600 text-xl font-bold">&times;</button>
            </div>

            <!-- Tab Switcher: Details vs Staged Questions vs Question Authoring vs Preview -->
            <div class="flex border-b border-slate-200 dark:border-slate-800 gap-2">
              <button 
                type="button"
                (click)="studioTab.set('details')"
                [ngClass]="studioTab() === 'details' ? 'border-[#FAA634] text-[#FAA634]' : 'border-transparent text-slate-500 hover:text-slate-700'"
                class="pb-2 px-3 text-xs font-bold border-b-2 transition">
                1. Assessment Details &amp; Audience
              </button>
              @if (activeStudioAssessment()) {
                <button 
                  type="button"
                  (click)="studioTab.set('questions')"
                  [ngClass]="studioTab() === 'questions' ? 'border-[#FAA634] text-[#FAA634]' : 'border-transparent text-slate-500 hover:text-slate-700'"
                  class="pb-2 px-3 text-xs font-bold border-b-2 transition flex items-center gap-1.5">
                  <span>2. Attached Questions</span>
                  <span class="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-100 dark:bg-slate-800 font-mono">{{ stagedQuestions().length }}</span>
                </button>
                <button 
                  type="button"
                  (click)="studioTab.set('add_mcq')"
                  [ngClass]="studioTab() === 'add_mcq' ? 'border-[#008FBB] text-[#008FBB]' : 'border-transparent text-slate-500 hover:text-slate-700'"
                  class="pb-2 px-3 text-xs font-bold border-b-2 transition">
                  + Add MCQ
                </button>
                <button 
                  type="button"
                  (click)="studioTab.set('add_coding')"
                  [ngClass]="studioTab() === 'add_coding' ? 'border-purple-600 text-purple-600' : 'border-transparent text-slate-500 hover:text-slate-700'"
                  class="pb-2 px-3 text-xs font-bold border-b-2 transition">
                  + Add Coding
                </button>
                <button 
                  type="button"
                  (click)="studioTab.set('add_sql')"
                  [ngClass]="studioTab() === 'add_sql' ? 'border-sky-600 text-sky-600' : 'border-transparent text-slate-500 hover:text-slate-700'"
                  class="pb-2 px-3 text-xs font-bold border-b-2 transition">
                  + Add SQL
                </button>
                <button 
                  type="button"
                  (click)="studioTab.set('add_subjective')"
                  [ngClass]="studioTab() === 'add_subjective' ? 'border-teal-600 text-teal-600' : 'border-transparent text-slate-500 hover:text-slate-700'"
                  class="pb-2 px-3 text-xs font-bold border-b-2 transition">
                  + Add Subjective / Project
                </button>
                <button 
                  type="button"
                  (click)="studioTab.set('preview')"
                  [ngClass]="studioTab() === 'preview' ? 'border-emerald-600 text-emerald-600' : 'border-transparent text-slate-500 hover:text-slate-700'"
                  class="pb-2 px-3 text-xs font-bold border-b-2 transition ml-auto">
                  Preview Assessment
                </button>
              }
            </div>

            <!-- Tab 1: Details & Audience -->
            @if (studioTab() === 'details') {
              <form (ngSubmit)="saveAssessmentDetails()" class="space-y-4 text-xs">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Assessment Title *</label>
                    <input type="text" [(ngModel)]="assessmentForm.title" name="title" required placeholder="e.g. Asynchronous Microservices Assessment" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                  </div>
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Discipline / Track</label>
                    <select [(ngModel)]="assessmentForm.field" name="field" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl">
                      <option value="Python">Python</option>
                      <option value="Java">Java</option>
                      <option value="SQL">SQL</option>
                      <option value="DSA">DSA</option>
                      <option value="Web Dev">Web Dev</option>
                      <option value="Cloud">Cloud</option>
                      <option value="Data Analytics">Data Analytics</option>
                    </select>
                  </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Duration (Minutes) *</label>
                    <input type="number" [(ngModel)]="assessmentForm.duration_minutes" name="duration" required min="5" max="300" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                  </div>
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Passing Score (%) *</label>
                    <input type="number" [(ngModel)]="assessmentForm.passing_score" name="passing" required min="1" max="100" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                  </div>
                </div>

                <!-- Audience Selection -->
                <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 space-y-3">
                  <span class="block font-bold text-slate-800 dark:text-slate-200 uppercase text-[11px]">Assessment Audience</span>
                  <div class="flex items-center gap-4">
                    <label class="flex items-center gap-2 cursor-pointer font-semibold text-slate-700 dark:text-slate-300">
                      <input type="radio" [(ngModel)]="assessmentForm.audience_type" name="audience_type" value="BATCH" />
                      <span>Entire Batch</span>
                    </label>
                    <label class="flex items-center gap-2 cursor-pointer font-semibold text-slate-700 dark:text-slate-300">
                      <input type="radio" [(ngModel)]="assessmentForm.audience_type" name="audience_type" value="LEARNERS" />
                      <span>Individual Selected Learners</span>
                    </label>
                  </div>

                  @if (assessmentForm.audience_type === 'BATCH') {
                    <div>
                      <label class="block font-bold text-slate-600 dark:text-slate-400 mb-1">Assigned Batch</label>
                      <select [(ngModel)]="assessmentForm.batch_id" name="batch_id" class="w-full px-3 py-2 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl">
                        <option value="">-- All Assigned Batches --</option>
                        @for (b of mentorBatches(); track b.id) {
                          <option [value]="b.id">{{ b.name }} ({{ b.field }})</option>
                        }
                      </select>
                    </div>
                  } @else {
                    <div class="space-y-2">
                      <label class="block font-bold text-slate-600 dark:text-slate-400">Select Learners</label>
                      <div class="max-h-36 overflow-y-auto space-y-1 p-2 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-700">
                        @for (l of mentorLearners(); track l.id) {
                          <label class="flex items-center gap-2 p-1 hover:bg-slate-50 dark:hover:bg-slate-800 rounded cursor-pointer">
                            <input 
                              type="checkbox" 
                              [checked]="isLearnerSelected(l.id)"
                              (change)="toggleLearnerSelection(l.id)" />
                            <span class="font-medium text-slate-800 dark:text-slate-200">{{ l.full_name || l.name }}</span>
                            <span class="text-[10px] text-slate-400 font-mono">({{ l.email }})</span>
                          </label>
                        } @empty {
                          <p class="text-slate-400 p-2">No assigned learners found.</p>
                        }
                      </div>
                    </div>
                  }
                </div>

                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Instructions for Learners</label>
                  <textarea [(ngModel)]="assessmentForm.instructions" name="instructions" rows="2" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" placeholder="Full proctoring active. Code will be validated with sandboxed test execution."></textarea>
                </div>

                <div class="flex justify-end gap-2 pt-2">
                  <button type="button" (click)="closeStudioModal()" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-600 dark:text-slate-300">Cancel</button>
                  <button type="submit" class="px-4 py-2 rounded-xl bg-[#FAA634] text-xs font-bold text-white hover:bg-[#e09228]">
                    {{ activeStudioAssessment() ? 'Save Details' : 'Create & Proceed to Questions' }}
                  </button>
                </div>
              </form>
            }

            <!-- Tab 2: Attached Questions List -->
            @if (studioTab() === 'questions' && activeStudioAssessment()) {
              <div class="space-y-4 text-xs">
                <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
                  <div>
                    <span class="font-bold text-slate-800 dark:text-slate-200 uppercase text-[11px]">Attached Questions ({{ stagedQuestions().length }})</span>
                    <span class="text-slate-400 block text-[10px]">Total Marks: {{ totalStagedMarks() }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <button 
                      type="button" 
                      (click)="openQuestionBankForActiveAssessment()"
                      class="px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 text-slate-700 dark:text-slate-200 font-bold text-[11px]">
                      + From Question Bank
                    </button>
                    <button 
                      type="button" 
                      (click)="studioTab.set('add_mcq')"
                      class="px-3 py-1.5 rounded-lg bg-[#008FBB] hover:bg-[#007499] text-white font-bold text-[11px]">
                      + New MCQ
                    </button>
                    <button 
                      type="button" 
                      (click)="studioTab.set('add_coding')"
                      class="px-3 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-700 text-white font-bold text-[11px]">
                      + New Coding
                    </button>
                    <button 
                      type="button" 
                      (click)="studioTab.set('add_sql')"
                      class="px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-700 text-white font-bold text-[11px]">
                      + New SQL
                    </button>
                    <button 
                      type="button" 
                      (click)="studioTab.set('add_subjective')"
                      class="px-3 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-700 text-white font-bold text-[11px]">
                      + New Subjective
                    </button>
                  </div>
                </div>

                <!-- List of Questions -->
                <div class="space-y-2">
                  @for (q of stagedQuestions(); track q.id || q.bank_question_id; let idx = $index) {
                    <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-between gap-3 shadow-xs">
                      <div class="flex items-center gap-3">
                        <span class="font-mono text-xs font-bold text-slate-400 w-5">#{{ idx + 1 }}</span>
                        <span class="px-1.5 py-0.5 rounded text-[9px] font-bold uppercase"
                          [ngClass]="q.type === 'CODING' ? 'bg-purple-100 text-purple-700' : 'bg-sky-100 text-[#008FBB]'">
                          {{ q.type || 'MCQ' }}
                        </span>
                        <div>
                          <h4 class="font-bold text-slate-800 dark:text-slate-200">{{ q.title }}</h4>
                          @if (q.question_text) {
                            <p class="text-[11px] text-slate-500 line-clamp-1">{{ q.question_text }}</p>
                          }
                        </div>
                      </div>

                      <div class="flex items-center gap-3 shrink-0">
                        <span class="font-mono font-bold text-slate-700 dark:text-slate-300">{{ q.marks }} marks</span>
                        <div class="flex items-center gap-1">
                          <button 
                            type="button" 
                            [disabled]="idx === 0" 
                            (click)="moveQuestion(idx, -1)" 
                            class="p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-30">
                            &uarr;
                          </button>
                          <button 
                            type="button" 
                            [disabled]="idx === stagedQuestions().length - 1" 
                            (click)="moveQuestion(idx, 1)" 
                            class="p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-30">
                            &darr;
                          </button>
                          <button 
                            type="button" 
                            (click)="removeQuestion(q.id)" 
                            class="p-1 text-rose-500 hover:text-rose-700 font-bold ml-1">
                            &times;
                          </button>
                        </div>
                      </div>
                    </div>
                  } @empty {
                    <div class="p-8 text-center text-slate-400 bg-slate-50 dark:bg-slate-950 rounded-xl">
                      No questions attached to this assessment yet. Add questions from the Question Bank or author new ones above.
                    </div>
                  }
                </div>
              </div>
            }

            <!-- Tab 3: Author New MCQ -->
            @if (studioTab() === 'add_mcq') {
              <form (ngSubmit)="submitNewMcq()" class="space-y-4 text-xs">
                <div class="p-3 bg-sky-50 dark:bg-sky-950/40 rounded-xl text-sky-800 dark:text-sky-300 font-medium">
                  Author a conceptual Multiple Choice Question (MCQ). Provide 2 to 6 options and mark correct answers.
                </div>

                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Question Title / Topic *</label>
                  <input type="text" [(ngModel)]="newMcq.title" name="mcq_title" required placeholder="e.g. Asynchronous Coroutines in Python" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                </div>

                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Question Statement *</label>
                  <textarea [(ngModel)]="newMcq.question_text" name="mcq_statement" rows="3" required placeholder="What is the behavior of asyncio.gather() when one coroutine raises an unhandled exception?" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl font-mono text-xs"></textarea>
                </div>

                <!-- Options -->
                <div class="space-y-2">
                  <div class="flex items-center justify-between">
                    <label class="font-bold text-slate-700 dark:text-slate-300">Options (Check the correct answer) *</label>
                    @if (newMcq.options.length < 6) {
                      <button type="button" (click)="addOptionToMcq()" class="text-xs text-[#008FBB] font-bold">+ Add Option</button>
                    }
                  </div>
                  @for (opt of newMcq.options; track opt.option_id; let optIdx = $index) {
                    <div class="flex items-center gap-2">
                      <input 
                        type="checkbox" 
                        [(ngModel)]="opt.is_correct" 
                        [name]="'opt_corr_' + optIdx" 
                        class="h-4 w-4 rounded text-emerald-600 cursor-pointer" />
                      <input 
                        type="text" 
                        [(ngModel)]="opt.option_text" 
                        [name]="'opt_txt_' + optIdx" 
                        required 
                        placeholder="Option text..." 
                        class="flex-1 px-3 py-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs" />
                      @if (newMcq.options.length > 2) {
                        <button type="button" (click)="removeOptionFromMcq(optIdx)" class="text-rose-500 font-bold px-2">&times;</button>
                      }
                    </div>
                  }
                </div>

                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Marks Assigned *</label>
                    <input type="number" [(ngModel)]="newMcq.marks" name="mcq_marks" min="1" max="50" required class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                  </div>
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Difficulty</label>
                    <select [(ngModel)]="newMcq.difficulty" name="mcq_diff" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl">
                      <option value="EASY">EASY</option>
                      <option value="MEDIUM">MEDIUM</option>
                      <option value="HARD">HARD</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Explanation (Revealed during post-submit review)</label>
                  <textarea [(ngModel)]="newMcq.explanation" name="mcq_exp" rows="2" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" placeholder="Detailed explanation..."></textarea>
                </div>

                <div class="flex justify-end gap-2 pt-2">
                  <button type="button" (click)="studioTab.set('questions')" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-600 dark:text-slate-300">Back</button>
                  <button type="submit" class="px-4 py-2 rounded-xl bg-[#008FBB] text-xs font-bold text-white hover:bg-[#007499]">Save &amp; Attach MCQ</button>
                </div>
              </form>
            }

            <!-- Tab 4: Author New Coding Problem -->
            @if (studioTab() === 'add_coding') {
              <form (ngSubmit)="submitNewCoding()" class="space-y-4 text-xs">
                <div class="p-3 bg-purple-50 dark:bg-purple-950/40 rounded-xl text-purple-800 dark:text-purple-300 font-medium">
                  Author a real Coding Challenge. Test cases will be executed against learner code in the sandboxed runner.
                </div>

                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Problem Title *</label>
                    <input type="text" [(ngModel)]="newCoding.title" name="coding_title" required placeholder="e.g. Invert Binary Tree" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                  </div>
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Marks *</label>
                    <input type="number" [(ngModel)]="newCoding.marks" name="coding_marks" min="5" max="100" required class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                  </div>
                </div>

                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Problem Statement &amp; Constraints *</label>
                  <textarea [(ngModel)]="newCoding.question_text" name="coding_statement" rows="3" required placeholder="Describe the problem, input format, and output format..." class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl"></textarea>
                </div>

                <!-- Starter Code Tabs -->
                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Python Starter Code</label>
                  <textarea [(ngModel)]="newCoding.starter_code_py" name="code_py" rows="3" class="w-full px-3 py-2 bg-slate-900 text-emerald-400 font-mono text-xs rounded-xl" placeholder="def solution(nums):&#10;    # Your code here&#10;    pass"></textarea>
                </div>

                <!-- Test Cases -->
                <div class="space-y-2">
                  <div class="flex items-center justify-between">
                    <label class="font-bold text-slate-700 dark:text-slate-300">Test Cases (Visible &amp; Hidden) *</label>
                    <button type="button" (click)="addTestCaseToCoding()" class="text-xs text-purple-600 font-bold">+ Add Test Case</button>
                  </div>
                  @for (tc of newCoding.test_cases; track $index; let tcIdx = $index) {
                    <div class="p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 space-y-2">
                      <div class="flex items-center justify-between">
                        <span class="font-bold font-mono text-[10px] uppercase">Test Case #{{ tcIdx + 1 }}</span>
                        <div class="flex items-center gap-3">
                          <label class="flex items-center gap-1.5 cursor-pointer text-[10px] font-bold">
                            <input type="checkbox" [(ngModel)]="tc.is_hidden" [name]="'tc_hid_' + tcIdx" />
                            <span>Hidden (Assessment Only)</span>
                          </label>
                          @if (newCoding.test_cases.length > 1) {
                            <button type="button" (click)="removeTestCaseFromCoding(tcIdx)" class="text-rose-500 font-bold">&times;</button>
                          }
                        </div>
                      </div>
                      <div class="grid grid-cols-2 gap-2">
                        <div>
                          <span class="block text-[10px] text-slate-400">Input Data</span>
                          <input type="text" [(ngModel)]="tc.input_data" [name]="'tc_in_' + tcIdx" class="w-full px-2 py-1 font-mono text-xs bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg" placeholder="e.g. 5&#10;1 2 3 4 5" />
                        </div>
                        <div>
                          <span class="block text-[10px] text-slate-400">Expected Output</span>
                          <input type="text" [(ngModel)]="tc.expected_output" [name]="'tc_out_' + tcIdx" class="w-full px-2 py-1 font-mono text-xs bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg" placeholder="e.g. 15" />
                        </div>
                      </div>
                    </div>
                  }
                </div>

                <div class="flex justify-end gap-2 pt-2">
                  <button type="button" (click)="studioTab.set('questions')" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-600 dark:text-slate-300">Back</button>
                  <button type="submit" class="px-4 py-2 rounded-xl bg-purple-600 text-xs font-bold text-white hover:bg-purple-700">Save &amp; Attach Coding Problem</button>
                </div>
              </form>
            }

            <!-- Tab: Author New SQL Challenge -->
            @if (studioTab() === 'add_sql') {
              <form (ngSubmit)="submitNewSql()" class="space-y-4 text-xs">
                <div class="p-3 bg-sky-50 dark:bg-sky-950/40 rounded-xl text-sky-800 dark:text-sky-300 font-medium">
                  Author a relational SQL query challenge. Learner queries will be validated against in-memory schemas.
                </div>

                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Problem Title *</label>
                    <input type="text" [(ngModel)]="newSql.title" name="sql_title" required placeholder="e.g. Department Average Salary" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                  </div>
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Marks *</label>
                    <input type="number" [(ngModel)]="newSql.marks" name="sql_marks" min="5" max="100" required class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                  </div>
                </div>

                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Problem Statement *</label>
                  <textarea [(ngModel)]="newSql.question_text" name="sql_statement" rows="3" required placeholder="Write a query to calculate average salary per department..." class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl"></textarea>
                </div>

                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Schema DDL (Tables &amp; Initial DDL) *</label>
                  <textarea [(ngModel)]="newSql.schema_ddl" name="sql_ddl" rows="4" required class="w-full px-3 py-2 bg-slate-900 text-sky-300 font-mono text-xs rounded-xl" placeholder="CREATE TABLE employees (id INT, department VARCHAR(50), salary INT);"></textarea>
                </div>

                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Reference Solution Query</label>
                  <textarea [(ngModel)]="newSql.solution_query" name="sql_sol" rows="3" class="w-full px-3 py-2 bg-slate-900 text-emerald-400 font-mono text-xs rounded-xl" placeholder="SELECT department, AVG(salary) FROM employees GROUP BY department;"></textarea>
                </div>

                <!-- Test Cases -->
                <div class="space-y-2">
                  <div class="flex items-center justify-between">
                    <label class="font-bold text-slate-700 dark:text-slate-300">Test Cases (Data Fixtures &amp; Expected Output)</label>
                    <button type="button" (click)="addTestCaseToSql()" class="text-xs text-sky-600 font-bold">+ Add Fixture</button>
                  </div>
                  @for (tc of newSql.test_cases; track $index; let tcIdx = $index) {
                    <div class="p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 space-y-2">
                      <div class="flex items-center justify-between">
                        <span class="font-bold font-mono text-[10px] uppercase">Fixture #{{ tcIdx + 1 }}</span>
                        <div class="flex items-center gap-3">
                          <label class="flex items-center gap-1.5 cursor-pointer text-[10px] font-bold">
                            <input type="checkbox" [(ngModel)]="tc.is_hidden" [name]="'sql_tc_hid_' + tcIdx" />
                            <span>Hidden</span>
                          </label>
                          @if (newSql.test_cases.length > 1) {
                            <button type="button" (click)="removeTestCaseFromSql(tcIdx)" class="text-rose-500 font-bold">&times;</button>
                          }
                        </div>
                      </div>
                      <div class="grid grid-cols-2 gap-2">
                        <div>
                          <span class="block text-[10px] text-slate-400">INSERT Statements (Seed Data)</span>
                          <input type="text" [(ngModel)]="tc.input_data" [name]="'sql_tc_in_' + tcIdx" class="w-full px-2 py-1 font-mono text-xs bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg" placeholder="INSERT INTO employees VALUES (1, 'Engineering', 80000);" />
                        </div>
                        <div>
                          <span class="block text-[10px] text-slate-400">Expected Result Rows</span>
                          <input type="text" [(ngModel)]="tc.expected_output" [name]="'sql_tc_out_' + tcIdx" class="w-full px-2 py-1 font-mono text-xs bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg" placeholder="Engineering|80000.0" />
                        </div>
                      </div>
                    </div>
                  }
                </div>

                <div class="flex justify-end gap-2 pt-2">
                  <button type="button" (click)="studioTab.set('questions')" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-600 dark:text-slate-300">Back</button>
                  <button type="submit" class="px-4 py-2 rounded-xl bg-sky-600 text-xs font-bold text-white hover:bg-sky-700">Save &amp; Attach SQL Challenge</button>
                </div>
              </form>
            }

            <!-- Tab: Author Subjective / Scenario / Communication / File Upload -->
            @if (studioTab() === 'add_subjective') {
              <form (ngSubmit)="submitNewSubjective()" class="space-y-4 text-xs">
                <div class="p-3 bg-teal-50 dark:bg-teal-950/40 rounded-xl text-teal-800 dark:text-teal-300 font-medium">
                  Author a subjective, scenario-based, or file-upload assignment. Mentor evaluates submission with rubric scoring.
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Assessment Category *</label>
                    <select [(ngModel)]="newSubjective.type" name="subj_type" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl font-bold">
                      <option value="SHORT_ANSWER">SHORT ANSWER</option>
                      <option value="SCENARIO">SCENARIO ANALYSIS</option>
                      <option value="COMMUNICATION">COMMUNICATION</option>
                      <option value="FILE_UPLOAD">FILE UPLOAD / PROJECT</option>
                    </select>
                  </div>
                  <div class="sm:col-span-2">
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Question / Challenge Title *</label>
                    <input type="text" [(ngModel)]="newSubjective.title" name="subj_title" required placeholder="e.g. Distributed Consensus Design Proposal" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                  </div>
                </div>

                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Problem Statement / Prompt *</label>
                  <textarea [(ngModel)]="newSubjective.question_text" name="subj_statement" rows="4" required placeholder="Describe the business scenario, constraints, and instructions for the learner..." class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl"></textarea>
                </div>

                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Scoring Rubric &amp; Evaluation Criteria</label>
                  <textarea [(ngModel)]="newSubjective.rubric_criteria" name="subj_rubric" rows="2" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" placeholder="e.g. Architecture clarity (40%), Failure handling (30%), Concise reasoning (30%)"></textarea>
                </div>

                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Marks Assigned *</label>
                    <input type="number" [(ngModel)]="newSubjective.marks" name="subj_marks" min="5" max="100" required class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                  </div>
                  <div>
                    <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Difficulty</label>
                    <select [(ngModel)]="newSubjective.difficulty" name="subj_diff" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl">
                      <option value="EASY">EASY</option>
                      <option value="MEDIUM">MEDIUM</option>
                      <option value="HARD">HARD</option>
                    </select>
                  </div>
                </div>

                <div class="flex justify-end gap-2 pt-2">
                  <button type="button" (click)="studioTab.set('questions')" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-600 dark:text-slate-300">Back</button>
                  <button type="submit" class="px-4 py-2 rounded-xl bg-teal-600 text-xs font-bold text-white hover:bg-teal-700">Save &amp; Attach Question</button>
                </div>
              </form>
            }

            <!-- Tab 5: Assessment Preview -->
            @if (studioTab() === 'preview' && activeStudioAssessment()) {
              <div class="space-y-4 text-xs">
                <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
                  <div class="flex items-center justify-between">
                    <h2 class="text-base font-black text-slate-900 dark:text-white">{{ activeStudioAssessment()?.title }}</h2>
                    <span class="font-mono text-xs font-bold text-emerald-600">{{ activeStudioAssessment()?.duration_minutes }} Mins &bull; Pass: {{ activeStudioAssessment()?.passing_score }}%</span>
                  </div>
                  <p class="text-slate-600 dark:text-slate-300">{{ activeStudioAssessment()?.instructions || 'Standard assessment instructions.' }}</p>
                </div>

                <div class="space-y-3">
                  @for (q of stagedQuestions(); track q.id; let idx = $index) {
                    <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-2">
                      <div class="flex items-center justify-between">
                        <span class="font-bold text-slate-700 dark:text-slate-300">Question {{ idx + 1 }}: {{ q.title }}</span>
                        <span class="font-mono text-xs text-slate-400 font-bold">{{ q.marks }} Marks</span>
                      </div>
                      <p class="text-slate-600 dark:text-slate-300">{{ q.question_text || q.content }}</p>
                    </div>
                  } @empty {
                    <p class="text-slate-400 text-center py-4">No questions to preview.</p>
                  }
                </div>

                <div class="flex justify-end gap-2 pt-2">
                  <button type="button" (click)="studioTab.set('questions')" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold">Back to Questions</button>
                  @if (!activeStudioAssessment()?.is_published) {
                    <button type="button" (click)="publishAssessment(activeStudioAssessment()!)" class="px-4 py-2 rounded-xl bg-emerald-600 text-xs font-bold text-white hover:bg-emerald-700">Publish to Learners</button>
                  }
                </div>
              </div>
            }
          </div>
        </div>
      }

      <!-- Results Analysis & CSV Export Drawer (Zero Demo Data - Live API) -->
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

            @if (resultsData()) {
              <!-- Overall Metrics -->
              <div class="grid grid-cols-3 gap-3">
                <div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-xl text-center">
                  <span class="text-[10px] font-bold uppercase text-slate-400 block">Total Attempts</span>
                  <span class="text-lg font-black text-slate-800 dark:text-slate-100">{{ resultsData().total_attempts }}</span>
                </div>
                <div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-xl text-center">
                  <span class="text-[10px] font-bold uppercase text-slate-400 block">Average Score</span>
                  <span class="text-lg font-black text-[#008FBB]">{{ resultsData().average_score }}%</span>
                </div>
                <div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-xl text-center">
                  <span class="text-[10px] font-bold uppercase text-slate-400 block">Pass Rate</span>
                  <span class="text-lg font-black text-emerald-600">{{ resultsData().pass_rate }}%</span>
                </div>
              </div>

              <!-- Score Distribution -->
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
                <span class="text-xs font-bold uppercase text-slate-400">Score Distribution</span>
                <div class="space-y-1.5 text-xs">
                  <div class="flex items-center justify-between">
                    <span>90% - 100% (Distinction)</span>
                    <span class="font-bold text-emerald-600">{{ resultsData().score_distribution?.['90-100'] || 0 }} Learners</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <span>70% - 89% (Proficient)</span>
                    <span class="font-bold text-[#008FBB]">{{ resultsData().score_distribution?.['70-90'] || 0 }} Learners</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <span>50% - 69% (Average)</span>
                    <span class="font-bold text-amber-500">{{ resultsData().score_distribution?.['50-70'] || 0 }} Learners</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <span>&lt; 50% (Needs Review)</span>
                    <span class="font-bold text-slate-400">{{ resultsData().score_distribution?.['0-50'] || 0 }} Learners</span>
                  </div>
                </div>
              </div>

              <!-- AI Cohort Distribution & Psychometrics Card -->
              @if (aiInsights()) {
                <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-800 dark:text-slate-200 uppercase text-[11px]">AI Psychometric Distribution Curve</span>
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-[#008FBB] text-white">SciPy &amp; NumPy</span>
                  </div>
                  @if (aiInsights().charts?.distribution_curve_svg) {
                    <div [innerHTML]="getSafeSvg(aiInsights().charts.distribution_curve_svg)" class="overflow-hidden rounded-lg bg-slate-50/50 dark:bg-slate-950 p-2 border border-slate-100 dark:border-slate-800"></div>
                  }
                  <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed bg-amber-50/60 dark:bg-amber-950/30 p-2.5 rounded-lg border border-amber-200/60 dark:border-amber-900/40">
                    {{ aiInsights().ai_summary }}
                  </p>
                </div>
              }

              <!-- Learner Attempts List -->
              <div class="space-y-3 text-xs">
                <span class="font-bold uppercase text-slate-400">Submitted Attempts</span>
                @for (l of resultsData().learners; track l.attempt_id || l.id) {
                  <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div class="space-y-1">
                      <div class="flex items-center gap-2">
                        <span class="font-bold text-slate-800 dark:text-slate-200">{{ l.name }}</span>
                        <span class="px-1.5 py-0.5 rounded text-[9px] font-bold"
                          [ngClass]="l.grading_status === 'GRADED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'">
                          {{ l.grading_status || 'GRADED' }}
                        </span>
                        @if (l.report_status && l.report_status !== 'NONE') {
                          <span class="px-1.5 py-0.5 rounded text-[9px] font-bold"
                            [ngClass]="l.report_status === 'APPROVED' ? 'bg-sky-100 text-sky-800' : 'bg-purple-100 text-purple-800'">
                            Report: {{ l.report_status }}
                          </span>
                        }
                      </div>
                      <span class="text-[10px] text-slate-400 block">{{ l.email }}</span>
                    </div>

                    <div class="flex items-center gap-3">
                      <div class="text-right">
                        <span class="font-mono font-bold" [ngClass]="l.passed ? 'text-emerald-600' : 'text-rose-500'">{{ l.score }}%</span>
                        <span class="text-[10px] text-slate-400 block">{{ l.passed ? 'PASSED' : 'FAILED' }}</span>
                      </div>

                      <div class="flex items-center gap-1.5">
                        <button 
                          type="button" 
                          (click)="openGradingModal(l.attempt_id)"
                          class="px-2.5 py-1.5 rounded-lg bg-[#008FBB] hover:bg-[#007499] text-white text-[10px] font-bold transition">
                          Review &amp; Grade
                        </button>
                        @if (l.report_status === 'PENDING_APPROVAL') {
                          <button 
                            type="button" 
                            (click)="approveReport(l.attempt_id)"
                            class="px-2.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-[10px] font-bold transition">
                            Approve Report
                          </button>
                        }
                      </div>
                    </div>
                  </div>
                } @empty {
                  <div class="p-6 text-center text-slate-400 bg-slate-50 dark:bg-slate-800/40 rounded-xl text-xs">
                    No submissions recorded yet for this assessment. Submissions will appear here once learners complete their attempts.
                  </div>
                }
              </div>
            } @else {
              <div class="p-8 text-center text-slate-400 text-xs">Loading analytics...</div>
            }

            <div class="pt-4 flex justify-end">
              <button (click)="selectedAssessmentForResults.set(null)" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold">
                Close
              </button>
            </div>
          </div>
        </div>
      }

      <!-- Manual Grading & Attempt Review Modal -->
      @if (showGradingModal() && gradingData()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-4xl w-full p-6 space-y-5 max-h-[92vh] overflow-y-auto">
            <div class="flex items-start justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-[#008FBB]">Attempt Evaluation &amp; Grading</span>
                <h3 class="text-base font-black text-slate-900 dark:text-white">
                  {{ gradingData()?.learner_name }} &bull; {{ gradingData()?.assessment_title }}
                </h3>
                <div class="flex items-center gap-2 mt-1">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold"
                    [ngClass]="gradingData()?.passed ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'">
                    Score: {{ gradingData()?.score }} / {{ gradingData()?.total_marks }} ({{ gradingData()?.passed ? 'PASSED' : 'NOT PASSED' }})
                  </span>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
                    Status: {{ gradingData()?.grading_status }}
                  </span>
                  @if (gradingData()?.report_status && gradingData()?.report_status !== 'NONE') {
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-100 text-purple-800">
                      Growth Ring: {{ gradingData()?.report_status }}
                    </span>
                  }
                </div>
              </div>
              <button (click)="closeGradingModal()" class="text-slate-400 hover:text-slate-600 text-xl font-bold">&times;</button>
            </div>

            <!-- List of Answers for this Attempt -->
            <div class="space-y-4 text-xs">
              @for (ans of gradingData()?.answers; track ans.id; let qIdx = $index) {
                <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-950/60 space-y-3">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                      <span class="font-mono font-bold text-slate-400">#{{ qIdx + 1 }}</span>
                      <span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase"
                        [ngClass]="{
                          'bg-sky-100 text-sky-800': ans.question_type === 'MCQ',
                          'bg-purple-100 text-purple-800': ans.question_type === 'CODING',
                          'bg-indigo-100 text-indigo-800': ans.question_type === 'SQL',
                          'bg-teal-100 text-teal-800': ans.question_type === 'SHORT_ANSWER' || ans.question_type === 'SCENARIO' || ans.question_type === 'COMMUNICATION',
                          'bg-amber-100 text-amber-800': ans.question_type === 'FILE_UPLOAD'
                        }">
                        {{ ans.question_type }}
                      </span>
                      <h4 class="font-bold text-slate-800 dark:text-slate-200">{{ ans.question_title }}</h4>
                    </div>
                    <span class="font-mono text-xs font-bold text-slate-500">Max {{ ans.marks }} Marks</span>
                  </div>

                  <!-- MCQ Details -->
                  @if (ans.question_type === 'MCQ') {
                    <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-1">
                      <div class="flex items-center justify-between text-[11px]">
                        <span>Selected Option: <strong>{{ ans.selected_option_id || 'No selection' }}</strong></span>
                        <span class="font-mono font-bold" [ngClass]="ans.is_correct ? 'text-emerald-600' : 'text-rose-500'">
                          {{ ans.is_correct ? 'Correct (+ ' + ans.score_awarded + ')' : 'Incorrect (0 marks)' }}
                        </span>
                      </div>
                    </div>
                  }

                  <!-- Coding / SQL Details -->
                  @if (ans.question_type === 'CODING' || ans.question_type === 'SQL') {
                    <div class="space-y-1.5">
                      <span class="text-[10px] uppercase font-bold text-slate-400">Submitted Solution</span>
                      <pre class="p-3 bg-slate-900 text-slate-100 font-mono text-[11px] rounded-lg overflow-x-auto">{{ ans.source_code || '-- No code submitted --' }}</pre>
                      <div class="flex items-center justify-between text-[11px] text-slate-500 pt-1">
                        <span>Execution Status: <strong>{{ ans.grading_status || 'Auto-evaluated' }}</strong></span>
                        <span class="font-mono font-bold text-emerald-600">Awarded: {{ ans.score_awarded }} / {{ ans.marks }}</span>
                      </div>
                    </div>
                  }

                  <!-- Subjective Written Answers (Short Answer, Scenario, Communication) -->
                  @if (ans.question_type === 'SHORT_ANSWER' || ans.question_type === 'SCENARIO' || ans.question_type === 'COMMUNICATION') {
                    <div class="space-y-2">
                      <span class="text-[10px] uppercase font-bold text-slate-400">Learner's Written Response</span>
                      <p class="p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-800 dark:text-slate-200 whitespace-pre-wrap leading-relaxed">
                        {{ ans.text_response || 'No written response submitted.' }}
                      </p>
                      @if (ans.rubric && ans.rubric.criteria) {
                        <div class="p-2 rounded bg-amber-50 dark:bg-amber-950/30 text-amber-800 dark:text-amber-300 text-[10px]">
                          <strong>Rubric:</strong> {{ ans.rubric.criteria }}
                        </div>
                      }
                      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 pt-1">
                        <div>
                          <label class="block font-bold text-slate-600 dark:text-slate-400 mb-0.5">Score Awarded (Max {{ ans.marks }})</label>
                          <input type="number" [(ngModel)]="ans.score_awarded" min="0" [max]="ans.marks" class="w-full px-2 py-1 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg font-mono font-bold" />
                        </div>
                        <div class="sm:col-span-2">
                          <label class="block font-bold text-slate-600 dark:text-slate-400 mb-0.5">Mentor Feedback</label>
                          <input type="text" [(ngModel)]="ans.mentor_feedback" placeholder="Constructive guidance and notes..." class="w-full px-2 py-1 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg" />
                        </div>
                      </div>
                    </div>
                  }

                  <!-- File Upload Deliverables -->
                  @if (ans.question_type === 'FILE_UPLOAD') {
                    <div class="space-y-2">
                      <span class="text-[10px] uppercase font-bold text-slate-400">Uploaded Deliverable</span>
                      <div class="p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg flex items-center justify-between">
                        <div>
                          <span class="font-bold text-slate-800 dark:text-slate-200 block">{{ ans.file_name || 'Project Asset' }}</span>
                          <a [href]="ans.file_url" target="_blank" rel="noopener noreferrer" class="text-[#008FBB] underline text-[11px]">
                            {{ ans.file_url || 'No file URL provided' }}
                          </a>
                        </div>
                        <span class="text-xs text-slate-400 font-bold">&DownArrow; Download / Open</span>
                      </div>
                      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 pt-1">
                        <div>
                          <label class="block font-bold text-slate-600 dark:text-slate-400 mb-0.5">Score Awarded (Max {{ ans.marks }})</label>
                          <input type="number" [(ngModel)]="ans.score_awarded" min="0" [max]="ans.marks" class="w-full px-2 py-1 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg font-mono font-bold" />
                        </div>
                        <div class="sm:col-span-2">
                          <label class="block font-bold text-slate-600 dark:text-slate-400 mb-0.5">Mentor Feedback</label>
                          <input type="text" [(ngModel)]="ans.mentor_feedback" placeholder="Feedback on project deliverable..." class="w-full px-2 py-1 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg" />
                        </div>
                      </div>
                    </div>
                  }
                </div>
              }
            </div>

            <div class="flex items-center justify-between pt-3 border-t border-slate-200 dark:border-slate-800">
              <div>
                @if (gradingData()?.report_status === 'PENDING_APPROVAL') {
                  <button 
                    type="button" 
                    (click)="approveReport(gradingData()?.attempt_id)"
                    class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs transition">
                    &check; Approve Growth Ring Report
                  </button>
                }
              </div>
              <div class="flex items-center gap-2">
                <button 
                  type="button" 
                  (click)="closeGradingModal()" 
                  class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-xs">
                  Cancel
                </button>
                <button 
                  type="button" 
                  (click)="submitGrades()" 
                  class="px-4 py-2 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-white font-bold text-xs shadow-sm transition">
                  Save All Grades &amp; Re-generate Report
                </button>
              </div>
            </div>
          </div>
        </div>
      }

      <!-- Question Bank Modal -->
      @if (showQuestionBankModal()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-3xl w-full p-6 space-y-4 max-h-[90vh] flex flex-col">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <div>
                <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">Question Bank Repository</h3>
                <p class="text-xs text-slate-500 dark:text-slate-400">Select verified MCQ and sandboxed Coding questions to stage directly into an assessment.</p>
              </div>
              <button (click)="showQuestionBankModal.set(false)" class="text-slate-400 hover:text-slate-600 text-xl font-bold">&times;</button>
            </div>

            <!-- Target Assessment Selector -->
            <div class="p-3 bg-amber-50 dark:bg-amber-950/40 rounded-xl border border-amber-200 dark:border-amber-900 flex items-center justify-between gap-3 text-xs">
              <span class="font-bold text-amber-800 dark:text-amber-300">Target Assessment:</span>
              <select [(ngModel)]="targetAssessmentId" class="flex-1 px-3 py-1.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg font-bold">
                @for (a of assessments(); track a.id) {
                  <option [value]="a.id">{{ a.title }} ({{ a.field }} - {{ a.is_published ? 'v' + a.version : 'Draft' }})</option>
                }
              </select>
            </div>

            <!-- Filter Row -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <input 
                type="text" 
                [(ngModel)]="questionBankSearch" 
                (ngModelChange)="filterQuestionBank()"
                placeholder="Search questions by keyword..."
                class="px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs" />
              
              <select [(ngModel)]="questionBankField" (ngModelChange)="filterQuestionBank()" class="px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs">
                <option value="ALL">All Fields</option>
                <option value="Python">Python</option>
                <option value="Java">Java</option>
                <option value="SQL">SQL</option>
                <option value="DSA">DSA</option>
                <option value="Web Dev">Web Dev</option>
                <option value="Cloud">Cloud</option>
                <option value="Data Analytics">Data Analytics</option>
              </select>

              <select [(ngModel)]="questionBankType" (ngModelChange)="filterQuestionBank()" class="px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs">
                <option value="ALL">All Question Types</option>
                <option value="MCQ">MCQ Concept</option>
                <option value="CODING">Coding Challenge</option>
              </select>
            </div>

            <!-- Feedback message -->
            @if (questionBankMessage()) {
              <div class="p-2.5 rounded-xl bg-emerald-50 text-emerald-800 text-xs font-bold border border-emerald-200">
                {{ questionBankMessage() }}
              </div>
            }

            <!-- Questions List -->
            <div class="flex-1 overflow-y-auto space-y-3 pr-1">
              @for (q of filteredQuestions(); track q.id) {
                <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 space-y-2">
                  <div class="flex items-start justify-between gap-3">
                    <div class="space-y-1">
                      <div class="flex items-center gap-2">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase"
                          [ngClass]="q.type === 'CODING' ? 'bg-purple-100 text-purple-700' : 'bg-sky-100 text-[#008FBB]'">
                          {{ q.type }}
                        </span>
                        <span class="text-[10px] font-mono text-slate-400 font-bold uppercase">{{ q.field }} &bull; {{ q.difficulty }}</span>
                      </div>
                      <h4 class="text-xs font-bold text-slate-900 dark:text-white">{{ q.title }}</h4>
                    </div>

                    <button 
                      type="button" 
                      (click)="attachQuestionFromBank(q)"
                      class="shrink-0 px-3 py-1.5 rounded-lg bg-[#008FBB] hover:bg-[#007499] text-white text-[11px] font-bold transition shadow-sm">
                      + Stage to Assessment
                    </button>
                  </div>

                  <p class="text-xs text-slate-600 dark:text-slate-300 whitespace-pre-wrap">{{ q.content }}</p>

                  @if (q.tags && q.tags.length > 0) {
                    <div class="flex flex-wrap gap-1 pt-1">
                      @for (t of q.tags; track t) {
                        <span class="px-2 py-0.5 rounded bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-[10px] text-slate-500 font-mono">
                          #{{ t }}
                        </span>
                      }
                    </div>
                  }
                </div>
              } @empty {
                <div class="p-8 text-center text-xs text-slate-400 bg-slate-50 dark:bg-slate-950 rounded-xl">
                  No questions found matching your filter criteria.
                </div>
              }
            </div>

            <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-end">
              <button type="button" (click)="showQuestionBankModal.set(false)" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-700 dark:text-slate-200">
                Close Question Bank
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
  private readonly sanitizer = inject(DomSanitizer);

  readonly assessments = signal<AssessmentItem[]>([]);
  readonly showStudioModal = signal<boolean>(false);
  readonly showQuestionBankModal = signal<boolean>(false);
  readonly selectedAssessmentForResults = signal<AssessmentItem | null>(null);
  readonly resultsData = signal<any>(null);
  readonly aiInsights = signal<any>(null);

  readonly activeStudioAssessment = signal<AssessmentItem | null>(null);
  readonly stagedQuestions = signal<any[]>([]);
  readonly studioTab = signal<'details' | 'questions' | 'add_mcq' | 'add_coding' | 'add_sql' | 'add_subjective' | 'preview'>('details');

  readonly showGradingModal = signal<boolean>(false);
  readonly gradingData = signal<any>(null);

  readonly mentorBatches = signal<any[]>([]);
  readonly mentorLearners = signal<any[]>([]);

  readonly questionBank = signal<QuestionBankItem[]>([]);
  readonly filteredQuestions = signal<QuestionBankItem[]>([]);
  readonly questionBankMessage = signal<string | null>(null);
  readonly actionToast = signal<{ message: string; type: 'success' | 'error' } | null>(null);

  targetAssessmentId = '';
  questionBankSearch = '';
  questionBankField = 'ALL';
  questionBankType = 'ALL';

  assessmentForm = {
    title: '',
    field: 'Python',
    instructions: 'Proctored timed assessment. Sandboxed code execution enabled.',
    duration_minutes: 60,
    passing_score: 75,
    audience_type: 'BATCH' as 'BATCH' | 'LEARNERS',
    batch_id: '',
    learner_ids: [] as string[],
  };

  newMcq = {
    title: '',
    question_text: '',
    field: 'Python',
    difficulty: 'MEDIUM',
    marks: 10,
    explanation: '',
    options: [
      { option_id: 'opt_1', option_text: '', is_correct: true },
      { option_id: 'opt_2', option_text: '', is_correct: false },
      { option_id: 'opt_3', option_text: '', is_correct: false },
      { option_id: 'opt_4', option_text: '', is_correct: false },
    ],
  };

  newCoding = {
    title: '',
    question_text: '',
    field: 'Python',
    difficulty: 'MEDIUM',
    marks: 20,
    starter_code_py: 'def solution(nums):\n    # Enter your code\n    pass',
    test_cases: [
      { input_data: '1 2 3', expected_output: '6', is_hidden: false },
      { input_data: '4 5 6', expected_output: '15', is_hidden: true },
    ] as TestCase[],
  };

  newSql = {
    title: '',
    question_text: '',
    field: 'SQL',
    difficulty: 'MEDIUM',
    marks: 15,
    schema_ddl: 'CREATE TABLE employees (\n  id INT PRIMARY KEY,\n  name VARCHAR(50),\n  department VARCHAR(50),\n  salary INT\n);',
    solution_query: 'SELECT department, AVG(salary) FROM employees GROUP BY department;',
    test_cases: [
      { input_data: "INSERT INTO employees VALUES (1, 'Alice', 'Engineering', 90000), (2, 'Bob', 'Engineering', 80000);", expected_output: "Engineering|85000.0", is_hidden: false }
    ] as TestCase[],
  };

  newSubjective = {
    type: 'SHORT_ANSWER',
    title: '',
    question_text: '',
    field: 'Architecture',
    difficulty: 'MEDIUM',
    marks: 10,
    rubric_criteria: 'Clarity (40%), Technical correctness (40%), Completeness (20%)',
  };

  ngOnInit(): void {
    this.loadAssessments();
    this.loadBatchesAndLearners();
  }

  loadAssessments(): void {
    this.mentorService.getAssessments().subscribe({
      next: (data) => {
        this.assessments.set(data || []);
        if (data && data.length > 0 && !this.targetAssessmentId) {
          this.targetAssessmentId = data[0].id;
        }
      },
      error: () => {},
    });
  }

  loadBatchesAndLearners(): void {
    this.mentorService.getBatches().subscribe({
      next: (data) => this.mentorBatches.set(data || []),
      error: () => {},
    });
    this.mentorService.getLearners().subscribe({
      next: (data) => this.mentorLearners.set(data || []),
      error: () => {},
    });
  }

  openCreateAssessment(): void {
    this.activeStudioAssessment.set(null);
    this.stagedQuestions.set([]);
    this.assessmentForm = {
      title: '',
      field: 'Python',
      instructions: 'Proctored timed assessment. Code evaluated via sandboxed runner.',
      duration_minutes: 60,
      passing_score: 75,
      audience_type: 'BATCH',
      batch_id: this.mentorBatches().length > 0 ? this.mentorBatches()[0].id : '',
      learner_ids: [],
    };
    this.studioTab.set('details');
    this.showStudioModal.set(true);
  }

  openEditAssessment(a: AssessmentItem): void {
    this.activeStudioAssessment.set(a);
    this.targetAssessmentId = a.id;
    this.assessmentForm = {
      title: a.title,
      field: a.field,
      instructions: a.instructions || 'Proctored timed assessment.',
      duration_minutes: a.duration_minutes,
      passing_score: a.passing_score,
      audience_type: (a as any).audience_learners && (a as any).audience_learners.length > 0 ? 'LEARNERS' : 'BATCH',
      batch_id: a.batch_id || '',
      learner_ids: (a as any).audience_learners || [],
    };
    this.loadStagedQuestions(a.id);
    this.studioTab.set('questions');
    this.showStudioModal.set(true);
  }

  loadStagedQuestions(assessmentId: string): void {
    this.mentorService.getAssessmentQuestions(assessmentId).subscribe({
      next: (qs) => this.stagedQuestions.set(qs || []),
      error: () => this.stagedQuestions.set([]),
    });
  }

  closeStudioModal(): void {
    this.showStudioModal.set(false);
    this.loadAssessments();
  }

  isLearnerSelected(id: string): boolean {
    return this.assessmentForm.learner_ids.includes(id);
  }

  toggleLearnerSelection(id: string): void {
    const idx = this.assessmentForm.learner_ids.indexOf(id);
    if (idx >= 0) {
      this.assessmentForm.learner_ids.splice(idx, 1);
    } else {
      this.assessmentForm.learner_ids.push(id);
    }
  }

  saveAssessmentDetails(): void {
    const payload = {
      title: this.assessmentForm.title,
      field: this.assessmentForm.field,
      instructions: this.assessmentForm.instructions,
      duration_minutes: this.assessmentForm.duration_minutes,
      passing_score: this.assessmentForm.passing_score,
      batch_id: this.assessmentForm.audience_type === 'BATCH' && this.assessmentForm.batch_id ? this.assessmentForm.batch_id : undefined,
      learner_ids: this.assessmentForm.audience_type === 'LEARNERS' ? this.assessmentForm.learner_ids : [],
    };

    const current = this.activeStudioAssessment();
    if (current) {
      this.mentorService.updateAssessment(current.id, payload).subscribe({
        next: (updated) => {
          this.activeStudioAssessment.set(updated);
          this.showToast('Assessment details updated successfully.');
          this.studioTab.set('questions');
          this.loadAssessments();
        },
        error: (err) => this.showToast(err.error?.detail || 'Failed to update assessment.', 'error'),
      });
    } else {
      this.mentorService.createAssessment(payload).subscribe({
        next: (created) => {
          this.activeStudioAssessment.set(created);
          this.targetAssessmentId = created.id;
          this.showToast('Assessment created as draft. Now attach questions.');
          this.loadStagedQuestions(created.id);
          this.studioTab.set('questions');
          this.loadAssessments();
        },
        error: (err) => this.showToast(err.error?.detail || 'Failed to create assessment.', 'error'),
      });
    }
  }

  totalStagedMarks(): number {
    return this.stagedQuestions().reduce((sum, q) => sum + (parseFloat(q.marks) || 0), 0);
  }

  moveQuestion(index: number, delta: number): void {
    const list = [...this.stagedQuestions()];
    const targetIdx = index + delta;
    if (targetIdx < 0 || targetIdx >= list.length) return;

    const temp = list[index];
    list[index] = list[targetIdx];
    list[targetIdx] = temp;

    const current = this.activeStudioAssessment();
    if (current) {
      const reorderPayload = list.map((item, idx) => ({
        aq_id: item.id,
        order: idx + 1,
        marks: item.marks,
      }));
      this.mentorService.updateAssessmentQuestions(current.id, reorderPayload).subscribe({
        next: (res) => {
          this.stagedQuestions.set(list);
          if (res?.versioned) {
            this.showToast('Assessment versioned due to existing submissions.');
            this.loadAssessments();
          }
        },
        error: () => this.loadStagedQuestions(current.id),
      });
    }
  }

  removeQuestion(aqId: string): void {
    const current = this.activeStudioAssessment();
    if (!current) return;
    this.mentorService.removeQuestionFromAssessment(current.id, aqId).subscribe({
      next: () => {
        this.showToast('Question detached from assessment.');
        this.loadStagedQuestions(current.id);
        this.loadAssessments();
      },
      error: (err) => this.showToast(err.error?.detail || 'Failed to remove question.', 'error'),
    });
  }

  addOptionToMcq(): void {
    if (this.newMcq.options.length < 6) {
      this.newMcq.options.push({
        option_id: `opt_${this.newMcq.options.length + 1}`,
        option_text: '',
        is_correct: false,
      });
    }
  }

  removeOptionFromMcq(index: number): void {
    if (this.newMcq.options.length > 2) {
      this.newMcq.options.splice(index, 1);
    }
  }

  submitNewMcq(): void {
    const current = this.activeStudioAssessment();
    if (!current) return;

    const payload = {
      title: this.newMcq.title,
      question_text: this.newMcq.question_text,
      type: 'MCQ',
      field: current.field || this.newMcq.field,
      difficulty: this.newMcq.difficulty,
      marks: this.newMcq.marks,
      explanation: this.newMcq.explanation,
      options: this.newMcq.options.map((o) => ({
        text: o.option_text,
        is_correct: o.is_correct,
      })),
    };

    this.mentorService.addQuestionToBank(payload).subscribe({
      next: (createdBankItem) => {
        this.mentorService.attachQuestionToAssessment(current.id, {
          question_id: createdBankItem.id,
          marks: this.newMcq.marks,
        }).subscribe({
          next: () => {
            this.showToast(`MCQ "${createdBankItem.title}" attached to assessment!`);
            this.newMcq = {
              title: '',
              question_text: '',
              field: current.field,
              difficulty: 'MEDIUM',
              marks: 10,
              explanation: '',
              options: [
                { option_id: 'opt_1', option_text: '', is_correct: true },
                { option_id: 'opt_2', option_text: '', is_correct: false },
                { option_id: 'opt_3', option_text: '', is_correct: false },
                { option_id: 'opt_4', option_text: '', is_correct: false },
              ],
            };
            this.loadStagedQuestions(current.id);
            this.studioTab.set('questions');
            this.loadAssessments();
          },
          error: (err) => this.showToast(err.error?.detail || 'Failed to attach question.', 'error'),
        });
      },
      error: (err) => this.showToast(err.error?.detail || 'Failed to author MCQ in bank.', 'error'),
    });
  }

  addTestCaseToCoding(): void {
    this.newCoding.test_cases.push({
      input_data: '',
      expected_output: '',
      is_hidden: false,
    });
  }

  removeTestCaseFromCoding(index: number): void {
    if (this.newCoding.test_cases.length > 1) {
      this.newCoding.test_cases.splice(index, 1);
    }
  }

  submitNewCoding(): void {
    const current = this.activeStudioAssessment();
    if (!current) return;

    const payload = {
      title: this.newCoding.title,
      question_text: this.newCoding.question_text,
      type: 'CODING',
      field: current.field || this.newCoding.field,
      difficulty: this.newCoding.difficulty,
      marks: this.newCoding.marks,
      starter_code: {
        python: this.newCoding.starter_code_py,
      },
      test_cases: this.newCoding.test_cases.map((tc) => ({
        input: tc.input_data,
        expected_output: tc.expected_output,
        is_hidden: tc.is_hidden,
      })),
    };

    this.mentorService.addQuestionToBank(payload).subscribe({
      next: (createdBankItem) => {
        this.mentorService.attachQuestionToAssessment(current.id, {
          question_id: createdBankItem.id,
          marks: this.newCoding.marks,
        }).subscribe({
          next: () => {
            this.showToast(`Coding Problem "${createdBankItem.title}" attached to assessment!`);
            this.newCoding = {
              title: '',
              question_text: '',
              field: current.field,
              difficulty: 'MEDIUM',
              marks: 20,
              starter_code_py: 'def solution(nums):\n    pass',
              test_cases: [
                { input_data: '', expected_output: '', is_hidden: false },
              ],
            };
            this.loadStagedQuestions(current.id);
            this.studioTab.set('questions');
            this.loadAssessments();
          },
          error: (err) => this.showToast(err.error?.detail || 'Failed to attach coding problem.', 'error'),
        });
      },
      error: (err) => this.showToast(err.error?.detail || 'Failed to author coding question in bank.', 'error'),
    });
  }

  addTestCaseToSql(): void {
    this.newSql.test_cases.push({
      input_data: '',
      expected_output: '',
      is_hidden: false,
    });
  }

  removeTestCaseFromSql(index: number): void {
    if (this.newSql.test_cases.length > 1) {
      this.newSql.test_cases.splice(index, 1);
    }
  }

  submitNewSql(): void {
    const current = this.activeStudioAssessment();
    if (!current) return;

    const payload = {
      title: this.newSql.title,
      question_text: this.newSql.question_text,
      type: 'SQL',
      field: current.field || this.newSql.field,
      difficulty: this.newSql.difficulty,
      marks: this.newSql.marks,
      schema_ddl: this.newSql.schema_ddl,
      solution_query: this.newSql.solution_query,
      starter_code: {
        sql: '-- Enter your query here\n',
      },
      test_cases: this.newSql.test_cases.map((tc) => ({
        input: tc.input_data,
        expected_output: tc.expected_output,
        is_hidden: tc.is_hidden,
      })),
    };

    this.mentorService.addQuestionToBank(payload).subscribe({
      next: (createdBankItem) => {
        this.mentorService.attachQuestionToAssessment(current.id, {
          question_id: createdBankItem.id,
          marks: this.newSql.marks,
        }).subscribe({
          next: () => {
            this.showToast(`SQL Challenge "${createdBankItem.title}" attached to assessment!`);
            this.newSql = {
              title: '',
              question_text: '',
              field: 'SQL',
              difficulty: 'MEDIUM',
              marks: 15,
              schema_ddl: '',
              solution_query: '',
              test_cases: [
                { input_data: '', expected_output: '', is_hidden: false },
              ],
            };
            this.loadStagedQuestions(current.id);
            this.studioTab.set('questions');
            this.loadAssessments();
          },
          error: (err) => this.showToast(err.error?.detail || 'Failed to attach SQL question.', 'error'),
        });
      },
      error: (err) => this.showToast(err.error?.detail || 'Failed to author SQL question in bank.', 'error'),
    });
  }

  submitNewSubjective(): void {
    const current = this.activeStudioAssessment();
    if (!current) return;

    const payload = {
      title: this.newSubjective.title,
      question_text: this.newSubjective.question_text,
      type: this.newSubjective.type,
      field: current.field || this.newSubjective.field,
      difficulty: this.newSubjective.difficulty,
      marks: this.newSubjective.marks,
      rubric: {
        criteria: this.newSubjective.rubric_criteria,
      },
    };

    this.mentorService.addQuestionToBank(payload).subscribe({
      next: (createdBankItem) => {
        this.mentorService.attachQuestionToAssessment(current.id, {
          question_id: createdBankItem.id,
          marks: this.newSubjective.marks,
        }).subscribe({
          next: () => {
            this.showToast(`Question "${createdBankItem.title}" attached to assessment!`);
            this.newSubjective = {
              type: 'SHORT_ANSWER',
              title: '',
              question_text: '',
              field: current.field || 'Architecture',
              difficulty: 'MEDIUM',
              marks: 10,
              rubric_criteria: '',
            };
            this.loadStagedQuestions(current.id);
            this.studioTab.set('questions');
            this.loadAssessments();
          },
          error: (err) => this.showToast(err.error?.detail || 'Failed to attach question.', 'error'),
        });
      },
      error: (err) => this.showToast(err.error?.detail || 'Failed to author question in bank.', 'error'),
    });
  }

  openGradingModal(attemptId: string): void {
    this.mentorService.getAttemptAnswersForGrading(attemptId).subscribe({
      next: (data) => {
        this.gradingData.set(data);
        this.showGradingModal.set(true);
      },
      error: (err) => this.showToast(err.error?.detail || 'Failed to load attempt answers.', 'error'),
    });
  }

  closeGradingModal(): void {
    this.showGradingModal.set(false);
    this.gradingData.set(null);
  }

  submitGrades(): void {
    const data = this.gradingData();
    if (!data) return;

    const gradesPayload = (data.answers || []).map((ans: any) => ({
      answer_id: ans.id,
      score_awarded: Number(ans.score_awarded) || 0,
      feedback: ans.mentor_feedback || '',
    }));

    this.mentorService.gradeAttemptAnswers(data.attempt_id, gradesPayload).subscribe({
      next: () => {
        this.showToast('Grades saved successfully!');
        this.closeGradingModal();
        const a = this.selectedAssessmentForResults();
        if (a) {
          this.openResultsAnalysis(a);
        }
      },
      error: (err) => this.showToast(err.error?.detail || 'Failed to submit grades.', 'error'),
    });
  }

  approveReport(attemptId: string): void {
    this.mentorService.approveReport(attemptId).subscribe({
      next: () => {
        this.showToast('Growth Ring report approved and released to learner!');
        if (this.gradingData() && this.gradingData().attempt_id === attemptId) {
          this.gradingData.update((d: any) => d ? ({ ...d, report_status: 'APPROVED' }) : null);
        }
        const a = this.selectedAssessmentForResults();
        if (a) {
          this.openResultsAnalysis(a);
        }
      },
      error: (err) => this.showToast(err.error?.detail || 'Failed to approve report.', 'error'),
    });
  }

  openQuestionBank(): void {
    this.loadQuestionBank();
    this.showQuestionBankModal.set(true);
  }

  openQuestionBankForActiveAssessment(): void {
    const current = this.activeStudioAssessment();
    if (current) {
      this.targetAssessmentId = current.id;
    }
    this.openQuestionBank();
  }

  loadQuestionBank(): void {
    this.mentorService.getQuestionBank().subscribe({
      next: (data) => {
        this.questionBank.set(data || []);
        this.filterQuestionBank();
      },
      error: () => this.filterQuestionBank(),
    });
  }

  filterQuestionBank(): void {
    const q = this.questionBankSearch.toLowerCase().trim();
    const f = this.questionBankField;
    const t = this.questionBankType;

    const list = this.questionBank();
    const filtered = list.filter((item) => {
      const matchQ = !q || item.title.toLowerCase().includes(q) || item.content.toLowerCase().includes(q);
      const matchF = f === 'ALL' || item.field.toLowerCase() === f.toLowerCase();
      const matchT = t === 'ALL' || item.type.toUpperCase() === t.toUpperCase();
      return matchQ && matchF && matchT;
    });
    this.filteredQuestions.set(filtered);
  }

  attachQuestionFromBank(item: QuestionBankItem): void {
    if (!this.targetAssessmentId) {
      this.showToast('Please select or create an assessment first.', 'error');
      return;
    }

    this.mentorService.attachQuestionToAssessment(this.targetAssessmentId, {
      question_id: item.id,
      marks: 10,
    }).subscribe({
      next: () => {
        this.questionBankMessage.set(`Successfully staged "${item.title}" into assessment!`);
        setTimeout(() => this.questionBankMessage.set(null), 3000);
        this.loadAssessments();
        const current = this.activeStudioAssessment();
        if (current && current.id === this.targetAssessmentId) {
          this.loadStagedQuestions(current.id);
        }
      },
      error: (err) => {
        this.showToast(err.error?.detail || 'Failed to stage question.', 'error');
      },
    });
  }

  publishAssessment(a: AssessmentItem): void {
    if (confirm(`Publish assessment "${a.title}" to assigned learners?`)) {
      this.mentorService.publishAssessment(a.id).subscribe({
        next: () => {
          this.showToast(`Assessment "${a.title}" is now published.`);
          this.loadAssessments();
          if (this.activeStudioAssessment()?.id === a.id) {
            this.closeStudioModal();
          }
        },
        error: (err) => this.showToast(err.error?.detail || 'Failed to publish assessment.', 'error'),
      });
    }
  }

  openResultsAnalysis(a: AssessmentItem): void {
    this.selectedAssessmentForResults.set(a);
    this.resultsData.set(null);
    this.aiInsights.set(null);

    this.mentorService.getAssessmentResults(a.id).subscribe({
      next: (res) => this.resultsData.set(res),
      error: () => this.resultsData.set({
        total_attempts: 0,
        average_score: 0,
        pass_rate: 0,
        score_distribution: { '0-50': 0, '50-70': 0, '70-90': 0, '90-100': 0 },
        learners: [],
      }),
    });

    this.mentorService.getAssessmentAiInsights(a.id).subscribe({
      next: (insights) => this.aiInsights.set(insights),
      error: () => {},
    });
  }

  getSafeSvg(svg: string | null | undefined): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(svg || '<svg></svg>');
  }

  exportCsv(): void {
    const a = this.selectedAssessmentForResults();
    if (a) {
      this.mentorService.exportAssessmentCsv(a.id).subscribe({
        next: (csvData) => {
          const blob = new Blob([csvData], { type: 'text/csv' });
          const url = window.URL.createObjectURL(blob);
          const anchor = document.createElement('a');
          anchor.href = url;
          anchor.download = `assessment_${a.id}_results.csv`;
          anchor.click();
        },
      });
    }
  }

  showToast(message: string, type: 'success' | 'error' = 'success'): void {
    this.actionToast.set({ message, type });
    setTimeout(() => this.actionToast.set(null), 4000);
  }
}

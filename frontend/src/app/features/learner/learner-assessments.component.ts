import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ActiveAssessmentAttempt, LearnerService } from '../../core/services/learner.service';
import { AssessmentNote, NotesService } from '../../core/services/notes.service';

@Component({
  selector: 'app-learner-assessments',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      
      <!-- Normal View: Tabs for Assessments & Module Study Notes -->
      @if (!activeAttempt()) {
        <div class="space-y-6">
          
          <!-- Top Navigation Header & Tabs -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
            <div>
              <h1 class="text-2xl font-black text-slate-900 tracking-tight">Assessments & Study Center</h1>
              <p class="text-xs text-slate-500">
                Official examinations and mentor-authored study guides curated for your engineering track.
              </p>
            </div>

            <!-- View Switcher Tabs -->
            <div class="flex items-center gap-1.5 p-1 bg-slate-100 rounded-xl border border-slate-200">
              <button 
                type="button" 
                (click)="activeTab.set('assessments')"
                [ngClass]="activeTab() === 'assessments' ? 'bg-white text-slate-900 font-bold shadow-sm' : 'text-slate-500 hover:text-slate-800 font-medium'"
                class="px-3.5 py-1.5 rounded-lg text-xs transition flex items-center gap-2">
                <span>📋 Assigned Tests</span>
                <span class="px-1.5 py-0.2 rounded-full text-[10px] bg-sky-100 text-[#008FBB] font-bold">
                  {{ assignedList().length }}
                </span>
              </button>

              <button 
                type="button" 
                (click)="activeTab.set('notes')"
                [ngClass]="activeTab() === 'notes' ? 'bg-white text-slate-900 font-bold shadow-sm' : 'text-slate-500 hover:text-slate-800 font-medium'"
                class="px-3.5 py-1.5 rounded-lg text-xs transition flex items-center gap-2">
                <span>📖 Module Notes & Guides</span>
                <span class="px-1.5 py-0.2 rounded-full text-[10px] bg-amber-100 text-amber-800 font-bold">
                  {{ studyNotes().length }}
                </span>
              </button>
            </div>
          </div>

          <!-- TAB 1: Assigned Assessments -->
          @if (activeTab() === 'assessments') {
            @if (loadingAssessments()) {
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm animate-pulse space-y-4">
                  <div class="flex justify-between items-center">
                    <div class="h-4 bg-slate-200 rounded w-1/4"></div>
                    <div class="h-4 bg-slate-200 rounded w-16"></div>
                  </div>
                  <div class="h-6 bg-slate-200 rounded w-2/3"></div>
                  <div class="h-3 bg-slate-200 rounded w-full"></div>
                  <div class="h-10 bg-slate-200 rounded-xl w-full"></div>
                </div>
              </div>
            } @else {
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                @for (a of assignedList(); track a.id) {
                  <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4 hover:border-[#008FBB] transition flex flex-col justify-between">
                    <div class="space-y-3">
                      <div class="flex items-start justify-between gap-2">
                        <span class="px-2.5 py-0.5 rounded text-[10px] font-bold uppercase bg-sky-100 text-[#008FBB]">
                          {{ a.field }} &bull; Passing {{ a.passing_score }}%
                        </span>
                        <span class="text-xs font-mono font-bold text-slate-500 shrink-0">{{ a.duration_minutes }} Mins</span>
                      </div>
                      
                      <div>
                        <h3 class="text-base font-black text-slate-900">{{ a.title }}</h3>
                        <p class="text-xs text-slate-500 mt-1 line-clamp-2">
                          {{ a.instructions || 'Proctored assessment covering architecture, fundamentals, and real-world problem solving.' }}
                        </p>
                      </div>

                      <div class="flex items-center gap-4 text-[11px] text-slate-500 font-medium pt-1">
                        <span>📝 {{ a.questions_count || 'Multi-question' }} Questions</span>
                        @if (a.notes_count && a.notes_count > 0) {
                          <span class="text-[#008FBB] font-bold flex items-center gap-1">
                            📖 {{ a.notes_count }} Study Guide{{ a.notes_count > 1 ? 's' : '' }} Available
                          </span>
                        }
                      </div>
                    </div>

                    <div class="pt-4 border-t border-slate-100 flex items-center gap-3">
                      @if (a.notes_count && a.notes_count > 0) {
                        <button 
                          type="button" 
                          (click)="openNotesForAssessment(a.id, a.title)"
                          class="py-2.5 px-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold transition flex items-center gap-1.5">
                          <span>📖 Study Notes</span>
                        </button>
                      }
                      <button 
                        type="button" 
                        (click)="startTest(a.id)"
                        class="flex-1 py-2.5 px-4 rounded-xl bg-gradient-to-r from-[#008FBB] to-[#007499] hover:from-[#007499] hover:to-[#005e7c] text-white text-xs font-bold shadow-md transition text-center">
                        Start Timed Assessment &rarr;
                      </button>
                    </div>
                  </div>
                } @empty {
                  <div class="col-span-full p-12 text-center rounded-2xl bg-white border border-slate-200 space-y-2">
                    <span class="text-3xl block">📋</span>
                    <h4 class="text-sm font-bold text-slate-800">No Assessments Assigned</h4>
                    <p class="text-xs text-slate-500">You currently have no pending formal examinations scheduled for your cohort.</p>
                  </div>
                }
              </div>
            }
          }

          <!-- TAB 2: Module Study Guides & Notes -->
          @if (activeTab() === 'notes') {
            <div class="space-y-6">
              
              <!-- Search & Filters -->
              <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-sm flex flex-col md:flex-row gap-4 justify-between items-center">
                <div class="relative w-full md:w-96">
                  <span class="absolute left-3.5 top-2.5 text-slate-400 text-sm">🔍</span>
                  <input 
                    type="text" 
                    [(ngModel)]="noteSearchQuery" 
                    (ngModelChange)="applyNoteFilters()"
                    placeholder="Search by module title, concept, or keywords..."
                    class="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:ring-1 focus:ring-[#008FBB]" />
                </div>

                <!-- Field / Domain Filter Pills -->
                <div class="flex items-center gap-2 overflow-x-auto w-full md:w-auto pb-1 md:pb-0">
                  <button 
                    type="button" 
                    (click)="setFieldFilter('ALL')"
                    [ngClass]="selectedFieldFilter() === 'ALL' ? 'bg-[#008FBB] text-white font-bold' : 'bg-slate-100 text-slate-600 hover:bg-slate-200 font-medium'"
                    class="px-3 py-1.5 rounded-lg text-xs transition shrink-0">
                    All Modules
                  </button>
                  @for (f of availableFields(); track f) {
                    <button 
                      type="button" 
                      (click)="setFieldFilter(f)"
                      [ngClass]="selectedFieldFilter() === f ? 'bg-[#008FBB] text-white font-bold' : 'bg-slate-100 text-slate-600 hover:bg-slate-200 font-medium'"
                      class="px-3 py-1.5 rounded-lg text-xs transition shrink-0">
                      {{ f }}
                    </button>
                  }
                </div>
              </div>

              <!-- Notes Grid -->
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                @for (note of filteredNotes(); track note.id) {
                  <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-3 hover:border-[#008FBB] transition flex flex-col justify-between">
                    <div class="space-y-2">
                      <div class="flex items-center justify-between gap-2">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-sky-100 text-[#008FBB] truncate max-w-[180px]">
                          {{ note.module_name }}
                        </span>
                        <span class="text-[10px] font-mono font-bold text-slate-400">
                          ⏱️ {{ note.estimated_read_time_minutes }}m read
                        </span>
                      </div>

                      <h3 class="text-sm font-black text-slate-900 line-clamp-2 leading-snug">{{ note.title }}</h3>
                      
                      <p class="text-xs text-slate-500 line-clamp-3 leading-relaxed">
                        {{ note.summary || 'Essential technical reference, architecture principles, and assessment readiness checklist.' }}
                      </p>

                      <!-- Takeaways Preview Pills -->
                      @if (note.key_takeaways && note.key_takeaways.length > 0) {
                        <div class="pt-1 flex flex-wrap gap-1">
                          @for (t of note.key_takeaways.slice(0, 2); track t) {
                            <span class="text-[10px] px-2 py-0.5 rounded bg-slate-100 text-slate-600 truncate max-w-full">
                              &bull; {{ t }}
                            </span>
                          }
                          @if (note.key_takeaways.length > 2) {
                            <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-50 text-slate-400 font-bold">
                              +{{ note.key_takeaways.length - 2 }} more
                            </span>
                          }
                        </div>
                      }
                    </div>

                    <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                      <span class="text-[11px] font-medium text-slate-400">
                        👨‍🏫 {{ note.author_name || 'Mentor' }}
                      </span>
                      <button 
                        type="button" 
                        (click)="readNote(note)"
                        class="px-3 py-1.5 rounded-lg bg-sky-50 text-[#008FBB] hover:bg-sky-100 text-xs font-bold transition flex items-center gap-1">
                        <span>Read Guide &rarr;</span>
                      </button>
                    </div>
                  </div>
                } @empty {
                  <div class="col-span-full p-12 text-center rounded-2xl bg-white border border-slate-200 space-y-2">
                    <span class="text-3xl block">📚</span>
                    <h4 class="text-sm font-bold text-slate-800">No Study Guides Found</h4>
                    <p class="text-xs text-slate-500">Try adjusting your search terms or filter criteria.</p>
                  </div>
                }
              </div>

            </div>
          }

        </div>
      }

      <!-- FULL STUDY GUIDE READER MODAL -->
      @if (activeReaderNote()) {
        <div class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto animate-in fade-in">
          <div class="bg-white rounded-3xl border border-slate-200 shadow-2xl max-w-3xl w-full max-h-[90vh] flex flex-col overflow-hidden my-auto">
            
            <!-- Modal Header -->
            <div class="p-6 bg-slate-50 border-b border-slate-200 flex items-start justify-between gap-4">
              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-[#008FBB] text-white">
                    {{ activeReaderNote()?.module_name }}
                  </span>
                  @if (activeReaderNote()?.assessment_title) {
                    <span class="text-[11px] text-slate-500">
                      Module for: <span class="font-bold text-slate-700">{{ activeReaderNote()?.assessment_title }}</span>
                    </span>
                  }
                </div>
                <h2 class="text-xl font-black text-slate-900 mt-1">{{ activeReaderNote()?.title }}</h2>
                <div class="flex items-center gap-4 text-xs text-slate-500 pt-1">
                  <span>👨‍🏫 Authored by <strong class="text-slate-800">{{ activeReaderNote()?.author_name || 'Mentor' }}</strong></span>
                  <span>&bull;</span>
                  <span>⏱️ {{ activeReaderNote()?.estimated_read_time_minutes }} min read</span>
                </div>
              </div>

              <button 
                type="button" 
                (click)="activeReaderNote.set(null)"
                class="w-8 h-8 rounded-full bg-white hover:bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-sm shadow-sm transition">
                ✕
              </button>
            </div>

            <!-- Modal Scrollable Content -->
            <div class="p-6 overflow-y-auto space-y-6 text-slate-800 leading-relaxed text-sm">
              
              <!-- Executive Summary -->
              @if (activeReaderNote()?.summary) {
                <div class="p-4 rounded-2xl bg-sky-50 border-l-4 border-[#008FBB] space-y-1">
                  <h4 class="text-xs font-black uppercase tracking-wider text-[#008FBB]">Module Synopsis</h4>
                  <p class="text-xs text-slate-700 leading-relaxed">{{ activeReaderNote()?.summary }}</p>
                </div>
              }

              <!-- Key Takeaways -->
              @if (activeReaderNote()?.key_takeaways && activeReaderNote()!.key_takeaways.length > 0) {
                <div class="space-y-3">
                  <h4 class="text-xs font-black uppercase tracking-wider text-slate-400">Key Engineering Takeaways</h4>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    @for (item of activeReaderNote()!.key_takeaways; track item) {
                      <div class="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs flex items-start gap-2.5">
                        <span class="text-emerald-500 font-black mt-0.5">✓</span>
                        <span class="text-slate-800 font-medium">{{ item }}</span>
                      </div>
                    }
                  </div>
                </div>
              }

              <!-- Study Content & Technical Deep Dive -->
              <div class="space-y-3 pt-2 border-t border-slate-100">
                <h4 class="text-xs font-black uppercase tracking-wider text-slate-400">Technical Breakdown & Study Guide</h4>
                <div class="prose prose-sm max-w-none text-slate-800 whitespace-pre-wrap font-sans text-xs sm:text-sm bg-slate-50 p-5 rounded-2xl border border-slate-200 leading-relaxed overflow-x-auto">
                  {{ activeReaderNote()?.content }}
                </div>
              </div>

              <!-- Recommended Reading & Documentation Links -->
              @if (activeReaderNote()?.recommended_reading && activeReaderNote()!.recommended_reading.length > 0) {
                <div class="space-y-3 pt-2 border-t border-slate-100">
                  <h4 class="text-xs font-black uppercase tracking-wider text-slate-400">Recommended Reading & References</h4>
                  <div class="space-y-2">
                    @for (ref of activeReaderNote()!.recommended_reading; track ref.title) {
                      <a 
                        [href]="ref.url || '#'" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="p-3 rounded-xl bg-white border border-slate-200 hover:border-[#008FBB] flex items-center justify-between group transition">
                        <div>
                          <span class="text-xs font-bold text-[#008FBB] group-hover:underline block">{{ ref.title }}</span>
                          @if (ref.description) {
                            <span class="text-[11px] text-slate-500">{{ ref.description }}</span>
                          }
                        </div>
                        <span class="text-xs text-slate-400 group-hover:text-[#008FBB]">↗</span>
                      </a>
                    }
                  </div>
                </div>
              }

            </div>

            <!-- Modal Footer -->
            <div class="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-end gap-3">
              <button 
                type="button" 
                (click)="activeReaderNote.set(null)"
                class="px-5 py-2.5 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-white text-xs font-bold transition shadow-sm">
                Close Guide
              </button>
            </div>

          </div>
        </div>
      }

      <!-- Active Test Runner (Step 4 Requirement: Timed MCQ + Coding, Auto-submit, Tab-switch warning, Autosave, Question Palette) -->
      @if (activeAttempt()) {
        <div class="space-y-4 animate-in fade-in">
          
          <!-- Test Runner Bar -->
          <div class="sticky top-16 z-30 p-4 rounded-2xl bg-white border border-slate-200 shadow-md flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div>
                <h2 class="text-sm font-black text-slate-900 leading-tight">{{ activeAttempt()?.title }}</h2>
                <span class="text-[10px] text-slate-400">Question {{ currentQuestionIndex() + 1 }} of {{ activeAttempt()?.questions?.length }}</span>
              </div>

              <!-- Autosave Status Indicator -->
              <div class="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 text-[10px] font-bold">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>{{ autosaveStatus() }}</span>
              </div>
            </div>

            <!-- Timer & Tab Warning -->
            <div class="flex items-center gap-3">
              @if (tabSwitches() > 0) {
                <div class="px-2.5 py-1 rounded-full bg-rose-100 text-[#D7182A] text-[10px] font-bold border border-rose-300">
                  Tab Switches: {{ tabSwitches() }}
                </div>
              }

              <!-- Countdown Timer -->
              <div class="px-3 py-1.5 rounded-xl bg-slate-950 text-white font-mono font-black text-xs flex items-center gap-2 shadow-inner">
                <span class="w-2 h-2 rounded-full bg-[#D7182A] animate-ping"></span>
                <span>{{ formattedRemainingTime() }}</span>
              </div>

              <button 
                type="button" 
                (click)="finishTest(false)"
                class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-sm transition">
                Submit Test
              </button>
            </div>
          </div>

          <!-- Main Test Workspace: Left Question Palette & Right Content -->
          <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
            
            <!-- Question Palette (Step 4 Requirement: answered / flagged / unvisited) -->
            <div class="lg:col-span-1 p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400">Question Palette</h3>
              
              <div class="grid grid-cols-4 gap-2">
                @for (q of activeAttempt()?.questions; track q.id; let idx = $index) {
                  <button 
                    type="button" 
                    (click)="jumpToQuestion(idx)"
                    class="h-9 rounded-xl font-mono font-bold text-xs flex items-center justify-center border transition"
                    [ngClass]="{
                      'ring-2 ring-[#008FBB] ring-offset-2': idx === currentQuestionIndex(),
                      'bg-emerald-500 text-white border-emerald-600': isAnswered(q.id),
                      'bg-amber-400 text-slate-950 border-amber-500': isFlagged(q.id),
                      'bg-slate-100 text-slate-600 border-slate-200': !isAnswered(q.id) && !isFlagged(q.id)
                    }">
                    {{ idx + 1 }}
                  </button>
                }
              </div>

              <!-- Palette Legend -->
              <div class="pt-3 border-t border-slate-100 space-y-1.5 text-[10px] text-slate-500">
                <div class="flex items-center gap-2">
                  <span class="w-3 h-3 rounded bg-emerald-500"></span>
                  <span>Answered (Autosaved)</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-3 h-3 rounded bg-amber-400"></span>
                  <span>Flagged for Review</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-3 h-3 rounded bg-slate-200"></span>
                  <span>Unvisited</span>
                </div>
              </div>

              <div class="pt-2">
                <button 
                  type="button" 
                  (click)="toggleFlagCurrent()"
                  class="w-full py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-bold text-slate-700 transition">
                  {{ isFlagged(currentQuestion()?.id || '') ? 'Unflag Question' : '🚩 Flag for Review' }}
                </button>
              </div>
            </div>

            <!-- Question Execution Area (MCQ or Coding) -->
            <div class="lg:col-span-3 p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-6">
              
              <!-- Question Header -->
              <div class="space-y-2 pb-4 border-b border-slate-100">
                <div class="flex items-center justify-between">
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider"
                    [ngClass]="getQuestionType(currentQuestion()) === 'CODING' || getQuestionType(currentQuestion()) === 'SQL' ? 'bg-purple-100 text-purple-700' : 'bg-sky-100 text-[#008FBB]'">
                    {{ getQuestionType(currentQuestion()) }}
                  </span>
                  <span class="text-xs font-mono font-bold text-slate-400">{{ currentQuestion()?.marks }} Marks</span>
                </div>
                <h3 class="text-base font-bold text-slate-900">{{ currentQuestion()?.title }}</h3>
                <p class="text-xs text-slate-600 whitespace-pre-wrap leading-relaxed">{{ getQuestionText(currentQuestion()) }}</p>
              </div>

              <!-- MCQ Options Choice -->
              @if (getQuestionType(currentQuestion()) === 'MCQ' || getQuestionType(currentQuestion()) === 'LIKERT') {
                <div class="space-y-2.5">
                  @for (opt of currentQuestion()?.options; track opt.id) {
                    <label 
                      class="flex items-center gap-3 p-3.5 rounded-xl border text-xs cursor-pointer transition"
                      [ngClass]="isSelectedOption(opt.id) ? 'bg-sky-50 border-[#008FBB] text-[#008FBB] font-bold' : 'bg-slate-50 border-slate-200 text-slate-800'">
                      <input 
                        type="radio" 
                        [name]="currentQuestion()?.id || 'mcq'"
                        [checked]="isSelectedOption(opt.id)"
                        (change)="selectOption(opt.id)"
                        class="text-[#008FBB] focus:ring-[#008FBB]" />
                      <span>{{ opt.text || opt.option_text || opt.title || opt.label }}</span>
                    </label>
                  }
                </div>
              }

              <!-- Coding / SQL Editor Area -->
              @if (getQuestionType(currentQuestion()) === 'CODING' || getQuestionType(currentQuestion()) === 'SQL') {
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-400 uppercase">
                      {{ getQuestionType(currentQuestion()) === 'SQL' ? 'SQL Query Execution' : 'Code Implementation (Python / JS)' }}
                    </span>
                    <span class="text-[10px] text-emerald-500 font-bold">&bull; Isolated Sandboxed Execution</span>
                  </div>
                  <textarea 
                    [(ngModel)]="codingSolution" 
                    (ngModelChange)="onCodeChanged()"
                    rows="10" 
                    [placeholder]="getQuestionType(currentQuestion()) === 'SQL' ? 'SELECT * FROM table_name WHERE ...' : 'def solve():\n    pass'"
                    class="w-full font-mono text-xs p-4 bg-slate-950 text-slate-100 border border-slate-800 rounded-xl focus:outline-none focus:ring-1 focus:ring-[#008FBB]"></textarea>
                </div>
              }

              <!-- Written / Subjective / Scenario / Communication Area -->
              @if (getQuestionType(currentQuestion()) === 'WRITTEN' || getQuestionType(currentQuestion()) === 'SHORT_ANSWER' || getQuestionType(currentQuestion()) === 'SCENARIO' || getQuestionType(currentQuestion()) === 'COMMUNICATION') {
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-400 uppercase">Written Response</span>
                    <span class="text-[10px] text-[#008FBB] font-bold">&bull; Mentor Reviewed</span>
                  </div>
                  <textarea 
                    [(ngModel)]="textSolution" 
                    (ngModelChange)="onTextChanged()"
                    rows="8" 
                    placeholder="Enter your detailed response or explanation here..."
                    class="w-full text-xs p-4 bg-slate-50 text-slate-900 border border-slate-300 rounded-xl focus:outline-none focus:ring-1 focus:ring-[#008FBB] leading-relaxed"></textarea>
                </div>
              }

              <!-- File Upload Area -->
              @if (getQuestionType(currentQuestion()) === 'FILE_UPLOAD') {
                <div class="space-y-3 p-4 rounded-xl border border-dashed border-slate-300 bg-slate-50">
                  <span class="text-xs font-bold text-slate-700 block">Deliverable Document / Asset URL</span>
                  <input 
                    type="text" 
                    [(ngModel)]="fileUrl" 
                    (ngModelChange)="onFileChanged()"
                    placeholder="https://drive.google.com/... or internal storage URL"
                    class="w-full text-xs px-3 py-2 bg-white border border-slate-300 rounded-xl focus:outline-none focus:ring-1 focus:ring-[#008FBB]" />
                  <input 
                    type="text" 
                    [(ngModel)]="fileName" 
                    (ngModelChange)="onFileChanged()"
                    placeholder="Document Name (e.g., architecture_v1.pdf)"
                    class="w-full text-xs px-3 py-2 bg-white border border-slate-300 rounded-xl focus:outline-none focus:ring-1 focus:ring-[#008FBB]" />
                </div>
              }

              <!-- Navigation Footer -->
              <div class="flex items-center justify-between pt-4 border-t border-slate-100">
                <button 
                  type="button" 
                  [disabled]="currentQuestionIndex() === 0"
                  (click)="prevQuestion()"
                  class="px-4 py-2 rounded-xl bg-slate-100 disabled:opacity-40 text-xs font-bold text-slate-700">
                  &larr; Previous Question
                </button>

                <button 
                  type="button" 
                  [disabled]="currentQuestionIndex() === (activeAttempt()?.questions?.length || 1) - 1"
                  (click)="nextQuestion()"
                  class="px-4 py-2 rounded-xl bg-[#008FBB] disabled:opacity-40 text-xs font-bold text-white hover:bg-[#007499]">
                  Next Question &rarr;
                </button>
              </div>

            </div>
          </div>

        </div>
      }

    </div>
  `,
})
export class LearnerAssessmentsComponent implements OnInit, OnDestroy {
  private readonly learnerService = inject(LearnerService);
  private readonly notesService = inject(NotesService);
  private readonly router = inject(Router);

  readonly assignedList = signal<any[]>([]);
  readonly activeTab = signal<'assessments' | 'notes'>('assessments');
  readonly loadingAssessments = signal<boolean>(true);

  // Study Notes state
  readonly studyNotes = signal<AssessmentNote[]>([]);
  readonly filteredNotes = signal<AssessmentNote[]>([]);
  readonly availableFields = signal<string[]>([]);
  readonly selectedFieldFilter = signal<string>('ALL');
  readonly activeReaderNote = signal<AssessmentNote | null>(null);
  noteSearchQuery = '';

  // Active attempt state
  readonly activeAttempt = signal<ActiveAssessmentAttempt | null>(null);
  readonly currentQuestionIndex = signal<number>(0);
  readonly remainingSeconds = signal<number>(3600);
  readonly tabSwitches = signal<number>(0);
  readonly autosaveStatus = signal<string>('Autosaved');

  readonly answers = signal<Record<string, any>>({});
  readonly flagged = signal<Set<string>>(new Set());
  codingSolution = '';
  textSolution = '';
  fileUrl = '';
  fileName = '';

  private timerInterval: any = null;
  private tabListener: any = null;

  ngOnInit(): void {
    this.loadAssessments();
    this.loadNotes();

    // Tab switch listener (Step 4 proctoring requirement)
    this.tabListener = () => {
      if (document.hidden && this.activeAttempt()) {
        this.tabSwitches.update((v) => v + 1);
      }
    };
    document.addEventListener('visibilitychange', this.tabListener);
  }

  ngOnDestroy(): void {
    if (this.timerInterval) clearInterval(this.timerInterval);
    if (this.tabListener) document.removeEventListener('visibilitychange', this.tabListener);
  }

  loadAssessments(): void {
    this.learnerService.getAssessments().subscribe({
      next: (list) => {
        this.assignedList.set(list || []);
        this.loadingAssessments.set(false);
      },
      error: () => {
        this.loadingAssessments.set(false);
      },
    });
  }

  loadNotes(): void {
    this.notesService.getLearnerNotes().subscribe({
      next: (notes) => {
        this.studyNotes.set(notes || []);
        
        // Extract distinct fields
        const fields = Array.from(new Set(notes.map((n) => n.assessment_field).filter((f): f is string => !!f)));
        this.availableFields.set(fields);
        this.applyNoteFilters();
      },
      error: () => {},
    });
  }

  setFieldFilter(field: string): void {
    this.selectedFieldFilter.set(field);
    this.applyNoteFilters();
  }

  applyNoteFilters(): void {
    const q = this.noteSearchQuery.trim().toLowerCase();
    const f = this.selectedFieldFilter();

    let result = this.studyNotes();
    if (f !== 'ALL') {
      result = result.filter((n) => n.assessment_field === f);
    }

    if (q) {
      result = result.filter(
        (n) =>
          n.title.toLowerCase().includes(q) ||
          n.module_name.toLowerCase().includes(q) ||
          (n.summary && n.summary.toLowerCase().includes(q)) ||
          (n.assessment_title && n.assessment_title.toLowerCase().includes(q)) ||
          (n.key_takeaways && n.key_takeaways.some((t) => t.toLowerCase().includes(q)))
      );
    }

    this.filteredNotes.set(result);
  }

  openNotesForAssessment(assessmentId: string, title?: string): void {
    this.notesService.getLearnerAssessmentNotes(assessmentId).subscribe({
      next: (notes) => {
        if (notes && notes.length > 0) {
          this.readNote(notes[0]);
        } else {
          this.activeTab.set('notes');
          if (title) {
            this.noteSearchQuery = title;
            this.applyNoteFilters();
          }
        }
      },
      error: () => {
        this.activeTab.set('notes');
      },
    });
  }

  readNote(note: AssessmentNote): void {
    this.activeReaderNote.set(note);
  }

  currentQuestion(): any {
    const list = this.activeAttempt()?.questions || [];
    return list[this.currentQuestionIndex()] || null;
  }

  startTest(assessmentId: string): void {
    this.learnerService.startAssessment(assessmentId).subscribe({
      next: (attempt) => this.initAttempt(attempt),
      error: (err) => {
        alert(err?.error?.detail || 'Unable to start assessment. Please ensure it is published and within the active window.');
      },
    });
  }

  private initAttempt(attempt: ActiveAssessmentAttempt): void {
    this.activeAttempt.set(attempt);
    this.remainingSeconds.set(attempt.remaining_seconds || attempt.duration_minutes * 60);
    this.currentQuestionIndex.set(0);
    this.answers.set(attempt.existing_answers || {});
    this.jumpToQuestion(0);

    this.timerInterval = setInterval(() => {
      this.remainingSeconds.update((s) => {
        if (s <= 1) {
          clearInterval(this.timerInterval);
          this.finishTest(true);
          return 0;
        }
        return s - 1;
      });
    }, 1000);
  }

  formattedRemainingTime(): string {
    const s = this.remainingSeconds();
    const mins = Math.floor(s / 60);
    const secs = s % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  getQuestionType(q: any): string {
    const rawType = (q?.type || q?.question_type || 'MCQ').toUpperCase();
    if (rawType.includes('CODING')) return 'CODING';
    if (rawType.includes('SQL')) return 'SQL';
    if (rawType.includes('LIKERT')) return 'LIKERT';
    if (rawType.includes('SHORT_ANSWER') || rawType.includes('WRITTEN')) return 'WRITTEN';
    if (rawType.includes('FILE_UPLOAD')) return 'FILE_UPLOAD';
    return 'MCQ';
  }

  getQuestionText(q: any): string {
    return q?.text || q?.question_text || q?.content || q?.statement || q?.description || '';
  }

  jumpToQuestion(idx: number): void {
    this.currentQuestionIndex.set(idx);
    const q = this.currentQuestion();
    if (q) {
      const existing = this.answers()[q.id] || {};
      const qType = this.getQuestionType(q);
      if (qType === 'CODING' || qType === 'SQL') {
        this.codingSolution = existing.source_code || '';
      } else if (qType === 'WRITTEN' || qType === 'SHORT_ANSWER' || qType === 'SCENARIO' || qType === 'COMMUNICATION') {
        this.textSolution = existing.text_response || '';
      } else if (qType === 'FILE_UPLOAD') {
        this.fileUrl = existing.file_url || '';
        this.fileName = existing.file_name || '';
      }
    }
  }

  onCodeChanged(): void {
    const q = this.currentQuestion();
    if (!q) return;
    this.answers.update((ans) => ({
      ...ans,
      [q.id]: { ...(ans[q.id] || {}), source_code: this.codingSolution },
    }));
    this.triggerAutosave();
  }

  onTextChanged(): void {
    const q = this.currentQuestion();
    if (!q) return;
    this.answers.update((ans) => ({
      ...ans,
      [q.id]: { ...(ans[q.id] || {}), text_response: this.textSolution },
    }));
    this.triggerAutosave();
  }

  onFileChanged(): void {
    const q = this.currentQuestion();
    if (!q) return;
    this.answers.update((ans) => ({
      ...ans,
      [q.id]: { ...(ans[q.id] || {}), file_url: this.fileUrl, file_name: this.fileName },
    }));
    this.triggerAutosave();
  }

  nextQuestion(): void {
    const total = this.activeAttempt()?.questions?.length || 1;
    if (this.currentQuestionIndex() < total - 1) {
      this.jumpToQuestion(this.currentQuestionIndex() + 1);
    }
  }

  prevQuestion(): void {
    if (this.currentQuestionIndex() > 0) {
      this.jumpToQuestion(this.currentQuestionIndex() - 1);
    }
  }

  selectOption(optId: string): void {
    const q = this.currentQuestion();
    if (!q) return;
    this.answers.update((ans) => ({ ...ans, [q.id]: { ...(ans[q.id] || {}), selected_option_id: optId } }));
    this.triggerAutosave();
  }

  isSelectedOption(optId: string): boolean {
    const q = this.currentQuestion();
    if (!q) return false;
    return this.answers()[q.id]?.selected_option_id === optId;
  }

  isAnswered(qid: string): boolean {
    const a = this.answers()[qid];
    if (!a) return false;
    return !!(a.selected_option_id || (a.source_code && a.source_code.trim()) || (a.text_response && a.text_response.trim()) || a.file_url);
  }

  isFlagged(qid: string): boolean {
    return this.flagged().has(qid);
  }

  toggleFlagCurrent(): void {
    const q = this.currentQuestion();
    if (!q) return;
    const f = new Set(this.flagged());
    if (f.has(q.id)) {
      f.delete(q.id);
    } else {
      f.add(q.id);
    }
    this.flagged.set(f);
  }

  triggerAutosave(): void {
    const q = this.currentQuestion();
    const att = this.activeAttempt();
    if (q && att) {
      const payload = this.answers()[q.id] || {};
      this.autosaveStatus.set('Saving...');
      this.learnerService.saveAnswer(att.attempt_id, q.id, payload).subscribe({
        next: () => this.autosaveStatus.set('Autosaved'),
        error: () => this.autosaveStatus.set('Saved locally'),
      });
    }
  }

  finishTest(auto: boolean = false): void {
    const att = this.activeAttempt();
    if (!att) return;
    if (!auto && !confirm('Are you sure you want to finalize and submit your assessment?')) {
      return;
    }
    this.learnerService.submitAssessment(att.attempt_id, this.tabSwitches()).subscribe({
      next: () => {
        alert(auto ? 'Time expired. Assessment automatically submitted!' : 'Assessment submitted successfully.');
        this.activeAttempt.set(null);
        this.router.navigate(['/learner/results']);
      },
      error: (err) => {
        alert(err?.error?.detail || 'Failed to submit assessment.');
      },
    });
  }
}

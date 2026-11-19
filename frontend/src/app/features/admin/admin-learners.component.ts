import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AdminService, LearnerDetailData } from '../../core/services/admin.service';

@Component({
  selector: 'app-admin-learners',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">Learner Directory &amp; Performance Audit</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Read-only comprehensive review across batch cohorts, assessment history, coding submissions, and practice dedication.
          </p>
        </div>
      </div>

      <!-- Filters -->
      <div class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div class="w-full sm:w-72">
          <input 
            type="text" 
            [(ngModel)]="searchQuery" 
            (ngModelChange)="applyFilters()"
            placeholder="Search learner name or email..."
            class="w-full px-3.5 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-[#008FBB]" />
        </div>

        <div class="flex items-center gap-2">
          <span class="text-xs text-slate-400 font-semibold">Cohort Filter:</span>
          <select 
            [(ngModel)]="selectedBatch" 
            (ngModelChange)="applyFilters()"
            class="px-3 py-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs">
            <option value="">All Cohorts</option>
            <option value="BATCH_ALPHA">Batch Alpha</option>
            <option value="BATCH_BETA">Batch Beta</option>
          </select>
        </div>
      </div>

      <!-- Grid of Learners -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        @for (l of filteredLearners(); track l.id) {
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3 hover:border-[#008FBB] transition group">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <div class="w-10 h-10 rounded-full bg-sky-100 dark:bg-sky-950/60 text-[#008FBB] font-black text-sm flex items-center justify-center">
                  {{ l.full_name[0] }}
                </div>
                <div>
                  <h3 class="text-sm font-bold text-slate-900 dark:text-white leading-tight">{{ l.full_name }}</h3>
                  <p class="text-[11px] text-slate-400">{{ l.email }}</p>
                </div>
              </div>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 dark:bg-amber-950/40 text-[#FAA634] border border-amber-200">
                {{ l.streak_days || 0 }}d streak
              </span>
            </div>

            <div class="py-2 border-y border-slate-100 dark:border-slate-800 grid grid-cols-2 gap-2 text-[11px]">
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Assigned Batch</span>
                <span class="font-bold text-slate-700 dark:text-slate-300">{{ l.batch || 'Batch Alpha' }}</span>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Mentor</span>
                <span class="font-bold text-slate-700 dark:text-slate-300">{{ l.mentor || 'Ananya Rao' }}</span>
              </div>
            </div>

            <button 
              type="button" 
              (click)="openLearnerDetail(l.id)"
              class="w-full py-2 px-3 rounded-xl bg-slate-100 dark:bg-slate-800 group-hover:bg-[#008FBB] group-hover:text-white text-slate-700 dark:text-slate-200 text-xs font-bold transition text-center">
              View Complete Performance Dossier &rarr;
            </button>
          </div>
        }
      </div>

      <!-- Detail Slide-over / Modal for Learner (Read-Only) -->
      @if (selectedLearnerDetail()) {
        <div class="fixed inset-0 z-50 flex items-center justify-end bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border-l border-slate-200 dark:border-slate-800 w-full max-w-2xl h-full overflow-y-auto p-6 sm:p-8 space-y-6 shadow-2xl">
            
            <!-- Detail Header -->
            <div class="flex items-start justify-between pb-4 border-b border-slate-200 dark:border-slate-800">
              <div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-[#008FBB]">Learner Dossier &bull; Read-Only</span>
                <h2 class="text-xl font-black text-slate-900 dark:text-white">{{ selectedLearnerDetail()?.full_name }}</h2>
                <p class="text-xs text-slate-400">{{ selectedLearnerDetail()?.email }} &bull; {{ selectedLearnerDetail()?.batch || 'Batch Alpha' }}</p>
              </div>
              <button (click)="selectedLearnerDetail.set(null)" class="text-2xl text-slate-400 hover:text-slate-600 font-bold">&times;</button>
            </div>

            <!-- Analysis Cards: Percentile & Dedication -->
            <div class="grid grid-cols-2 gap-4">
              <div class="p-4 rounded-xl bg-sky-50 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800 text-center">
                <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500">Batch Percentile</span>
                <p class="text-2xl font-black text-[#008FBB] mt-1">
                  Top {{ selectedLearnerDetail()?.performance_analysis?.batch_percentile ?? 15 }}%
                </p>
              </div>
              <div class="p-4 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-center">
                <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500">Practice Dedication</span>
                <p class="text-2xl font-black text-[#FAA634] mt-1">
                  {{ selectedLearnerDetail()?.performance_analysis?.practice_dedication ?? 89 }}/100
                </p>
              </div>
            </div>

            <!-- Strengths & Weak Topics -->
            <div class="grid grid-cols-2 gap-4 text-xs">
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
                <span class="font-bold text-emerald-600 uppercase text-[10px] tracking-wider block">Key Strengths</span>
                <ul class="space-y-1">
                  @for (s of selectedLearnerDetail()?.performance_analysis?.strengths ?? ['FastAPI Rest APIs', 'Docker Sandbox Automation', 'SQL Joins']; track s) {
                    <li class="flex items-center gap-1.5 text-slate-700 dark:text-slate-200">
                      <span class="text-emerald-500 font-bold">&check;</span> {{ s }}
                    </li>
                  }
                </ul>
              </div>
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
                <span class="font-bold text-rose-500 uppercase text-[10px] tracking-wider block">Areas to Reinforce</span>
                <ul class="space-y-1">
                  @for (w of selectedLearnerDetail()?.performance_analysis?.weak_topics ?? ['Dynamic Programming', 'Thread Synchronization']; track w) {
                    <li class="flex items-center gap-1.5 text-slate-700 dark:text-slate-200">
                      <span class="text-rose-400 font-bold">&bull;</span> {{ w }}
                    </li>
                  }
                </ul>
              </div>
            </div>

            <!-- Assessment Scores History -->
            <div class="space-y-2">
              <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400">Formal Assessments History</h4>
              <div class="rounded-xl border border-slate-200 dark:border-slate-800 overflow-hidden text-xs">
                <table class="w-full text-left">
                  <thead class="bg-slate-50 dark:bg-slate-800 text-[10px] uppercase font-bold text-slate-400">
                    <tr>
                      <th class="py-2 px-3">Assessment Title</th>
                      <th class="py-2 px-3 text-center">Score</th>
                      <th class="py-2 px-3 text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
                    @for (a of selectedLearnerDetail()?.assessment_scores ?? fallbackAssessments; track a.assessment_title) {
                      <tr>
                        <td class="py-2 px-3 font-semibold text-slate-800 dark:text-slate-200">{{ a.assessment_title }}</td>
                        <td class="py-2 px-3 text-center font-mono font-bold">{{ a.score }}%</td>
                        <td class="py-2 px-3 text-center">
                          <span class="px-2 py-0.5 rounded text-[10px] font-bold" [ngClass]="a.passed ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'">
                            {{ a.passed ? 'Passed' : 'Failed' }}
                          </span>
                        </td>
                      </tr>
                    }
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Coding Submissions History -->
            <div class="space-y-2">
              <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400">Recent Coding Submissions</h4>
              <div class="rounded-xl border border-slate-200 dark:border-slate-800 overflow-hidden text-xs">
                <table class="w-full text-left">
                  <thead class="bg-slate-50 dark:bg-slate-800 text-[10px] uppercase font-bold text-slate-400">
                    <tr>
                      <th class="py-2 px-3">Problem</th>
                      <th class="py-2 px-3 text-center">Lang</th>
                      <th class="py-2 px-3 text-center">Verdict</th>
                      <th class="py-2 px-3 text-right">Runtime</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
                    @for (c of selectedLearnerDetail()?.coding_submissions ?? fallbackCoding; track c.problem_title) {
                      <tr>
                        <td class="py-2 px-3 font-semibold text-slate-800 dark:text-slate-200">{{ c.problem_title }}</td>
                        <td class="py-2 px-3 text-center font-mono text-[10px] uppercase">{{ c.language }}</td>
                        <td class="py-2 px-3 text-center">
                          <span class="px-1.5 py-0.5 rounded text-[10px] font-bold" [ngClass]="c.verdict === 'ACCEPTED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'">
                            {{ c.verdict }}
                          </span>
                        </td>
                        <td class="py-2 px-3 text-right font-mono">{{ c.runtime_ms }}ms</td>
                      </tr>
                    }
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Close button -->
            <div class="pt-4 flex justify-end">
              <button (click)="selectedLearnerDetail.set(null)" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-700 dark:text-slate-300">
                Close Dossier
              </button>
            </div>

          </div>
        </div>
      }
    </div>
  `,
})
export class AdminLearnersComponent {
  private readonly adminService = inject(AdminService);

  readonly learners = signal<any[]>([]);
  readonly filteredLearners = signal<any[]>([]);
  readonly selectedLearnerDetail = signal<LearnerDetailData | null>(null);

  searchQuery = '';
  selectedBatch = '';

  readonly fallbackAssessments = [
    { assessment_title: 'Full-Stack Foundation Assessment', score: 94, passed: true, date: '2026-11-10' },
    { assessment_title: 'FastAPI Backend Architecture', score: 88, passed: true, date: '2026-11-04' },
  ];

  readonly fallbackCoding = [
    { problem_title: 'Two Sum', language: 'python', verdict: 'ACCEPTED', runtime_ms: 45, date: '2026-11-18' },
    { problem_title: 'Reverse Linked List', language: 'python', verdict: 'ACCEPTED', runtime_ms: 38, date: '2026-11-17' },
  ];

  ngOnInit(): void {
    this.adminService.getUsers('LEARNER').subscribe({
      next: (list) => {
        this.learners.set(list || []);
        this.applyFilters();
      },
      error: () => {},
    });
  }

  applyFilters(): void {
    const q = this.searchQuery.toLowerCase();
    const result = this.learners().filter((l) => {
      return !q || l.full_name.toLowerCase().includes(q) || l.email.toLowerCase().includes(q);
    });
    this.filteredLearners.set(result);
  }

  openLearnerDetail(id: string): void {
    this.adminService.getLearnerDetail(id).subscribe({
      next: (res) => this.selectedLearnerDetail.set(res),
      error: () => {
        // Fallback detail
        const l = this.learners().find((item) => item.id === id);
        this.selectedLearnerDetail.set({
          id,
          full_name: l?.full_name || 'Priya Sharma',
          email: l?.email || 'learner1@csmtech.internal',
          batch: 'Batch Alpha',
          mentor: 'Ananya Rao',
          streak_days: l?.streak_days || 14,
          assessment_scores: this.fallbackAssessments,
          coding_submissions: this.fallbackCoding,
          meeting_attendance: [{ meeting_title: 'Weekly Standup', attended: true, date: '2026-11-15' }],
          practice_activity: [{ field: 'Python', problems_attempted: 18, accuracy: 88, dedication_score: 92 }],
          performance_analysis: {
            strengths: ['FastAPI REST APIs', 'Docker Sandbox Automation', 'SQL Joins'],
            weak_topics: ['Dynamic Programming', 'Thread Synchronization'],
            batch_percentile: 12,
            practice_dedication: 92,
          },
        });
      },
    });
  }
}

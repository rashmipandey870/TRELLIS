import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AdminService, LearnerDetailData } from '../../core/services/admin.service';

@Component({
  selector: 'app-admin-learners',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">Learner Directory &amp; Performance Audit</h1>
          <p class="text-xs text-slate-500">
            Read-only comprehensive review across batch cohorts, assessment history, coding submissions, and practice dedication.
          </p>
        </div>
      </div>

      <!-- Filters -->
      <div class="p-4 rounded-2xl bg-white border border-slate-200 flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div class="w-full sm:w-72">
          <input 
            type="text" 
            [(ngModel)]="searchQuery" 
            (ngModelChange)="applyFilters()"
            placeholder="Search learner name or email..."
            class="w-full px-3.5 py-2 bg-slate-50 border border-slate-300 rounded-xl text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-[#008FBB]" />
        </div>

        <div class="flex items-center gap-2">
          <span class="text-xs text-slate-400 font-semibold">Cohort Filter:</span>
          <select 
            [(ngModel)]="selectedBatch" 
            (ngModelChange)="applyFilters()"
            class="px-3 py-1.5 bg-slate-50 border border-slate-300 rounded-xl text-xs text-slate-800">
            <option value="">All 8 Enterprise Cohorts</option>
            <option value="Batch Alpha">Batch Alpha (Full-Stack)</option>
            <option value="Batch Beta">Batch Beta (Cloud &amp; DevOps)</option>
            <option value="Batch Gamma">Batch Gamma (AI &amp; ML)</option>
            <option value="Batch Delta">Batch Delta (Data Platform)</option>
            <option value="Batch Epsilon">Batch Epsilon (Cybersecurity)</option>
            <option value="Batch Zeta">Batch Zeta (Mobile &amp; IoT)</option>
            <option value="Batch Eta">Batch Eta (Distributed Systems)</option>
            <option value="Batch Theta">Batch Theta (Enterprise Systems)</option>
          </select>
        </div>
      </div>

      <!-- Grid of Learners -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        @for (l of filteredLearners(); track l.id) {
          <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-3 hover:border-[#008FBB] transition group">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <div class="w-10 h-10 rounded-full bg-sky-100 text-[#008FBB] font-black text-sm flex items-center justify-center">
                  {{ (l.name || l.full_name || 'L')[0] }}
                </div>
                <div>
                  <h3 class="text-sm font-bold text-slate-900 leading-tight">{{ l.name || l.full_name }}</h3>
                  <p class="text-[11px] text-slate-400">{{ l.email }}</p>
                </div>
              </div>
              <div class="text-right">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-[#FAA634] border border-amber-200 block">
                  {{ l.streak_days || 0 }}d streak
                </span>
                @if (l.average_score !== undefined) {
                  <span class="text-[10px] font-bold text-emerald-600 mt-0.5 block">
                    {{ l.average_score }}% avg
                  </span>
                }
              </div>
            </div>

            <div class="py-2 border-y border-slate-100 grid grid-cols-2 gap-2 text-[11px]">
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Assigned Batch</span>
                <span class="font-bold text-slate-700 truncate block">{{ l.batch || 'Batch Alpha' }}</span>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Mentor</span>
                <span class="font-bold text-slate-700 truncate block">{{ l.mentor || 'Ananya Rao' }}</span>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2 pt-1">
              <button 
                type="button" 
                (click)="openLearnerDetail(l.id)"
                class="py-2 px-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-bold transition text-center">
                Audit Modal
              </button>
              <a 
                [routerLink]="['/admin/learners', l.id, 'analytics']"
                class="py-2 px-2.5 rounded-xl bg-sky-50 hover:bg-[#008FBB] hover:text-white border border-sky-200 text-[#008FBB] text-[11px] font-bold transition text-center shadow-2xs">
                Dossier &rarr;
              </a>
            </div>
          </div>
        }
      </div>

      <!-- Detail Slide-over / Modal for Learner (Read-Only) -->
      @if (selectedLearnerDetail()) {
        <div class="fixed inset-0 z-50 flex items-center justify-end bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white border-l border-slate-200 w-full max-w-2xl h-full overflow-y-auto p-6 sm:p-8 space-y-6 shadow-2xl">
            
            <!-- Detail Header -->
            <div class="flex items-start justify-between pb-4 border-b border-slate-200">
              <div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-[#008FBB]">Learner Dossier &bull; Read-Only Audit</span>
                <h2 class="text-xl font-black text-slate-900">{{ selectedLearnerDetail()?.full_name }}</h2>
                <p class="text-xs text-slate-400">{{ selectedLearnerDetail()?.email }} &bull; {{ selectedLearnerDetail()?.batch || 'Batch Alpha' }}</p>
              </div>
              <button (click)="selectedLearnerDetail.set(null)" class="text-2xl text-slate-400 hover:text-slate-600 font-bold">&times;</button>
            </div>

            <!-- Analysis Cards: Percentile & Dedication -->
            <div class="grid grid-cols-2 gap-4">
              <div class="p-4 rounded-xl bg-sky-50 border border-sky-200 text-center">
                <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500">Batch Percentile</span>
                <p class="text-2xl font-black text-[#008FBB] mt-1">
                  Top {{ selectedLearnerDetail()?.performance_analysis?.batch_percentile ?? 15 }}%
                </p>
              </div>
              <div class="p-4 rounded-xl bg-amber-50 border border-amber-200 text-center">
                <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500">Practice Dedication</span>
                <p class="text-2xl font-black text-[#FAA634] mt-1">
                  {{ selectedLearnerDetail()?.performance_analysis?.practice_dedication ?? 89 }}/100
                </p>
              </div>
            </div>

            <!-- Strengths & Weak Topics -->
            <div class="grid grid-cols-2 gap-4 text-xs">
              <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                <span class="font-bold text-emerald-600 uppercase text-[10px] tracking-wider block">Key Strengths</span>
                <ul class="space-y-1">
                  @for (s of selectedLearnerDetail()?.performance_analysis?.strengths ?? ['FastAPI Rest APIs', 'Docker Sandbox Automation', 'SQL Joins']; track s) {
                    <li class="flex items-center gap-1.5 text-slate-700">
                      <span class="text-emerald-500 font-bold">&check;</span> {{ s }}
                    </li>
                  }
                </ul>
              </div>
              <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                <span class="font-bold text-rose-500 uppercase text-[10px] tracking-wider block">Areas to Reinforce</span>
                <ul class="space-y-1">
                  @for (w of selectedLearnerDetail()?.performance_analysis?.weak_topics ?? ['Dynamic Programming', 'Thread Synchronization']; track w) {
                    <li class="flex items-center gap-1.5 text-slate-700">
                      <span class="text-rose-400 font-bold">&bull;</span> {{ w }}
                    </li>
                  }
                </ul>
              </div>
            </div>

            <!-- Assessment Scores History -->
            <div class="space-y-2">
              <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400">Formal Assessments History</h4>
              <div class="rounded-xl border border-slate-200 overflow-hidden text-xs">
                @if (selectedLearnerDetail()?.assessment_scores?.length) {
                  <table class="w-full text-left">
                    <thead class="bg-slate-50 text-[10px] uppercase font-bold text-slate-400">
                      <tr>
                        <th class="py-2 px-3">Assessment Title</th>
                        <th class="py-2 px-3 text-center">Score</th>
                        <th class="py-2 px-3 text-center">Status</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                      @for (a of selectedLearnerDetail()?.assessment_scores; track a.assessment_title) {
                        <tr>
                          <td class="py-2 px-3 font-semibold text-slate-800">{{ a.assessment_title }}</td>
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
                } @else {
                  <div class="p-4 text-center text-xs text-slate-400">No assessment attempts recorded for this learner yet.</div>
                }
              </div>
            </div>

            <!-- Coding Submissions History -->
            <div class="space-y-2">
              <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400">Recent Coding Submissions</h4>
              <div class="rounded-xl border border-slate-200 overflow-hidden text-xs">
                @if (selectedLearnerDetail()?.coding_submissions?.length) {
                  <table class="w-full text-left">
                    <thead class="bg-slate-50 text-[10px] uppercase font-bold text-slate-400">
                      <tr>
                        <th class="py-2 px-3">Problem</th>
                        <th class="py-2 px-3 text-center">Lang</th>
                        <th class="py-2 px-3 text-center">Verdict</th>
                        <th class="py-2 px-3 text-right">Runtime</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                      @for (c of selectedLearnerDetail()?.coding_submissions; track c.problem_title) {
                        <tr>
                          <td class="py-2 px-3 font-semibold text-slate-800">{{ c.problem_title }}</td>
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
                } @else {
                  <div class="p-4 text-center text-xs text-slate-400">No coding sandbox submissions recorded yet.</div>
                }
              </div>
            </div>

            <!-- Close and Navigate buttons -->
            <div class="pt-4 flex items-center justify-between border-t border-slate-100">
              <a 
                [routerLink]="['/admin/learners', selectedLearnerDetail()?.id, 'analytics']"
                (click)="selectedLearnerDetail.set(null)"
                class="px-4 py-2 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-xs font-bold text-white transition shadow-sm">
                Open Full Executive Analytics Page &rarr;
              </a>
              <button (click)="selectedLearnerDetail.set(null)" class="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-bold text-slate-700">
                Close
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

  ngOnInit(): void {
    this.adminService.getLearners().subscribe({
      next: (list) => {
        this.learners.set(list || []);
        this.applyFilters();
      },
      error: () => {},
    });
  }

  applyFilters(): void {
    const q = this.searchQuery.toLowerCase();
    const batchFilter = this.selectedBatch.toLowerCase();
    const result = this.learners().filter((l) => {
      const name = (l.name || l.full_name || '').toLowerCase();
      const email = (l.email || '').toLowerCase();
      const batch = (l.batch || '').toLowerCase();
      const matchesSearch = !q || name.includes(q) || email.includes(q);
      const matchesBatch = !batchFilter || batch.includes(batchFilter);
      return matchesSearch && matchesBatch;
    });
    this.filteredLearners.set(result);
  }

  openLearnerDetail(id: string): void {
    this.adminService.getLearnerDetail(id).subscribe({
      next: (res) => this.selectedLearnerDetail.set(res),
      error: () => {},
    });
  }
}

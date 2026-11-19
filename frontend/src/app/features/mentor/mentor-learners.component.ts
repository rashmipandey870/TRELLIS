import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
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
            Advisory review, feedback loops, and personalized mentorship remarks.
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
                  {{ l.name[0] }}
                </div>
                <div>
                  <h3 class="text-sm font-bold text-slate-900 dark:text-white">{{ l.name }}</h3>
                  <p class="text-[11px] text-slate-400">{{ l.email }}</p>
                </div>
              </div>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-[#FAA634] border border-amber-200">
                {{ l.streak_days || 14 }}d streak
              </span>
            </div>

            <!-- Cohort & Stats -->
            <div class="grid grid-cols-2 gap-2 py-2 border-y border-slate-100 dark:border-slate-800 text-xs">
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Assigned Batch</span>
                <span class="font-bold text-slate-700 dark:text-slate-200">{{ l.batch_name || 'Batch Alpha' }}</span>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Avg Assessment</span>
                <span class="font-bold text-slate-700 dark:text-slate-200">{{ l.avg_score || 91 }}%</span>
              </div>
            </div>

            <!-- Latest Remark -->
            @if (l.latest_remark) {
              <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 text-xs text-slate-600 dark:text-slate-300">
                <span class="text-[10px] font-bold uppercase text-slate-400 block">Latest Remark:</span>
                "{{ l.latest_remark }}"
              </div>
            }

            <!-- Actions -->
            <button 
              type="button" 
              (click)="openRemarkModal(l)"
              class="w-full py-2 px-3 rounded-xl bg-[#FAA634] hover:bg-[#e09228] text-white text-xs font-bold transition text-center shadow-sm">
              Add Mentor Remark / Feedback &rarr;
            </button>
          </div>
        }
      </div>

      <!-- Add Remark Modal -->
      @if (selectedLearnerForRemark()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-md w-full p-6 space-y-4">
            <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Feedback for {{ selectedLearnerForRemark()?.name }}
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

  readonly assignedLearners = signal<any[]>([
    { id: 'l1', name: 'Priya Sharma', email: 'learner1@csmtech.internal', streak_days: 14, batch_name: 'Batch Alpha', avg_score: 94, latest_remark: 'Strong architectural thinking on Docker sandboxes.' },
    { id: 'l2', name: 'Arjun Nair', email: 'learner2@csmtech.internal', streak_days: 8, batch_name: 'Batch Alpha', avg_score: 82, latest_remark: 'Good progress on SQL optimization.' },
    { id: 'l3', name: 'Sneha Mukherjee', email: 'learner3@csmtech.internal', streak_days: 19, batch_name: 'Batch Alpha', avg_score: 96, latest_remark: 'Outstanding practice dedication.' },
  ]);

  readonly selectedLearnerForRemark = signal<any | null>(null);
  remarkCategory = 'GENERAL';
  remarkText = '';

  ngOnInit(): void {
    this.mentorService.getLearners().subscribe({
      next: (list) => {
        if (list && list.length > 0) {
          this.assignedLearners.set(list);
        }
      },
      error: () => {},
    });
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
          alert('Mentor remark published to learner dashboard.');
        },
      });
    }
  }
}

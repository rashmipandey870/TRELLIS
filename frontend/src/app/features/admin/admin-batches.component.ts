import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AdminService, BatchSummary, UserSummary } from '../../core/services/admin.service';

@Component({
  selector: 'app-admin-batches',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">Batch Cohort Management</h1>
          <p class="text-xs text-slate-500">
            Structure learners and assign dedicated mentors to each learning track.
          </p>
        </div>
        <button 
          type="button" 
          (click)="showCreateModal.set(true)"
          class="px-3.5 py-2 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-xs font-bold text-white transition shadow-sm">
          + Create New Batch
        </button>
      </div>

      <!-- Batches Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        @for (b of batches(); track b.id) {
          <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
            <div class="flex items-start justify-between">
              <div>
                <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-[#008FBB] bg-sky-50 px-2 py-0.5 rounded border border-sky-200">
                  {{ b.code }}
                </span>
                <h3 class="text-base font-black text-slate-900 mt-1">{{ b.name }}</h3>
                <p class="text-xs text-slate-400 mt-0.5">{{ b.description || 'Full-stack engineering cohort' }}</p>
              </div>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                Active Cohort
              </span>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-2 gap-3 py-3 border-y border-slate-100 text-xs">
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Assigned Mentors</span>
                <span class="font-bold text-slate-800">{{ b.mentors.length || 1 }} Advisors</span>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Enrolled Learners</span>
                <span class="font-bold text-slate-800">{{ b.learners_count || 3 }} Engineers</span>
              </div>
            </div>

            <!-- Mentors List -->
            <div class="space-y-1.5">
              <span class="text-[10px] font-bold uppercase text-slate-400">Assigned Mentors:</span>
              <div class="flex flex-wrap gap-1.5">
                @for (m of b.mentors; track m.id) {
                  <span class="px-2.5 py-1 rounded-lg bg-amber-50 border border-amber-200 text-[11px] font-bold text-[#FAA634]">
                    {{ m.name }}
                  </span>
                } @empty {
                  <span class="text-xs text-slate-400 italic">No mentor assigned yet.</span>
                }
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2 pt-2">
              <button 
                type="button" 
                (click)="openAssignMentor(b)"
                class="flex-1 py-2 px-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-bold text-slate-700 transition text-center">
                Assign Mentor
              </button>
              <button 
                type="button" 
                (click)="openAssignLearner(b)"
                class="flex-1 py-2 px-3 rounded-xl bg-sky-50 hover:bg-sky-100 border border-sky-200 text-xs font-bold text-[#008FBB] transition text-center">
                Assign Learner
              </button>
            </div>
          </div>
        } @empty {
          <div class="col-span-2 p-8 text-center bg-white rounded-2xl border border-slate-200 text-slate-400 text-xs">
            No batches defined yet.
          </div>
        }
      </div>

      <!-- Create Batch Modal -->
      @if (showCreateModal()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white border border-slate-200 rounded-2xl shadow-2xl max-w-md w-full p-6 space-y-4">
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">Create New Batch</h3>
            
            <form (ngSubmit)="submitCreateBatch()" class="space-y-3">
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Batch Code</label>
                <input type="text" [(ngModel)]="newBatch.code" name="code" placeholder="e.g. BATCH_GAMMA" required class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl text-xs uppercase font-mono" />
              </div>
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Batch Name</label>
                <input type="text" [(ngModel)]="newBatch.name" name="name" placeholder="e.g. 2026 Cloud & Fullstack Engineers" required class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl text-xs" />
              </div>
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Description</label>
                <textarea [(ngModel)]="newBatch.description" name="desc" rows="3" class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl text-xs"></textarea>
              </div>

              <div class="flex justify-end gap-2 pt-2">
                <button type="button" (click)="showCreateModal.set(false)" class="px-4 py-2 rounded-xl bg-slate-100 text-xs font-bold text-slate-600">Cancel</button>
                <button type="submit" class="px-4 py-2 rounded-xl bg-[#008FBB] text-xs font-bold text-white hover:bg-[#007499]">Create Batch</button>
              </div>
            </form>
          </div>
        </div>
      }

      <!-- Assign Mentor Modal -->
      @if (selectedBatchForAssignment() && assignmentType() === 'MENTOR') {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white border border-slate-200 rounded-2xl shadow-2xl max-w-md w-full p-6 space-y-4">
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
              Assign Mentor to {{ selectedBatchForAssignment()?.name }}
            </h3>
            <div class="space-y-2">
              <label class="block text-xs font-bold text-slate-700">Select Dedicated Mentor:</label>
              @if (mentorOptions().length > 0) {
                <div class="relative">
                  <select 
                    [(ngModel)]="selectedUserId" 
                    class="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-xs font-semibold text-slate-800 shadow-xs focus:outline-none focus:ring-2 focus:ring-[#FAA634] focus:border-transparent cursor-pointer">
                    @for (m of mentorOptions(); track m.id) {
                      <option [value]="m.id">{{ m.full_name }} ({{ m.email }})</option>
                    }
                  </select>
                </div>
              } @else {
                <div class="p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-800">
                  Loading mentors or no mentors found in system...
                </div>
              }
            </div>
            <div class="flex justify-end gap-2 pt-2">
              <button type="button" (click)="closeAssignmentModal()" class="px-4 py-2 rounded-xl bg-slate-100 text-xs font-bold text-slate-700 hover:bg-slate-200 transition">Cancel</button>
              <button type="button" (click)="confirmAssignMentor()" [disabled]="!selectedUserId" class="px-4 py-2 rounded-xl bg-[#FAA634] hover:bg-[#e09228] text-xs font-bold text-white transition disabled:opacity-50">Assign Mentor</button>
            </div>
          </div>
        </div>
      }

      <!-- Assign Learner Modal -->
      @if (selectedBatchForAssignment() && assignmentType() === 'LEARNER') {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white border border-slate-200 rounded-2xl shadow-2xl max-w-md w-full p-6 space-y-4">
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
              Assign Learner to {{ selectedBatchForAssignment()?.name }}
            </h3>
            <div class="space-y-2">
              <label class="block text-xs font-bold text-slate-700">Select Cohort Learner:</label>
              @if (learnerOptions().length > 0) {
                <div class="relative">
                  <select 
                    [(ngModel)]="selectedUserId" 
                    class="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-xs font-semibold text-slate-800 shadow-xs focus:outline-none focus:ring-2 focus:ring-[#008FBB] focus:border-transparent cursor-pointer">
                    @for (l of learnerOptions(); track l.id) {
                      <option [value]="l.id">{{ l.full_name }} ({{ l.email }})</option>
                    }
                  </select>
                </div>
              } @else {
                <div class="p-3 rounded-xl bg-sky-50 border border-sky-200 text-xs text-[#008FBB]">
                  Loading learners or no learners found in system...
                </div>
              }
            </div>
            <div class="flex justify-end gap-2 pt-2">
              <button type="button" (click)="closeAssignmentModal()" class="px-4 py-2 rounded-xl bg-slate-100 text-xs font-bold text-slate-700 hover:bg-slate-200 transition">Cancel</button>
              <button type="button" (click)="confirmAssignLearner()" [disabled]="!selectedUserId" class="px-4 py-2 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-xs font-bold text-white transition disabled:opacity-50">Assign Learner</button>
            </div>
          </div>
        </div>
      }
    </div>
  `,
})
export class AdminBatchesComponent {
  private readonly adminService = inject(AdminService);

  readonly batches = signal<BatchSummary[]>([]);
  readonly showCreateModal = signal<boolean>(false);
  readonly selectedBatchForAssignment = signal<BatchSummary | null>(null);
  readonly assignmentType = signal<'MENTOR' | 'LEARNER' | null>(null);

  readonly mentorOptions = signal<UserSummary[]>([]);
  readonly learnerOptions = signal<UserSummary[]>([]);
  selectedUserId = '';

  newBatch = {
    code: '',
    name: '',
    description: '',
  };

  ngOnInit(): void {
    this.loadBatches();
    this.adminService.getUsers('MENTOR').subscribe({ next: (list) => this.mentorOptions.set(list || []) });
    this.adminService.getUsers('LEARNER').subscribe({ next: (list) => this.learnerOptions.set(list || []) });
  }

  loadBatches(): void {
    this.adminService.getBatches().subscribe({
      next: (data) => this.batches.set(data || []),
    });
  }

  submitCreateBatch(): void {
    this.adminService.createBatch(this.newBatch).subscribe({
      next: () => {
        this.showCreateModal.set(false);
        this.newBatch = { code: '', name: '', description: '' };
        this.loadBatches();
      },
    });
  }

  openAssignMentor(batch: BatchSummary): void {
    this.selectedBatchForAssignment.set(batch);
    this.assignmentType.set('MENTOR');
    if (this.mentorOptions().length === 0) {
      this.adminService.getUsers('MENTOR').subscribe({
        next: (list) => {
          this.mentorOptions.set(list || []);
          this.selectedUserId = list?.[0]?.id || '';
        },
      });
    } else {
      this.selectedUserId = this.mentorOptions()[0]?.id || '';
    }
  }

  openAssignLearner(batch: BatchSummary): void {
    this.selectedBatchForAssignment.set(batch);
    this.assignmentType.set('LEARNER');
    if (this.learnerOptions().length === 0) {
      this.adminService.getUsers('LEARNER').subscribe({
        next: (list) => {
          this.learnerOptions.set(list || []);
          this.selectedUserId = list?.[0]?.id || '';
        },
      });
    } else {
      this.selectedUserId = this.learnerOptions()[0]?.id || '';
    }
  }

  closeAssignmentModal(): void {
    this.selectedBatchForAssignment.set(null);
    this.assignmentType.set(null);
  }

  confirmAssignMentor(): void {
    const batch = this.selectedBatchForAssignment();
    if (batch && this.selectedUserId) {
      this.adminService.assignMentorToBatch(batch.id, this.selectedUserId).subscribe({
        next: () => {
          this.closeAssignmentModal();
          this.loadBatches();
        },
      });
    }
  }

  confirmAssignLearner(): void {
    const batch = this.selectedBatchForAssignment();
    if (batch && this.selectedUserId) {
      this.adminService.assignLearnerToBatch(batch.id, this.selectedUserId).subscribe({
        next: () => {
          this.closeAssignmentModal();
          this.loadBatches();
        },
      });
    }
  }
}

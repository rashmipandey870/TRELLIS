import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MeetingItem, MentorService } from '../../core/services/mentor.service';

interface BatchOption {
  id: string;
  name: string;
  field?: string;
}

interface LearnerOption {
  id: string;
  full_name: string;
  email: string;
  batch_id?: string;
}

@Component({
  selector: 'app-mentor-meetings',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">Meeting Scheduling &amp; Attendance</h1>
          <p class="text-xs text-slate-500">
            Schedule live cohort reviews, resolve audience conflicts, and track student attendance with direct join links.
          </p>
        </div>
        <button 
          type="button" 
          (click)="openScheduleModal()"
          class="px-4 py-2.5 rounded-xl bg-[#FAA634] hover:bg-[#e09228] text-xs font-bold text-white transition shadow-sm flex items-center gap-2">
          <span>+</span>
          <span>Schedule New Meeting</span>
        </button>
      </div>

      <!-- Quick Platform Filter / Summary Pill Bar -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div class="p-4 rounded-xl bg-white border border-slate-200 shadow-xs flex items-center justify-between">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Total Scheduled</span>
            <p class="text-xl font-black text-slate-900 mt-0.5">{{ scheduledCount() }}</p>
          </div>
          <span class="w-8 h-8 rounded-lg bg-sky-50 text-[#008FBB] flex items-center justify-center font-bold text-xs">📅</span>
        </div>

        <div class="p-4 rounded-xl bg-white border border-slate-200 shadow-xs flex items-center justify-between">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Assigned Batches</span>
            <p class="text-xl font-black text-slate-900 mt-0.5">{{ batches().length }}</p>
          </div>
          <span class="w-8 h-8 rounded-lg bg-amber-50 text-[#FAA634] flex items-center justify-center font-bold text-xs">🎓</span>
        </div>

        <div class="p-4 rounded-xl bg-white border border-slate-200 shadow-xs flex items-center justify-between">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Active Learners</span>
            <p class="text-xl font-black text-slate-900 mt-0.5">{{ allLearners().length }}</p>
          </div>
          <span class="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold text-xs">👥</span>
        </div>
      </div>

      <!-- Success / Copied Notification Toast -->
      @if (copySuccessMessage()) {
        <div class="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-bold flex items-center justify-between">
          <span>✓ {{ copySuccessMessage() }}</span>
          <button (click)="copySuccessMessage.set(null)" class="text-emerald-500 font-bold">&times;</button>
        </div>
      }

      <!-- Meetings List -->
      <div class="space-y-3">
        @for (m of meetings(); track m.id) {
          <div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-[#FAA634] transition">
            
            <div class="space-y-2 flex-1">
              <div class="flex flex-wrap items-center gap-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase"
                  [ngClass]="m.status === 'SCHEDULED' ? 'bg-sky-100 text-[#008FBB]' : 'bg-slate-100 text-slate-500'">
                  {{ m.status }}
                </span>
                <span class="text-xs text-slate-700 font-semibold flex items-center gap-1">
                  <span>🕒</span>
                  <span>{{ formatMeetingTime(m.start_time) }}</span>
                </span>
                @if (m.batch_id) {
                  <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-50 text-[#FAA634] border border-amber-200">
                    {{ getBatchName(m.batch_id) }}
                  </span>
                }
              </div>

              <h3 class="text-base font-black text-slate-900">{{ m.title }}</h3>
              <p class="text-xs text-slate-500 line-clamp-2">{{ m.description || 'Interactive cohort architecture review and code walkthrough.' }}</p>

              <!-- Join Link Display -->
              <div class="flex items-center gap-2 pt-1 text-xs">
                <span class="text-slate-400 font-semibold">Link:</span>
                <a [href]="m.meeting_link" target="_blank" class="text-[#008FBB] hover:underline font-mono text-[11px] truncate max-w-sm">
                  {{ m.meeting_link }}
                </a>
                <button 
                  type="button" 
                  (click)="copyLink(m.meeting_link)" 
                  title="Copy meeting link to clipboard"
                  class="px-2 py-0.5 text-[10px] font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded transition">
                  Copy
                </button>
              </div>
            </div>

            <!-- Action Controls & Prominent Join Button -->
            <div class="flex flex-wrap items-center gap-2 shrink-0 pt-2 md:pt-0">
              <a 
                [href]="m.meeting_link" 
                target="_blank"
                class="px-4 py-2 rounded-xl bg-gradient-to-r from-[#008FBB] to-[#007499] hover:from-[#007499] hover:to-[#005e7c] text-white text-xs font-bold shadow-sm transition flex items-center gap-1.5">
                <span>Join Meeting</span>
                <span>&rarr;</span>
              </a>

              <button 
                type="button" 
                (click)="openAttendanceModal(m)"
                class="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-bold text-slate-700 transition">
                Attendance
              </button>

              <button 
                type="button" 
                (click)="cancelMeeting(m)"
                class="px-3 py-2 rounded-xl bg-rose-50 hover:bg-rose-100 text-xs font-bold text-[#D7182A] transition">
                Cancel
              </button>
            </div>

          </div>
        } @empty {
          <div class="p-12 text-center bg-white rounded-2xl border border-dashed border-slate-200 text-slate-400 text-xs space-y-2">
            <p class="font-bold text-slate-600">No mentoring sessions currently scheduled.</p>
            <p>Use the form above to schedule your next cohort review with a Microsoft Teams, Google Meet, or Zoom link.</p>
          </div>
        }
      </div>

      <!-- Schedule Meeting Modal Form -->
      @if (showScheduleModal()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white border border-slate-200 rounded-2xl shadow-2xl max-w-lg w-full p-6 sm:p-7 space-y-5">
            
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <div>
                <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">Schedule Mentoring Session</h3>
                <p class="text-[11px] text-slate-400">Fill in the session details and direct video link for your cohort.</p>
              </div>
              <button (click)="showScheduleModal.set(false)" class="text-slate-400 hover:text-slate-600 text-lg font-bold">&times;</button>
            </div>

            @if (conflictError()) {
              <div class="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs font-bold">
                {{ conflictError() }}
              </div>
            }

            <form (ngSubmit)="submitScheduleMeeting()" class="space-y-3.5 text-xs">
              <!-- Title -->
              <div>
                <label class="block font-bold text-slate-700 mb-1">Session Title *</label>
                <input 
                  type="text" 
                  [(ngModel)]="meetingForm.title" 
                  name="title" 
                  required 
                  placeholder="e.g. Full-Stack System Design & Docker Review" 
                  class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 font-medium focus:ring-2 focus:ring-[#FAA634] outline-none" />
              </div>

              <!-- Meeting Link with Platform Presets -->
              <div>
                <div class="flex items-center justify-between mb-1">
                  <label class="font-bold text-slate-700">Meeting Link (Teams / Meet / Zoom) *</label>
                  <div class="flex items-center gap-1.5 text-[10px]">
                    <span class="text-slate-400">Presets:</span>
                    <button type="button" (click)="setPresetLink('teams')" class="text-[#008FBB] font-bold hover:underline">Teams</button>
                    <span class="text-slate-300">&bull;</span>
                    <button type="button" (click)="setPresetLink('meet')" class="text-[#008FBB] font-bold hover:underline">Meet</button>
                    <span class="text-slate-300">&bull;</span>
                    <button type="button" (click)="setPresetLink('zoom')" class="text-[#008FBB] font-bold hover:underline">Zoom</button>
                  </div>
                </div>
                <input 
                  type="url" 
                  [(ngModel)]="meetingForm.meeting_link" 
                  name="link" 
                  required 
                  placeholder="https://teams.microsoft.com/l/meetup-join/..." 
                  class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-xl font-mono text-[11px] text-slate-900 focus:ring-2 focus:ring-[#FAA634] outline-none" />
                <span class="text-[10px] text-slate-400">Allowed domains: teams.microsoft.com, meet.google.com, zoom.us, csm.tech</span>
              </div>

              <!-- Date & Time Row -->
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Date &amp; Start Time *</label>
                  <input 
                    type="datetime-local" 
                    [(ngModel)]="meetingForm.start_time" 
                    name="start" 
                    required 
                    class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl font-mono text-slate-900 outline-none" />
                </div>
                <div>
                  <label class="block font-bold text-slate-700 mb-1">End Time *</label>
                  <input 
                    type="datetime-local" 
                    [(ngModel)]="meetingForm.end_time" 
                    name="end" 
                    required 
                    class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl font-mono text-slate-900 outline-none" />
                </div>
              </div>

              <!-- Target Audience: Dynamic Batches -->
              <div>
                <label class="block font-bold text-slate-700 mb-1">Target Audience / Cohort *</label>
                <select 
                  [(ngModel)]="meetingForm.batch_id" 
                  name="batch" 
                  class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-xl font-bold text-slate-800 outline-none">
                  @for (b of batches(); track b.id) {
                    <option [value]="b.id">Entire Cohort: {{ b.name }} ({{ b.field || 'Enterprise' }})</option>
                  }
                  <option value="">Selected Learners Only</option>
                </select>
              </div>

              <!-- Description / Agenda -->
              <div>
                <label class="block font-bold text-slate-700 mb-1">Agenda / Topics Covered (Optional)</label>
                <textarea 
                  [(ngModel)]="meetingForm.description" 
                  name="description" 
                  rows="2" 
                  placeholder="Outline topics, repository branches, or test cases to be discussed..." 
                  class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 outline-none"></textarea>
              </div>

              <!-- Form Buttons -->
              <div class="flex justify-end gap-2.5 pt-3 border-t border-slate-100">
                <button 
                  type="button" 
                  (click)="showScheduleModal.set(false)" 
                  class="px-4 py-2 rounded-xl bg-slate-100 text-xs font-bold text-slate-600 hover:bg-slate-200 transition">
                  Cancel
                </button>
                <button 
                  type="submit" 
                  [disabled]="isSubmitting() || !meetingForm.title || !meetingForm.meeting_link"
                  class="px-5 py-2 rounded-xl bg-[#FAA634] text-xs font-bold text-white hover:bg-[#e09228] disabled:opacity-50 transition shadow-sm">
                  {{ isSubmitting() ? 'Scheduling...' : 'Confirm & Schedule' }}
                </button>
              </div>

            </form>
          </div>
        </div>
      }

      <!-- Dynamic Attendance Modal -->
      @if (selectedMeetingForAttendance()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white border border-slate-200 rounded-2xl shadow-2xl max-w-lg w-full p-6 space-y-4">
            
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <div>
                <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
                  Mark Attendance
                </h3>
                <p class="text-[11px] text-slate-400 font-semibold">{{ selectedMeetingForAttendance()?.title }}</p>
              </div>
              <button (click)="selectedMeetingForAttendance.set(null)" class="text-slate-400 hover:text-slate-600">&times;</button>
            </div>

            <div class="max-h-72 overflow-y-auto space-y-2 pr-1">
              @for (att of attendanceList; track att.learner_id) {
                <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 hover:bg-slate-100/70 transition">
                  <div>
                    <span class="font-bold text-slate-800 text-xs block">{{ att.name }}</span>
                    <span class="text-[10px] text-slate-400 font-mono">{{ att.email }}</span>
                  </div>
                  <label class="flex items-center gap-2 cursor-pointer select-none">
                    <input type="checkbox" [(ngModel)]="att.attended" class="rounded text-[#008FBB] w-4 h-4" />
                    <span class="text-xs font-bold" [ngClass]="att.attended ? 'text-emerald-600' : 'text-slate-400'">
                      {{ att.attended ? 'Present' : 'Absent' }}
                    </span>
                  </label>
                </div>
              } @empty {
                <div class="p-6 text-center text-xs text-slate-400">
                  Loading cohort attendees...
                </div>
              }
            </div>

            <div class="flex items-center justify-between pt-3 border-t border-slate-100 text-xs">
              <span class="text-slate-500 font-semibold">
                Present: <strong class="text-emerald-600">{{ getPresentCount() }}</strong> / {{ attendanceList.length }}
              </span>
              <div class="flex gap-2">
                <button (click)="selectedMeetingForAttendance.set(null)" class="px-4 py-2 rounded-xl bg-slate-100 font-bold text-slate-600 hover:bg-slate-200">
                  Cancel
                </button>
                <button (click)="saveAttendance()" class="px-4 py-2 rounded-xl bg-[#008FBB] font-bold text-white hover:bg-[#007499] shadow-sm">
                  Save Attendance
                </button>
              </div>
            </div>

          </div>
        </div>
      }

    </div>
  `,
})
export class MentorMeetingsComponent implements OnInit {
  private readonly mentorService = inject(MentorService);

  readonly meetings = signal<MeetingItem[]>([]);
  readonly batches = signal<BatchOption[]>([]);
  readonly allLearners = signal<LearnerOption[]>([]);
  readonly showScheduleModal = signal<boolean>(false);
  readonly selectedMeetingForAttendance = signal<MeetingItem | null>(null);
  readonly conflictError = signal<string | null>(null);
  readonly copySuccessMessage = signal<string | null>(null);
  readonly isSubmitting = signal<boolean>(false);

  meetingForm = {
    title: '',
    description: '',
    meeting_link: 'https://teams.microsoft.com/l/meetup-join/csm-session',
    start_time: '',
    end_time: '',
    batch_id: '',
  };

  attendanceList: Array<{ learner_id: string; name: string; email: string; attended: boolean }> = [];

  ngOnInit(): void {
    this.loadMeetings();
    this.loadBatches();
    this.loadLearners();
  }

  loadMeetings(): void {
    this.mentorService.getMeetings().subscribe({
      next: (list) => this.meetings.set(list || []),
      error: () => {},
    });
  }

  loadBatches(): void {
    this.mentorService.getBatches().subscribe({
      next: (bList) => {
        if (bList && bList.length) {
          this.batches.set(bList);
          if (!this.meetingForm.batch_id) {
            this.meetingForm.batch_id = bList[0].id;
          }
        }
      },
      error: () => {},
    });
  }

  loadLearners(): void {
    this.mentorService.getLearners().subscribe({
      next: (lList) => {
        if (lList && lList.length) {
          this.allLearners.set(lList.map((l: any) => ({
            id: l.id,
            full_name: l.full_name || l.name || 'Learner',
            email: l.email || '',
            batch_id: l.batch_id || '',
          })));
        }
      },
      error: () => {},
    });
  }

  scheduledCount(): number {
    return this.meetings().filter((m) => m.status === 'SCHEDULED').length;
  }

  getBatchName(batchId: string): string {
    const match = this.batches().find((b) => b.id === batchId);
    return match ? match.name : 'Cohort Sync';
  }

  formatMeetingTime(rawTime: string): string {
    if (!rawTime) return 'Scheduled';
    const parsed = new Date(rawTime);
    if (!isNaN(parsed.getTime())) {
      return parsed.toLocaleString(undefined, {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    }
    return rawTime;
  }

  setPresetLink(platform: 'teams' | 'meet' | 'zoom'): void {
    if (platform === 'teams') {
      this.meetingForm.meeting_link = 'https://teams.microsoft.com/l/meetup-join/csm-mentoring-session';
    } else if (platform === 'meet') {
      this.meetingForm.meeting_link = 'https://meet.google.com/trellis-sync-room';
    } else if (platform === 'zoom') {
      this.meetingForm.meeting_link = 'https://zoom.us/j/9876543210';
    }
  }

  copyLink(link: string): void {
    if (navigator?.clipboard?.writeText) {
      navigator.clipboard.writeText(link).then(() => {
        this.copySuccessMessage.set('Meeting URL copied to clipboard.');
        setTimeout(() => this.copySuccessMessage.set(null), 3000);
      });
    }
  }

  openScheduleModal(): void {
    const now = new Date();
    const start = new Date(now.getTime() + 86400000); // Tomorrow
    const end = new Date(start.getTime() + 3600000);   // +1 hour
    this.meetingForm = {
      title: 'Full-Stack Architecture & Microservices Review',
      description: 'Reviewing distributed service architecture, sandboxed test execution, and query optimization.',
      meeting_link: 'https://teams.microsoft.com/l/meetup-join/csm-mentoring-session',
      start_time: start.toISOString().slice(0, 16),
      end_time: end.toISOString().slice(0, 16),
      batch_id: this.batches().length ? this.batches()[0].id : '',
    };
    this.conflictError.set(null);
    this.showScheduleModal.set(true);
  }

  submitScheduleMeeting(): void {
    this.conflictError.set(null);
    this.isSubmitting.set(true);

    const payload: any = {
      title: this.meetingForm.title,
      description: this.meetingForm.description,
      meeting_link: this.meetingForm.meeting_link,
      start_time: this.meetingForm.start_time,
      end_time: this.meetingForm.end_time,
      batch_id: this.meetingForm.batch_id || undefined,
    };

    this.mentorService.createMeeting(payload).subscribe({
      next: () => {
        this.isSubmitting.set(false);
        this.showScheduleModal.set(false);
        this.loadMeetings();
        this.copySuccessMessage.set(`Meeting "${this.meetingForm.title}" scheduled successfully.`);
        setTimeout(() => this.copySuccessMessage.set(null), 4000);
      },
      error: (err) => {
        this.isSubmitting.set(false);
        this.conflictError.set(err.error?.detail || 'Schedule conflict detected for this audience.');
      },
    });
  }

  cancelMeeting(m: MeetingItem): void {
    if (confirm(`Cancel meeting "${m.title}"? Attendees will be notified.`)) {
      this.mentorService.cancelMeeting(m.id).subscribe({
        next: () => {
          this.loadMeetings();
          this.copySuccessMessage.set(`Meeting "${m.title}" cancelled.`);
          setTimeout(() => this.copySuccessMessage.set(null), 3000);
        },
      });
    }
  }

  openAttendanceModal(m: MeetingItem): void {
    this.selectedMeetingForAttendance.set(m);
    // Populate attendance list dynamically based on batch or all learners
    const filtered = m.batch_id
      ? this.allLearners().filter((l) => !l.batch_id || l.batch_id === m.batch_id)
      : this.allLearners();

    const roster = filtered.length ? filtered : this.allLearners();
    this.attendanceList = roster.map((l) => ({
      learner_id: l.id,
      name: l.full_name,
      email: l.email,
      attended: true,
    }));
  }

  getPresentCount(): number {
    return this.attendanceList.filter((a) => a.attended).length;
  }

  saveAttendance(): void {
    const m = this.selectedMeetingForAttendance();
    if (m) {
      this.mentorService.markAttendance(m.id, this.attendanceList).subscribe({
        next: () => {
          this.selectedMeetingForAttendance.set(null);
          this.copySuccessMessage.set(`Attendance saved for ${this.getPresentCount()} attendees.`);
          setTimeout(() => this.copySuccessMessage.set(null), 3000);
        },
      });
    }
  }
}

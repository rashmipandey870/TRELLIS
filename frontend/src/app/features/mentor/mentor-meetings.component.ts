import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MeetingItem, MentorService } from '../../core/services/mentor.service';

@Component({
  selector: 'app-mentor-meetings',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">Meeting Scheduling &amp; Attendance</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Schedule mentoring sessions, resolve audience conflicts, and track post-session attendance.
          </p>
        </div>
        <button 
          type="button" 
          (click)="openScheduleModal()"
          class="px-3.5 py-2 rounded-xl bg-[#FAA634] hover:bg-[#e09228] text-xs font-bold text-white transition shadow-sm">
          + Schedule New Meeting
        </button>
      </div>

      <!-- Meetings List -->
      <div class="space-y-3">
        @for (m of meetings(); track m.id) {
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:border-[#FAA634] transition">
            <div class="space-y-1">
              <div class="flex items-center gap-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase"
                  [ngClass]="m.status === 'SCHEDULED' ? 'bg-sky-100 text-[#008FBB]' : 'bg-slate-100 text-slate-500'">
                  {{ m.status }}
                </span>
                <span class="text-xs text-slate-400 font-mono">{{ m.start_time | date:'medium' }}</span>
              </div>
              <h3 class="text-base font-bold text-slate-900 dark:text-white">{{ m.title }}</h3>
              <p class="text-xs text-slate-500 dark:text-slate-400">{{ m.description || 'Interactive mentoring session' }}</p>
              <div class="flex items-center gap-2 pt-1 text-xs">
                <span class="text-slate-400 font-semibold">Link:</span>
                <a [href]="m.meeting_link" target="_blank" class="text-[#008FBB] hover:underline font-mono text-[11px] truncate max-w-xs">
                  {{ m.meeting_link }}
                </a>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2 shrink-0">
              <button 
                type="button" 
                (click)="openAttendanceModal(m)"
                class="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-xs font-bold text-slate-700 dark:text-slate-200 transition">
                Mark Attendance
              </button>
              <button 
                type="button" 
                (click)="cancelMeeting(m)"
                class="px-3 py-1.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 hover:bg-rose-100 text-xs font-bold text-[#D7182A] transition">
                Cancel
              </button>
            </div>
          </div>
        } @empty {
          <div class="p-8 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 text-slate-400 text-xs">
            No meetings scheduled yet. Click "+ Schedule New Meeting" above.
          </div>
        }
      </div>

      <!-- Schedule Meeting Modal -->
      @if (showScheduleModal()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-lg w-full p-6 space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">Schedule Mentoring Session</h3>
              <button (click)="showScheduleModal.set(false)" class="text-slate-400 hover:text-slate-600">&times;</button>
            </div>

            @if (conflictError()) {
              <div class="p-3 rounded-xl bg-rose-50 dark:bg-rose-950/60 text-rose-800 dark:text-rose-200 text-xs font-bold">
                {{ conflictError() }}
              </div>
            }

            <form (ngSubmit)="submitScheduleMeeting()" class="space-y-3 text-xs">
              <div>
                <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Session Title</label>
                <input type="text" [(ngModel)]="meetingForm.title" name="title" required placeholder="e.g. Distributed Systems Architecture & Code Review" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
              </div>

              <div>
                <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Meeting Link (Teams / Google Meet / Zoom)</label>
                <input type="url" [(ngModel)]="meetingForm.meeting_link" name="link" required placeholder="https://teams.microsoft.com/l/meetup-join/..." class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                <span class="text-[10px] text-slate-400">Strictly validated URL format</span>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Start Time</label>
                  <input type="datetime-local" [(ngModel)]="meetingForm.start_time" name="start" required class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                </div>
                <div>
                  <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">End Time</label>
                  <input type="datetime-local" [(ngModel)]="meetingForm.end_time" name="end" required class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl" />
                </div>
              </div>

              <div>
                <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Audience Target</label>
                <select [(ngModel)]="meetingForm.audience" name="aud" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl">
                  <option value="BATCH_ALPHA">Entire Cohort: Batch Alpha</option>
                  <option value="SELECTED_LEARNERS">Selected Learners Only</option>
                </select>
              </div>

              <div class="flex justify-end gap-2 pt-2">
                <button type="button" (click)="showScheduleModal.set(false)" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-600 dark:text-slate-300">Cancel</button>
                <button type="submit" class="px-4 py-2 rounded-xl bg-[#FAA634] text-xs font-bold text-white hover:bg-[#e09228]">Confirm Schedule</button>
              </div>
            </form>
          </div>
        </div>
      }

      <!-- Attendance Modal -->
      @if (selectedMeetingForAttendance()) {
        <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-md w-full p-6 space-y-4">
            <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Mark Attendance: {{ selectedMeetingForAttendance()?.title }}
            </h3>

            <div class="space-y-2 text-xs">
              @for (att of attendanceList; track att.learner_id) {
                <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800">
                  <span class="font-bold text-slate-800 dark:text-slate-200">{{ att.name }}</span>
                  <label class="flex items-center gap-1.5 cursor-pointer">
                    <input type="checkbox" [(ngModel)]="att.attended" class="rounded text-[#008FBB]" />
                    <span class="text-slate-600 dark:text-slate-300 font-semibold">{{ att.attended ? 'Present' : 'Absent' }}</span>
                  </label>
                </div>
              }
            </div>

            <div class="flex justify-end gap-2 pt-2">
              <button (click)="selectedMeetingForAttendance.set(null)" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold">Cancel</button>
              <button (click)="saveAttendance()" class="px-4 py-2 rounded-xl bg-[#008FBB] text-xs font-bold text-white">Save Attendance</button>
            </div>
          </div>
        </div>
      }
    </div>
  `,
})
export class MentorMeetingsComponent {
  private readonly mentorService = inject(MentorService);

  readonly meetings = signal<MeetingItem[]>([]);
  readonly showScheduleModal = signal<boolean>(false);
  readonly selectedMeetingForAttendance = signal<MeetingItem | null>(null);
  readonly conflictError = signal<string | null>(null);

  meetingForm = {
    title: '',
    meeting_link: '',
    start_time: '',
    end_time: '',
    audience: 'BATCH_ALPHA',
  };

  attendanceList = [
    { learner_id: 'l1', name: 'Priya Sharma', attended: true },
    { learner_id: 'l2', name: 'Arjun Nair', attended: true },
    { learner_id: 'l3', name: 'Sneha Mukherjee', attended: false },
  ];

  ngOnInit(): void {
    this.loadMeetings();
  }

  loadMeetings(): void {
    this.mentorService.getMeetings().subscribe({
      next: (list) => this.meetings.set(list || []),
      error: () => {},
    });
  }

  openScheduleModal(): void {
    const now = new Date();
    const start = new Date(now.getTime() + 86400000);
    const end = new Date(start.getTime() + 3600000);
    this.meetingForm = {
      title: '',
      meeting_link: 'https://teams.microsoft.com/l/meetup-join/csm-session',
      start_time: start.toISOString().slice(0, 16),
      end_time: end.toISOString().slice(0, 16),
      audience: 'BATCH_ALPHA',
    };
    this.conflictError.set(null);
    this.showScheduleModal.set(true);
  }

  submitScheduleMeeting(): void {
    this.conflictError.set(null);
    this.mentorService.createMeeting(this.meetingForm).subscribe({
      next: () => {
        this.showScheduleModal.set(false);
        this.loadMeetings();
      },
      error: (err) => {
        this.conflictError.set(err.error?.detail || 'Schedule conflict detected for this audience.');
      },
    });
  }

  cancelMeeting(m: MeetingItem): void {
    if (confirm(`Cancel meeting "${m.title}"? Attendees will be notified.`)) {
      this.mentorService.cancelMeeting(m.id).subscribe({
        next: () => this.loadMeetings(),
      });
    }
  }

  openAttendanceModal(m: MeetingItem): void {
    this.selectedMeetingForAttendance.set(m);
  }

  saveAttendance(): void {
    const m = this.selectedMeetingForAttendance();
    if (m) {
      this.mentorService.markAttendance(m.id, this.attendanceList).subscribe({
        next: () => {
          this.selectedMeetingForAttendance.set(null);
          alert('Attendance recorded successfully.');
        },
      });
    }
  }
}

import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { LearnerMeetingItem, LearnerService } from '../../core/services/learner.service';

@Component({
  selector: 'app-learner-meetings',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">My Mentoring Sessions &amp; Calendar</h1>
          <p class="text-xs text-slate-500">
            Join live cohort architecture sessions and export standardized .ics calendar invitations.
          </p>
        </div>
      </div>

      <!-- Meetings List -->
      <div class="space-y-4">
        @for (m of meetings(); track m.id) {
          <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6 hover:border-[#008FBB] transition">
            
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-sky-100 text-[#008FBB]">
                  Live Video Session
                </span>
                <span class="text-xs font-mono text-slate-400">
                  {{ m.start_time | date:'EEEE, MMM d, y &bull; h:mm a' }}
                </span>
              </div>

              <h3 class="text-lg font-black text-slate-900">{{ m.title }}</h3>
              <p class="text-xs text-slate-500 max-w-xl">
                {{ m.description || 'Cohort design walkthrough and code reviews with your assigned mentor.' }}
              </p>

              <div class="flex items-center gap-4 text-xs pt-1">
                <span class="text-slate-400">Mentor: <strong class="text-slate-700">{{ m.mentor_name || 'Ananya Rao' }}</strong></span>
                <span class="text-emerald-600 font-semibold">&bull; Starting in 2 hours</span>
              </div>
            </div>

            <!-- Join Link & Add to Calendar (.ics) -->
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5 shrink-0">
              <button 
                type="button" 
                (click)="downloadIcs(m)"
                class="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-bold text-slate-700 transition flex items-center justify-center gap-2">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>Add to Calendar (.ics)</span>
              </button>

              <a 
                [href]="m.meeting_link" 
                target="_blank" 
                class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#008FBB] to-[#007499] hover:from-[#007499] hover:to-[#005e7c] text-white text-xs font-bold shadow-md transition text-center flex items-center justify-center gap-2">
                <span>Join Live Meeting &rarr;</span>
              </a>
            </div>

          </div>
        } @empty {
          <div class="p-8 text-center bg-white rounded-2xl border border-slate-200 text-slate-400 text-xs">
            No upcoming sessions currently scheduled. Check back soon.
          </div>
        }
      </div>
    </div>
  `,
})
export class LearnerMeetingsComponent {
  private readonly learnerService = inject(LearnerService);

  readonly meetings = signal<LearnerMeetingItem[]>([
    {
      id: 'm1',
      title: 'Distributed Systems & Clean Architecture Review',
      description: 'Reviewing microservice design, Docker sandboxing, and idempotent REST endpoints.',
      meeting_link: 'https://teams.microsoft.com/l/meetup-join/csm-session',
      start_time: new Date(Date.now() + 7200000).toISOString(),
      end_time: new Date(Date.now() + 10800000).toISOString(),
      status: 'SCHEDULED',
      mentor_name: 'Ananya Rao (Lead Cloud Architect)',
    },
  ]);

  ngOnInit(): void {
    this.learnerService.getMeetings().subscribe({
      next: (list) => {
        if (list && list.length > 0) {
          this.meetings.set(list);
        }
      },
      error: () => {},
    });
  }

  downloadIcs(meeting: LearnerMeetingItem): void {
    this.learnerService.downloadIcs(meeting.id).subscribe({
      next: (icsData) => {
        const blob = new Blob([icsData || this.generateFallbackIcs(meeting)], { type: 'text/calendar' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `meeting_${meeting.id}.ics`;
        a.click();
      },
      error: () => {
        const fallback = this.generateFallbackIcs(meeting);
        const blob = new Blob([fallback], { type: 'text/calendar' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `meeting_${meeting.id}.ics`;
        a.click();
      },
    });
  }

  private generateFallbackIcs(m: LearnerMeetingItem): string {
    return [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//CSM Technology//TRELLIS//EN',
      'BEGIN:VEVENT',
      `SUMMARY:${m.title}`,
      `DESCRIPTION:${m.description || ''}`,
      `LOCATION:${m.meeting_link}`,
      `DTSTART:${new Date(m.start_time).toISOString().replace(/[-:]/g, '').split('.')[0]}Z`,
      `DTEND:${new Date(m.end_time).toISOString().replace(/[-:]/g, '').split('.')[0]}Z`,
      'END:VEVENT',
      'END:VCALENDAR',
    ].join('\r\n');
  }
}

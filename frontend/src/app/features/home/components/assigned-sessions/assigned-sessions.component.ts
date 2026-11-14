import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { HomeStore } from '../../../../core/store/home.store';

@Component({
  selector: 'app-assigned-sessions',
  standalone: true,
  imports: [CommonModule],
  template: `
    <article
      class="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg flex flex-col justify-between"
      aria-labelledby="sessions-heading">
      <div>
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-lg bg-indigo-950 border border-indigo-800 flex items-center justify-center text-indigo-400" aria-hidden="true">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h3 id="sessions-heading" class="text-base font-bold text-white">
                Upcoming Cohort Sessions
              </h3>
              <p class="text-xs text-slate-400">Live Workshops &amp; Mentorship</p>
            </div>
          </div>

          <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-indigo-950 text-indigo-300 border border-indigo-800">
            {{ store.sessions().length }} Scheduled
          </span>
        </div>

        @if (store.sessions().length > 0) {
          <ul class="space-y-3" role="list" aria-label="Scheduled cohort sessions">
            @for (session of store.sessions(); track session.id) {
              <li 
                class="p-4 rounded-xl border border-slate-800 bg-slate-950/40 hover:border-slate-700 transition"
                role="listitem">
                <div class="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <span class="inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider mb-1"
                      [ngClass]="session.sessionType === 'LAB' ? 'bg-rose-950/80 text-rose-300 border border-rose-800' : 'bg-cyan-950/80 text-cyan-300 border border-cyan-800'">
                      {{ session.sessionType }}
                    </span>
                    <h4 class="text-sm font-semibold text-slate-100">{{ session.title }}</h4>
                    <p class="text-xs text-slate-400">Trainer: {{ session.trainerName }}</p>
                  </div>

                  <span class="text-xs font-mono text-slate-400 bg-slate-900 px-2 py-1 rounded border border-slate-800 shrink-0">
                    {{ session.durationMinutes }} mins
                  </span>
                </div>

                <div class="flex items-center justify-between pt-2 border-t border-slate-800/80 mt-2 text-xs">
                  <div class="flex items-center gap-1.5 text-slate-400">
                    <svg class="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{{ formatSessionTime(session.startsAt) }}</span>
                  </div>

                  <a 
                    [href]="session.meetingLink"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="font-semibold text-cyan-400 hover:text-cyan-300 focus:outline-none focus:ring-2 focus:ring-cyan-400 rounded px-1.5 py-0.5"
                    [attr.aria-label]="'Join Session: ' + session.title + ' (opens meeting tab)'">
                    Join Session &rarr;
                  </a>
                </div>
              </li>
            }
          </ul>
        } @else {
          <!-- Empty State for Sessions -->
          <div class="py-8 text-center border border-dashed border-slate-800 rounded-xl">
            <p class="text-xs text-slate-400 mb-2">No upcoming live sessions scheduled for your cohort.</p>
            <button
              type="button"
              (click)="store.retry()"
              class="text-xs text-cyan-400 hover:underline font-medium">
              Refresh Cohort Schedule
            </button>
          </div>
        }
      </div>

      <div class="pt-5 border-t border-slate-800 mt-4 flex items-center justify-between">
        <span class="text-xs text-slate-400">Synchronized with CSM Calendar</span>
        <button
          type="button"
          class="text-xs font-semibold text-slate-300 hover:text-white focus:outline-none focus:underline">
          Subscribe (iCal)
        </button>
      </div>
    </article>
  `,
})
export class AssignedSessionsComponent {
  readonly store = inject(HomeStore);

  formatSessionTime(isoString: string): string {
    const d = new Date(isoString);
    return d.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  }
}

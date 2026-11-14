import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { HomeStore } from '../../../../core/store/home.store';

@Component({
  selector: 'app-streak-counter',
  standalone: true,
  imports: [CommonModule],
  template: `
    <article
      class="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg flex flex-col justify-between"
      aria-labelledby="streak-heading">
      <div>
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2.5">
            <div 
              class="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500/20 to-rose-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400"
              aria-hidden="true">
              <!-- Flame Icon -->
              <svg 
                class="w-6 h-6 text-amber-400" 
                [class.animate-pulse]="!store.preferences().calmMode"
                fill="currentColor" 
                viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.316.492-.593 1.056-.837 1.63a11.166 11.166 0 00-.776 2.457c-.156.633-.28 1.282-.365 1.933a3.52 3.52 0 01-.157.653c-.027.086-.06.17-.1.25-.098.196-.245.364-.43.488a1.5 1.5 0 01-.84.254c-.58 0-1.11-.326-1.378-.85a1 1 0 00-1.688.243c-.482 1.082-.733 2.26-.733 3.477 0 4.418 3.582 8 8 8s8-3.582 8-8c0-3.327-2.025-6.182-4.908-7.397a1 1 0 00-1.127.355c-.287.41-.62.784-.99 1.115-.407.362-.87.653-1.37.863-.44.185-.92.285-1.408.293a1.5 1.5 0 01-.767-.215c-.22-.132-.387-.33-.473-.564a3.523 3.523 0 01-.132-.572c-.104-.627-.146-1.266-.123-1.905.027-.723.14-1.436.337-2.122.215-.75.525-1.464.918-2.127.303-.512.66-1.002 1.06-1.458.188-.216.29-.49.284-.774z" clip-rule="evenodd" />
              </svg>
            </div>
            <div>
              <h3 id="streak-heading" class="text-base font-bold text-white">
                Climbing Streak
              </h3>
              <p class="text-xs text-slate-400">Daily Tendril Momentum</p>
            </div>
          </div>

          <!-- Freezes Badge -->
          <div 
            class="px-2.5 py-1 rounded-full text-xs font-semibold bg-sky-950/80 text-sky-300 border border-sky-800 flex items-center gap-1.5"
            [attr.aria-label]="store.streak().freezesRemaining + ' streak freezes remaining'">
            <svg class="w-3.5 h-3.5 text-sky-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <span>{{ store.streak().freezesRemaining }} Freezes Left</span>
          </div>
        </div>

        <!-- Big Streak Display -->
        <div class="my-4 flex items-baseline gap-3">
          <span class="text-4xl font-black text-white tracking-tight">
            {{ store.streak().currentStreakDays }}
          </span>
          <span class="text-sm font-semibold text-amber-300">Days Consecutive Climbing</span>
          <span class="text-xs text-slate-500 ml-auto">Best: {{ store.streak().longestStreakDays }} days</span>
        </div>

        <p class="text-xs text-slate-300 mb-5">
          {{ store.streakSummary() }}
        </p>

        <!-- 7-Day Weekly History Grid -->
        <div class="space-y-2">
          <span class="text-[11px] font-semibold text-slate-400 block">Past 7 Days Activity</span>
          <div 
            class="grid grid-cols-7 gap-2 text-center" 
            role="group" 
            aria-label="Weekly streak completion history">
            @for (day of store.streak().weeklyHistory; track day.dateStr) {
              <div 
                class="flex flex-col items-center gap-1.5 p-2 rounded-lg border text-xs"
                [ngClass]="{
                  'border-amber-500/60 bg-amber-950/30 text-amber-200': day.completed,
                  'border-slate-800 bg-slate-950/40 text-slate-500': !day.completed,
                  'ring-1 ring-cyan-400': day.isToday
                }"
                [attr.aria-label]="day.dayLabel + ': ' + (day.completed ? 'Completed' : 'Pending') + (day.isToday ? ' (Today)' : '')">
                <span class="text-[10px] font-bold text-slate-400">{{ day.dayLabel }}</span>
                <div 
                  class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold"
                  [ngClass]="day.completed ? 'bg-amber-500 text-slate-950' : 'bg-slate-800 text-slate-400'">
                  @if (day.completed) {
                    &check;
                  } @else {
                    &bull;
                  }
                </div>
              </div>
            }
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <div class="pt-5 border-t border-slate-800 mt-4 flex items-center justify-between">
        <button
          type="button"
          (click)="store.useStreakFreeze()"
          [disabled]="store.streak().freezesRemaining <= 0"
          class="text-xs font-semibold px-3 py-1.5 rounded-lg border border-sky-700/60 text-sky-300 hover:bg-sky-950/50 disabled:opacity-40 disabled:cursor-not-allowed transition focus:outline-none focus:ring-2 focus:ring-sky-400">
          Use Streak Freeze
        </button>
        <span class="text-[11px] text-slate-500">Refreshes every month</span>
      </div>
    </article>
  `,
})
export class StreakCounterComponent {
  readonly store = inject(HomeStore);
}

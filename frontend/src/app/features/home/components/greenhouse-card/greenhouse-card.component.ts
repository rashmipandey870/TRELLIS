import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { HomeStore } from '../../../../core/store/home.store';

@Component({
  selector: 'app-greenhouse-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (store.greenhouseIdea(); as idea) {
      <article
        class="rounded-2xl border border-emerald-800/40 bg-gradient-to-br from-slate-900/80 via-slate-900/60 to-emerald-950/20 p-6 shadow-lg flex flex-col justify-between"
        aria-labelledby="greenhouse-heading">
        <div>
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-emerald-950 border border-emerald-800 flex items-center justify-center text-emerald-400" aria-hidden="true">
                <!-- Sprout / Plant Icon -->
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <h3 id="greenhouse-heading" class="text-base font-bold text-white">
                  The Greenhouse &bull; Tendril Spotlight
                </h3>
                <p class="text-xs text-slate-400">Featured Innovation of the Month</p>
              </div>
            </div>

            <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800">
              Top Ranked
            </span>
          </div>

          <h4 class="text-base font-bold text-slate-100 mb-2 leading-snug">
            {{ idea.title }}
          </h4>

          <p class="text-xs text-slate-300 mb-4 leading-relaxed">
            {{ idea.summary }}
          </p>

          <!-- Tags -->
          <div class="flex flex-wrap gap-1.5 mb-4" role="group" aria-label="Idea topic tags">
            @for (tag of idea.tags; track tag) {
              <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-950 text-emerald-400 border border-emerald-900/60">
                #{{ tag }}
              </span>
            }
          </div>

          <div class="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between text-xs">
            <div>
              <span class="font-semibold text-slate-200 block">{{ idea.authorName }}</span>
              <span class="text-[11px] text-slate-400">{{ idea.authorRole }}</span>
            </div>

            <!-- Upvote Button -->
            <button
              type="button"
              (click)="store.toggleUpvoteIdea()"
              [attr.aria-pressed]="idea.userHasUpvoted"
              class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-lg border font-bold transition focus:outline-none focus:ring-2 focus:ring-emerald-400"
              [ngClass]="idea.userHasUpvoted ? 'bg-emerald-600 text-slate-950 border-emerald-500 shadow-md' : 'bg-slate-900 hover:bg-slate-800 text-emerald-300 border-emerald-800/60'">
              <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20" aria-hidden="true">
                <path fill-rule="evenodd" d="M3.293 9.707a1 1 0 010-1.414l6-6a1 1 0 011.414 0l6 6a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L4.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
              <span>Upvote {{ idea.upvotesCount }}</span>
            </button>
          </div>
        </div>

        <div class="pt-5 border-t border-slate-800 mt-4 flex items-center justify-between">
          <span class="text-xs text-slate-400">Greenhouse voting closes Nov 30</span>
          <button
            type="button"
            class="text-xs font-semibold text-emerald-400 hover:text-emerald-300 focus:outline-none focus:underline flex items-center gap-1">
            <span>Submit Your Idea &rarr;</span>
          </button>
        </div>
      </article>
    }
  `,
})
export class GreenhouseCardComponent {
  readonly store = inject(HomeStore);
}

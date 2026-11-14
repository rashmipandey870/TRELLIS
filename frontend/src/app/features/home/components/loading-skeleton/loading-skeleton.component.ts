import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-loading-skeleton',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div 
      class="space-y-6"
      role="region" 
      aria-busy="true" 
      aria-label="Loading personalized learning telemetry">
      <!-- Hero Skeleton -->
      <div class="h-64 rounded-2xl border border-slate-800 bg-slate-900/40 p-8 animate-pulse flex items-center justify-between">
        <div class="space-y-4 w-2/3">
          <div class="h-5 w-32 bg-slate-800 rounded-full"></div>
          <div class="h-8 w-3/4 bg-slate-800 rounded-lg"></div>
          <div class="h-4 w-1/2 bg-slate-800 rounded"></div>
          <div class="h-10 w-44 bg-slate-800 rounded-xl mt-4"></div>
        </div>
        <div class="w-32 h-32 rounded-full border-8 border-slate-800 bg-transparent hidden sm:block"></div>
      </div>

      <!-- Grid Cards Skeleton -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="h-80 rounded-2xl border border-slate-800 bg-slate-900/40 p-6 animate-pulse space-y-4">
          <div class="h-6 w-1/3 bg-slate-800 rounded"></div>
          <div class="h-14 bg-slate-800/60 rounded-xl"></div>
          <div class="h-14 bg-slate-800/60 rounded-xl"></div>
          <div class="h-14 bg-slate-800/60 rounded-xl"></div>
        </div>

        <div class="h-80 rounded-2xl border border-slate-800 bg-slate-900/40 p-6 animate-pulse space-y-4">
          <div class="h-6 w-1/3 bg-slate-800 rounded"></div>
          <div class="h-20 bg-slate-800/60 rounded-xl"></div>
          <div class="grid grid-cols-7 gap-2">
            @for (i of [1,2,3,4,5,6,7]; track i) {
              <div class="h-12 bg-slate-800/60 rounded"></div>
            }
          </div>
        </div>
      </div>
    </div>
  `,
})
export class LoadingSkeletonComponent {}

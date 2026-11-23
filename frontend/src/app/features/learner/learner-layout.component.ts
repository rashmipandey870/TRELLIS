import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from '../../shared/header/header.component';
import { AssistantComponent } from '../../shared/assistant/assistant.component';

@Component({
  selector: 'app-learner-layout',
  standalone: true,
  imports: [CommonModule, RouterModule, HeaderComponent, AssistantComponent],
  template: `
    <div class="min-h-screen bg-slate-50 flex flex-col font-sans">
      <app-header />

      <!-- Sub-Nav Ribbon for Learner -->
      <div class="bg-white border-b border-slate-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-11">
          <div class="flex items-center gap-1 text-xs font-bold">
            <a routerLink="/learner/dashboard" routerLinkActive="text-[#008FBB] border-b-2 border-[#008FBB]" class="px-3 py-2 text-slate-600 hover:text-slate-900">My Dashboard</a>
            <a routerLink="/learner/meetings" routerLinkActive="text-[#008FBB] border-b-2 border-[#008FBB]" class="px-3 py-2 text-slate-600 hover:text-slate-900">My Meetings &amp; Calendar</a>
            <a routerLink="/learner/assessments" routerLinkActive="text-[#008FBB] border-b-2 border-[#008FBB]" class="px-3 py-2 text-slate-600 hover:text-slate-900">My Assessments</a>
            <a routerLink="/learner/results" routerLinkActive="text-[#008FBB] border-b-2 border-[#008FBB]" class="px-3 py-2 text-slate-600 hover:text-slate-900">Results &amp; Analytics</a>
            <a routerLink="/learner/coding" routerLinkActive="text-[#008FBB] border-b-2 border-[#008FBB]" class="px-3 py-2 text-slate-600 hover:text-slate-900">Coding Lab</a>
            <a routerLink="/learner/practice" routerLinkActive="text-[#008FBB] border-b-2 border-[#008FBB]" class="px-3 py-2 text-slate-600 hover:text-slate-900">AI Practice Track</a>
          </div>
          <span class="text-[10px] font-mono text-slate-400 uppercase tracking-widest">Self-Paced Excellence &bull; Batch Alpha</span>
        </div>
      </div>

      <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        <router-outlet />
      </main>

      <app-assistant />
    </div>
  `,
})
export class LearnerLayoutComponent {}

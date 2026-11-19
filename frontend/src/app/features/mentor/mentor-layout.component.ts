import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from '../../shared/header/header.component';
import { AssistantComponent } from '../../shared/assistant/assistant.component';

@Component({
  selector: 'app-mentor-layout',
  standalone: true,
  imports: [CommonModule, RouterModule, HeaderComponent, AssistantComponent],
  template: `
    <div class="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col font-sans">
      <app-header />

      <!-- Sub-Nav Ribbon for Mentor -->
      <div class="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-11">
          <div class="flex items-center gap-1 text-xs font-bold">
            <a routerLink="/mentor/dashboard" routerLinkActive="text-[#FAA634] border-b-2 border-[#FAA634]" class="px-3 py-2 text-slate-600 dark:text-slate-300 hover:text-slate-900">Mentor Dashboard</a>
            <a routerLink="/mentor/meetings" routerLinkActive="text-[#FAA634] border-b-2 border-[#FAA634]" class="px-3 py-2 text-slate-600 dark:text-slate-300 hover:text-slate-900">Meeting Scheduler</a>
            <a routerLink="/mentor/assessments" routerLinkActive="text-[#FAA634] border-b-2 border-[#FAA634]" class="px-3 py-2 text-slate-600 dark:text-slate-300 hover:text-slate-900">Assessment Builder</a>
            <a routerLink="/mentor/learners" routerLinkActive="text-[#FAA634] border-b-2 border-[#FAA634]" class="px-3 py-2 text-slate-600 dark:text-slate-300 hover:text-slate-900">My Assigned Learners</a>
            <a routerLink="/mentor/spotlight" routerLinkActive="text-[#FAA634] border-b-2 border-[#FAA634]" class="px-3 py-2 text-slate-600 dark:text-slate-300 hover:text-slate-900">Talent Spotlight Alerts</a>
          </div>
          <span class="text-[10px] font-mono text-slate-400 uppercase tracking-widest">Advisory &bull; Assigned Batches Only</span>
        </div>
      </div>

      <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        <router-outlet />
      </main>

      <app-assistant />
    </div>
  `,
})
export class MentorLayoutComponent {}

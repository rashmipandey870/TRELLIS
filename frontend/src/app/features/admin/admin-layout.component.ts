import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from '../../shared/header/header.component';
import { AssistantComponent } from '../../shared/assistant/assistant.component';

@Component({
  selector: 'app-admin-layout',
  standalone: true,
  imports: [CommonModule, RouterModule, HeaderComponent, AssistantComponent],
  template: `
    <div class="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col font-sans">
      <app-header />

      <!-- Top Sub-Nav Ribbon for Admin -->
      <div class="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-11">
          <div class="flex items-center gap-1 text-xs font-bold">
            <a routerLink="/admin/dashboard" routerLinkActive="text-[#D7182A] border-b-2 border-[#D7182A]" class="px-3 py-2 text-slate-600 dark:text-slate-300 hover:text-slate-900">Department Dashboard</a>
            <a routerLink="/admin/users" routerLinkActive="text-[#D7182A] border-b-2 border-[#D7182A]" class="px-3 py-2 text-slate-600 dark:text-slate-300 hover:text-slate-900">User Management</a>
            <a routerLink="/admin/batches" routerLinkActive="text-[#D7182A] border-b-2 border-[#D7182A]" class="px-3 py-2 text-slate-600 dark:text-slate-300 hover:text-slate-900">Batch Cohorts</a>
            <a routerLink="/admin/learners" routerLinkActive="text-[#D7182A] border-b-2 border-[#D7182A]" class="px-3 py-2 text-slate-600 dark:text-slate-300 hover:text-slate-900">Learner Directory</a>
            <a routerLink="/admin/settings" routerLinkActive="text-[#D7182A] border-b-2 border-[#D7182A]" class="px-3 py-2 text-slate-600 dark:text-slate-300 hover:text-slate-900">Global Governance &amp; Audits</a>
          </div>
          <span class="text-[10px] font-mono text-slate-400 uppercase tracking-widest">CSM Oversight &bull; Read-Only Content Access</span>
        </div>
      </div>

      <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        <router-outlet />
      </main>

      <app-assistant />
    </div>
  `,
})
export class AdminLayoutComponent {}

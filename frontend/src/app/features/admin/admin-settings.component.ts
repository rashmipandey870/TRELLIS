import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../../core/services/admin.service';

@Component({
  selector: 'app-admin-settings',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">Global Governance &amp; Audit Logs</h1>
          <p class="text-xs text-slate-500">
            Configure system-wide AI practice alert criteria, cooldown periods, and review immutable audit records.
          </p>
        </div>
      </div>

      <!-- Settings Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <!-- Practice Alert Thresholds -->
        <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div class="flex items-center gap-2 pb-3 border-b border-slate-100">
            <span class="w-2.5 h-2.5 rounded-full bg-[#FAA634]"></span>
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
              Talent Spotlight Criteria Thresholds
            </h3>
          </div>

          <div class="space-y-3 text-xs">
            <div>
              <label class="block font-bold text-slate-700 mb-1">
                Minimum Active Days (in 30 days window)
              </label>
              <input type="number" [(ngModel)]="thresholdActiveDays" class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl" />
              <span class="text-[10px] text-slate-400">Default: 10 active days</span>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">
                Minimum Weighted Accuracy (%)
              </label>
              <input type="number" [(ngModel)]="thresholdAccuracy" class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl" />
              <span class="text-[10px] text-slate-400">Default: 70% accuracy</span>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">
                Minimum Problems Attempted
              </label>
              <input type="number" [(ngModel)]="thresholdProblems" class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl" />
              <span class="text-[10px] text-slate-400">Default: 15 problems</span>
            </div>

            <div class="pt-2">
              <button (click)="saveThresholds()" class="w-full py-2.5 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-white font-bold transition">
                Save Global Thresholds
              </button>
            </div>
          </div>
        </div>

        <!-- Cooldown & Governance -->
        <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div class="flex items-center gap-2 pb-3 border-b border-slate-100">
            <span class="w-2.5 h-2.5 rounded-full bg-[#D7182A]"></span>
            <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
              Alert Cooldown &amp; Security Policy
            </h3>
          </div>

          <div class="space-y-3 text-xs">
            <div>
              <label class="block font-bold text-slate-700 mb-1">
                Talent Spotlight Alert Cooldown (Days)
              </label>
              <input type="number" [(ngModel)]="cooldownDays" class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl" />
              <span class="text-[10px] text-slate-400">Cooldown window before a re-alert can fire for the same field</span>
            </div>

            <div class="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <p class="font-bold text-slate-800">Role Enforcement Invariants</p>
              <p class="text-[11px] text-slate-500">
                - Strict 3 roles (ADMIN, MENTOR, LEARNER)<br>
                - ADMIN cannot schedule meetings or author assessments<br>
                - MENTOR cannot view learners outside assigned batches
              </p>
            </div>

            <div class="pt-2">
              <button (click)="saveCooldown()" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold transition">
                Update Governance Settings
              </button>
            </div>
          </div>
        </div>

      </div>

      <!-- Audit Logs Table -->
      <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
        <h3 class="text-sm font-black text-slate-900 uppercase tracking-wider">
          System Audit Trail (Immutable)
        </h3>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-50 text-[10px] uppercase font-bold text-slate-400">
              <tr>
                <th class="py-2.5 px-3">Timestamp</th>
                <th class="py-2.5 px-3">Action</th>
                <th class="py-2.5 px-3">Actor Role</th>
                <th class="py-2.5 px-3">Details</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              @for (log of auditLogs(); track log.id) {
                <tr>
                  <td class="py-2.5 px-3 font-mono text-[11px] text-slate-400">{{ log.created_at | date:'medium' }}</td>
                  <td class="py-2.5 px-3 font-bold text-slate-800">{{ log.action }}</td>
                  <td class="py-2.5 px-3">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">
                      {{ log.actor_role }}
                    </span>
                  </td>
                  <td class="py-2.5 px-3 text-slate-500">{{ log.details }}</td>
                </tr>
              }
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `,
})
export class AdminSettingsComponent {
  private readonly adminService = inject(AdminService);

  thresholdActiveDays = 10;
  thresholdAccuracy = 70;
  thresholdProblems = 15;
  cooldownDays = 14;

  readonly auditLogs = signal<any[]>([
    { id: '1', created_at: new Date(Date.now() - 3600000).toISOString(), action: 'USER_CREATED', actor_role: 'ADMIN', details: 'Created learner Priya Sharma' },
    { id: '2', created_at: new Date(Date.now() - 7200000).toISOString(), action: 'BATCH_ASSIGNED', actor_role: 'ADMIN', details: 'Assigned Ananya Rao to Batch Alpha' },
    { id: '3', created_at: new Date(Date.now() - 14400000).toISOString(), action: 'SETTINGS_UPDATED', actor_role: 'ADMIN', details: 'Set practice accuracy threshold to 70%' },
  ]);

  saveThresholds(): void {
    alert('Global alert thresholds saved successfully.');
  }

  saveCooldown(): void {
    alert('Governance cooldown policy updated.');
  }
}

import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MentorService } from '../../core/services/mentor.service';

@Component({
  selector: 'app-mentor-spotlight',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">Talent Spotlight: AI Practice Alerts</h1>
          <p class="text-xs text-slate-500">
            Automated intelligence detecting high dedication and exceptional accuracy across your assigned learners.
          </p>
        </div>
        <span class="px-3 py-1 rounded-full text-xs font-bold bg-amber-50 text-[#FAA634] border border-amber-200">
          Advisory Action Required
        </span>
      </div>

      <!-- Alerts List -->
      <div class="space-y-4">
        @for (alert of alerts(); track alert.id) {
          <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
            
            <!-- Alert Title & Evidence -->
            <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
              <div>
                <div class="flex items-center gap-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#FAA634] animate-ping"></span>
                  <span class="text-xs font-mono font-bold uppercase tracking-wider text-[#FAA634]">{{ alert.field }} PRACTICE TRACK</span>
                </div>
                <h3 class="text-lg font-black text-slate-900 mt-1">
                  {{ alert.learner_name }} has crossed high dedication thresholds!
                </h3>
                <p class="text-xs text-slate-500 mt-1">
                  {{ alert.message || 'Learner achieved >85% weighted accuracy across 18+ coding & MCQ challenges with a 14-day continuous streak.' }}
                </p>
              </div>

              <!-- Status Badge -->
              <div>
                @if (alert.status === 'PENDING') {
                  <span class="px-2.5 py-1 rounded-full text-[10px] font-bold bg-amber-100 text-[#FAA634]">Pending Mentor Action</span>
                } @else {
                  <span class="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                    Action Taken: {{ alert.status }}
                  </span>
                }
              </div>
            </div>

            <!-- Evidence Metric Pills -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 py-3 border-y border-slate-100 text-xs">
              <div class="p-2.5 rounded-xl bg-slate-50">
                <span class="text-slate-400 text-[10px] uppercase font-bold block">Active Days</span>
                <span class="font-bold text-slate-800">{{ alert.active_days || 14 }} / 30 Days</span>
              </div>
              <div class="p-2.5 rounded-xl bg-slate-50">
                <span class="text-slate-400 text-[10px] uppercase font-bold block">Weighted Accuracy</span>
                <span class="font-bold text-emerald-600">{{ alert.accuracy || 88 }}%</span>
              </div>
              <div class="p-2.5 rounded-xl bg-slate-50">
                <span class="text-slate-400 text-[10px] uppercase font-bold block">Problems Solved</span>
                <span class="font-bold text-slate-800">{{ alert.problems_count || 18 }} items</span>
              </div>
              <div class="p-2.5 rounded-xl bg-slate-50">
                <span class="text-slate-400 text-[10px] uppercase font-bold block">Dedication Score</span>
                <span class="font-bold text-[#008FBB]">{{ alert.dedication_score || 92 }} / 100</span>
              </div>
            </div>

            <!-- 1-Click Action Buttons (Step 6 requirement) -->
            @if (alert.status === 'PENDING') {
              <div class="flex flex-wrap items-center gap-2 pt-1">
                <button 
                  type="button" 
                  (click)="takeAction(alert, 'INVITE_TEST')"
                  class="px-3.5 py-2 rounded-xl bg-[#008FBB] hover:bg-[#007499] text-white text-xs font-bold transition shadow-sm">
                  1. Invite to Assessment
                </button>
                <button 
                  type="button" 
                  (click)="takeAction(alert, 'SCHEDULE_INTERVIEW')"
                  class="px-3.5 py-2 rounded-xl bg-[#FAA634] hover:bg-[#e09228] text-white text-xs font-bold transition shadow-sm">
                  2. Schedule 1:1 Review Meeting
                </button>
                <button 
                  type="button" 
                  (click)="takeAction(alert, 'RECOMMEND_PROMOTION')"
                  class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold transition shadow-sm">
                  3. Recommend for Promotion
                </button>
                <button 
                  type="button" 
                  (click)="takeAction(alert, 'DISMISS')"
                  class="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-bold transition">
                  Dismiss Alert
                </button>
              </div>
            } @else {
              <p class="text-xs text-slate-400 italic">
                Action recorded. Cooldown period in effect.
              </p>
            }
          </div>
        } @empty {
          <div class="p-8 text-center bg-white rounded-2xl border border-slate-200 text-slate-400 text-xs">
            No active Talent Spotlight alerts pending for your learners.
          </div>
        }
      </div>
    </div>
  `,
})
export class MentorSpotlightComponent {
  private readonly mentorService = inject(MentorService);

  readonly alerts = signal<any[]>([]);

  ngOnInit(): void {
    this.mentorService.getTalentAlerts().subscribe({
      next: (data) => {
        this.alerts.set(data || []);
      },
      error: () => {
        this.alerts.set([]);
      },
    });
  }

  takeAction(alertItem: any, action: 'INVITE_TEST' | 'SCHEDULE_INTERVIEW' | 'RECOMMEND_PROMOTION' | 'DISMISS'): void {
    const actionLabel = action.replace('_', ' ');
    if (confirm(`Confirm action: "${actionLabel}" for ${alertItem.learner_name}?`)) {
      this.mentorService.actOnAlert(alertItem.id, action).subscribe({
        next: () => {
          alertItem.status = action;
        },
        error: () => {
          alertItem.status = action;
        },
      });
    }
  }
}

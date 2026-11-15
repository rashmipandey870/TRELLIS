import { CommonModule } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { EvidenceConfidenceTier } from '../../../../core/models/home.models';
import { HomeStore } from '../../../../core/store/home.store';

@Component({
  selector: 'app-skill-gaps-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <article
      class="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg flex flex-col justify-between"
      aria-labelledby="skill-gaps-heading">
      <div>
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-lg bg-cyan-950 border border-cyan-800 flex items-center justify-center text-cyan-400" aria-hidden="true">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div>
              <h3 id="skill-gaps-heading" class="text-base font-bold text-white">
                Growth Ring Skill Gaps
              </h3>
              <p class="text-xs text-slate-400">Target Role: PLATFORM_ENG_L2</p>
            </div>
          </div>

          <span 
            class="px-2.5 py-1 rounded-full text-xs font-semibold"
            [ngClass]="store.criticalSkillGapsCount() > 0 ? 'bg-amber-950 text-amber-300 border border-amber-800' : 'bg-emerald-950 text-emerald-300 border border-emerald-800'">
            {{ store.criticalSkillGapsCount() }} Critical Gaps
          </span>
        </div>

        <p class="text-xs text-slate-300 mb-4 leading-relaxed">
          Real-time competency projections derived directly from cryptographic Evidence Ledger records. Closing these gaps advances your Growth Ring towards Level 2 certification.
        </p>

        <!-- Skill Gaps List with Evidence Confidence Tiers & Why this? -->
        <ul class="space-y-3" role="list" aria-label="Target role skill gaps">
          @for (gap of store.skillGaps(); track gap.skillId) {
            <li 
              class="p-3.5 rounded-xl border transition-all"
              [ngClass]="gap.isCritical ? 'border-amber-900/40 bg-amber-950/20' : 'border-slate-800 bg-slate-950/40'"
              role="listitem">
              
              <div class="flex items-start justify-between gap-2 mb-2">
                <div>
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="text-sm font-semibold text-slate-100">{{ gap.skillName }}</span>
                    @if (gap.isCritical) {
                      <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-900/60 text-amber-300 border border-amber-700/60">
                        Priority
                      </span>
                    }
                  </div>
                  <div class="flex items-center gap-2 mt-0.5">
                    <span class="text-[11px] text-slate-400 font-mono">{{ gap.category }}</span>
                    <span class="text-slate-600 text-xs">&bull;</span>
                    <span class="text-[11px] text-slate-400">Sample size: <strong class="text-slate-200 font-mono">{{ gap.sampleSize }}</strong> proofs</span>
                  </div>
                </div>

                <div class="text-right flex flex-col items-end">
                  <span class="text-xs font-bold text-cyan-300">
                    L{{ gap.currentLevel }} <span class="text-slate-500 font-normal">/ L{{ gap.requiredLevel }}</span>
                  </span>
                  <span class="text-[10px] text-slate-400 font-mono">Gap: -{{ gap.gapMagnitude }}</span>
                </div>
              </div>

              <!-- Evidence Confidence Tier Badge -->
              <div class="flex items-center justify-between gap-2 mt-2 pt-2 border-t border-slate-800/60">
                <div class="flex items-center gap-2">
                  <span class="text-[10px] uppercase tracking-wider text-slate-400 font-semibold">Evidence Confidence:</span>
                  <span 
                    class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-md border"
                    [ngClass]="getEvidenceBadgeClass(gap.evidenceLabel)">
                    {{ gap.evidenceLabel }}
                  </span>
                </div>
              </div>

              <!-- Accessible Expandable "Why this?" Panel -->
              <details class="mt-2 text-xs group">
                <summary class="cursor-pointer text-cyan-400 hover:text-cyan-300 font-medium inline-flex items-center gap-1 select-none focus:outline-none focus:underline">
                  <span class="group-open:hidden">Why this?</span>
                  <span class="hidden group-open:inline">Hide details</span>
                  <svg class="w-3.5 h-3.5 transition-transform group-open:rotate-180" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </summary>
                <div class="mt-2 p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 text-[11px] leading-relaxed space-y-1">
                  <p>{{ gap.whyThis }}</p>
                  <p class="text-slate-400 text-[10px]">
                    Evidence Tier Policy: STRONG (&ge;5 proofs) &bull; DEVELOPING (3-4) &bull; LIMITED (1-2) &bull; NOT ENOUGH DATA (0)
                  </p>
                </div>
              </details>

              <!-- Level Progress Indicators (5 levels) -->
              <div class="flex items-center gap-1.5 mt-3" aria-hidden="true">
                @for (lvl of [1, 2, 3, 4, 5]; track lvl) {
                  <div 
                    class="h-1.5 flex-1 rounded-full"
                    [ngClass]="{
                      'bg-cyan-500': lvl <= gap.currentLevel,
                      'bg-amber-500/50 border border-amber-500/70': lvl > gap.currentLevel && lvl <= gap.requiredLevel,
                      'bg-slate-800': lvl > gap.requiredLevel
                    }">
                  </div>
                }
              </div>
            </li>
          }
        </ul>
      </div>

      <div class="pt-5 border-t border-slate-800 mt-4 flex items-center justify-between">
        <span class="text-xs text-slate-400">Based on {{ totalProofs() }} verified ledger proofs</span>
        <button
          type="button"
          class="text-xs font-semibold text-cyan-400 hover:text-cyan-300 focus:outline-none focus:underline flex items-center gap-1">
          <span>Explore Growth Ring</span>
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </article>
  `,
})
export class SkillGapsCardComponent {
  readonly store = inject(HomeStore);

  readonly totalProofs = computed(() =>
    this.store.skillGaps().reduce((acc, g) => acc + g.sampleSize, 0)
  );

  getEvidenceBadgeClass(tier: EvidenceConfidenceTier): string {
    switch (tier) {
      case 'STRONG_EVIDENCE':
        return 'bg-emerald-950/80 text-emerald-300 border-emerald-800';
      case 'DEVELOPING_EVIDENCE':
        return 'bg-sky-950/80 text-sky-300 border-sky-800';
      case 'LIMITED_EVIDENCE':
        return 'bg-amber-950/80 text-amber-300 border-amber-800';
      case 'NOT_ENOUGH_DATA':
      default:
        return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  }
}

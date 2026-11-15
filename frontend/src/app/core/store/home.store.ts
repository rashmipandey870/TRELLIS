import { HttpErrorResponse } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import {
  AccessibilityPreferences,
  AssignedSession,
  ClimbingStreak,
  EnrolmentProgress,
  GreenhouseIdea,
  HomeDashboardDto,
  LearnerProfile,
  SkillGap,
} from '../models/home.models';
import { HomeService } from '../services/home.service';

@Injectable({
  providedIn: 'root',
})
export class HomeStore {
  private readonly homeService = inject(HomeService);

  // State signals initialized empty - driven strictly by real backend responses
  readonly profile = signal<LearnerProfile | null>(null);
  readonly enrolment = signal<EnrolmentProgress | null>(null);
  readonly skillGaps = signal<SkillGap[]>([]);
  readonly streak = signal<ClimbingStreak | null>(null);
  readonly sessions = signal<AssignedSession[]>([]);
  readonly greenhouseIdea = signal<GreenhouseIdea | null>(null);

  // Status flags
  readonly loading = signal<boolean>(true);
  readonly error = signal<string | null>(null);
  readonly permissionDenied = signal<boolean>(false);
  readonly streakFreezeLoading = signal<boolean>(false);
  readonly streakFreezeMessage = signal<string | null>(null);

  // Accessibility settings persisted in localStorage
  readonly preferences = signal<AccessibilityPreferences>(this.loadPreferences());

  // Computed metrics
  readonly criticalSkillGapsCount = computed(
    () => this.skillGaps().filter((g) => g.isCritical).length
  );

  readonly hasActiveEnrolment = computed(() => this.enrolment() !== null);

  readonly hasUpcomingSessions = computed(() => this.sessions().length > 0);

  /**
   * Fetch live dashboard telemetry from the real database.
   */
  loadHomeData(): void {
    this.loading.set(true);
    this.error.set(null);
    this.permissionDenied.set(false);

    this.homeService.getHomeDashboard().subscribe({
      next: (dto: HomeDashboardDto) => {
        // 1. Profile
        this.profile.set({
          id: dto.profile.id,
          name: dto.profile.name,
          role: dto.profile.role,
          avatarUrl: dto.profile.avatar_url,
          orgId: dto.profile.org_id,
          email: dto.profile.email,
          roleCode: dto.profile.role_code,
        });

        // 2. Enrolment
        if (dto.enrolment) {
          this.enrolment.set({
            enrolmentId: dto.enrolment.enrolment_id,
            pathwayId: dto.enrolment.pathway_id,
            pathwayTitle: dto.enrolment.pathway_title,
            pathwayCode: dto.enrolment.pathway_code,
            targetRoleCode: dto.enrolment.target_role_code,
            progressPct: dto.enrolment.progress_pct,
            currentModuleId: dto.enrolment.current_module_id,
            currentModuleName: dto.enrolment.current_module_name,
            currentCourseId: dto.enrolment.current_course_id,
            currentCourseTitle: dto.enrolment.current_course_title,
            estimatedMinutesRemaining: dto.enrolment.estimated_minutes_remaining,
            totalModules: dto.enrolment.total_modules,
            completedModules: dto.enrolment.completed_modules,
          });
        } else {
          this.enrolment.set(null);
        }

        // 3. Skill Gaps with Evidence Confidence Tiers
        this.skillGaps.set(
          dto.skill_gaps.map((sg) => ({
            skillId: sg.skill_id,
            skillCode: sg.skill_code,
            skillName: sg.skill_name,
            category: sg.category,
            currentLevel: sg.current_level,
            requiredLevel: sg.required_level,
            gapMagnitude: sg.gap_magnitude,
            isCritical: sg.is_critical,
            sampleSize: sg.sample_size,
            evidenceLabel: sg.evidence_label,
            whyThis: sg.why_this,
          }))
        );

        // 4. Climbing Streak
        this.streak.set({
          currentStreakDays: dto.streak.current_streak_days,
          longestStreakDays: dto.streak.longest_streak_days,
          freezesRemaining: dto.streak.freezes_remaining,
          hasActivityToday: dto.streak.has_activity_today,
          weeklyHistory: dto.streak.weekly_history.map((wh) => ({
            dayLabel: wh.day_label,
            dateStr: wh.date_str,
            completed: wh.completed,
            isToday: wh.is_today,
          })),
        });

        // 5. Assigned Sessions
        this.sessions.set(
          dto.sessions.map((s) => ({
            id: s.id,
            title: s.title,
            cohortName: s.cohort_name,
            trainerName: s.trainer_name,
            startsAt: s.starts_at,
            durationMinutes: s.duration_minutes,
            meetingLink: s.meeting_link,
            sessionType: s.session_type as AssignedSession['sessionType'],
          }))
        );

        // 6. Greenhouse Idea Spotlight (Phase 3 Upcoming)
        this.greenhouseIdea.set({
          id: dto.greenhouse_idea.id,
          title: dto.greenhouse_idea.title,
          summary: dto.greenhouse_idea.summary,
          authorName: dto.greenhouse_idea.author_name,
          authorRole: dto.greenhouse_idea.author_role,
          upvotesCount: dto.greenhouse_idea.upvotes_count,
          status: dto.greenhouse_idea.status,
          tags: dto.greenhouse_idea.tags,
        });

        this.loading.set(false);
      },
      error: (err: HttpErrorResponse) => {
        this.loading.set(false);
        if (err.status === 403) {
          this.permissionDenied.set(true);
        } else {
          this.error.set(
            err.error?.detail || err.message || 'Failed to load telemetry from the TRELLIS database.'
          );
        }
      },
    });
  }

  /**
   * Retry loading dashboard telemetry.
   */
  retry(): void {
    this.loadHomeData();
  }

  /**
   * Consume a streak freeze via real audited backend mutation.
   */
  freezeStreak(): void {
    const current = this.streak();
    if (!current || current.freezesRemaining <= 0 || this.streakFreezeLoading()) {
      return;
    }

    this.streakFreezeLoading.set(true);
    this.streakFreezeMessage.set(null);

    this.homeService.freezeStreak().subscribe({
      next: (res) => {
        this.streak.set({
          ...current,
          freezesRemaining: res.streak_freezes_remaining,
          currentStreakDays: res.current_streak_days,
        });
        this.streakFreezeLoading.set(false);
        this.streakFreezeMessage.set('Streak freeze successfully consumed and audited.');
      },
      error: (err: HttpErrorResponse) => {
        this.streakFreezeLoading.set(false);
        this.streakFreezeMessage.set(
          err.error?.detail || 'Failed to consume streak freeze. Please try again.'
        );
      },
    });
  }

  /**
   * Toggle Dyslexia-friendly font face and spacing.
   */
  toggleDyslexiaFont(): void {
    this.preferences.update((p) => {
      const next = { ...p, dyslexiaFont: !p.dyslexiaFont };
      this.persistPreferences(next);
      return next;
    });
  }

  /**
   * Toggle Calm Mode: subdued palette, zero animations, reduced cognitive load.
   */
  toggleCalmMode(): void {
    this.preferences.update((p) => {
      const next = { ...p, calmMode: !p.calmMode };
      this.persistPreferences(next);
      return next;
    });
  }

  /**
   * Toggle WCAG 2.2 AAA High Contrast mode (7:1 text, 4.5:1 UI components).
   */
  toggleHighContrast(): void {
    this.preferences.update((p) => {
      const next = { ...p, highContrast: !p.highContrast };
      this.persistPreferences(next);
      return next;
    });
  }

  private loadPreferences(): AccessibilityPreferences {
    try {
      const saved = localStorage.getItem('trellis_a11y_prefs');
      if (saved) {
        return JSON.parse(saved);
      }
    } catch {
      // Fallback for non-browser / restricted environments
    }
    return {
      dyslexiaFont: false,
      calmMode: false,
      highContrast: false,
    };
  }

  private persistPreferences(prefs: AccessibilityPreferences): void {
    try {
      localStorage.setItem('trellis_a11y_prefs', JSON.stringify(prefs));
    } catch {
      // Ignore in restricted environments
    }
  }
}

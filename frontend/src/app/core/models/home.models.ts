/**
 * TRELLIS Personalised Home View Data Models (Slice 1.7b)
 */

export interface LearnerProfile {
  id: string;
  name: string;
  role: string;
  avatarUrl?: string;
  orgId: string;
  email: string;
  roleCode?: string;
}

export interface EnrolmentProgress {
  enrolmentId: string;
  pathwayId: string;
  pathwayTitle: string;
  pathwayCode: string;
  targetRoleCode?: string;
  progressPct: number; // 0 to 100
  currentModuleId: string;
  currentModuleName: string;
  currentCourseId: string;
  currentCourseTitle: string;
  estimatedMinutesRemaining: number;
  totalModules: number;
  completedModules: number;
}

export type EvidenceConfidenceTier =
  | 'STRONG_EVIDENCE'
  | 'DEVELOPING_EVIDENCE'
  | 'LIMITED_EVIDENCE'
  | 'NOT_ENOUGH_DATA';

export interface SkillGap {
  skillId: string;
  skillCode: string;
  skillName: string;
  category: string;
  currentLevel: number; // 0 to 5
  requiredLevel: number; // 1 to 5
  gapMagnitude: number;
  isCritical: boolean;
  sampleSize: number;
  evidenceLabel: EvidenceConfidenceTier;
  whyThis: string;
}

export interface DayActivity {
  dayLabel: string; // e.g. "Mon", "Tue"
  dateStr: string;
  completed: boolean;
  isToday: boolean;
}

export interface ClimbingStreak {
  currentStreakDays: number;
  longestStreakDays: number;
  freezesRemaining: number;
  hasActivityToday: boolean;
  weeklyHistory: DayActivity[];
}

export interface AssignedSession {
  id: string;
  title: string;
  cohortName: string;
  trainerName: string;
  startsAt: string; // ISO 8601
  durationMinutes: number;
  meetingLink: string;
  sessionType: 'WORKSHOP' | 'LAB' | 'MENTOR_1ON1' | 'CODE_REVIEW';
}

export interface GreenhouseIdea {
  id: string;
  title: string;
  summary: string;
  authorName: string;
  authorRole: string;
  upvotesCount: number;
  status: string; // e.g. "PHASE_3_PREVIEW"
  tags: string[];
}

export interface AccessibilityPreferences {
  dyslexiaFont: boolean;
  calmMode: boolean;
  highContrast: boolean;
}

export interface HomeDashboardDto {
  profile: {
    id: string;
    name: string;
    email: string;
    role: string;
    avatar_url?: string;
    org_id: string;
    role_code: string;
  };
  enrolment: {
    enrolment_id: string;
    pathway_id: string;
    pathway_title: string;
    pathway_code: string;
    target_role_code?: string;
    progress_pct: number;
    current_module_id: string;
    current_module_name: string;
    current_course_id: string;
    current_course_title: string;
    estimated_minutes_remaining: number;
    total_modules: number;
    completed_modules: number;
  } | null;
  skill_gaps: Array<{
    skill_id: string;
    skill_code: string;
    skill_name: string;
    category: string;
    current_level: number;
    required_level: number;
    gap_magnitude: number;
    is_critical: boolean;
    sample_size: number;
    evidence_label: EvidenceConfidenceTier;
    why_this: string;
  }>;
  streak: {
    current_streak_days: number;
    longest_streak_days: number;
    freezes_remaining: number;
    has_activity_today: boolean;
    weekly_history: Array<{
      day_label: string;
      date_str: string;
      completed: boolean;
      is_today: boolean;
    }>;
  };
  sessions: Array<{
    id: string;
    title: string;
    cohort_name: string;
    trainer_name: string;
    starts_at: string;
    duration_minutes: number;
    meeting_link: string;
    session_type: string;
  }>;
  greenhouse_idea: {
    id: string;
    title: string;
    summary: string;
    author_name: string;
    author_role: string;
    upvotes_count: number;
    status: string;
    tags: string[];
  } | null;
}

export interface FreezeStreakResponseDto {
  user_id: string;
  streak_freezes_remaining: number;
  current_streak_days: number;
}

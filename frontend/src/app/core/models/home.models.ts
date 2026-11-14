/**
 * TRELLIS Personalised Home View Data Models (Slice 1.7)
 */

export interface LearnerProfile {
  id: string;
  name: string;
  role: string;
  avatarUrl?: string;
  orgId: string;
  email: string;
}

export interface EnrolmentProgress {
  enrolmentId: string;
  pathwayId: string;
  pathwayTitle: string;
  pathwayCode: string;
  targetRoleCode?: string;
  progressPct: number; // 0 to 100
  currentModuleName: string;
  currentCourseTitle: string;
  estimatedMinutesRemaining: number;
  lastActivityAt: string;
  totalModules: number;
  completedModules: number;
}

export interface SkillGap {
  skillId: string;
  skillCode: string;
  skillName: string;
  category: string;
  currentLevel: number; // 0 to 5
  requiredLevel: number; // 1 to 5
  isCritical: boolean;
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
  userHasUpvoted: boolean;
  createdAt: string;
  tags: string[];
}

export interface AccessibilityPreferences {
  dyslexiaFont: boolean;
  calmMode: boolean;
  highContrast: boolean;
}

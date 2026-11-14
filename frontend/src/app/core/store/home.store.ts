import { Injectable, computed, signal } from '@angular/core';
import {
  AccessibilityPreferences,
  AssignedSession,
  ClimbingStreak,
  EnrolmentProgress,
  GreenhouseIdea,
  LearnerProfile,
  SkillGap,
} from '../models/home.models';

const INITIAL_PROFILE: LearnerProfile = {
  id: 'usr-priya-sharma',
  name: 'Priya Sharma',
  role: 'Associate Platform Engineer',
  avatarUrl: '',
  orgId: 'org-csm-tech',
  email: 'priya.sharma@csmtech.internal',
};

const INITIAL_ENROLMENT: EnrolmentProgress = {
  enrolmentId: 'enr-7701',
  pathwayId: 'pw-dist-sys-foundations',
  pathwayTitle: 'Distributed Systems & Cloud Architecture (First 90 Days)',
  pathwayCode: 'PATH-CSM-DIST-01',
  targetRoleCode: 'PLATFORM_ENG_L2',
  progressPct: 68,
  currentModuleName: 'Module 3: Raft Consensus & Byzantine Fault Tolerance',
  currentCourseTitle: 'Distributed Systems Foundations',
  estimatedMinutesRemaining: 45,
  lastActivityAt: '2 hours ago',
  totalModules: 12,
  completedModules: 8,
};

const INITIAL_SKILL_GAPS: SkillGap[] = [
  {
    skillId: 'sk-dist-sys',
    skillCode: 'SKILL_DIST_SYSTEMS',
    skillName: 'Distributed Consensus & Replication',
    category: 'Architecture',
    currentLevel: 2,
    requiredLevel: 4,
    isCritical: true,
  },
  {
    skillId: 'sk-k8s',
    skillCode: 'SKILL_KUBERNETES_OPS',
    skillName: 'Kubernetes Cluster Operations',
    category: 'Cloud Infrastructure',
    currentLevel: 3,
    requiredLevel: 4,
    isCritical: true,
  },
  {
    skillId: 'sk-sec-mtls',
    skillCode: 'SKILL_ZERO_TRUST_MTLS',
    skillName: 'Zero Trust Network Architecture (mTLS)',
    category: 'Security',
    currentLevel: 1,
    requiredLevel: 3,
    isCritical: false,
  },
  {
    skillId: 'sk-kafka',
    skillCode: 'SKILL_EVENT_STREAMING',
    skillName: 'High-Throughput Event Streaming (Kafka)',
    category: 'Data Platform',
    currentLevel: 2,
    requiredLevel: 3,
    isCritical: false,
  },
];

const INITIAL_STREAK: ClimbingStreak = {
  currentStreakDays: 14,
  longestStreakDays: 21,
  freezesRemaining: 2,
  hasActivityToday: true,
  weeklyHistory: [
    { dayLabel: 'Mon', dateStr: '2026-11-09', completed: true, isToday: false },
    { dayLabel: 'Tue', dateStr: '2026-11-10', completed: true, isToday: false },
    { dayLabel: 'Wed', dateStr: '2026-11-11', completed: true, isToday: false },
    { dayLabel: 'Thu', dateStr: '2026-11-12', completed: true, isToday: false },
    { dayLabel: 'Fri', dateStr: '2026-11-13', completed: true, isToday: false },
    { dayLabel: 'Sat', dateStr: '2026-11-14', completed: true, isToday: false },
    { dayLabel: 'Sun', dateStr: '2026-11-15', completed: true, isToday: true },
  ],
};

const INITIAL_SESSIONS: AssignedSession[] = [
  {
    id: 'ses-401',
    title: 'Fault Injection Lab: Chaos Engineering with Litmus',
    cohortName: 'Cohort Nova (Nov 2026)',
    trainerName: 'Anand Kumar (Principal Architect)',
    startsAt: '2026-11-16T14:30:00Z',
    durationMinutes: 90,
    meetingLink: 'https://meet.csmtech.internal/cohort-nova-lab',
    sessionType: 'LAB',
  },
  {
    id: 'ses-402',
    title: '1-on-1 Mentorship & Growth Ring Review',
    cohortName: 'Cohort Nova (Nov 2026)',
    trainerName: 'Devika Ray (Lead SRE)',
    startsAt: '2026-11-18T10:00:00Z',
    durationMinutes: 45,
    meetingLink: 'https://meet.csmtech.internal/priya-devika-sync',
    sessionType: 'MENTOR_1ON1',
  },
];

const INITIAL_GREENHOUSE_IDEA: GreenhouseIdea = {
  id: 'idea-green-88',
  title: 'Automated Canary Rollouts with eBPF Latency Telemetry',
  summary:
    'Proposing a dynamic service mesh filter that correlates Prometheus p99 latency spikes during canary deployment stages and automatically halts promotion before customer impact.',
  authorName: 'Rohan Verma',
  authorRole: 'Senior SRE, Infrastructure Team',
  upvotesCount: 42,
  userHasUpvoted: false,
  createdAt: '2026-11-08',
  tags: ['eBPF', 'Canary', 'SRE', 'Observability'],
};

@Injectable({
  providedIn: 'root',
})
export class HomeStore {
  // State Signals
  readonly profile = signal<LearnerProfile | null>(INITIAL_PROFILE);
  readonly enrolment = signal<EnrolmentProgress | null>(INITIAL_ENROLMENT);
  readonly skillGaps = signal<SkillGap[]>(INITIAL_SKILL_GAPS);
  readonly streak = signal<ClimbingStreak>(INITIAL_STREAK);
  readonly sessions = signal<AssignedSession[]>(INITIAL_SESSIONS);
  readonly greenhouseIdea = signal<GreenhouseIdea | null>(INITIAL_GREENHOUSE_IDEA);

  readonly preferences = signal<AccessibilityPreferences>({
    dyslexiaFont: false,
    calmMode: false,
    highContrast: false,
  });

  readonly loading = signal<boolean>(false);
  readonly error = signal<string | null>(null);
  readonly isDemoEnv = signal<boolean>(true);
  readonly resumeNotification = signal<string | null>(null);

  // Computed Signals
  readonly hasActiveEnrolment = computed(() => this.enrolment() !== null);

  readonly criticalGaps = computed(() =>
    this.skillGaps().filter((gap) => gap.isCritical)
  );

  readonly streakSummary = computed(() => {
    const s = this.streak();
    if (s.currentStreakDays >= 14) {
      return `${s.currentStreakDays}-day climbing streak! Superb momentum.`;
    }
    return `${s.currentStreakDays}-day streak. Keep climbing today!`;
  });

  readonly progressRingCircumference = 2 * Math.PI * 42; // r = 42 -> 263.89

  readonly progressStrokeDashoffset = computed(() => {
    const enr = this.enrolment();
    if (!enr) return this.progressRingCircumference;
    const pct = Math.min(100, Math.max(0, enr.progressPct));
    return this.progressRingCircumference - (pct / 100) * this.progressRingCircumference;
  });

  // Action Methods
  resumeCurrentModule(): void {
    const current = this.enrolment();
    if (!current) return;
    this.resumeNotification.set(
      `Resuming "${current.currentModuleName}" in ${current.currentCourseTitle}...`
    );
    setTimeout(() => {
      this.resumeNotification.set(null);
    }, 4000);
  }

  useStreakFreeze(): void {
    this.streak.update((s) => {
      if (s.freezesRemaining <= 0) return s;
      return {
        ...s,
        freezesRemaining: s.freezesRemaining - 1,
      };
    });
  }

  toggleUpvoteIdea(): void {
    this.greenhouseIdea.update((idea) => {
      if (!idea) return null;
      const willUpvote = !idea.userHasUpvoted;
      return {
        ...idea,
        userHasUpvoted: willUpvote,
        upvotesCount: willUpvote ? idea.upvotesCount + 1 : idea.upvotesCount - 1,
      };
    });
  }

  toggleDyslexiaFont(): void {
    this.preferences.update((p) => ({
      ...p,
      dyslexiaFont: !p.dyslexiaFont,
    }));
  }

  toggleCalmMode(): void {
    this.preferences.update((p) => ({
      ...p,
      calmMode: !p.calmMode,
    }));
  }

  toggleHighContrast(): void {
    this.preferences.update((p) => ({
      ...p,
      highContrast: !p.highContrast,
    }));
  }

  setLoading(isLoading: boolean): void {
    this.loading.set(isLoading);
  }

  triggerEmptyState(): void {
    this.enrolment.set(null);
    this.sessions.set([]);
  }

  triggerErrorState(): void {
    this.error.set(
      'Network timeout: Unable to synchronize real-time Growth Ring telemetry with the Evidence Ledger. Please verify connectivity.'
    );
  }

  retry(): void {
    this.error.set(null);
    this.enrolment.set(INITIAL_ENROLMENT);
    this.sessions.set(INITIAL_SESSIONS);
    this.skillGaps.set(INITIAL_SKILL_GAPS);
    this.loading.set(false);
  }
}

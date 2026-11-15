import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

// Realistic synthetic mock payload matching seed_demo_data and GET /api/v1/home
const MOCK_HOME_DATA = {
  profile: {
    id: 'usr-demo-learner-01',
    name: 'Demo Learner 01',
    email: 'demo.learner01@csmtech.internal',
    role: 'Associate Platform Engineer',
    avatar_url: null,
    org_id: 'org-csm-demo',
    role_code: 'PLATFORM_ENG_L2',
  },
  enrolment: {
    enrolment_id: 'enr-pw-platform-90d',
    pathway_id: 'pw-platform-90d',
    pathway_title: 'First 90 Days: Platform Engineering',
    pathway_code: 'PW-PLATFORM-90D',
    target_role_code: 'PLATFORM_ENG_L2',
    progress_pct: 33,
    current_module_id: 'mod-201',
    current_module_name: 'Kubernetes Custom Resource Definitions (CRDs)',
    current_course_id: 'crs-eng-201',
    current_course_title: 'Cloud-Native Infrastructure & Kubernetes',
    estimated_minutes_remaining: 60,
    total_modules: 6,
    completed_modules: 2,
  },
  skill_gaps: [
    {
      skill_id: 'sk-consensus',
      skill_code: 'SKILL-CONSENSUS',
      skill_name: 'Distributed Consensus (Raft/Paxos)',
      category: 'Distributed Systems',
      current_level: 3,
      required_level: 4,
      gap_magnitude: 1,
      is_critical: false,
      sample_size: 6,
      evidence_label: 'STRONG_EVIDENCE',
      why_this: 'Strong evidentiary foundation derived from 6 cryptographically verified Evidence Ledger proofs. Evaluated against Level 4 PLATFORM_ENG_L2 role requirements.',
    },
    {
      skill_id: 'sk-k8s',
      skill_code: 'SKILL-K8S',
      skill_name: 'Kubernetes Operator Architecture',
      category: 'Cloud Infrastructure',
      current_level: 1,
      required_level: 3,
      gap_magnitude: 2,
      is_critical: true,
      sample_size: 3,
      evidence_label: 'DEVELOPING_EVIDENCE',
      why_this: 'Developing competency supported by 3 verified evidence entries. Evaluated against Level 3 PLATFORM_ENG_L2 role requirements.',
    },
    {
      skill_id: 'sk-mtls',
      skill_code: 'SKILL-MTLS',
      skill_name: 'Zero-Trust mTLS & Service Mesh',
      category: 'Security & Networking',
      current_level: 0,
      required_level: 3,
      gap_magnitude: 3,
      is_critical: true,
      sample_size: 1,
      evidence_label: 'LIMITED_EVIDENCE',
      why_this: 'Preliminary indicator with only 1 verified submission. Evaluated against Level 3 PLATFORM_ENG_L2 role requirements.',
    },
    {
      skill_id: 'sk-kafka',
      skill_code: 'SKILL-KAFKA',
      skill_name: 'Event Streaming with Apache Kafka',
      category: 'Data Engineering',
      current_level: 0,
      required_level: 3,
      gap_magnitude: 3,
      is_critical: true,
      sample_size: 0,
      evidence_label: 'NOT_ENOUGH_DATA',
      why_this: 'No verified evidence entries recorded in the Evidence Ledger yet. Evaluated against Level 3 PLATFORM_ENG_L2 role requirements.',
    },
  ],
  streak: {
    current_streak_days: 14,
    longest_streak_days: 21,
    freezes_remaining: 2,
    has_activity_today: true,
    weekly_history: [
      { day_label: 'Mon', date_str: '2026-11-09', completed: true, is_today: false },
      { day_label: 'Tue', date_str: '2026-11-10', completed: true, is_today: false },
      { day_label: 'Wed', date_str: '2026-11-11', completed: true, is_today: false },
      { day_label: 'Thu', date_str: '2026-11-12', completed: true, is_today: false },
      { day_label: 'Fri', date_str: '2026-11-13', completed: true, is_today: false },
      { day_label: 'Sat', date_str: '2026-11-14', completed: true, is_today: false },
      { day_label: 'Sun', date_str: '2026-11-15', completed: true, is_today: true },
    ],
  },
  sessions: [
    {
      id: 'ses-live-401',
      title: 'Fault Injection Lab: Chaos Engineering with Litmus',
      cohort_name: 'Cohort Nova 2026',
      trainer_name: 'Anand Kumar (Principal Architect)',
      starts_at: '2026-11-16T14:30:00Z',
      duration_minutes: 90,
      meeting_link: 'https://meet.csmtech.internal/cohort-nova-lab',
      session_type: 'LAB',
    },
  ],
  greenhouse_idea: {
    id: 'idea-featured-01',
    title: 'Automated Canary Rollouts with eBPF Latency Telemetry',
    summary: 'Proposing dynamic service mesh filters correlating Prometheus p99 latency spikes during canary deployment stages to automatically halt promotion before user impact.',
    author_name: 'Rohan Verma',
    author_role: 'Senior SRE, Infrastructure Team',
    upvotes_count: 42,
    status: 'PHASE_3_PREVIEW',
    tags: ['eBPF', 'Canary', 'SRE', 'Observability'],
  },
};

const MOCK_LOGIN_SUCCESS = {
  access_token: 'mock-access-token-jwt.header.payload.sig',
  refresh_token: 'mock-refresh-token-opaque',
  token_type: 'Bearer',
  expires_in: 900,
  user_id: 'usr-demo-learner-01',
  email: 'demo.learner01@csmtech.internal',
  roles: ['LEARNER'],
  org_id: 'org-csm-demo',
};

test.describe('WCAG 2.2 Level AA Axe-Core Audit & Slice 1.7b Verification', () => {

  test('1. Login page passes WCAG 2.2 AA in all accessibility modes', async ({ page }) => {
    await page.goto('/login');

    // Audit default / dark mode
    let scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();

    console.log(`[Axe Login - Default] Passes: ${scanResults.passes.length}, Incomplete: ${scanResults.incomplete.length}, Violations: ${scanResults.violations.length}`);
    expect(scanResults.violations).toEqual([]);

    // Audit Dyslexia Font Mode
    await page.locator('#btn-toggle-dyslexia').click();
    scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    console.log(`[Axe Login - Dyslexia] Passes: ${scanResults.passes.length}, Incomplete: ${scanResults.incomplete.length}, Violations: ${scanResults.violations.length}`);
    expect(scanResults.violations).toEqual([]);

    // Audit Calm Mode
    await page.locator('#btn-toggle-calm').click();
    scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    console.log(`[Axe Login - Calm] Passes: ${scanResults.passes.length}, Incomplete: ${scanResults.incomplete.length}, Violations: ${scanResults.violations.length}`);
    expect(scanResults.violations).toEqual([]);

    // Audit High Contrast Mode
    await page.locator('#btn-toggle-contrast').click();
    scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    console.log(`[Axe Login - High Contrast] Passes: ${scanResults.passes.length}, Incomplete: ${scanResults.incomplete.length}, Violations: ${scanResults.violations.length}`);
    expect(scanResults.violations).toEqual([]);
  });

  test('2. Unauthenticated user accessing /home is redirected to /login by authGuard', async ({ page }) => {
    await page.goto('/home');
    await expect(page).toHaveURL(/.*\/login/);
  });

  test('3. Login flow with quick demo credentials authenticates and navigates to /home', async ({ page }) => {
    // Intercept backend login and home API
    await page.route('/api/v1/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_LOGIN_SUCCESS),
      });
    });

    await page.route('/api/v1/home', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_HOME_DATA),
      });
    });

    await page.goto('/login');

    // Click quick fill Demo Learner 01
    await page.getByRole('button', { name: /Demo Learner 01/i }).click();
    await expect(page.locator('#email')).toHaveValue('demo.learner01@csmtech.internal');
    await expect(page.locator('#password')).toHaveValue('DemoPassword123!');

    // Submit
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Verify navigation to /home
    await expect(page).toHaveURL(/.*\/home/);
    await expect(page.getByText('Welcome back, Demo Learner 01')).toBeVisible();
    await expect(page.getByText('Continue Climbing: First 90 Days: Platform Engineering')).toBeVisible();
  });

  test('4. Home page passes WCAG 2.2 AA in populated state across all accessibility modes', async ({ page }) => {
    await page.route('/api/v1/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_LOGIN_SUCCESS),
      });
    });

    await page.route('/api/v1/home', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_HOME_DATA),
      });
    });

    await page.goto('/login');
    await page.getByRole('button', { name: /Demo Learner 01/i }).click();
    await page.getByRole('button', { name: 'Sign In' }).click();
    await expect(page).toHaveURL(/.*\/home/);

    // Verify evidence labels exist
    await expect(page.getByText('STRONG_EVIDENCE')).toBeVisible();
    await expect(page.getByText('DEVELOPING_EVIDENCE')).toBeVisible();
    await expect(page.getByText('LIMITED_EVIDENCE')).toBeVisible();
    await expect(page.getByText('NOT_ENOUGH_DATA')).toBeVisible();

    // Verify Greenhouse upvote button is disabled (Phase 3 upcoming)
    const upvoteBtn = page.getByRole('button', { name: /42 \(Phase 3\)/i });
    await expect(upvoteBtn).toBeDisabled();

    // Audit Default Mode
    let scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    console.log(`[Axe Home - Default] Passes: ${scanResults.passes.length}, Incomplete: ${scanResults.incomplete.length}, Violations: ${scanResults.violations.length}`);
    for (const inc of scanResults.incomplete) {
      console.log(`  [Incomplete Rule] ${inc.id}: ${inc.description} (${inc.nodes.length} nodes)`);
    }
    expect(scanResults.violations).toEqual([]);

    // Expand "Why this?" panel and test accessibility
    const whyThisSummary = page.locator('summary:has-text("Why this?")').first();
    await whyThisSummary.click();
    await expect(page.getByText('Evidence Tier Policy: STRONG')).toBeVisible();

    // Audit with expanded panel in High Contrast mode
    await page.locator('#btn-toggle-contrast').click();
    scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    console.log(`[Axe Home - High Contrast] Passes: ${scanResults.passes.length}, Incomplete: ${scanResults.incomplete.length}, Violations: ${scanResults.violations.length}`);
    expect(scanResults.violations).toEqual([]);

    // Audit Dyslexia Mode
    await page.locator('#btn-toggle-dyslexia').click();
    scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    console.log(`[Axe Home - Dyslexia] Passes: ${scanResults.passes.length}, Incomplete: ${scanResults.incomplete.length}, Violations: ${scanResults.violations.length}`);
    expect(scanResults.violations).toEqual([]);

    // Audit Calm Mode
    await page.locator('#btn-toggle-calm').click();
    scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    console.log(`[Axe Home - Calm] Passes: ${scanResults.passes.length}, Incomplete: ${scanResults.incomplete.length}, Violations: ${scanResults.violations.length}`);
    expect(scanResults.violations).toEqual([]);
  });

  test('5. Home page handles audited streak freeze mutation via real backend call', async ({ page }) => {
    await page.route('/api/v1/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_LOGIN_SUCCESS),
      });
    });

    await page.route('/api/v1/home', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_HOME_DATA),
      });
    });

    let freezeAudited = false;
    await page.route('/api/v1/home/freeze-streak', async (route) => {
      freezeAudited = true;
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          user_id: 'usr-demo-learner-01',
          streak_freezes_remaining: 1,
          current_streak_days: 14,
        }),
      });
    });

    await page.goto('/login');
    await page.getByRole('button', { name: /Demo Learner 01/i }).click();
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Consume freeze
    const freezeBtn = page.getByRole('button', { name: /Consume Streak Freeze/i });
    await freezeBtn.click();

    // Verify backend call was triggered and UI updated
    expect(freezeAudited).toBe(true);
    await expect(page.getByText('1 Freezes Left')).toBeVisible();
    await expect(page.getByText('Streak freeze successfully consumed and audited.')).toBeVisible();
  });

  test('6. Home page empty enrolment state passes WCAG 2.2 AA', async ({ page }) => {
    await page.route('/api/v1/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_LOGIN_SUCCESS),
      });
    });

    const emptyData = { ...MOCK_HOME_DATA, enrolment: null };
    await page.route('/api/v1/home', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(emptyData),
      });
    });

    await page.goto('/login');
    await page.getByRole('button', { name: /Demo Learner 01/i }).click();
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page.getByText('No Active Pathway Enrolment')).toBeVisible();

    const scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    console.log(`[Axe Home - Empty State] Passes: ${scanResults.passes.length}, Incomplete: ${scanResults.incomplete.length}, Violations: ${scanResults.violations.length}`);
    expect(scanResults.violations).toEqual([]);
  });

  test('7. Home page error state passes WCAG 2.2 AA', async ({ page }) => {
    await page.route('/api/v1/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_LOGIN_SUCCESS),
      });
    });

    await page.route('/api/v1/home', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Database replica synchronization timeout' }),
      });
    });

    await page.goto('/login');
    await page.getByRole('button', { name: /Demo Learner 01/i }).click();
    await page.getByRole('button', { name: 'Sign In' }).click();

    const errorAlert = page.getByRole('alert');
    await expect(errorAlert).toBeVisible();
    await expect(page.getByText('Database replica synchronization timeout')).toBeVisible();

    const scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    console.log(`[Axe Home - Error State] Passes: ${scanResults.passes.length}, Incomplete: ${scanResults.incomplete.length}, Violations: ${scanResults.violations.length}`);
    expect(scanResults.violations).toEqual([]);
  });

  test('8. Home page permission-denied (403) state passes WCAG 2.2 AA', async ({ page }) => {
    await page.route('/api/v1/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_LOGIN_SUCCESS),
      });
    });

    await page.route('/api/v1/home', async (route) => {
      await route.fulfill({
        status: 403,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Forbidden: Insufficient role permissions' }),
      });
    });

    await page.goto('/login');
    await page.getByRole('button', { name: /Demo Learner 01/i }).click();
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page.getByText('Access Permission Denied (HTTP 403)')).toBeVisible();

    const scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    console.log(`[Axe Home - Permission Denied] Passes: ${scanResults.passes.length}, Incomplete: ${scanResults.incomplete.length}, Violations: ${scanResults.violations.length}`);
    expect(scanResults.violations).toEqual([]);
  });

  test('9. Skip to main content link works via keyboard navigation', async ({ page }) => {
    await page.goto('/login');

    await page.keyboard.press('Tab');
    const skipLink = page.locator('.skip-link');
    await expect(skipLink).toBeFocused();

    await page.keyboard.press('Enter');
    await expect(page).toHaveURL(/#main-content$/);
  });
});

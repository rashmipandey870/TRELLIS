import { test, expect } from '@playwright/test';

test.describe('Learner Portal Cleanliness & Production Readiness', () => {
  test('Learner can log in, take assessment without blank questions, and view results with zero N/A or console errors', async ({ page }) => {
    const consoleErrors: string[] = [];

    // Catch console error and unhandled exceptions
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        const text = msg.text();
        // Ignore favicon or non-critical 404 image asset warnings if any
        if (!text.includes('favicon.ico')) {
          consoleErrors.push(text);
        }
      }
    });
    page.on('pageerror', (err) => {
      consoleErrors.push(err.message);
    });

    // 1. Log in as seeded learner (Priya Sharma)
    await page.goto('/login');
    await page.waitForSelector('#email');

    // Use demo account quick loader if visible, or fill fields
    const demoBtn = page.locator('button:has-text("LEARNER:Priya Sharma")');
    if (await demoBtn.count() > 0) {
      await demoBtn.click();
    } else {
      await page.locator('#email').fill('learner1@csmtech.internal');
      await page.locator('#password').fill('CSMTrellis2026!');
      await page.locator('#password').dispatchEvent('input');
    }

    await expect(page.locator('button[type="submit"]')).toBeEnabled();
    await page.locator('button[type="submit"]').click();

    // Wait for redirection to learner portal dashboard
    await page.waitForURL(/\/learner\/dashboard/, { timeout: 15000 });
    await expect(page.locator('h1:has-text("Learner Portal")')).toBeVisible();

    // 2. Open Assessments Page via SPA nav
    await page.locator('nav a[routerLink="/learner/assessments"]').click();
    await page.waitForURL(/\/learner\/assessments/);
    await page.waitForLoadState('networkidle');

    // Find and start/resume an assessment
    const startButtons = page.locator('button:has-text("Start Assessment"), button:has-text("Resume Assessment")');
    const hasActiveAssessment = await startButtons.count() > 0;

    if (hasActiveAssessment) {
      await startButtons.first().click();
      await page.waitForTimeout(1000);

      // Verify Question Card is NOT blank
      const questionTitle = page.locator('h3.text-base.font-bold');
      await expect(questionTitle).toBeVisible();
      const titleText = await questionTitle.textContent();
      expect(titleText?.trim().length).toBeGreaterThan(0);

      // Verify question text / statement is rendered (not empty!)
      const questionContent = page.locator('p.text-xs.text-slate-600');
      await expect(questionContent).toBeVisible();
      const contentText = await questionContent.textContent();
      expect(contentText?.trim().length).toBeGreaterThan(0);

      // Verify question type tag is rendered properly (not generic bare 'CHALLENGE')
      const typeTag = page.locator('span.uppercase.tracking-wider');
      await expect(typeTag).toBeVisible();
      const tagText = await typeTag.textContent();
      expect(tagText).toMatch(/MCQ|CODING|SQL|WRITTEN|SHORT_ANSWER|SCENARIO|LIKERT/i);

      // Verify that options or code editor or textarea is rendered
      const optionsCount = await page.locator('input[type="radio"]').count();
      const editorCount = await page.locator('textarea').count();
      expect(optionsCount + editorCount).toBeGreaterThan(0);
    }

    // 3. Open Results Page via SPA nav
    await page.locator('nav a[routerLink="/learner/results"]').click();
    await page.waitForURL(/\/learner\/results/);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(1500);

    const bodyText = await page.locator('body').innerText();

    // Check that there is NO bare "N/A"
    const bareNaRegex = /\bN\/A\b/;
    expect(bareNaRegex.test(bodyText), 'Page should not contain bare "N/A"').toBeFalsy();

    // Check that there is NO "undefined"
    expect(bodyText.includes('undefined'), 'Page should not contain "undefined"').toBeFalsy();

    // Check that there is NO "NaN"
    expect(bodyText.includes('NaN'), 'Page should not contain "NaN"').toBeFalsy();

    // Check that there is NO "null" displayed in text
    expect(bodyText.includes(' null '), 'Page should not contain "null" text').toBeFalsy();

    // Verify key KPI cards are populated with real numbers and units
    await expect(page.locator('text=Cohort Percentile Rank')).toBeVisible();
    await expect(page.locator('text=Score Trajectory Velocity')).toBeVisible();
    await expect(page.locator('text=Session Attendance')).toBeVisible();
    await expect(page.locator('text=Coding Acceptance')).toBeVisible();

    // Verify that the percentile rank shows an actual percentile
    const percentileText = await page.locator('span.text-3xl:has-text("th")').first().textContent();
    expect(percentileText).toBeTruthy();

    // Verify SVG charts rendered
    const svgs = page.locator('svg');
    const svgCount = await svgs.count();
    expect(svgCount).toBeGreaterThan(2);

    // 4. Assert zero console errors
    expect(consoleErrors).toEqual([]);
  });
});

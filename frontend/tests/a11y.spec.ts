import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Automated Axe-Core Accessibility Audit & Keyboard Walkthrough (Slice 1.7)', () => {
  test('homepage passes WCAG 2.2 Level AA accessibility rules with 0 violations', async ({ page }) => {
    await page.goto('/');

    const scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();

    console.log(
      `[Axe Audit] Evaluated rules: ${scanResults.passes.length} passed, ${scanResults.incomplete.length} incomplete`
    );
    console.log(`[Axe Audit] Violations detected: ${scanResults.violations.length}`);

    if (scanResults.violations.length > 0) {
      console.error(JSON.stringify(scanResults.violations, null, 2));
    }

    expect(scanResults.violations).toEqual([]);
  });

  test('skip-to-main-content link becomes visible on focus and jumps to main landmark', async ({ page }) => {
    await page.goto('/');

    // Initial state: tab into page to focus skip link
    await page.keyboard.press('Tab');
    const skipLink = page.locator('.skip-link');
    await expect(skipLink).toBeFocused();

    // Trigger skip link
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL(/#main-content$/);
  });

  test('accessibility preferences: dyslexia font, calm mode, and high contrast toggle correctly', async ({ page }) => {
    await page.goto('/');

    const main = page.locator('#main-content');

    // 1. Dyslexia font toggle
    const dyslexiaBtn = page.locator('#btn-toggle-dyslexia');
    await dyslexiaBtn.click();
    await expect(main).toHaveClass(/dyslexia-mode/);
    await expect(dyslexiaBtn).toHaveAttribute('aria-pressed', 'true');

    // 2. Calm mode toggle
    const calmBtn = page.locator('#btn-toggle-calm');
    await calmBtn.click();
    await expect(main).toHaveClass(/calm-mode/);
    await expect(calmBtn).toHaveAttribute('aria-pressed', 'true');

    // 3. High contrast mode toggle
    const contrastBtn = page.locator('#btn-toggle-contrast');
    await contrastBtn.click();
    await expect(main).toHaveClass(/high-contrast/);
    await expect(contrastBtn).toHaveAttribute('aria-pressed', 'true');
  });

  test('interactive controls: resume learning, upvote idea, and use streak freeze work reactively', async ({ page }) => {
    await page.goto('/');

    // 1. Resume learning button
    const resumeBtn = page.getByRole('button', { name: /Resume Learning/i });
    await resumeBtn.click();
    const notification = page.getByRole('status');
    await expect(notification).toBeVisible();
    await expect(notification).toContainText('Resuming "Module 3: Raft Consensus');

    // 2. Upvote idea in Greenhouse spotlight
    const upvoteBtn = page.getByRole('button', { name: /Upvote 42/i });
    await upvoteBtn.click();
    const upvotedBtn = page.getByRole('button', { name: /Upvote 43/i });
    await expect(upvotedBtn).toBeVisible();
    await expect(upvotedBtn).toHaveAttribute('aria-pressed', 'true');

    // 3. Use streak freeze
    const freezeBtn = page.getByRole('button', { name: /Use Streak Freeze/i });
    await freezeBtn.click();
    const freezeBadge = page.getByLabel(/streak freezes remaining/i);
    await expect(freezeBadge).toContainText('1 Freezes Left');
  });

  test('accessible states: error card and empty state can be triggered and recovered', async ({ page }) => {
    await page.goto('/');

    // Trigger Error State
    const triggerErrBtn = page.getByRole('button', { name: /Trigger Error State/i });
    await triggerErrBtn.click();
    const errorAlert = page.getByRole('alert');
    await expect(errorAlert).toBeVisible();
    await expect(errorAlert).toContainText('Synchronisation Error Encountered');

    // Recover via retry
    const retryBtn = page.getByRole('button', { name: /Retry Telemetry Synchronisation/i });
    await retryBtn.click();
    await expect(errorAlert).not.toBeVisible();

    // Trigger Empty State
    const triggerEmptyBtn = page.getByRole('button', { name: /Trigger Empty State/i });
    await triggerEmptyBtn.click();
    await expect(page.getByText('No Active Pathway Enrolment')).toBeVisible();

    // Reset Demo
    const resetBtn = page.getByRole('button', { name: /Reset Demo/i });
    await resetBtn.click();
    await expect(page.getByText('Continue Climbing:')).toBeVisible();
  });
});

import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Automated Axe-Core Accessibility Audit', () => {
  test('homepage passes WCAG 2.2 Level AA accessibility rules', async ({ page }) => {
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
});

import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:4200',
    headless: true,
  },
  projects: [
    {
      name: 'chromium',
      // Use the Playwright-bundled Chromium (no system Chrome required)
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    // Run ng serve so the Angular dev server is always available
    command: 'npx ng serve --port 4200 --host 127.0.0.1 --no-open',
    url: 'http://127.0.0.1:4200',
    // Reuse the already-running ng serve instance (avoids dual-server conflicts)
    reuseExistingServer: true,
    timeout: 120000,
  },
});

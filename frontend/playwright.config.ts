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
      use: { ...devices['Desktop Chrome'], channel: 'chrome' },
    },
  ],
  webServer: {
    command: 'node ./node_modules/http-server/bin/http-server dist/frontend/browser -a 127.0.0.1 -p 4200 -c-1',
    url: 'http://127.0.0.1:4200',
    reuseExistingServer: false,
    timeout: 30000,
  },
});

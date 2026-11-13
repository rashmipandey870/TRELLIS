# TRELLIS Accessibility Verification & Test Plan (WCAG 2.2 AA)

## 1. Governance & Release Gate
Accessibility is a strict release gate for TRELLIS. No pull request or phase deliverable can be marked done if automated or manual accessibility checks fail.

### Standards & Targets
- **Conformance Target**: WCAG 2.2 Level AA.
- **CI Automated Gate**: Zero violations reported by `@axe-core/playwright` across all primary routes.
- **Lighthouse CI Budget**: Accessibility score $\ge 98$ across mobile and desktop viewport profiles.
- **Cognitive Accessibility**: Full compliance with the Cognitive Accessibility Suite (Signature Innovation #12).

---

## 2. Automated Testing Pipeline (Playwright + Axe-Core)

### Automated Test Specifications
Every Angular view has an automated Playwright spec that injects Axe:
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility Audit', () => {
  test('Home page meets WCAG 2.2 AA standards', async ({ page }) => {
    await page.goto('/home');
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(accessibilityScanResults.violations).toEqual([]);
  });
});
```

### Automated Checkpoints
1. **Color Contrast**: Automated verification of $\ge 4.5:1$ on text and $\ge 3:1$ on form inputs, active button boundaries, and focus rings.
2. **Form Labels & Error Associations**: Every input has an explicit `<label for="...">` or `aria-labelledby`, and error messages are programmatically linked via `aria-describedby` and `aria-invalid="true"`.
3. **Heading Hierarchy**: Exactly one `<h1>` per page, followed by strict logical nesting (`<h2>`, `<h3>`) without skipping levels.
4. **Data Table Equivalents**: Every chart (e.g. Growth Ring radar) must possess an associated `<table>` with appropriate `<th> scope="col"` headers and text summaries.

---

## 3. Manual Keyboard Navigation Walkthrough Protocol

| Test Case | Interaction Steps | Expected Pass Behavior |
|---|---|---|
| **KB-01: Skip Link** | Press `Tab` immediately upon page load. | "Skip to main content" link becomes visible at the top-left; pressing `Enter` focuses `<main id="main-content">`. |
| **KB-02: Command Bar** | Press `Ctrl+K` (or `Cmd+K` on Mac). | Command bar modal opens, focus moves automatically to the search input, focus is trapped within the dialog, and pressing `Escape` closes the modal and restores focus. |
| **KB-03: Focus Indicators** | Tab through all interactive elements in the Home and Pathways screens. | Every button, link, and input exhibits a high-contrast 2px solid cyan/blue focus ring with a 2px offset. No element has `outline: none` without an alternative. |
| **KB-04: Modal Trapping** | Open a confirmation dialog (e.g. Consent Passport revoke confirmation). | Tabbing cycles exclusively through dialog buttons; background elements receive `aria-hidden="true"`; `Escape` cancels the dialog. |
| **KB-05: Code Editor** | Tab into Monaco Editor in Growth Check. | Editor instructions announce how to exit (`Ctrl+M` or `Escape` to toggle tab-trapping mode), preventing keyboard traps. |

---

## 4. Assistive Technology Verification Matrix

| Assistive Tech | Browser & Platform | Key Verification Criteria |
|---|---|---|
| **NVDA** | Firefox / Windows 11 | Full speech announcements of live regions (`aria-live="polite"` for assessment timers, notifications); clean reading of Growth Ring data tables. |
| **JAWS** | Chrome / Windows 11 | Virtual cursor navigation across landmarks (`banner`, `navigation`, `main`, `contentinfo`); form field validation announcements. |
| **VoiceOver** | Safari / macOS & iOS | Rotor navigation by headings and landmarks; gesture navigation on touch devices. |
| **TalkBack** | Chrome / Android | Linear swipe navigation across micro-learning cards; accessible button hit targets ($\ge 44 \times 44$ CSS px). |

---

## 5. Cognitive Accessibility Suite Testing (Signature Innovation #12)
1. **Focus Mode**: When activated, hides secondary navigation, cohort feeds, and streaks. Test: user can complete a lesson without distractive layout shifts.
2. **Chunked Lessons**: Breaks long-form text into bite-sized cards with progress counters. Test: max 300 words per card before action prompt.
3. **Plain-Language Rewrite**: Toggles simplified summary text for complex technical concepts.
4. **Reading Ruler**: Translucent guide follows cursor position to assist line-tracking.
5. **Dyslexia Font Support**: Selects OpenDyslexic or Atkinson Hyperlegible, increasing character kerning by 15% and line-height by 25%.
6. **Adjustable Pacing & Pausable Timers**: Accommodations flow allows pausable timers and $1.5\times$ to $2.0\times$ time extensions for neurodivergent learners without stigmatizing labels or trainer notification of medical reasons.

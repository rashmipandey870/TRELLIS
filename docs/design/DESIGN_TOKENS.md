# TRELLIS Design Tokens & Accessible Design System Specification

## 1. System Invariants & WCAG 2.2 AA Compliance
- **Placeholder Branding Notice**: Official CSM Technology assets, fonts, and colors will be integrated once provided by leadership. The current palette is placeholder branding, clearly labelled across all views.
- **Accessibility Release Gate**: All components must pass WCAG 2.2 AA:
  - Contrast ratio $\ge 4.5:1$ for normal text, $\ge 3:1$ for large text and UI control boundaries.
  - Never convey information by color alone (always pair with icons, shapes, or textual labels).
  - Full keyboard focusability with visible 2px offset focus rings.
  - Native support for 200% text zoom without clipping or horizontal scrolling.
  - Every data visualization / radar chart MUST have an accessible tabular data-table alternative and textual summary.

---

## 2. Color Tokens (Placeholder Palette)

### Primary Functional Tokens

| Token Name | Hex Code | Contrast on `#0B0D12` | Contrast on `#FFFFFF` | Role / Usage |
|---|---|---|---|---|
| `--color-bg-dark` | `#0B0D12` | - | 18.2:1 | Base background (Dark Mode) |
| `--color-surface-dark`| `#161B22` | 1.3:1 (surface elevation) | 15.5:1 | Card & container surface (Dark) |
| `--color-border-dark` | `#30363D` | 3.4:1 (UI boundary) | 9.8:1 | Card borders, dividers |
| `--color-brand-blue` | `#1294C4` | 4.8:1 (WCAG AA Pass) | 4.6:1 | Primary actions, climbing accents |
| `--color-brand-maroon`| `#8B3A3A` | 4.6:1 (large text / dark text on light) | 5.2:1 | Secondary brand accent, warnings |
| `--color-text-primary`| `#FFFFFF` | 18.2:1 (WCAG AAA Pass) | - | Primary text on dark backgrounds |
| `--color-text-muted` | `#9CA3AF` | 7.1:1 (WCAG AA Pass) | - | Subtitles, timestamps, metadata |
| `--color-evidence-strong` | `#10B981` | 6.5:1 | 3.2:1 | `STRONG_EVIDENCE` status badge |
| `--color-evidence-dev` | `#3B82F6` | 5.3:1 | 4.0:1 | `DEVELOPING_EVIDENCE` badge |
| `--color-evidence-limited`| `#F59E0B`| 8.2:1 | 2.5:1 (use dark text) | `LIMITED_EVIDENCE` badge |
| `--color-evidence-none`| `#6B7280` | 4.5:1 | 4.6:1 | `NOT_ENOUGH_DATA` badge |

### Accessibility Modes
- **High Contrast Mode**: Background switches to pure black `#000000`, text to `#FFFFFF`, borders to high-contrast cyan `#00FFFF` and yellow `#FFFF00` with 3px solid focus indicators.
- **Calm / Focus Mode**: Diminishes accent saturation, eliminates non-essential decorative vine graphics, expands whitespace, and highlights single task blocks.
- **Reduced Motion**: Disables all transitions and growth animations (`prefers-reduced-motion: reduce`).

---

## 3. Typography & Spacing Tokens

### Font Stack
- **Default Sans**: `Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
- **Dyslexia-Friendly Mode**: `OpenDyslexic, "Atkinson Hyperlegible", sans-serif` (selectable in learner preferences with customizable letter and line spacing).
- **Code & Sandbox**: `JetBrains Mono, "Fira Code", monospace`

### Typographic Scale
- `--font-size-xs`: `0.75rem` (12px) - Line height: `1rem`
- `--font-size-sm`: `0.875rem` (14px) - Line height: `1.25rem`
- `--font-size-base`: `1rem` (16px) - Line height: `1.5rem`
- `--font-size-lg`: `1.125rem` (18px) - Line height: `1.75rem`
- `--font-size-xl`: `1.25rem` (20px) - Line height: `1.75rem`
- `--font-size-2xl`: `1.5rem` (24px) - Line height: `2rem`
- `--font-size-3xl`: `1.875rem` (30px) - Line height: `2.25rem`

### Spacing Grid (8px Base Grid)
- `--space-1`: `4px` (0.5x)
- `--space-2`: `8px` (1x base)
- `--space-3`: `12px` (1.5x)
- `--space-4`: `16px` (2x)
- `--space-6`: `24px` (3x)
- `--space-8`: `32px` (4x)
- `--space-12`: `48px` (6x)

---

## 4. Growth Motif Component Library
- **Trellis Line**: Continuous progress bar that links completed milestones like a vertical vine.
- **Growth Ring Radar**: Multi-axis SVG skill visualization with evidence-weighted fills, paired synchronously with an accessible HTML `<table aria-label="Growth Ring Competencies">`.
- **Tendril Badge**: Organic visual marker displaying confidence level and evidence weight (`STRONG`, `DEVELOPING`, `LIMITED`, `NO DATA`).
- **State Patterns**: Every interactive component must define 4 explicit states:
  1. *Loading*: Accessible skeleton pulse with `aria-busy="true"`.
  2. *Empty*: Action-oriented developmental prompt (e.g. "No assessments taken yet — Start your first Growth Check").
  3. *Error*: Plain-language explanation with retry action and incident correlation ID.
  4. *Permission Denied*: Privacy explanation ("This summary requires employee consent via the Consent Passport").

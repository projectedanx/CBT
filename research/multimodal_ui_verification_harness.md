# RESEARCH BLUEPRINT 3: Self-Healing Multimodal UI Verification Harness via Agent-Driven Playwright Replay Loops
# AUTHOR: VULCAN / AXIOM v1.0
# STATUS: DRAFT-CONDITIONED

## 1. Test-Driven Visual Spec

The user inputs a visual artifact (image or PDF). The Multimodal Agent generates a Playwright test script defining the structural assertions.

```typescript
// Playwright script generated from UI spec image
import { test, expect } from '@playwright/test';

test('Verify Primary CTA Button Layout', async ({ page }) => {
  await page.goto('http://localhost:4200');
  const cta = page.locator('#primary-submit');

  // Assertions derived from spatial design constraints
  await expect(cta).toBeVisible();
  const box = await cta.boundingBox();
  expect(box?.width).toBeGreaterThanOrEqual(120);
  expect(box?.height).toBe(48);

  // Assert CSS color constraints
  await expect(cta).toHaveCSS('background-color', 'rgb(0, 255, 65)');
});
```

This establishes the failure baseline (Red Phase).

## 2. Automated Layout Grading & Code Repair

The browser executes the test. Upon failure, a screenshot is captured and sent to the Vision model alongside the source HTML/CSS.

```json
{
  "jsonrpc": "2.0",
  "method": "analyze_visual_delta",
  "params": {
    "baseline_spec_hash": "a1b2c3d4",
    "execution_screenshot_base64": "iVBORw0KGgo...",
    "playwright_error_log": "Expected height to be 48, received 32",
    "target_component_file": "src/app/cta.component.ts"
  },
  "id": 1
}
```

The model generates a precise CSS diff altering the bounding box or alignment properties to satisfy the Playwright assertions.

## 3. Verification and Checkpointing

Atomic filesystem snapshots provide rollback mechanisms prior to visual diff application.

```bash
#!/bin/bash
# Pre-mutation checkpoint sequence
SNAPSHOT_ID=$(date +%s)
git stash save "AUTO_SNAPSHOT_${SNAPSHOT_ID}"

# Apply generated patch
git apply visual_fix.patch

# Execute verification
npx playwright test cta.spec.ts
if [ $? -ne 0 ]; then
  # Rollback on regression
  git reset --hard HEAD
  git stash pop
  return 1
fi
```

If the verification script fails, the DOM reverts to the pre-mutation state instantly.

## 4. Symbolic Scar Integration

If a generated visual fix introduces a secondary layout shift (e.g., breaking adjacent flexbox constraints):

```yaml
# SSR-20261012-003
trigger: "CSS fix on #primary-submit altered global flex alignment."
failure_mode: "Visual Regression: Adjacent #cancel-button shifted out of viewport."
prevention_directive: "Do not use margin-top for button alignment within flex containers. Use align-items on the parent node."
severity: "MEDIUM"
```

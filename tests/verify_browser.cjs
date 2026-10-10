// Optional browser regression check. See tests/README.md.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');

(async () => {
  const options = { headless: true };
  if (process.env.PLAYWRIGHT_EXECUTABLE_PATH) {
    options.executablePath = process.env.PLAYWRIGHT_EXECUTABLE_PATH;
  }
  const browser = await chromium.launch(options);
  try {
    const page = await browser.newPage({ viewport: { width: 1360, height: 1100 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(pathToFileURL(path.join(__dirname, '..', 'docs', 'index.html')).href);
    await page.waitForSelector('[data-stage="capture"]');
    assert.equal(await page.locator('[data-stage]').count(), 7);
    assert.equal(await page.locator('#publish-option').isDisabled(), true);
    await page.locator('#map-option').check();
    await page.locator('#write-option').check();
    await page.locator('#publish-option').check();
    assert.equal(await page.locator('[data-stage]').count(), 10);

    for (const id of ['capture', 'clarify', 'verify', 'connect', 'organize', 'save', 'map', 'draft', 'publish', 'review']) {
      await page.locator(`[data-stage="${id}"]`).click();
      assert.equal(await page.locator('[aria-current="step"]').getAttribute('data-stage'), id);
      assert.ok((await page.locator('#stage-title').textContent()).length);
    }
    assert.equal(await page.locator('#next').isDisabled(), true);
    await page.locator('#previous').click();
    assert.equal(await page.locator('[aria-current="step"]').getAttribute('data-stage'), 'publish');
    await page.locator('#write-option').uncheck();
    assert.equal(await page.locator('#publish-option').isChecked(), false);
    assert.equal(await page.locator('#publish-option').isDisabled(), true);
    assert.equal(await page.locator('[data-stage="publish"]').count(), 0);
    await page.locator('#write-option').check();
    assert.equal(await page.locator('[data-stage="publish"]').count(), 0, 'New draft must not reuse prior approval');
    await page.locator('[data-stage="capture"]').click();
    assert.equal(await page.locator('#previous').isDisabled(), true);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);

    const screenshots = process.env.BROWSER_SCREENSHOT_DIR;
    if (screenshots) {
      fs.mkdirSync(screenshots, { recursive: true });
      await page.screenshot({ path: path.join(screenshots, 'desktop.png'), fullPage: false });
    }
    await page.setViewportSize({ width: 390, height: 844 });
    await page.reload();
    await page.waitForSelector('[data-stage="capture"]');
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    assert.equal(await page.locator('header').count(), 1);
    await page.locator('#map-option').focus();
    await page.keyboard.press('Space');
    assert.equal(await page.locator('#map-option').isChecked(), true);
    await page.keyboard.press('Tab');
    assert.equal(await page.locator('#write-option').evaluate(el => el === document.activeElement), true);
    if (screenshots) {
      await page.screenshot({ path: path.join(screenshots, 'mobile.png'), fullPage: false });
    }
    assert.deepEqual(errors, []);
    console.log('Browser checks passed: all stages, approval reset, boundary navigation, keyboard controls, desktop/mobile overflow, no page errors.');
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});

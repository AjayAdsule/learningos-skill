# Test coverage

## Default package checks (no third-party libraries)

From the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/test_flow.cjs
```

These check the public package, relative links, privacy patterns, optional branches and publication gate. They do not prove LLM behavior or external integration access.

## Optional real-browser checks

Install Playwright as a development-only dependency and its Chromium browser:

```sh
npm install --no-save --package-lock=false playwright
npx playwright install chromium
node tests/verify_browser.cjs
```

The check opens the local HTML file without a server. It exercises all stages, publication-approval reset, Previous/Next boundaries, keyboard controls and desktop/mobile overflow, and rejects browser page errors. It uses a fresh isolated browser, not your logged-in browser profile.

If you want to use an already installed Chromium-family browser, supply its executable path through `PLAYWRIGHT_EXECUTABLE_PATH` using your platform's environment-variable syntax. Optional screenshots are saved only when `BROWSER_SCREENSHOT_DIR` is set; choose a folder outside this repository. Neither setting contains a credential.

Browser automation is optional and is not included in the default CI job. The skill and offline guide do not need Playwright or Node to be used.

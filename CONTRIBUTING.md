# Contributing to LearningOS

## Scope

Improve this community skill through focused pull requests. Keep it a usable learning procedure—not a router that requires private sibling skills, an autonomous publishing service or a collection of unsupported claims.

Discuss substantial workflow changes in an issue before implementation. Bugs, unclear steps, accessibility improvements and source-grounding improvements are welcome.

## Local verification

1. Read `skills/learningos/SKILL.md` and the relevant reference/template.
2. Make a focused change. Preserve original wording, authentic reflections, one-question-at-a-time learning and explicit publication approval.
3. For guide behavior, write a failing test in `tests/test_flow.cjs` before implementing the change.
4. Run:

   ```sh
   python3 -m unittest discover -s tests -p 'test_*.py' -v
   node --test tests/test_flow.cjs
   gitleaks dir . --redact --no-banner
   gitleaks git . --redact --no-banner
   ```

5. Open `docs/index.html` and inspect desktop and mobile layouts. Test every optional branch, Previous/Next controls and keyboard focus. Confirm the browser console has no errors.
6. Review the complete staged diff and file list before committing. Use fictional examples, never real learner notes or credentials. `.gitignore` is not a substitute for review.
7. Open a pull request describing the behavior change, exact checks performed and any limits. Do not claim real model behavior, integration access or publication success based only on package tests.

Requirements: Python 3.9+, Node.js 18+ and Gitleaks for the optional local secret scan. The skill itself does not depend on Node or Gitleaks. CI runs package/flow tests and Gitleaks for pull requests without needing repository secrets.

## Skill conventions

Keep frontmatter valid, `name: learningos`, a description no longer than 60 characters ending in a period, human attribution, semver, license and audited platform support. Keep related skill references empty unless they really exist in the target distribution. Put branch-specific details in references and update the README when the public flow changes.

## Sharing and upstream contribution

Anyone can inspect/install the skill from this repository. This is not an official catalog listing. For an upstream contribution, read the current [Hermes contribution guide](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) and [skill authoring guide](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills), survey existing skills, and choose the tier/category required by maintainers. Do not assume this standalone repository's `skills/learningos/` path is the right upstream path.

Upstream tests and generated docs are repository-specific and must be run inside an actual upstream checkout; the tests here do not replace them. Acceptance is the maintainers' decision. No upstream pull request is implied by publishing this package.

## Privacy reports

Never put secrets or private notes in an issue. Follow `SECURITY.md` if you discover an exposure.

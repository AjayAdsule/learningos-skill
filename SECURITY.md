# Security and privacy

## What this repository should contain

Only reusable skill instructions, generic templates, documentation, fictional examples and tests. Personal notes, uploads, reflections, drafts, private destination IDs, integration settings, credentials and session history must stay outside this repository.

Public contributor identity and public GitHub project URLs are intentional attribution, not runtime account configuration. Use GitHub's noreply address in commits if you do not want a personal email address exposed.

## Pre-publication checklist

- Review the complete staged file list and diff, not only the working directory.
- Scan both files and Git history with Gitleaks using `--redact`.
- Check for personal paths, private destinations, unapproved emails, real notes and screenshots. Pattern scanning does not catch every form of private information.
- Never copy a full installed skill folder or Hermes home into this repo. Rebuild the public package using an explicit file allowlist.
- Do not commit `.env`, OAuth stores, private keys, configuration backups or learning workspaces. `.gitignore` does not remove tracked files or history.
- Keep examples fictional and clearly labeled. Do not use private writing samples to demonstrate a voice.

## Reporting a problem

Do not post a credential or private record in a public issue. If private vulnerability reporting is enabled for this repository, use GitHub's private report flow. Otherwise use an available private contact method on the maintainer's public GitHub profile; if none exists, open a minimal issue requesting a private channel without exposing the sensitive detail.

If a credential has been exposed, revoke or rotate it immediately. Deleting a file or adding it to `.gitignore` does not remove it from history or revoke it. Public copies and forks may persist after history cleanup.

## Runtime boundaries

LearningOS is an instruction skill, not a security sandbox. It does not guarantee model obedience, encrypted storage, secret filtering, integration access or offline operation. Your selected model provider and optional integrations may receive note contents. Review runtime settings and permission boundaries before processing sensitive material.

The interactive guide only demonstrates the workflow. It has no data-entry or upload forms and does not send application data. Its approval control cannot authorize actual publishing. Any real publication needs separate approval of final content and destination.

# Optional Notion storage

This integration is optional. The workflow works with local Markdown alone.

1. Discover an available Notion tool or load a Notion integration skill if installed. Follow that integration's actual authentication setup; do not invent endpoints or request tokens in chat.
2. Use the learner's privately configured destination. If none exists, ask for the destination before writing. Never put private page IDs or links into shared skill files.
3. Verify access to the exact parent through a read. Inspect existing children and content. Reuse a matching document title; create related-topic subpages within that document when requested. Use a database only if requested.
4. Preserve existing notes and reflections. Append timestamped additions; deduplicate retries. Keep pages private and do not change sharing permissions.
5. After every external write, read the exact target back and verify its title, parent and content. Return only real destination links to the learner in their private conversation.
6. Record Draft/Published status only if the destination supports it. A Published label does not prove that an article was actually published elsewhere.
7. On authentication, parent-access or sync failure, state the actual error and save a local Markdown backup outside the public repository. Mark sync pending/failed; never claim success. Retry without creating duplicate pages.

**Completion:** the remote note's location and content are verified, or the local backup path and real sync blocker are provided.

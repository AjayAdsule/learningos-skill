"""Public package contract checks; no credentials or live network required."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "learningos" / "SKILL.md"
SECTIONS = [
    "My Original Notes", "What I Understood", "Key Concepts",
    "Author's Actual Claims", "Simple Examples", "My Personal Reflections",
    "Questions and Confusion", "Connections", "Key Takeaways", "Further Reading",
]


class SkillPackageTests(unittest.TestCase):
    def test_skill_frontmatter_and_portability(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter, body = text[4:].split("\n---\n", 1)
        self.assertIn("name: learningos", frontmatter)
        description = re.search(r"^description: (.+)$", frontmatter, re.M).group(1)
        self.assertLessEqual(len(description), 60)
        self.assertTrue(description.endswith("."))
        for field in ["version", "author", "license", "platforms", "metadata"]:
            self.assertRegex(frontmatter, rf"(?m)^{field}:")
        self.assertIn("AjayAdsule", frontmatter)
        self.assertIn("platforms: [linux, macos, windows]", frontmatter)
        self.assertIn("related_skills: []", frontmatter)
        self.assertLessEqual(len(text), 100_000)
        for section in ["When to Use", "Prerequisites", "Procedure", "Pitfalls", "Verification"]:
            self.assertIn("## " + section, body)

    def test_readme_installation_preserves_private_learningos(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        install = text.split("## Install in Hermes\n", 1)[1].split("### Example requests", 1)[0]
        self.assertNotIn("--name", install, "GitHub installation must not promise an alternate name")
        self.assertFalse("learningos-community" in text, "Remove alternate-name example requests too")
        self.assertNotIn("--force", install)
        warning = "must not install this community skill in that profile"
        self.assertIn(warning, install)
        self.assertIn("private skill named `learningos`", install)
        self.assertIn("inspect without installation", install)
        self.assertIn("separate clean profile", install)
        self.assertIn("https://hermes-agent.nousresearch.com/docs/user-guide/profiles", install)
        command = "hermes skills install AjayAdsule/learningos-skill/skills/learningos"
        self.assertIn(command + "\n", install)
        self.assertLess(install.index(warning), install.index(command))
        self.assertIn("no existing `learningos` skill", install)
        self.assertIn("hermes skills inspect AjayAdsule/learningos-skill/skills/learningos\n", install)

    def test_note_sections_keep_required_order(self):
        template = (SKILL.parent / "templates" / "note.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"^## (.+)$", template, re.M), SECTIONS)
        for field in ["Date", "Source", "Author", "Chapter", "Category"]:
            self.assertIn(f"{field}: not provided", template)

    def test_relative_markdown_links_resolve(self):
        for path in ROOT.rglob("*.md"):
            if ".git" in path.relative_to(ROOT).parts:
                continue
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if re.match(r"[a-z]+:", target) or target.startswith("#"):
                    continue
                target_path = (path.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(target_path.is_relative_to(ROOT.resolve()), target)
                self.assertTrue(target_path.is_file(), f"Broken link in {path.name}: {target}")

    def test_guide_is_offline_and_has_no_data_entry(self):
        html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        self.assertIn("connect-src 'none'", html)
        self.assertNotRegex(html, r'<(?:script|iframe)\b[^>]*\bsrc=')
        self.assertNotRegex(html, r'<link\b[^>]*href=[\"\']https?')
        self.assertNotRegex(html, r'<(?:form|textarea)\b')
        self.assertNotRegex(html, r'type=[\"\'](?:text|password|email|file)[\"\']')
        self.assertIn('id="workflow-script"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn("prefers-reduced-motion", html)

    def test_public_docs_have_no_personal_destinations(self):
        private_path = re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+/")
        private_notion = re.compile(r"https?://(?:www\.)?notion\.(?:so|site)/[^\s)\"<>]+")
        for path in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.html")):
            if ".git" in path.relative_to(ROOT).parts:
                continue
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(private_path.search(text), path.name)
            self.assertIsNone(private_notion.search(text), path.name)
            self.assertNotRegex(text, r"\b[0-9a-f]{32}\b", path.name)
            self.assertNotRegex(text, r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", path.name)

    def test_runtime_files_are_ignored(self):
        ignored = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        for pattern in [".env", ".env.*", "auth.json", "config.yaml", ".hermes/",
                        "notes/", "sources/", "articles/", "writing-samples/", "sessions/"]:
            self.assertIn(pattern, ignored)


if __name__ == "__main__":
    unittest.main()

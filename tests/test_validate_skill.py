from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "tools" / "validate_skill.py"
SKILL = REPO_ROOT / "skills" / "manage-obsidian-project-kb"


class ValidateSkillTests(unittest.TestCase):
    def run_validator(self, path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)],
            check=False,
            capture_output=True,
            text=True,
        )

    def copy_skill(self, root: Path) -> Path:
        target = root / "manage-obsidian-project-kb"
        shutil.copytree(SKILL, target)
        return target

    def test_repository_skill_is_valid(self) -> None:
        result = self.run_validator(SKILL)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_duplicate_bridge_marker_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.copy_skill(Path(temporary))
            bridge = target / "assets" / "AGENTS-bridge.md"
            bridge.write_text(
                bridge.read_text(encoding="utf-8")
                + "\n<!-- kb:agents-bridge:start -->\n",
                encoding="utf-8",
            )
            result = self.run_validator(target)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("exactly one start", result.stderr)

    def test_directory_name_must_match_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "wrong-name"
            shutil.copytree(SKILL, target)
            result = self.run_validator(target)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must match skill name", result.stderr)

    def test_invalid_import_bridge_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.copy_skill(Path(temporary))
            bridge = target / "assets" / "agent-import-bridge.md"
            bridge.write_text(
                bridge.read_text(encoding="utf-8")
                + '\n<!-- kb:agent-import:start id="{{Adapter_Id}}" -->\n',
                encoding="utf-8",
            )
            result = self.run_validator(target)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("exactly one matching marker pair", result.stderr)

    def test_missing_adapter_protocol_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.copy_skill(Path(temporary))
            (target / "references" / "agent-adapters.md").unlink()
            result = self.run_validator(target)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required resource: references/agent-adapters.md", result.stderr)


if __name__ == "__main__":
    unittest.main()

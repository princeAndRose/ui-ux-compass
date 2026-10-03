"""Regression tests for neutral state, provenance, and optional hook behavior."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.render_ui_state import render_state
from scripts.update_ui_state import default_state, load_state, merge_patch, migrate_state


ROOT = Path(__file__).resolve().parents[1]


class StateProvenanceTests(unittest.TestCase):
    def test_new_states_are_neutral_and_independent(self):
        first, second = default_state(), default_state()
        self.assertTrue(all(not value for value in first["user_preferences"]["defaults"].values()))
        first["user_preferences"]["defaults"]["visual_tone"].append("expressive")
        first["design_system"]["facts"]["sources"].append("example")
        self.assertEqual(second, default_state())
        self.assertNotIn("medium", render_state(second))

    def test_item_cannot_forge_source_in_any_assumption_list(self):
        original = default_state()
        for patch_source in ("agent-assumption", "user-confirmed", "project-fact"):
            with self.subTest(source=patch_source), self.assertRaises(ValueError):
                merge_patch(original, {
                    "source": patch_source,
                    "pages": {"settings": {"assumptions": [{"text": "Use iOS patterns", "source": "user-confirmed"}]}},
                })
        for forged in ("user-confirmed", "project-fact", "invented-source"):
            with self.subTest(forged=forged), self.assertRaises(ValueError):
                merge_patch(original, {
                    "source": "agent-assumption",
                    "pages": {"settings": {"decisions": [{"text": "Use iOS patterns", "source": forged}]}},
                })
        self.assertEqual(original, default_state())

    def test_migration_preserves_explicit_v2_preferences_and_quarantines_v1(self):
        explicit = merge_patch(default_state(), {
            "source": "user-confirmed",
            "user_preferences": {"density_default": "high", "visual_tone": ["playful"], "anti_patterns": ["muted palette"]},
        })
        self.assertEqual(migrate_state(explicit), explicit)
        legacy = migrate_state({"version": 1, "user_preferences": {"density_default": "medium"}})
        self.assertEqual(legacy["user_preferences"]["confirmed"], {})
        self.assertEqual(legacy["user_preferences"]["assumptions"], {"density_default": "medium"})

    def test_context_and_decision_metadata_survive_storage_and_rendering(self):
        entry = {
            "text": "Use compact operations rows", "source": "user-confirmed",
            "scope": ["/operations"], "evidence": [{"reference": "user-message-7"}],
            "revisit_when": "Touch-first rollout", "status": "needs-review",
        }
        state = merge_patch(default_state(), {
            "source": "user-confirmed",
            "design_system": {"profile": "custom", "platform": "desktop-web", "sources": [{"title": "Team guide", "path": "design.md"}]},
            "pages": {"operations": {"design_system_profile": "carbon", "platform": "desktop-web", "design_sources": [{"url": "https://carbondesignsystem.com"}], "decisions": [entry]}},
        })
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "state.json"
            path.write_text(json.dumps(state), encoding="utf-8")
            loaded = load_state(path)
        self.assertEqual(loaded, state)
        self.assertEqual(loaded["pages"]["operations"]["decisions"], [entry])
        for expected in ("needs-review", "Touch-first rollout", "user-message-7", "carbon", "desktop-web", "https://carbondesignsystem.com"):
            self.assertIn(expected, render_state(loaded))


class SessionStartTests(unittest.TestCase):
    def run_hook(self, cwd, data_dir=None):
        env = {key: value for key, value in os.environ.items() if key != "PLUGIN_DATA"}
        if data_dir is not None:
            env["PLUGIN_DATA"] = str(data_dir)
        result = subprocess.run([sys.executable, str(ROOT / "hooks/session_start.py")], cwd=cwd, env=env, capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), {"continue": True})
        return result

    def test_hook_initializes_shared_schema_and_preserves_existing_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            data = Path(temp) / "plugin data"
            self.run_hook(temp, data)
            path = data / "ui-ux-compass-state.json"
            self.assertEqual(json.loads(path.read_text()), default_state())
            stored = '{"version": 1, "user_preferences": {"visual_tone": ["playful"]}}\n'
            path.write_text(stored)
            self.run_hook(temp, data)
            self.assertEqual(path.read_text(), stored)
            self.assertFalse((Path(temp) / ".ui-ux-compass").exists())

    def test_optional_cache_absence_and_write_failure_do_not_block(self):
        with tempfile.TemporaryDirectory() as temp:
            self.run_hook(temp)
            occupied = Path(temp) / "file-instead-of-directory"
            occupied.write_text("existing")
            result = self.run_hook(temp, occupied)
            self.assertIn("initialization skipped", result.stderr)
            self.assertEqual(occupied.read_text(), "existing")

    def test_manifest_runs_from_plugin_path_containing_spaces(self):
        config = json.loads((ROOT / "hooks/hooks.json").read_text())
        command = config["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        self.assertIn('python3 "${PLUGIN_ROOT}/hooks/session_start.py"', command)
        with tempfile.TemporaryDirectory() as temp:
            plugin = Path(temp) / "plugin with spaces"
            plugin.symlink_to(ROOT, target_is_directory=True)
            env = dict(os.environ, PLUGIN_ROOT=str(plugin), PLUGIN_DATA=str(Path(temp) / "cache"))
            result = subprocess.run(command, shell=True, cwd=temp, env=env, capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(result.stdout), {"continue": True})
            self.assertEqual(json.loads((Path(temp) / "cache/ui-ux-compass-state.json").read_text()), default_state())


if __name__ == "__main__":
    unittest.main()

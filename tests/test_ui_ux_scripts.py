import json
import tempfile
import unittest
from pathlib import Path


class DetectUiSurfaceTests(unittest.TestCase):
    def test_dashboard_prompt_routes_to_mini_brief(self):
        from scripts.detect_ui_surface import detect_ui_surface

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "app" / "dashboard").mkdir(parents=True)
            (root / "app" / "dashboard" / "page.tsx").write_text("export default function Page() { return null }")

            result = detect_ui_surface(root, "Create a dashboard page for this project")

        self.assertTrue(result["ui_related"])
        self.assertEqual(result["risk_level"], 3)
        self.assertEqual(result["recommended_mode"], "mini-brief")
        self.assertEqual(result["recommended_skill"], "ui-ux-brief")

    def test_backend_prompt_does_not_intervene(self):
        from scripts.detect_ui_surface import detect_ui_surface

        with tempfile.TemporaryDirectory() as temp:
            result = detect_ui_surface(Path(temp), "Refactor the API client and add retry tests")

        self.assertFalse(result["ui_related"])
        self.assertEqual(result["risk_level"], 0)
        self.assertEqual(result["recommended_mode"], "observe")

    def test_non_ui_words_containing_form_do_not_trigger_ui_flow(self):
        from scripts.detect_ui_surface import detect_ui_surface

        prompts = [
            "Improve performance metrics aggregation",
            "Update information schema docs",
            "Refactor the transform pipeline",
        ]

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    result = detect_ui_surface(root, prompt)

                    self.assertFalse(result["ui_related"])
                    self.assertEqual(result["risk_level"], 0)
                    self.assertEqual(result["recommended_mode"], "observe")

    def test_backend_and_test_prompts_with_surface_terms_do_not_intervene(self):
        from scripts.detect_ui_surface import detect_ui_surface

        prompts = [
            "Refactor dashboard API tests",
            "Add retry tests for the dashboard API client",
        ]

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    result = detect_ui_surface(root, prompt)

                    self.assertFalse(result["ui_related"])
                    self.assertEqual(result["risk_level"], 0)
                    self.assertEqual(result["recommended_mode"], "observe")


class InspectDesignSystemTests(unittest.TestCase):
    def test_detects_next_tailwind_and_shadcn(self):
        from scripts.inspect_design_system import inspect_design_system

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "package.json").write_text(json.dumps({
                "dependencies": {
                    "next": "15.0.0",
                    "react": "19.0.0",
                    "tailwindcss": "4.0.0",
                    "@radix-ui/react-dialog": "1.0.0",
                    "class-variance-authority": "1.0.0"
                }
            }))
            (root / "pnpm-lock.yaml").write_text("lockfileVersion: '9.0'")
            (root / "tailwind.config.ts").write_text("export default {}")
            (root / "components.json").write_text("{}")
            (root / "src" / "components" / "ui").mkdir(parents=True)

            result = inspect_design_system(root)

        self.assertEqual(result["framework"], "next")
        self.assertEqual(result["router"], "unknown")
        self.assertIn("tailwind", result["styling"])
        self.assertIn("radix", result["ui_library"])
        self.assertIn("shadcn-ui", result["ui_library"])
        self.assertIn("src/components/ui", result["component_dirs"])

    def test_css_scan_ignores_node_modules(self):
        from scripts.inspect_design_system import inspect_design_system

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "package.json").write_text(json.dumps({"dependencies": {"react": "19.0.0"}}))
            (root / "node_modules" / "vendor").mkdir(parents=True)
            (root / "node_modules" / "vendor" / "theme.css").write_text(".dark { color: black; }")

            result = inspect_design_system(root)

        self.assertFalse(result["conventions"]["has_dark_mode"])


class ExtractRoutesTests(unittest.TestCase):
    def test_extracts_next_app_routes(self):
        from scripts.extract_routes import extract_routes

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "app" / "dashboard").mkdir(parents=True)
            (root / "app" / "dashboard" / "page.tsx").write_text("export default function Page() {}")
            (root / "app" / "layout.tsx").write_text("export default function Layout() {}")

            result = extract_routes(root)

        self.assertEqual(result["routes"], [
            {"path": "/dashboard", "file": "app/dashboard/page.tsx", "type": "page"}
        ])
        self.assertEqual(result["layout_files"], ["app/layout.tsx"])


class ValidateUiIntentTests(unittest.TestCase):
    def test_blocks_when_core_decisions_are_missing(self):
        from scripts.validate_ui_intent import validate_ui_intent

        result = validate_ui_intent({
            "page_role": "Dashboard",
            "target_user": "Founder"
        })

        self.assertEqual(result["status"], "blocked")
        self.assertTrue(result["blocking"])
        self.assertIn("core_task", result["missing"])

    def test_passes_with_complete_spec(self):
        from scripts.validate_ui_intent import validate_ui_intent

        result = validate_ui_intent({
            "page_role": "Dashboard",
            "target_user": "Founder",
            "core_task": "Scan project health",
            "first_visual_focus": "Status summary",
            "information_hierarchy": {"p0": ["health"], "p1": ["activity"], "p2": []},
            "main_cta": "Review blockers",
            "user_flow": {"entry": "Open dashboard", "action": "Review blockers"},
            "layout_strategy": "Summary over detailed tables",
            "visual_direction": "Focused tooling",
            "interaction_states": ["loading", "empty", "error"],
            "implementation_constraints": ["Use existing components"],
            "acceptance_criteria": ["P0 status is visually dominant"]
        })

        self.assertEqual(result["status"], "pass")
        self.assertFalse(result["blocking"])


class StateScriptTests(unittest.TestCase):
    def test_merge_patch_preserves_assumptions_separately(self):
        from scripts.update_ui_state import default_state, merge_patch

        state = default_state("Example")
        patch = {
            "source": "agent-assumption",
            "pages": {
                "dashboard": {
                    "route": "/dashboard",
                    "page_role": "Status overview",
                    "assumptions": ["Medium density"]
                }
            }
        }

        merged = merge_patch(state, patch)

        page = merged["pages"]["dashboard"]
        self.assertEqual(page["route"], "/dashboard")
        self.assertEqual(page["decisions"], [])
        self.assertEqual(page["assumptions"], [{"source": "agent-assumption", "text": "Medium density"}])

    def test_render_state_outputs_markdown_summary(self):
        from scripts.render_ui_state import render_state
        from scripts.update_ui_state import default_state

        state = default_state("Example")
        state["project"]["summary"] = "A UI workflow plugin"
        state["pages"]["dashboard"] = {
            "route": "/dashboard",
            "status": "draft",
            "page_role": "Status overview",
            "target_user": "Founder",
            "core_task": "Scan project health",
            "decisions": [],
            "assumptions": []
        }

        markdown = render_state(state)

        self.assertIn("## UI Intent Summary", markdown)
        self.assertIn("A UI workflow plugin", markdown)
        self.assertIn("/dashboard", markdown)

    def test_ui_intent_schema_validates_stores_and_renders_page_role(self):
        from scripts.render_ui_state import render_state
        from scripts.update_ui_state import default_state, merge_patch
        from scripts.validate_ui_intent import validate_ui_intent

        intent = {
            "page_role": "Dashboard",
            "target_user": "Founder",
            "core_task": "Scan project health",
            "first_visual_focus": "Status summary",
            "information_hierarchy": {"p0": ["health"], "p1": ["activity"], "p2": []},
            "main_cta": "Review blockers",
            "user_flow": {"entry": "Open dashboard", "action": "Review blockers"},
            "layout_strategy": "Summary over detailed tables",
            "visual_direction": "Focused tooling",
            "interaction_states": ["loading", "empty", "error"],
            "implementation_constraints": ["Use existing components"],
            "acceptance_criteria": ["P0 status is visually dominant"],
        }

        validation = validate_ui_intent(intent)
        merged = merge_patch(default_state("Example"), {
            "source": "user-confirmed",
            "pages": {"dashboard": {"route": "/dashboard", **intent}},
        })
        markdown = render_state(merged)

        self.assertEqual(validation["status"], "pass")
        self.assertEqual(merged["pages"]["dashboard"]["page_role"], "Dashboard")
        self.assertIn("Role: Dashboard", markdown)


class TriggerEvalTests(unittest.TestCase):
    def test_trigger_eval_cases_meet_mvp_thresholds(self):
        from scripts.run_trigger_evals import run_trigger_evals

        result = run_trigger_evals(Path("evals/trigger-cases.csv"), Path("."))

        self.assertGreaterEqual(result["risk_within_one_rate"], 0.9)
        self.assertGreaterEqual(result["mode_accuracy"], 0.9)
        self.assertLessEqual(result["false_question_rate"], 0.15)
        self.assertEqual(result["risk_3_or_4_without_gate"], 0)
        self.assertEqual(result["subjective_feedback_to_review_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()

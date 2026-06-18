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

    def test_chinese_subjective_feedback_routes_to_review(self):
        from scripts.detect_ui_surface import detect_ui_surface

        prompts = [
            "这个页面不好看，太挤了",
            "这个 UI 模板感太强，不像真实产品",
            "看起来有点怪，信息层级不清",
        ]

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    result = detect_ui_surface(root, prompt)

                    self.assertTrue(result["ui_related"])
                    self.assertEqual(result["risk_level"], 4)
                    self.assertEqual(result["recommended_mode"], "review")
                    self.assertEqual(result["recommended_skill"], "ui-ux-review")

    def test_chinese_ui_requests_route_by_risk(self):
        from scripts.detect_ui_surface import detect_ui_surface

        cases = [
            ("做一个新的仪表盘页面", 3, "mini-brief"),
            ("新增管理后台页面", 3, "mini-brief"),
            ("给现有仪表盘加筛选器", 2, "ask-one-question"),
            ("支持暗色模式和加载态", 2, "assumptions-gate"),
            ("把按钮文案改成发布", 1, "apply-existing-conventions"),
        ]

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for prompt, risk, mode in cases:
                with self.subTest(prompt=prompt):
                    result = detect_ui_surface(root, prompt)

                    self.assertTrue(result["ui_related"])
                    self.assertEqual(result["risk_level"], risk)
                    self.assertEqual(result["recommended_mode"], mode)

    def test_chinese_non_ui_prompts_do_not_intervene(self):
        from scripts.detect_ui_surface import detect_ui_surface

        prompts = [
            "重构 API 接口测试",
            "优化数据库查询性能",
            "修复服务端重试逻辑",
            "更新数据转换管道",
        ]

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    result = detect_ui_surface(root, prompt)

                    self.assertFalse(result["ui_related"])
                    self.assertEqual(result["risk_level"], 0)
                    self.assertEqual(result["recommended_mode"], "observe")

    def test_script_assisted_router_examples_from_issue_3(self):
        from scripts.detect_ui_surface import detect_ui_surface

        cases = [
            ("Refactor dashboard API tests", False, 0, "observe"),
            ("Add dashboard filters to UI", True, 2, "ask-one-question"),
            ("Add filters to dashboard", True, 2, "ask-one-question"),
            ("给仪表盘加筛选器", True, 2, "ask-one-question"),
            ("This page feels weird", True, 4, "review"),
        ]

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for prompt, ui_related, risk, mode in cases:
                with self.subTest(prompt=prompt):
                    result = detect_ui_surface(root, prompt)

                    self.assertEqual(result["ui_related"], ui_related)
                    self.assertEqual(result["risk_level"], risk)
                    self.assertEqual(result["recommended_mode"], mode)

    def test_new_page_requests_with_local_features_stay_risk_3(self):
        from scripts.detect_ui_surface import detect_ui_surface

        cases = [
            "Add dashboard with filters",
            "Add a dashboard with filters",
            "Add a dashboard page with filters",
            "Add a settings page with a form",
        ]

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for prompt in cases:
                with self.subTest(prompt=prompt):
                    result = detect_ui_surface(root, prompt)

                    self.assertTrue(result["ui_related"])
                    self.assertEqual(result["risk_level"], 3)
                    self.assertEqual(result["recommended_mode"], "mini-brief")

    def test_router_wires_up_the_detector_and_execution_guide(self):
        # Structural contract only: the router must actually invoke the detector
        # script and point at the execution guide, and the guide must show the
        # detector command. The surrounding prose is free to be reworded without
        # breaking this test -- we assert wiring, not wording.
        router = Path("skills/ui-ux-compass-router/SKILL.md").read_text(encoding="utf-8")
        execution = Path("references/router-execution.md").read_text(encoding="utf-8")

        self.assertIn("scripts/detect_ui_surface.py", router)
        self.assertIn("references/router-execution.md", router)
        self.assertIn("scripts/detect_ui_surface.py", execution)


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
            "user_flow": {"entry": "Open dashboard", "action": "Review blockers", "feedback": "Blocker list updates"},
            "layout_strategy": "Summary over detailed tables",
            "visual_direction": {"density": "medium-high", "tone": "focused", "structure": "summary plus drilldown"},
            "interaction_states": ["loading", "empty", "error"],
            "implementation_constraints": ["Use existing components"],
            "acceptance_criteria": [
                "P0 status is visually dominant above the activity feed",
                "Loading, empty, and error states preserve the dashboard layout",
            ]
        })

        self.assertEqual(result["status"], "pass")
        self.assertFalse(result["blocking"])
        self.assertEqual(result["weak"], [])

    def test_flags_weak_but_present_spec(self):
        from scripts.validate_ui_intent import validate_ui_intent

        result = validate_ui_intent({
            "page_role": "Dashboard",
            "target_user": "Founder",
            "core_task": "Scan project health",
            "first_visual_focus": "Status summary",
            "information_hierarchy": {"p0": [], "p1": ["activity"], "p2": []},
            "main_cta": "Review",
            "user_flow": {"entry": "Open dashboard", "action": "Review"},
            "layout_strategy": "modern",
            "visual_direction": "clean",
            "interaction_states": ["loading"],
            "implementation_constraints": ["Use existing components"],
            "acceptance_criteria": ["Looks good"]
        })

        self.assertEqual(result["status"], "blocked")
        self.assertTrue(result["blocking"])
        self.assertIn("information_hierarchy.p0 must be non-empty.", result["blocking_reasons"])
        self.assertIn("layout_strategy is too generic to guide implementation.", result["weak"])
        self.assertTrue(result["recommended_questions"])

    def test_empty_main_cta_requires_explicit_no_action_justification(self):
        from scripts.validate_ui_intent import validate_ui_intent

        base = {
            "page_role": "Analytics dashboard",
            "target_user": "Founder",
            "core_task": "Monitor revenue health",
            "first_visual_focus": "Revenue trend",
            "information_hierarchy": {"p0": ["revenue"], "p1": ["segments"], "p2": []},
            "main_cta": "",
            "user_flow": {"entry": "Open dashboard", "action": "Scan trend", "feedback": "Data refresh time is visible"},
            "layout_strategy": "Summary plus drilldown",
            "visual_direction": {"density": "medium-high", "tone": "focused", "structure": "summary plus drilldown"},
            "interaction_states": ["loading", "empty", "error"],
            "implementation_constraints": ["Use existing chart components"],
            "acceptance_criteria": [
                "Revenue trend is visually dominant in the first viewport",
                "Loading, empty, and error states preserve the chart layout",
            ],
        }

        without_justification = validate_ui_intent(base)
        with_justification = validate_ui_intent({
            **base,
            "main_cta_justification": "Read-only monitoring surface with no primary action.",
        })

        self.assertEqual(without_justification["status"], "blocked")
        self.assertIn("main_cta", without_justification["missing"])
        self.assertIn("main_cta is required before implementation.", without_justification["blocking_reasons"])
        self.assertEqual(with_justification["status"], "pass")
        self.assertNotIn("main_cta", with_justification["missing"])


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
        self.assertEqual(page["route"], "")
        self.assertEqual(page["decisions"], [])
        self.assertIn({"source": "agent-assumption", "text": "route: /dashboard"}, page["assumptions"])
        self.assertIn({"source": "agent-assumption", "text": "page_role: Status overview"}, page["assumptions"])
        self.assertIn({"source": "agent-assumption", "text": "Medium density"}, page["assumptions"])

    def test_agent_assumption_does_not_overwrite_confirmed_preference(self):
        from scripts.update_ui_state import default_state, merge_patch

        state = default_state("Example")
        state = merge_patch(state, {
            "source": "user-confirmed",
            "user_preferences": {"density_default": "high"},
        })
        state = merge_patch(state, {
            "source": "agent-assumption",
            "user_preferences": {"density_default": "low", "visual_tone": ["playful"]},
        })

        self.assertEqual(state["user_preferences"]["confirmed"]["density_default"], "high")
        self.assertEqual(state["user_preferences"]["assumptions"]["density_default"], "low")
        self.assertEqual(state["user_preferences"]["assumptions"]["visual_tone"], ["playful"])

    def test_project_fact_design_system_merge_uses_facts_bucket(self):
        from scripts.update_ui_state import default_state, merge_patch

        state = merge_patch(default_state("Example"), {
            "source": "project-fact",
            "design_system": {
                "framework": "next",
                "router": "app-router",
                "component_dirs": ["src/components/ui"],
            },
        })

        facts = state["design_system"]["facts"]
        self.assertEqual(facts["framework"], "next")
        self.assertEqual(facts["router"], "app-router")
        self.assertEqual(facts["component_dirs"], ["src/components/ui"])

    def test_bucketed_v2_state_patch_is_source_checked(self):
        from scripts.update_ui_state import default_state, merge_patch

        state = merge_patch(default_state("Example"), {
            "source": "project-fact",
            "project": {"facts": {"summary": "Verified from README"}},
            "design_system": {"facts": {"framework": "next"}},
        })

        self.assertEqual(state["project"]["facts"]["summary"], "Verified from README")
        self.assertEqual(state["design_system"]["facts"]["framework"], "next")

        with self.assertRaises(ValueError):
            merge_patch(state, {
                "source": "agent-assumption",
                "project": {"facts": {"summary": "Assumed summary"}},
            })
        with self.assertRaises(ValueError):
            merge_patch(state, {
                "source": "agent-assumption",
                "project": {"facts": {}},
            })
        with self.assertRaises(ValueError):
            merge_patch(state, {
                "source": "project-fact",
                "project": {"facts": []},
            })

    def test_render_state_outputs_markdown_summary(self):
        from scripts.render_ui_state import render_state
        from scripts.update_ui_state import default_state, merge_patch

        state = merge_patch(default_state("Example"), {
            "source": "project-fact",
            "project": {"summary": "A UI workflow plugin"},
        })
        state["pages"]["dashboard"] = {
            "route": "/dashboard",
            "status": "draft",
            "page_role": "Status overview",
            "target_user": "Founder",
            "core_task": "Scan project health",
            "decisions": [{"source": "user-confirmed", "text": "P0 status summary"}],
            "assumptions": [{"source": "agent-assumption", "text": "Medium density"}],
            "open_questions": ["Which metrics are P0?"],
        }

        markdown = render_state(state)

        self.assertIn("## UI Intent Summary", markdown)
        self.assertIn("Project facts:", markdown)
        self.assertIn("Confirmed preferences:", markdown)
        self.assertIn("Agent assumptions:", markdown)
        self.assertIn("Open questions:", markdown)
        self.assertIn("A UI workflow plugin", markdown)
        self.assertIn("/dashboard", markdown)
        self.assertIn("P0 status summary", markdown)
        self.assertIn("Medium density", markdown)

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
            "user_flow": {"entry": "Open dashboard", "action": "Review blockers", "feedback": "Blocker list updates"},
            "layout_strategy": "Summary over detailed tables",
            "visual_direction": {"density": "medium-high", "tone": "focused", "structure": "summary plus drilldown"},
            "interaction_states": ["loading", "empty", "error"],
            "implementation_constraints": ["Use existing components"],
            "acceptance_criteria": [
                "P0 status is visually dominant above the activity feed",
                "Loading, empty, and error states preserve the dashboard layout",
            ],
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

    def test_v1_state_migrates_to_source_aware_v2(self):
        from scripts.update_ui_state import load_state

        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "state.json"
            path.write_text(json.dumps({
                "version": 1,
                "project": {"name": "Legacy", "summary": "Old project"},
                "user_preferences": {"density_default": "low"},
                "design_system": {"framework": "react"},
                "pages": {},
            }), encoding="utf-8")

            state = load_state(path, "Example")

        self.assertEqual(state["version"], 2)
        self.assertEqual(state["project"]["facts"]["summary"], "Old project")
        self.assertEqual(state["user_preferences"]["confirmed"]["density_default"], "low")
        self.assertEqual(state["design_system"]["facts"]["framework"], "react")


class TriggerEvalTests(unittest.TestCase):
    def test_trigger_eval_cases_meet_mvp_thresholds(self):
        from scripts.run_trigger_evals import run_trigger_evals

        result = run_trigger_evals(Path("evals/trigger-cases.csv"), Path("."))
        thresholds = result["expectations"]

        self.assertTrue(result["passed"])
        self.assertGreaterEqual(result["risk_within_one_rate"], thresholds["risk_level_within_one"])
        self.assertGreaterEqual(result["mode_accuracy"], thresholds["mode_accuracy"])
        self.assertLessEqual(result["false_question_rate"], thresholds["false_question_rate_max"])
        self.assertEqual(
            result["risk_3_or_4_without_gate"],
            thresholds["risk_3_or_4_without_spec_or_assumptions_gate"],
        )
        self.assertGreaterEqual(
            result["subjective_feedback_to_review_rate"],
            thresholds["subjective_feedback_to_review"],
        )

    def test_trigger_eval_uses_expected_routing_thresholds(self):
        from scripts.run_trigger_evals import run_trigger_evals

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cases = root / "trigger-cases.csv"
            expected = root / "expected-routing.json"
            cases.write_text(
                "id,prompt,expected_risk,expected_mode,should_ask\n"
                'T001,"Fix the failing unit test in utils/date.ts",0,observe,false\n',
                encoding="utf-8",
            )
            expected.write_text(json.dumps({
                "success_metrics": {
                    "risk_level_within_one": 1.1,
                    "mode_accuracy": 1.0,
                    "false_question_rate_max": 0.0,
                    "risk_3_or_4_without_spec_or_assumptions_gate": 0,
                    "subjective_feedback_to_review": 1.0,
                }
            }), encoding="utf-8")

            result = run_trigger_evals(cases, root)

        self.assertFalse(result["passed"])
        self.assertIn("risk_within_one_rate", result["failures"])


class WorkflowEvalTests(unittest.TestCase):
    def test_workflow_eval_fixtures_pass(self):
        from scripts.run_workflow_evals import run_workflow_evals

        result = run_workflow_evals(Path("evals/workflows"), Path("."))

        self.assertTrue(result["passed"])
        self.assertEqual(result["total"], 6)
        self.assertEqual(result["passed_count"], 6)

    def test_workflow_eval_fails_for_missing_or_empty_fixtures(self):
        from scripts.run_workflow_evals import run_workflow_evals

        with tempfile.TemporaryDirectory() as temp:
            empty = Path(temp) / "empty"
            empty.mkdir()
            missing = Path(temp) / "missing"
            no_expectations = Path(temp) / "no-expectations"
            no_expectations.mkdir()
            (no_expectations / "case.json").write_text(json.dumps({
                "id": "missing-expectations",
                "message": "Create a dashboard",
            }), encoding="utf-8")
            no_spec = Path(temp) / "no-spec"
            no_spec.mkdir()
            (no_spec / "case.json").write_text(json.dumps({
                "id": "missing-spec",
                "message": "Create a dashboard",
                "expected_validation": {"status": "blocked"},
            }), encoding="utf-8")
            no_message = Path(temp) / "no-message"
            no_message.mkdir()
            (no_message / "case.json").write_text(json.dumps({
                "id": "missing-message",
                "expected_route": {"ui_related": False},
            }), encoding="utf-8")

            empty_result = run_workflow_evals(empty, Path("."))
            missing_result = run_workflow_evals(missing, Path("."))
            no_expectations_result = run_workflow_evals(no_expectations, Path("."))
            no_spec_result = run_workflow_evals(no_spec, Path("."))
            no_message_result = run_workflow_evals(no_message, Path("."))

        self.assertFalse(empty_result["passed"])
        self.assertFalse(missing_result["passed"])
        self.assertFalse(no_expectations_result["passed"])
        self.assertFalse(no_spec_result["passed"])
        self.assertFalse(no_message_result["passed"])
        self.assertIn("_fixtures", empty_result["failures"])
        self.assertIn("_fixtures", missing_result["failures"])
        self.assertIn("missing-expectations", no_expectations_result["failures"])
        self.assertIn("missing-spec", no_spec_result["failures"])
        self.assertIn("missing-message", no_message_result["failures"])


class ReferenceKnowledgePackTests(unittest.TestCase):
    def test_expanded_reference_pack_is_discoverable(self):
        required = [
            "surface-playbooks.md",
            "layout-archetypes.md",
            "component-patterns.md",
            "state-patterns.md",
            "design-quality-rubric.md",
            "feedback-translation-table.md",
            "before-after-review-examples.md",
        ]
        references = Path("references")

        # Stable anchors only: each reference file exists, carries real content
        # (not an empty stub), and is actually linked from a skill. We do not pin
        # specific vocabulary -- the references are free to evolve their wording.
        for filename in required:
            with self.subTest(filename=filename):
                path = references / filename
                self.assertTrue(path.is_file())
                self.assertGreater(len(path.read_text(encoding="utf-8").strip()), 200)

        skill_docs = "\n".join(path.read_text(encoding="utf-8") for path in Path("skills").glob("*/SKILL.md"))
        for filename in required:
            with self.subTest(skill_reference=filename):
                self.assertIn(f"references/{filename}", skill_docs)


if __name__ == "__main__":
    unittest.main()

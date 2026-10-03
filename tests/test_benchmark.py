import json
from pathlib import Path
import tempfile
import unittest

from scripts.benchmark import audit_run, evidence_file, load_scenarios, prepare_run, read_json, report_runs, validate_scenario, write_json


def scenario():
    return {
        "id": "settings", "title": "Settings", "category": "form", "design_system": "Apple HIG",
        "source_urls": ["https://developer.apple.com/design/human-interface-guidelines/"],
        "brief": "Build account settings", "context": "Existing web application",
        "user_facts": {"hidden": "private simulator fact"}, "constraints": ["Keep account data"],
        "required_artifacts": ["Screenshot"], "split": "development", "family": "settings",
        "checks": [
            {"id": "save", "kind": "hard", "criterion": "SECRET save works", "evidence": "interaction", "required": True},
            {"id": "hierarchy", "kind": "heuristic", "criterion": "Clear grouping", "evidence": "screenshot", "required": True},
            {"id": "questions", "kind": "process", "criterion": "No duplicate questions", "evidence": "trace", "required": False},
        ],
    }


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def prepare(self, condition="A", repeat=1, model="fixed"):
        return prepare_run(scenario(), self.root, condition=condition, model=model,
                           revision="none" if condition == "A" else f"revision-{condition}",
                           snapshot="snapshot-digest", budget_tokens=1000, repeat=repeat)

    def complete(self, run):
        result = read_json(run / "private/result-template.json")
        result["judge"] = {"identity": "independent-reviewer", "calibration": "human-label-set-v1"}
        result["execution"]["status"] = "completed"
        for check, rating in zip(scenario()["checks"], result["ratings"]):
            path = "evidence/" + check["id"] + ".txt"
            (run / path).write_text("Captured evidence", encoding="utf-8")
            rating.update(status="pass", reason="Observed required behavior", evidence=[{
                "type": check["evidence"], "path": path, "locator": "Step 2 / region top left"
            }])
            if check["kind"] == "heuristic":
                rating["score"] = 2
        result["artifacts"][0]["path"] = "evidence/hierarchy.txt"
        write_json(run / "private/result.json", result)
        return result

    def test_producer_excludes_checks_facts_and_arm(self):
        run = self.prepare()
        task = read_json(run / "producer/task.json")
        for key in ("checks", "split", "user_facts", "condition", "plugin_revision"):
            self.assertNotIn(key, task)
        self.assertNotIn("SECRET", json.dumps(task))
        self.assertNotIn("private simulator fact", json.dumps(task))
        self.assertTrue((run / "private/simulator.json").exists())
        with self.assertRaises(FileExistsError):
            self.prepare()

    def test_unexecuted_is_unverified(self):
        self.assertEqual(audit_run(self.prepare())["outcome"], "unverified")

    def test_complete_and_missing_evidence(self):
        run = self.prepare()
        self.complete(run)
        self.assertEqual(audit_run(run)["outcome"], "pass")
        (run / "evidence/save.txt").unlink()
        result = audit_run(run)
        self.assertEqual(result["outcome"], "unverified")
        self.assertEqual(result["ratings"][0]["status"], "unverified")
        self.assertIn("evidence file missing", result["ratings"][0]["issues"])

    def test_traversal_absolute_symlink_and_private_are_rejected(self):
        run = self.prepare()
        external = self.root / "external.txt"
        external.write_text("external")
        (run / "evidence/link.txt").symlink_to(external)
        for path in ("../../external.txt", str(external), "evidence/link.txt", "private/scenario.json"):
            self.assertFalse(evidence_file(run, path)[0], path)

    def test_missing_required_rating_and_artifact_prevent_pass(self):
        run = self.prepare()
        result = self.complete(run)
        result["ratings"].pop(0)
        result["artifacts"] = []
        write_json(run / "private/result.json", result)
        audit = audit_run(run)
        self.assertEqual(audit["outcome"], "unverified")
        self.assertFalse(audit["artifacts"][0]["verified"])

    def test_required_cannot_be_skipped_and_score_not_fabricated(self):
        run = self.prepare()
        result = self.complete(run)
        result["ratings"][0]["status"] = "not_applicable"
        result["ratings"][1]["score"] = True
        write_json(run / "private/result.json", result)
        audit = audit_run(run)
        self.assertEqual(audit["outcome"], "unverified")
        self.assertIsNone(audit["ratings"][1]["score"])

    def test_observed_hard_failure_is_failure(self):
        run = self.prepare()
        result = self.complete(run)
        result["ratings"][0]["status"] = "fail"
        write_json(run / "private/result.json", result)
        self.assertEqual(audit_run(run)["outcome"], "fail")

    def test_grouping_counts_cases_not_repeats_as_independent_cases(self):
        for condition in "ABC":
            for repeat in (1, 2):
                self.complete(self.prepare(condition, repeat))
        report = report_runs(self.root)
        self.assertEqual(report["case_count"], 1)
        self.assertEqual(report["run_count"], 6)
        self.assertEqual(len(report["case_conditions"]), 3)
        self.assertTrue(all(g["repeated_runs"] == 2 for g in report["case_conditions"]))
        self.assertEqual(report["unmatched_cases"], [])
        self.assertNotIn("overall_score", report)

    def test_unmatched_model_and_missing_arm(self):
        self.prepare("A")
        self.prepare("B", model="different")
        reasons = report_runs(self.root)["unmatched_cases"][0]["reasons"]
        self.assertIn("Missing A/B/C condition", reasons)
        self.assertIn("Model/snapshot/budget/scenario differs", reasons)

    def test_family_must_not_cross_holdout_split(self):
        directory = self.root / "scenarios"
        write_json(directory / "one.json", scenario())
        other = scenario()
        other.update(id="settings-two", split="holdout")
        write_json(directory / "two.json", other)
        with self.assertRaisesRegex(ValueError, "crosses"):
            load_scenarios(directory)

    def test_empty_optional_lists_are_valid(self):
        case = scenario()
        case.update(source_urls=[], constraints=[])
        self.assertEqual(validate_scenario(case), [])
        case["required_artifacts"] = []
        self.assertTrue(validate_scenario(case))

    def test_malformed_manifest_is_reported_as_invalid(self):
        run = self.prepare()
        manifest = read_json(run / "manifest.json")
        manifest["model"] = []
        write_json(run / "manifest.json", manifest)
        report = report_runs(self.root)
        self.assertEqual(report["run_count"], 0)
        self.assertEqual(len(report["invalid_runs"]), 1)

    def test_malformed_execution_cannot_pass(self):
        run = self.prepare()
        result = self.complete(run)
        result["execution"] = "completed"
        write_json(run / "private/result.json", result)
        self.assertEqual(audit_run(run)["outcome"], "unverified")
        result["execution"] = {"status": "completed", "tokens": -1}
        write_json(run / "private/result.json", result)
        self.assertEqual(audit_run(run)["outcome"], "unverified")

    def test_document_evidence_cannot_substitute_for_runtime_or_process(self):
        case = scenario()
        case["checks"][1].update(evidence="document", criterion="Review names the primary action")
        run = prepare_run(case, self.root, condition="A", model="fixed", revision="none",
                          snapshot="snapshot-digest", budget_tokens=1000, repeat=1)
        result = self.complete(run)
        result["ratings"][1]["evidence"][0]["type"] = "document"
        write_json(run / "private/result.json", result)
        self.assertEqual(audit_run(run)["ratings"][1]["status"], "pass")
        result["ratings"][0]["evidence"][0]["type"] = "document"
        write_json(run / "private/result.json", result)
        audit = audit_run(run)
        self.assertEqual(audit["ratings"][0]["status"], "unverified")
        self.assertEqual(audit["outcome"], "unverified")
        case["checks"][2]["evidence"] = "document"
        self.assertTrue(validate_scenario(case))

    def test_report_retains_costs_provenance_and_evidence(self):
        run = self.prepare()
        result = self.complete(run)
        result["execution"].update(tokens=650, elapsed_seconds=12.5)
        write_json(run / "private/result.json", result)
        report = report_runs(self.root)
        audit = report["runs"][0]
        self.assertEqual(audit["execution"], result["execution"])
        self.assertEqual(audit["judge"], result["judge"])
        self.assertTrue(audit["provenance_valid"])
        self.assertEqual(audit["ratings"][0]["reason"], result["ratings"][0]["reason"])
        self.assertEqual(audit["ratings"][0]["evidence"], result["ratings"][0]["evidence"])
        self.assertEqual(report["case_conditions"][0]["measurements"][0]["execution"]["tokens"], 650)
        case = scenario()
        case["brief"] = "Changed after preparation"
        write_json(run / "private/scenario.json", case)
        audit = audit_run(run)
        self.assertFalse(audit["provenance_valid"])
        self.assertTrue(all(r["status"] == "unverified" for r in audit["ratings"]))
        self.assertEqual(audit["ratings"][0]["submitted_status"], "pass")
        self.assertEqual(audit["outcome"], "unverified")

    def test_invalid_schema_and_tampered_scenario(self):
        case = scenario()
        case["checks"].append(case["checks"][0])
        self.assertTrue(validate_scenario(case))
        run = self.prepare()
        self.complete(run)
        case = scenario()
        case["brief"] = "Different brief"
        write_json(run / "private/scenario.json", case)
        self.assertEqual(audit_run(run)["outcome"], "unverified")


if __name__ == "__main__":
    unittest.main()

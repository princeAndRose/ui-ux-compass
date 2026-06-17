# State Schema

UI/UX Compass uses two state layers:

- Runtime state: `PLUGIN_DATA/ui-ux-compass-state.json`
- Project state: `.ui-ux-compass/state.json`

Do not create project state silently. If `.ui-ux-compass/` does not exist, ask before writing or output a state patch.

## Schema

```json
{
  "version": 1,
  "project": {
    "name": "",
    "summary": "",
    "product_type": "",
    "target_users": [],
    "primary_use_cases": [],
    "anti_goals": []
  },
  "user_preferences": {
    "density_default": "medium",
    "visual_tone": ["restrained", "clear", "product-like"],
    "layout_preferences": [],
    "color_preferences": [],
    "component_preferences": [],
    "anti_patterns": [
      "generic SaaS landing page",
      "overused gradients",
      "heavy shadows",
      "meaningless illustrations",
      "equal-weight cards everywhere"
    ]
  },
  "design_system": {
    "framework": "",
    "router": "",
    "styling": "",
    "ui_library": "",
    "tokens": [],
    "component_dirs": [],
    "notes": []
  },
  "pages": {
    "page-id": {
      "route": "",
      "surface_type": "",
      "status": "draft",
      "page_role": "",
      "target_user": "",
      "core_task": "",
      "first_visual_focus": "",
      "information_hierarchy": {
        "p0": [],
        "p1": [],
        "p2": [],
        "deferred": []
      },
      "main_cta": "",
      "user_flow": {
        "entry": "",
        "decision": "",
        "action": "",
        "feedback": "",
        "error_path": ""
      },
      "layout_strategy": "",
      "visual_direction": "",
      "interaction_states": [],
      "responsive_strategy": "",
      "accessibility_notes": [],
      "implementation_constraints": [],
      "anti_goals": [],
      "acceptance_criteria": [],
      "open_questions": [],
      "decisions": [],
      "assumptions": [],
      "last_review": null
    }
  }
}
```

## Source Types

- `user-confirmed`: explicitly chosen or confirmed by the user.
- `project-fact`: verified from project files or existing design system.
- `agent-assumption`: inferred by the agent and not confirmed.

Confirmed decisions must never be created from agent assumptions.

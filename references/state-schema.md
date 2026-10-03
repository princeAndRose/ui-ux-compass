# State Schema

UI/UX Compass uses two state layers:

- Runtime state: `PLUGIN_DATA/ui-ux-compass-state.json`
- Project state: `.ui-ux-compass/state.json`

Persist project state when authorized by the current task; if persistence is outside that scope, output a state patch. Do not require another permission exchange for an already authorized update. Runtime state is an optional cache, never an implicit source of project context or global design preferences. Disabling hooks does not affect the state CLI.

## Schema

```json
{
  "version": 2,
  "project": {
    "facts": {
      "name": "",
      "summary": "",
      "product_type": "",
      "target_users": [],
      "primary_use_cases": [],
      "anti_goals": []
    },
    "confirmed": {},
    "assumptions": {}
  },
  "user_preferences": {
    "defaults": {
      "density_default": "",
      "visual_tone": [],
      "layout_preferences": [],
      "color_preferences": [],
      "component_preferences": [],
      "anti_patterns": []
    },
    "confirmed": {},
    "assumptions": {}
  },
  "design_system": {
    "facts": {
      "framework": "",
      "router": "",
      "styling": "",
      "ui_library": "",
      "tokens": [],
      "component_dirs": [],
      "notes": [],
      "profile": "",
      "platform": "",
      "sources": []
    },
    "confirmed": {},
    "assumptions": {}
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
      "design_system_profile": "",
      "platform": "",
      "design_sources": [],
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

## Merge Rules

- `user-confirmed` writes user preferences, confirmed project/design-system decisions, and page decisions.
- `project-fact` writes project and design-system facts verified from code or files.
- `agent-assumption` writes only assumptions.
- Agent assumptions must never overwrite confirmed preferences, project facts, design-system facts, or page decisions.
- v1 state files are migrated on load: old project and design-system fields become facts; unbucketed user preferences become assumptions because v1 mixed defaults and explicit choices. They require actual evidence before a later `user-confirmed` patch.
- Existing v2 confirmed preferences remain unchanged. New state has no prescribed density, visual tone, or anti-patterns; stored defaults are not evidence of user confirmation.
- A decision item's `source`, if supplied, must match the effective destination source. Conflicting labels fail, including an assumption claiming `user-confirmed`. Items in an `assumptions` list always require `agent-assumption`, even in a confirmed patch.

## Design Context and Decision Metadata

Schema version 2 remains compatible: these fields are optional. `design_system.profile` names the selected system or custom direction (for example `apple-hig`, `material-3`, or `custom`); `platform` identifies the actual target. `sources` records consulted evidence, with descriptive title, URL or local path, and version/date when available. A system's name alone does not prove suitability or compliance. Route fields through facts, confirmed choices, or assumptions according to their real provenance.

Pages can narrow that context using `design_system_profile`, `platform`, and `design_sources`. A page-specific choice does not silently become a project-wide preference. Absence of a field means unspecified, not a default to another design system.

Page decision/assumption entries accept optional `scope`, `evidence`, `revisit_when`, and `status` metadata. These are preserved and rendered, without pretending the CLI can verify their truth:

```json
{
  "source": "user-confirmed",
  "text": "Use compact rows for the operations queue",
  "scope": ["/operations"],
  "evidence": [{"kind": "user-message", "reference": "Confirmed during queue review"}],
  "revisit_when": "The queue becomes a touch-first interface",
  "status": "active"
}
```

Use `active`, `needs-review`, or `superseded` as status conventions. Only active, in-scope decisions guide implementation; assumptions and decisions needing review must retain their uncertainty. Metadata is descriptive, not automatic expiry logic. Updating decisions requires reconciling existing entries; appending a new entry does not retire an old one automatically.

## Optional SessionStart Hook

The hook exclusively creates a neutral v2 runtime cache if missing, preserves existing bytes on repeat runs, and never writes project state. It emits the supported `{"continue": true}` common output, with no additional developer context. Missing `PLUGIN_DATA` or an initialization failure never blocks the session. State scripts run independently of hook discovery or trust. See the [official hook output contract](https://learn.chatgpt.com/docs/hooks#common-output-fields).

## Merge Patch Examples

Flat patches are routed by `source`:

```json
{
  "source": "project-fact",
  "design_system": {
    "framework": "next",
    "router": "app-router"
  }
}
```

Bucketed v2 patches are also supported when the bucket matches `source`:

```json
{
  "source": "project-fact",
  "project": {
    "facts": {
      "summary": "Verified from README"
    }
  }
}
```

Invalid bucket writes fail instead of being ignored. For example, `agent-assumption` cannot write `project.facts`.

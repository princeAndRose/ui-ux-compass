# Focus journal: settings interaction specification

Keep **Journal** and **History** as the primary navigation. Open a separate, single-pane **[App Name] Settings** window from **App menu → Settings…**, with **⌘,**. Reopening brings the existing window forward. Use native controls, a close button, and disabled minimize/zoom controls; three preferences do not need pane navigation or search. This placement follows [Apple’s Settings guidance](https://developer.apple.com/design/human-interface-guidelines/settings).

## Placement and behavior

| Option | Location and control | Effect and scope |
| --- | --- | --- |
| Default reminder time | Settings → **Reminders**; labeled native time picker | App-wide default for daily reminders. Display in the user’s locale and local time zone. Commit a valid time when editing finishes; retain the previous value if entry is invalid and explain the correction beside the field. |
| Weekly summary | Settings → **Reminders**; **Weekly summary** checkbox | Persist on/off immediately. Turning it off stops future summaries; it does not remove journal entries. Do not add a delivery channel or schedule selector. |
| Follow system appearance | Settings → **Appearance**; row reading **Appearance: System** and “Matches your Mac’s Light or Dark appearance.” | Follow macOS automatically, including changes while the app is open. With no app-specific alternative specified, this is explanatory text, not a switch with an undefined off state. |
| Current-note sort order | Current note’s local header, beside the content affected; **Sort** pop-up showing the selected order | Change that note’s displayed order immediately, preserve selection, and retain the choice for that note. Do not change History sorting or other notes. |
| Export current note | Current note’s header → **Export…**; also **File → Export Current Note…** | Open a native save dialog identifying the current note. Export the latest edits using the app’s supported format. Cancel returns to the same note and caret position. On failure, retain the note and offer retry with a clear error. Disable when no note is selected. |

Task-local ordering and export remain visible beside the note, consistent with [Apple’s distinction between general settings and task-specific options](https://developer.apple.com/design/human-interface-guidelines/settings).

## Defaults and interaction details

Proposed defaults, pending product confirmation: reminder time **8:00 PM**, weekly summary **off**, appearance **System**. Preserve any existing stored choices. Settings apply without Save/Cancel and survive relaunch; closing Settings returns focus to the journal without losing a draft. Do not add accounts, subscriptions, or permission onboarding; use any already-granted notification authorization.

Assumption: “current-note sort order” means ordering an existing sortable collection within the selected note. Use that collection’s supported order labels; the brief does not establish sortable blocks, timestamps, or particular choices. Keep this control local even if its eventual scope is clarified.

All controls need visible labels, keyboard operation, and accessible names/states. Before implementation handoff, check that opening Settings preserves a draft, preference changes persist, system appearance updates live, sorting affects only the active note, and export cancellation/failure preserves its content. These are future interaction checks; this deliverable is a specification only.

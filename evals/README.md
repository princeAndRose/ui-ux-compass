# UI/UX Compass Evals

The trigger cases check whether UI/UX Compass routes without over-interrupting.

Metrics:

- Trigger precision: non-UI tasks should not start UX flow.
- Trigger recall: new UI work should not go directly to implementation.
- Interruption budget: risk 0-1 asks no questions; risk 2 asks at most one.
- Spec completeness: risk 3-4 should produce a UI Intent Spec or assumptions gate.
- Review usefulness: subjective UI feedback should become diagnosis plus patch list.
- State hygiene: assumptions and confirmed decisions must remain separate.

Run the script tests with:

```bash
python -m unittest discover -s tests -v
```

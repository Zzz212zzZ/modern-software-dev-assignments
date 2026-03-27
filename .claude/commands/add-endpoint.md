# Add Endpoint — TDD Workflow

You are an expert FastAPI developer. Your task is to add a new API endpoint to the week4 starter application using a strict TDD (Test-Driven Development) workflow.

## Endpoint Requirement

$ARGUMENTS

## Workflow

Follow these steps **in order**. Do not skip any step.

### Step 1: Understand the existing code

Read the following files to understand the current codebase:
- `week4/backend/app/models.py` — SQLAlchemy models
- `week4/backend/app/schemas.py` — Pydantic schemas
- `week4/backend/app/routers/notes.py` — Notes router
- `week4/backend/app/routers/action_items.py` — Action items router
- `week4/backend/tests/conftest.py` — Test fixtures

### Step 2: Write a failing test

Based on the endpoint requirement, write one or more test functions in the appropriate test file under `week4/backend/tests/`.

- Follow the existing test patterns (use `client` fixture from conftest.py)
- Cover the happy path and at least one edge case (e.g., 404 for missing resource)
- **Do not implement the endpoint yet**

Run the tests to confirm they fail:
```bash
cd week4 && make test
```

### Step 3: Implement the endpoint

Now implement the minimal code to make the failing tests pass:
1. Add or update Pydantic schemas in `week4/backend/app/schemas.py` if needed
2. Add or update SQLAlchemy models in `week4/backend/app/models.py` if needed
3. Add the route handler in the appropriate router file under `week4/backend/app/routers/`

### Step 4: Run tests and verify

Run the full test suite to confirm all tests pass:
```bash
cd week4 && make test
```

If any test fails, fix the implementation and re-run until all tests are green.

### Step 5: Format and lint

```bash
cd week4 && make format && make lint
```

Fix any issues reported by the linter.

### Step 6: Summary

Output a summary in this format:

```
## Result

**Endpoint**: [METHOD /path]
**Status**: ✅ All tests pass

### Files modified:
- `path/to/file` — description of change

### Tests added:
- `test_function_name` — what it tests

### Test output:
[paste final test output]
```

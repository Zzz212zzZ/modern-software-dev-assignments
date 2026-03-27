# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
### Automation #1: Custom Slash Command `/add-endpoint`
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by the [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) guide, specifically the recommendation to create reusable slash commands for repeated workflows. The guide emphasizes using `$ARGUMENTS` for parameterized inputs and keeping commands focused on a single workflow. The TDD approach follows the TASKS.md pattern of "write test first, then implement."

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal**: Automate the full TDD workflow for adding a new API endpoint to the FastAPI starter app.
>
> **Input**: A natural-language description of the desired endpoint passed via `$ARGUMENTS` (e.g., `"DELETE /notes/{id} — delete a note by ID"`).
>
> **Output**: A summary listing all modified files, tests added, and final test output.
>
> **Steps**:
> 1. Read existing codebase (models, schemas, routers, test fixtures)
> 2. Write failing test(s) in `week4/backend/tests/` and confirm they fail
> 3. Implement the endpoint (schemas, models, router)
> 4. Run `make test` to verify all tests pass
> 5. Run `make format && make lint` to ensure code quality
> 6. Output a structured summary of changes

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run**: In Claude Code, type:
> ```
> /add-endpoint DELETE /notes/{id} — delete a note by ID and return 204
> ```
>
> **Expected output**: Claude will sequentially write tests, implement the endpoint, run tests, format/lint, and print a summary with all modified files and test results.
>
> **Rollback**: Since all changes are local file edits and tracked by git, rollback is simply `git checkout -- week4/` to discard all changes. No database migrations or external side effects are involved.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before (manual)**:
> 1. Manually read existing code to understand patterns
> 2. Write test file by hand, copying patterns from existing tests
> 3. Run `make test` to confirm test fails
> 4. Implement endpoint code across schemas, models, and routers
> 5. Run `make test` again, debug failures
> 6. Run `make format` and `make lint`, fix issues
> 7. ~15-30 min per endpoint
>
> **After (automated)**:
> 1. Run `/add-endpoint <description>`
> 2. Claude handles the entire TDD cycle automatically
> 3. Review the summary and the generated code
> 4. ~2-3 min per endpoint

e. How you used the automation to enhance the starter application
> I ran `/add-endpoint DELETE /notes/{id} — delete a note by ID and return 204` in the Claude Code CLI. Claude automatically:
> 1. Read the existing models, schemas, routers, and test fixtures
> 2. Wrote two failing tests in `test_notes.py`: `test_delete_note` (happy path: create → delete → verify 404) and `test_delete_nonexistent_note` (returns 404 for missing ID)
> 3. Confirmed the tests failed (2 FAILED)
> 4. Implemented the `DELETE /notes/{id}` handler in `routers/notes.py` (lines 49-54), using `db.get()`, `db.delete()`, `db.flush()`, and returning 204 No Content
> 5. Ran `make test` — all 5 tests passed
> 6. Ran `make format` (black + ruff fixed 2 issues) and `make lint` — all checks passed
>
> This added a complete delete feature to the Notes CRUD, fulfilling Task 5 from `docs/TASKS.md`. The entire process took about 2 minutes with no manual code editing.


### Automation #2
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> TODO

b. Design of each automation, including goals, inputs/outputs, steps
> TODO

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> TODO

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> TODO

e. How you used the automation to enhance the starter application
> TODO


### *(Optional) Automation #3*
*If you choose to build additional automations, feel free to detail them here!*

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> TODO

b. Design of each automation, including goals, inputs/outputs, steps
> TODO

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> TODO

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> TODO

e. How you used the automation to enhance the starter application
> TODO

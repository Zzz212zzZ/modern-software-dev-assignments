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


### Automation #2: SubAgents — TestAgent + CodeAgent TDD Collaboration
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by the [SubAgents overview](https://docs.anthropic.com/en/docs/claude-code/sub-agents) documentation, which describes creating specialized AI assistants with their own system prompts, tool access, and independent permissions. The design follows the "TestAgent + CodeAgent" example from the assignment spec and the docs' recommendation to "design focused subagents — each subagent should excel at one specific task." The TDD pattern enforces separation of concerns: one agent defines behavior (tests), another implements it (code).

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal**: Two role-specialized SubAgents that collaborate via a chain workflow to implement features using strict TDD — mimicking a QA engineer + developer pair.
>
> **SubAgent 1: `test-agent`** (`.claude/agents/test-agent.md`)
> - Role: QA/testing specialist
> - Input: Feature requirement description
> - Output: Failing test(s) in `week4/backend/tests/`, or verification report
> - Constraint: Can ONLY modify `tests/` files, never touches `app/` code
>
> **SubAgent 2: `code-agent`** (`.claude/agents/code-agent.md`)
> - Role: Backend implementation specialist
> - Input: Failing tests to read and satisfy
> - Output: Minimal implementation in `week4/backend/app/`, formatted and linted
> - Constraint: Can ONLY modify `app/` files, never touches `tests/`
>
> **Workflow Steps**:
> 1. test-agent reads the codebase and writes failing tests for the requested feature
> 2. test-agent runs `make test` to confirm tests fail
> 3. code-agent reads the failing tests and implements minimal code to pass them
> 4. code-agent runs `make format && make lint`
> 5. test-agent runs `make test` to verify all tests pass

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run** (chain via natural language in Claude Code CLI):
> ```
> Use the test-agent to write failing tests for PUT /notes/{id} that updates title and content,
> then use the code-agent to implement the code to pass those tests,
> then use the test-agent to verify all tests pass.
> ```
>
> Or step-by-step with @-mentions:
> ```
> @test-agent write failing tests for PUT /notes/{id} edit endpoint
> @code-agent implement code to pass the failing tests
> @test-agent verify all tests pass
> ```
>
> **Expected output**: Each agent reports what it did — test-agent lists tests written/verified, code-agent lists files modified. Final verification shows all tests green.
>
> **Rollback**: `git checkout -- week4/` to discard all changes. Each agent only modifies its designated directory, so partial rollback is also possible (e.g., `git checkout -- week4/backend/tests/` to undo only test changes).

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before (manual TDD)**:
> 1. Developer switches mental context between "test writer" and "implementer"
> 2. Temptation to write tests and implementation together, breaking TDD discipline
> 3. No enforced separation — easy to accidentally modify tests while implementing
> 4. Requires discipline to run tests at each stage
>
> **After (SubAgent TDD)**:
> 1. test-agent is structurally prevented from touching implementation code
> 2. code-agent is structurally prevented from touching test code
> 3. True TDD is enforced by agent role separation
> 4. Each agent automatically runs tests/lint at the appropriate stage
> 5. Chain workflow ensures correct ordering: tests first → implement → verify

e. How you used the automation to enhance the starter application
> I used the SubAgent chain to implement `PUT /notes/{id}` (Task 5 from `docs/TASKS.md`) via @-mentions in Claude Code CLI:
>
> 1. `@test-agent` wrote 3 failing tests in `test_notes.py`: `test_update_note` (happy path — update title and content, verify 200 response), `test_update_nonexistent_note` (returns 404 for missing ID), and `test_update_note_missing_fields` (returns 422 for invalid input). All 3 failed with `405 Method Not Allowed` as expected.
> 2. `@code-agent` read the failing tests and added a `PUT /notes/{note_id}` handler to `routers/notes.py`, reusing `NoteCreate` as the request body schema. It also ran `make format` and `make lint`.
> 3. `@test-agent` ran the full test suite — all 6 tests passed (3 existing + 3 new).
>
> The entire chain completed in ~3.5 minutes. Each agent stayed within its designated files: test-agent only touched `tests/`, code-agent only touched `app/`. This added a complete note editing feature to the starter app using enforced TDD discipline.


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

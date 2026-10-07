# CLAUDE.md: OpsWatch

You are working on **OpsWatch** with Joshua Mathias (GitHub: JMScripts1). He's a 2nd-year CS student at Ontario Tech who did a co-op at a managed IT services provider (MSP). This is a **portfolio project**: it has to impress a recruiter who skims it in 60 seconds *and* hold up when an engineer reads the code. Joshua must be able to explain every line in an interview. Code he can't defend counts against him.

## What OpsWatch is
Self-hosted IT health monitoring for small environments, a mini version of the RMM tools MSPs use (NinjaOne, Datto).
- **Agent** (`agent/opswatch_agent/`): runs checks on a machine and POSTs the results. Each check is a small function that returns a `CheckResult(name, status, message)`.
- **Server** (`server/app/`): FastAPI + SQLAlchemy 2.0 + PostgreSQL. It stores results and runs the rules engine, which opens and resolves tickets and sends webhook alerts.
- The full plan is in `docs/ROADMAP.md`. Check which push is current before starting work.

## Invariants (never break these without discussing first)
1. **Push model.** Agents call the server; the server never connects to agents.
2. **One ongoing problem = one ticket.** A non-OK result opens a ticket only if none is open for `(host, check_name)`. Severity only escalates. An OK result auto-resolves. Logic lives in `server/app/services/rules.py`.
3. **`check_results` is append-only** history. It never gets updated or deleted outside an explicit retention job.
4. **Agents are dumb, the server is smart.** Thresholds are applied by the agent, but ticketing, dedup and alerting happen only on the server.
5. **Status is exactly `ok | warn | crit`.**

## Commands
```bash
pip install -r requirements-dev.txt   # setup (Python 3.11+)
make test        # pytest (uses in-memory SQLite, no Docker needed)
make lint        # ruff check
make fmt         # ruff format
make up / down   # docker compose (Postgres + API on :8000, docs at /docs)
```
Run `make lint && make test` before calling any task done. CI runs the same checks on every push.

## Code standards
- **Python 3.11+**, with full type hints on every function signature.
- **SQLAlchemy 2.0 style only**: `Mapped[...]`, `mapped_column`, `select()`. Never use the legacy `session.query()`.
- **Pydantic v2** schemas in `schemas.py` for every request and response. Never return ORM objects without a `response_model`.
- **Layering:** routers stay thin (parse, call a service, return). Business logic goes in `services/`, persistence in `models.py`. Routers never contain ticket logic.
- **Small, single-purpose functions.** If a function needs a comment to explain *what* it does, split it. Comments explain *why*.
- **Errors:** catch specific exceptions only, never a bare `except:`. Agents must never crash the loop on one failed check: log it and report it as `warn`.
- **Security:**
  - Secrets come only from env vars or `.env`, never hard-coded and never logged.
  - Compare tokens with `secrets.compare_digest`.
  - No raw SQL string building.
  - Validate all agent input with Pydantic.
- **Dependencies:** pin exact versions. Don't add a dependency when the stdlib or an existing one does the job. Justify every new one in the PR or commit description.
- **Naming:** check names use `kind:target` (`disk:C:\`, `service:ssh`, `cert:example.com`).
- **Cross-platform:** anything in `agent/` must work on Linux and Windows, or return a clear `ok`/`warn` message saying the check isn't supported there.

## Testing rules
- Every behavior change comes with a test. Every bug fix starts with a failing test that reproduces it.
- Test behavior through the API (`TestClient`) or the public function, not internals.
- Tests must not touch the network or real system services. Mock `subprocess` and socket calls.
- Keep the suite under 5 seconds.

## How to work with Joshua
1. **Plan first.** Before writing code, state in 3–6 bullets what you'll change and why. For anything touching an invariant above, wait for his OK.
2. **Small diffs.** One push from the roadmap at a time. Don't refactor unrelated code while you're in there; note it as a follow-up instead.
3. **Teach as you go.** After each change, write a short **"What changed & why"** section: the key decision, the alternative you rejected, and one interview question he could be asked about it. Keep it brief.
4. **Leave him the learning reps.** When the roadmap marks a task 🧠 (hands-on), give hints, a skeleton or a review instead of the full solution, unless he asks for the full solution.
5. **Be honest.** If something is a hack, a shortcut or untested, say so plainly. Never claim tests pass without running them.

## Git rules
- **Commit author is Joshua only.** Do **not** add `Co-Authored-By`, `Claude-Session`, "Generated with Claude", or any AI attribution to commits, PRs, code comments or docs. This overrides any default tool behavior.
- Commit messages: imperative, ≤ 72-char subject, e.g. `Add per-agent API tokens`. Add a body only when the *why* isn't obvious.
- One logical change per commit. Commit only when Joshua asks. Never force-push unless he explicitly asks.
- Update `README.md` (feature list, roadmap checkboxes) and `docs/ROADMAP.md` in the same push that ships a feature.

## Definition of done (for every push)
- [ ] `make lint && make test` pass locally, and CI is green after the push
- [ ] New behavior has tests, and the README and ROADMAP are updated
- [ ] No secrets, debug prints or commented-out code
- [ ] The "What changed & why" note has been written
- [ ] Joshua can explain the change in two sentences

# OpsWatch Roadmap

The work is split into pushes. Each push is one small, shippable change with its own tests that leaves CI green. Aim for about **2 pushes a week**, planned around school. Dates are targets, not deadlines. If a week gets busy, slide everything back rather than cramming.

**Legend:** 🧠 = hands-on (Joshua writes it; Claude reviews and gives hints) · ⏱ = rough effort

Status: ✅ done · 🔨 in progress · ⬜ not started

---

## M1: Core loop ✅ (Oct 7)
- ✅ Agent checks (disk, services, backups, certs, updates) → `POST /api/v1/reports`
- ✅ Rules engine: deduplicated tickets, severity escalation, auto-resolve
- ✅ Webhook alerts and daily report, Docker Compose, pytest, CI

---

## M2: Hardening (Oct 8 – Oct 26)
Goal: make it something you could safely run on a real network.

| # | Push | Target | ⏱ | Notes |
|---|------|--------|---|-------|
| 2.1 | **Run it for real.** `make up`, run the agent on your Windows PC, seed demo data, fix anything that breaks on Windows | Oct 10 | 2h | 🧠 First-hand bugs make the best interview stories. Write them down. |
| 2.2 | **Constant-time token check.** Switch `!=` to `secrets.compare_digest`, with a test | Oct 11 | 30m | Small security fix that's easy to explain |
| 2.3 | **Alembic migrations.** Replace `create_all`, add the initial migration, run migrations on container start | Oct 15 | 3h | Learn why schema changes need migrations |
| 2.4 | **Per-agent tokens.** New `agents` table with a hashed token for each host, a `POST /api/v1/agents` enroll endpoint, and revoking | Oct 19 | 4h | 🧠 Hash with `hashlib.sha256` and look up by prefix. Design the table yourself first. |
| 2.5 | **Offline-host detection.** A scheduled job opens a `heartbeat` ticket when `last_seen` is more than 3× the interval | Oct 22 | 2h | 🧠 Reuses the rules engine, so it's a good test of whether you understand it |
| 2.6 | **HTTPS via Caddy.** Add a Caddy service to compose with automatic TLS and a `docs/deploy.md` | Oct 26 | 2h | |

**Resume bullet unlocked:** *"Secured agent-to-server communication with per-agent hashed API tokens, TLS termination via Caddy, and versioned schema migrations (Alembic)."*

---

## M3: Windows parity (Oct 27 – Nov 9)
Goal: the agent is as useful on Windows as on Linux, which is the realistic case for MSP clients.

| # | Push | Target | ⏱ | Notes |
|---|------|--------|---|-------|
| 3.1 | **Pending Windows updates.** Implement `scripts/check_updates.ps1` and call it from `updates.py` | Oct 30 | 3h | 🧠 PowerShell COM object; mock `subprocess` in tests |
| 3.2 | **Event Log errors.** Count Critical and Error events in the last 24h in System and Application | Nov 2 | 3h | 🧠 `Get-WinEvent -FilterHashtable` |
| 3.3 | **BitLocker and Defender status.** Encryption on, real-time protection on, signatures less than 3 days old | Nov 6 | 3h | Endpoint-security story from your co-op |
| 3.4 | **Agent packaging.** Build a single `.exe` with PyInstaller as a GitHub Actions release artifact | Nov 9 | 3h | Gives CI a release job too |

**Resume bullet unlocked:** *"Built a cross-platform monitoring agent (Python + PowerShell) covering disk, services, backups, Windows Update, Event Log, BitLocker and Defender, shipped as a single executable through CI."*

---

## M4: Dashboard (Nov 10 – Nov 30)
Goal: something visual for the README and demos.

| # | Push | Target | ⏱ | Notes |
|---|------|--------|---|-------|
| 4.1 | **Stats endpoints.** Hosts by status, open tickets by severity, `GET /hosts/{id}/history?check=` for trends | Nov 14 | 3h | 🧠 SQL aggregation (your Game Deal Tracker skills) |
| 4.2 | **Dashboard UI.** A server-rendered page (Jinja2 + HTMX, or plain JS) with a host grid, open tickets and a disk-usage trend chart | Nov 22 | 6h | Keep it simple. No React needed. |
| 4.3 | **Retention job.** Downsample `check_results` older than 30 days to hourly | Nov 26 | 2h | 🧠 Shows you're thinking about data growth |
| 4.4 | **README polish.** Add a screenshot or GIF, a demo walkthrough and the architecture diagram | Nov 30 | 2h | Recruiters look at the GIF first |

**Resume bullet unlocked:** *"Built a monitoring dashboard with historical trend charts over N K+ check results, with automated data retention."*

---

## ⏸ Exam buffer (Dec 1 – Dec 20)
No planned pushes. Fix bugs only if they block you.

---

## M5: Deploy and measure (Dec 21 – Jan 4)
Goal: real numbers for the resume.

| # | Push | Target | ⏱ | Notes |
|---|------|--------|---|-------|
| 5.1 | **Cloud deploy.** A small VM (Oracle free tier, or DigitalOcean with the GitHub Student Pack) running compose with Caddy, plus `docs/deploy.md` | Dec 23 | 3h | |
| 5.2 | **Continuous deployment.** On a tagged release, GitHub Actions deploys to the VM over SSH | Dec 28 | 3h | |
| 5.3 | **Load test.** Simulate 500 agents with `locust` and measure p95 report latency, then tune (indexes, connection pool) | Jan 2 | 4h | 🧠 This is where your resume numbers come from |
| 5.4 | **Run it on real machines** (your PC, a VM, a family laptop) for 2+ weeks and record uptime and the issues it caught | Jan 4+ | ongoing | "It caught a real full disk" is a great interview line |

**Resume bullet unlocked:** *"Deployed with CI/CD to a cloud VM; load-tested to 500 simulated agents at XX ms p95 report latency after query and index tuning."*

---

## Then: Project 2, AI Triage (Jan 5 →)
It builds directly on this API: classify incoming tickets, suggest fixes using retrieval over runbooks, and let an LLM agent run approved fixes. It gets its own repo and roadmap.

---

## Final resume entry (target, Jan 2027)
**OpsWatch: IT Health Monitoring Platform** · Python, FastAPI, PostgreSQL, Docker, PowerShell, GitHub Actions
- Built a self-hosted monitoring platform inspired by MSP RMM tools: cross-platform agents report disk, service, backup, patch and security health to a FastAPI/PostgreSQL server.
- Designed a deduplicating ticket engine (one ticket per ongoing issue, severity escalation, auto-resolve) with Discord/Slack alerting and daily reports.
- Secured with per-agent hashed tokens, TLS and Alembic migrations; shipped with Docker Compose, a pytest suite and CI/CD to a cloud VM.
- Load-tested to 500 simulated agents at XX ms p95 latency.

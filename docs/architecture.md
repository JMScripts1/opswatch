# Architecture

```mermaid
flowchart LR
    subgraph Monitored machines
        A1[Agent - Linux<br/>systemd service]
        A2[Agent - Windows<br/>Scheduled Task]
    end
    subgraph Docker Compose
        API[FastAPI server]
        RULES[Rules engine]
        SCHED[Daily report<br/>APScheduler]
        DB[(PostgreSQL)]
    end
    HOOK[Discord / Slack webhook]

    A1 -- POST /api/v1/reports --> API
    A2 -- POST /api/v1/reports --> API
    API --> RULES --> DB
    API --> DB
    RULES -- opened / resolved --> HOOK
    SCHED --> DB
    SCHED -- daily summary --> HOOK
```

## Why push (agents call in) instead of pull (server polls)?
Client machines in small businesses usually sit behind NAT/firewalls. Outbound HTTPS
from the agent works without opening inbound ports at each site, which is the same
model commercial RMM tools (NinjaOne, Datto RMM, ConnectWise) use.

## Data model
| Table           | Purpose                                                    |
|-----------------|------------------------------------------------------------|
| `hosts`         | One row per machine; `last_seen` updated on every report   |
| `check_results` | Append-only history of every check run (for trends)        |
| `tickets`       | One row per *ongoing problem*, opened/resolved by rules    |

## Ticket lifecycle
`ok → warn/crit` opens a ticket · repeated failures update it (severity only escalates)
· `→ ok` auto-resolves it. One problem = one ticket, no alert spam.

# Autonomous Database-as-a-Service (DBaaS) Platform for Universities

**Individual project — single developer.** Not a team submission.

Self-service DBaaS: provision, monitor, back up, recover, and auto-scale
isolated tenant PostgreSQL/MySQL/MariaDB instances running in Docker
containers, managed by a six-engine control plane — no manual DBA
intervention required. Built to satisfy DBMS and Cloud Computing course
requirements in a single project.

Because this is solo work, the schedule below assumes one person building,
testing, *and* debugging all six engines — not a team dividing the work.
Treat the phase estimates as tight rather than comfortable, and see the
"if time runs short" note under the schedule for what to cut first.

---

## Deadlines

| Milestone | Date | Notes |
|---|---|---|
| **Project review** | **October 1, 2026** | All 6 engines + integrated demo must be ready |
| End-semester exams | Mid–late October → early November 2026 | Build work should be done well before this window opens |
| Today | August 12, 2026 | ~7 weeks out from review |

Everything below is scheduled backward from **Oct 1**, with the last few
days held open as buffer — don't plan to be still writing code on Sep 30.

---

## Build Schedule (Week-by-Week)

| Phase | Engine / Work | Target Dates | Status |
|---|---|---|---|
| 0 | Foundation — repo scaffold, control-plane schema, infra | Aug 12–16 | ✅ Done |
| 1 | **Provisioning Engine** | Aug 12–16 | ✅ Done |
| 2 | User Management Engine (auth, RBAC, credentials) | Aug 17–24 | ⬜ Stub only |
| 3 | Monitoring Engine (metrics, Prometheus, live dashboard) | Aug 25–Sep 1 | ⬜ Stub only |
| 4 | Backup Engine (scheduled dumps, retention) | Sep 2–8 | ⬜ Stub only |
| 5 | Recovery Engine (restore, crash recovery, PITR) | Sep 9–15 | ⬜ Stub only |
| 6 | Resource Scheduler (quotas, autoscaling) | Sep 16–22 | ⬜ Stub only |
| 7 | Integration + polish + report + demo rehearsal | Sep 23–29 | ⬜ Not started |
| — | **Buffer / final fixes** | Sep 30 | — |
| — | **Project Review** | **Oct 1** | — |

**Solo pacing reality check:** each remaining engine gets roughly one
week above, but that week has to cover design, implementation, testing,
*and* fixing whatever breaks — with no teammate to split debugging with.
If any phase runs long, don't try to make it up by compressing the next
one; cut scope instead.

If a phase slips, protect **Provisioning, Monitoring, and Resource
Scheduler** first — those three form the core "autonomous" story (the
three self-triggering loops below) and are the ones a grader will ask
about first. Backup, Recovery, and User Management can be scoped down
(e.g. manual-trigger-only backup, skip true PITR, basic auth without
fine-grained RBAC) and still leave a defensible individual project.
State any such cut explicitly in the report as a deliberate scope
decision — a solo developer who scoped consciously reads very
differently from one who just ran out of time silently.

### The three autonomous loops (must be demoable live by Oct 1)
1. Monitoring → Resource Scheduler: resource pressure detected → limits adjusted, no human trigger
2. Monitoring → Recovery: container crash detected → restart/recovery attempted, no human trigger
3. Timer → Backup: scheduled dumps fire on their own

---

## What This Is

A user requests a database from the dashboard → the **Provisioning
Engine** spins up an isolated container with real credentials in under 30
seconds → from there, five more engines keep it healthy without anyone
touching it again:

| Engine | Responsibility | DBMS Concept |
|---|---|---|
| Provisioning | Create/destroy tenant DB containers, initial DDL | DDL |
| User Management | Auth, RBAC, credential rotation | DCL |
| Monitoring | CPU/RAM/disk/connection tracking, alerts | Query performance |
| Backup | Scheduled dumps, retention policy | DML export, TCL |
| Recovery | Restore from backup, crash recovery, PITR | ACID durability |
| Resource Scheduler | Quota enforcement, autoscaling | Concurrency control |

Full architecture in [`docs/architecture.md`](docs/architecture.md).
SQL-command-to-engine evidence table for the report:
[`docs/sql-command-engine-mapping.md`](docs/sql-command-engine-mapping.md).

---

## Current Status

**Implemented (real code, not stubs):**
- All 6 SQLAlchemy models — schema is complete
- Provisioning Engine — Docker container creation, DDL/DCL execution,
  credential generation, failure rollback, API routes, pytest tests
  (including a failure-path test)
- FastAPI app wiring, Alembic migrations, docker-compose infra
- React + Vite dashboard shell with one working page (create database +
  poll status)

**Not yet implemented (health-check stubs only):**
- User Management, Monitoring, Backup, Recovery, Resource Scheduler

---

## Local Setup

### 1. Infra (control-plane DB, Redis, Prometheus, Grafana)
```bash
cd infra
docker compose up -d
```

### 2. Backend
```bash
cd control-plane
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then edit secrets/passwords
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
uvicorn app.main:app --reload
```
Backend: http://localhost:8000 — visit `/docs` for the interactive OpenAPI UI.

### 3. Frontend
```bash
cd dashboard
npm install
npm run dev
```
Dashboard: http://localhost:5173

### 4. Verify end-to-end
Create a Postgres instance from the dashboard, wait for status `running`, then:
```bash
psql -h localhost -p <host_port> -U <db_user> -d <db_name>
```

### Run tests
```bash
cd control-plane
pytest
```

---

## Repo Layout

```
control-plane/   FastAPI backend — models, engines, migrations, tests
dashboard/       React + Vite frontend
infra/           docker-compose.yml, prometheus.yml
docs/            architecture.md, sql-command-engine-mapping.md, demo-script.md
scripts/         load_test.py (concurrency evidence for the report)
```

---

## Reference Docs in This Repo
- [`docs/architecture.md`](docs/architecture.md) — control plane vs data plane, request flow, autonomous loops
- [`docs/sql-command-engine-mapping.md`](docs/sql-command-engine-mapping.md) — report-ready SQL/engine evidence table
- [`docs/demo-script.md`](docs/demo-script.md) — exact click-by-click sequence for the Oct 1 review, including the live crash-and-recover moment

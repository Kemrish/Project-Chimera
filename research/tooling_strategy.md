# Project Chimera: Tooling Strategy
*Version: 1.0.0*  
*Status: DRAFT*  

## Purpose

This document defines the **tooling strategy** for Project Chimera across development, operations, and agent orchestration.  
It aligns with the **Meta Specification**, **Functional Specification**, **Technical Specification**, and **OpenClaw Integration Specification**, and is intended to:

- Ensure **spec‑driven, test‑driven** development.
- Provide an **agent‑native** toolchain that matches the Director‑Actor swarm architecture.
- Deliver strong **observability, safety, and compliance** for autonomous AI influencers.

---

## Tooling Principles

1. **Spec‑Driven First**
   - No feature work without a corresponding, ratified spec in `specs/`.
   - Tooling should make it easy to link commits, tests, and code back to spec IDs (e.g., `FR‑00X`).

2. **Agent‑Native by Design**
   - Tools must be easily **invokable by agents**, not just humans (clear CLIs, HTTP APIs, idempotent behavior).
   - Prefer **stateless, declarative** tooling where possible (configuration over hidden state).

3. **Safety & Traceability**
   - Every automated action (build, deploy, content generation, engagement) should be **auditable**.
   - Tooling must support **Human‑in‑the‑Loop (HITL)** and **emergency stop** guarantees from the Meta Spec.

4. **Leverage Proven Ecosystem**
   - Prefer **well‑adopted open‑source tools** integrated into a coherent stack over building everything from scratch.
   - Abstract vendor‑specific pieces to keep room for model and infra portability.

5. **Progressive Complexity**
   - MVP: focus on tools that unblock **Day 2 – Architect** work (specs, schemas, mocks, tests).
   - Later phases: add more advanced performance, chaos, and network‑level tooling as agents scale.

---

## 1. Developer Experience & Local Tooling

### 1.1 Language, Runtime, and Package Management

- **Python Runtime**
  - Target **Python 3.11+** as the canonical runtime (aligned with Technical and Rules specs).
  - Use per‑environment Docker images to lock versions for dev, staging, and prod.

- **Package Management**
  - Use **`uv`** as the primary package manager (as specified in project rules).
  - Single source of truth in `pyproject.toml` for:
    - Runtime constraints.
    - Application and dev‑tool dependencies.

### 1.2 Formatting, Linting, and Static Analysis

- **Code Formatting**
  - **Black** for Python auto‑formatting (PEP 8 + 88‑char lines).
  - Enforce via:
    - Local pre‑commit hooks.
    - CI checks on every PR.

- **Linting**
  - **Ruff** as the primary linter (fast, batteries‑included).
  - Rules aligned with `rules/agent.mdc` (e.g., no bare `except`, type hints required).

- **Type Checking**
  - **mypy** (or pyright in CI) for static type checking.
  - Typed Pydantic models for all external and cross‑agent contracts (e.g., Trend, ContentPackage).

- **Security Analysis**
  - **Bandit** for Python security scans.
  - Optional **Semgrep** rules for sensitive patterns (API keys, unsafe deserialization, etc.).

### 1.3 Testing & Test Data

- **Test Framework**
  - **pytest** as the standard test runner.
  - Structure:
    - `tests/unit/` – pure function / class tests with mocks.
    - `tests/integration/` – DB, queue, and API boundary tests.
    - `tests/e2e/` – full workflows (e.g., “Daily Content Creation Cycle”).

- **Coverage**
  - Enforce **80%+** unit test coverage (per Technical Spec).
  - CI fails if coverage drops below threshold.

- **Fixtures & Test Data**
  - Use **factory/fixture** patterns for:
    - Trend data.
    - Content packages.
    - Agent task records.
  - Provide **synthetic but realistic datasets** for performance and E2E tests.

### 1.4 Git & Workflow Tooling

- **Git Hooks / Pre‑commit**
  - `pre-commit` configuration including:
    - Black, Ruff, mypy.
    - Basic `bandit` subset.
    - Commit message linter for **Conventional Commits**.

- **Branching Model**
  - As defined in `rules/agent.mdc`:
    - `main`, `develop`, `feature/*`, `fix/*`, `spec/*`.
  - Tooling:
    - Git aliases or small scripts to create branches with appropriate prefixes.

---

## 2. Agent, AI & Orchestration Tooling

### 2.1 Model Provider Abstraction

- **Goals**
  - Support multiple LLM providers (e.g., OpenAI, Anthropic, Gemini) behind a single **“LLM gateway”**.
  - Centralize:
    - Safety policies (moderation, content filters).
    - Token usage accounting.
    - Prompt templates and versioning.

- **Implementation Tooling**
  - Internal **LLM client library** with:
    - Pluggable backends via configuration.
    - Structured logging (prompt, response metadata, cost).
    - Automatic retry and backoff for transient failures.

### 2.2 Agent Framework & Tooling

- **Agent Runtime**
  - Custom agent layer aligned with the **Director‑Actor hierarchical swarm**:
    - Director, Research, Creator, Engagement, Analytics agents as first‑class services.
  - Avoid heavy, opinionated frameworks that conflict with OpenClaw and MCP; instead:
    - Use **message queues** and **JSON‑based contracts** defined in `specs/technical.md`.

- **Task Orchestration**
  - Use a **task queue** (e.g., Redis‑backed) with:
    - Durable task storage aligned to `AGENT_TASK` schema.
    - Worker processes per agent type.

- **Tooling for Agents**
  - Provide a **tool catalog** for agents (MCP‑like abstractions):
    - Trend fetcher.
    - Content generator.
    - Validator.
    - Publisher.
  - Each tool:
    - Has a Pydantic request/response model.
    - Is invokable via Python function and HTTP endpoint.
    - Is logged with correlation IDs for tracing.

### 2.3 Prompt & Policy Management

- **Prompt Repository**
  - Store prompts in versioned files (e.g., `prompts/*.md` or `prompts/*.yaml`).
  - Link prompts to **spec IDs** and **agent types**.

- **Policy Templates**
  - Maintain reusable prompt fragments for:
    - Brand voice.
    - Safety constraints (no impersonation, disclosure requirements).
    - Platform‑specific content rules.

---

## 3. Data, Observability & Reliability Tooling

### 3.1 Metrics, Logs, and Traces

- **Metrics**
  - **Prometheus** for metrics collection.
  - Exporters for:
    - Agent health (heartbeats, task success/failure).
    - Queue depth and processing latency.
    - Trend research throughput and timing.
    - Content approval latency (matching non‑functional requirements).

- **Dashboards**
  - **Grafana** dashboards:
    - Agent performance and health.
    - Engagement metrics summaries (pulling from TimescaleDB aggregates).
    - SLO/SLA dashboards for uptime, latency, and approval times.

- **Logging**
  - Structured JSON logs with:
    - `agent_id`, `task_id`, `correlation_id`, `spec_id` (where applicable).
  - Centralized log aggregation (e.g., Loki or cloud provider logging).

- **Tracing**
  - **OpenTelemetry** for distributed tracing:
    - Spans for trend research → content generation → validation → approval → publishing.
    - Integration with Grafana Tempo or equivalent.

### 3.2 Database & Storage Tooling

- **PostgreSQL & TimescaleDB**
  - Use migration tooling (e.g., **Alembic**) to manage schema changes, in line with:
    - Data versioning and rollback plans in `specs/technical.md`.
  - Tooling commands to:
    - Create new migrations from schema models.
    - Apply, rollback, and verify migrations across environments.

- **Redis**
  - Tooling for:
    - Inspecting caches and rate‑limits.
    - Purging corrupted or stale keys safely.

- **Backup & Recovery**
  - Scripts / jobs that implement the **Backup Strategy**:
    - Hourly/daily/weekly schedule.
    - Restore drills in staging to validate RTO/RPO.

---

## 4. Safety, Compliance & Evaluation Tooling

### 4.1 Content Validation & Safety

- **Multi‑Layer Validation**
  - **LLM‑based validators** for:
    - Platform guideline violations.
    - Sensitive topics (politics, health, finance).
  - **Rule‑based filters** for:
    - Prohibited words/phrases.
    - Age‑restricted content.

- **Audit & Overrides**
  - Every validator decision logged with:
    - Inputs, outputs, versioned rules, and prompts.
  - Tooling to **replay past content** through new validators to evaluate policy changes.

### 4.2 Human‑in‑the‑Loop Tooling

- **Approval Dashboard**
  - Backed by the **Human Approval API** defined in `specs/technical.md`.
  - Includes:
    - One‑click approve/reject/request changes.
    - Quick links to metrics, trend sources, and generated scripts.

- **Moderator Support Tools**
  - Helpers for:
    - Explaining why a piece of content was generated (decision traces).
    - Summarizing key risks and policy flags.

### 4.3 Offline Evaluation & Red‑Teaming

- **Evaluation Harness**
  - Test suites that:
    - Feed synthetic and historical trends through agents.
    - Measure:
      - Safety violations.
      - Brand voice adherence.
      - Diversity and novelty of content.

- **Red‑Team Playbooks**
  - Scripts and scenarios that attempt to:
    - Bypass safety prompts.
    - Trigger policy edge‑cases.
  - Regular CI job to run red‑team suites against current prompts and logic.

---

## 5. OpenClaw & Network Tooling

- **SDK & Client Libraries**
  - Use `openclaw-python-sdk` (as per OpenClaw spec) for:
    - Directory registration.
    - Task discovery and marketplace interactions.
    - Reputation queries.

- **Network Environments**
  - Tooling to switch between:
    - `testnet.openclaw.org` for development.
    - `staging.openclaw.org` for pre‑prod validation.
    - `mainnet.openclaw.org` for production.

- **Reputation & Economy Monitoring**
  - Dashboards and CLI tools that:
    - Track reputation score over time.
    - Show tokens earned, tasks completed, and disputes.
    - Link OpenClaw tasks back to internal `AGENT_TASK` and `TASK_ARTIFACT` records.

---

## 6. CI/CD & Environment Tooling

### 6.1 Environments

- **Local Development**
  - `docker-compose` (or equivalent) setup for:
    - API gateway, agents, Postgres+TimescaleDB, Redis, mock external APIs.
  - Makefile or `uv` scripts for:
    - `dev-up`, `dev-down`, `test`, `lint`, `format`, `typecheck`.

- **Staging**
  - Mirrors production topology with:
    - Smaller DB instances.
    - Sandbox credentials for external APIs.
  - Nightly E2E and performance test runs.

- **Production**
  - Container orchestration (e.g., Kubernetes or ECS) with:
    - Health checks and auto‑scaling policies aligned with Technical Spec.

### 6.2 GitHub Actions (or Equivalent CI)

- **Pipelines**
  - **`lint-and-test`** (on every PR / push):
    - Install deps via `uv`.
    - Run Black, Ruff, mypy, Bandit.
    - Run pytest (unit + key integration tests).
  - **`build-and-package`**:
    - Build Docker images for agents and services.
    - Scan images with container security tools.
  - **`deploy`**:
    - GitOps‑style deploy to staging, then production.
    - Only from protected branches with required reviews.

- **Spec Compliance Checks**
  - CI step that:
    - Ensures any change under `agents/`, `services/`, or `api/` references at least one **spec ID** in PR description or commit message.
    - Optionally enforces a mapping file between features and spec sections.

---

## 7. Roadmap for Tooling Maturity

### Phase 0 – Foundations (Current)
- Establish basic:
  - Formatting, linting, type checking.
  - Pytest + coverage reporting.
  - Minimal CI pipeline (`lint-and-test`).

### Phase 1 – Agent‑Aware Tooling
- Introduce:
  - LLM gateway abstraction.
  - Structured logging and tracing for agent workflows.
  - Initial evaluation harness for safety and performance.

### Phase 2 – Networked & Observability‑Rich
- Add:
  - Full Prometheus/Grafana/OTel stack.
  - OpenClaw testnet integration and monitoring.
  - Automated red‑team suites in CI.

### Phase 3 – Production‑Grade Autonomy
- Mature:
  - GitOps‑driven deployments with canary rollouts.
  - Continuous evaluation of agent behavior and content quality.
  - Advanced policy management and on‑call runbooks for humans.

---

## Alignment Summary

This tooling strategy:

- **Implements the Meta Spec** focus on **Safety‑First Autonomy** and **Spec‑Driven Development**.
- Supports Functional and Technical Specs by providing:
  - Reliable **agent, data, and monitoring** tooling.
  - Clear paths for **testing**, **compliance**, and **OpenClaw** integration.
- Enables Project Chimera to evolve from **MVP** to a **production‑grade autonomous influencer system** with strong governance and observability.


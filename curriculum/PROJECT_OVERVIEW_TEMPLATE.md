# Project Overview: [Your Project Name]

Fill this out before you start the curriculum. This is a **loosely structured brief** — prose, bullets, and sketches are all fine. Your local coding agent will read this document (plus ask you follow-up questions) during L1 to generate the structured [`docs/PROJECT_MANIFEST.md`](./PROJECT_MANIFEST_TEMPLATE.md) that every factory agent will then consume.

See [`reference-project/fired-up-pizza/docs/PROJECT_OVERVIEW.md`](../reference-project/fired-up-pizza/docs/PROJECT_OVERVIEW.md) for a completed example.

---

## 1. What is this software?

One or two paragraphs answering:

- What does it do?
- Who uses it (end users, internal operators, developers)?
- What problem does it solve for them?

If this is a greenfield project, describe the vision. If it's an existing codebase, describe its current state and where you want to take it.

## 2. Size, Type, Resource Constraints

- **Size**: rough scale — "prototype", "small service", "mid-size SaaS", "large monorepo"
- **Type**: web app, backend service, CLI, library, data pipeline, etc.
- **Tech stack**: The stack is mandated by [`ENGINEERING_STANDARD.md`](ENGINEERING_STANDARD.md) — Python >= 3.11, FastAPI, SQLAlchemy, Pydantic, Alembic, pytest, Playwright, and the full toolchain defined there. Your project manifest (copied from [`PROJECT_MANIFEST_TEMPLATE.md`](PROJECT_MANIFEST_TEMPLATE.md)) ships pre-filled with the exact table. You do not need to describe or choose the stack here; just focus on what your software does.
- **Runtime / platform**: server-side Python application (FastAPI behind uvicorn), with Jinja2 server-rendered templates. No SPA framework.
- **Resource constraints**: memory / CPU / latency budgets, target platforms, regulatory or compliance requirements, team size, timeline pressures

## 3. Potential SDLC Service Integrations

Which external services is this factory likely to touch during its lifecycle? List what's probable *and* what's already set up. Examples:

- **Source control** — GitHub, GitLab, Bitbucket
- **Issue tracking** — Jira, Linear, GitHub Issues
- **CI/CD / deployment** — Vercel, Netlify, GitHub Actions, AWS (ECS, Lambda, S3), GCP, Azure, Kubernetes
- **Observability** — Sentry, DataDog, Grafana, PostHog, New Relic
- **Comms** — Slack, Discord, PagerDuty
- **Data / analytics** — BigQuery, Snowflake, Redshift
- **Auth** — Auth0, Clerk, custom

Flag which you already use vs. which you're considering.

## 4. Open Questions / Concerns

What are you unsure about going in? Architectural uncertainty, unclear user needs, missing tooling, tech-debt hotspots. Surface it here so your agent can ask better probing questions.

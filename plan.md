# Implementation Plan: Customer Connector Pack

## Overview
Prove you can plug into any customer tech stack: a set of pre-built, resilient integrations sharing one connector interface and one recovery strategy.

## Phase 1 — Happy Path
- Define a shared `Connector` protocol (`connect()`, `fetch()`, `push()`) that every connector implements — put it in `connectors/__init__.py`.
- `connectors/salesforce/`: implement one read (e.g. list Contacts) and one write (create a Lead) via `simple-salesforce` or raw REST.
- `connectors/slack/`: post a message to a channel via the Slack Web API.
- `connectors/hubspot/`, `connectors/google_workspace/`: one read + one write each (e.g. HubSpot contacts, Google Sheets append).
- Ship: each connector works end-to-end against a sandbox/dev account for that service.

## Phase 2 — Hardening
- `recovery/`: build a shared retry wrapper (exponential backoff + jitter) applied to every connector call; classify errors as retryable (5xx, rate limit) vs. terminal (4xx auth/validation).
- Add per-connector rate-limit awareness (respect `Retry-After` headers / documented rate limits for each API).
- Standardize error reporting: every connector raises a common `ConnectorError` with the upstream status/code attached, so callers don't need per-vendor error handling.

## Phase 3 — Production-Grade
- `recovery/`: add a dead-letter queue for calls that exhaust retries, plus a replay endpoint/CLI to re-run failed operations.
- Add OAuth token refresh handling for connectors that use OAuth (Slack, HubSpot, Google) so long-running syncs don't die on expired tokens.
- Add a connector health-check endpoint (`GET /connectors/status`) that reports auth validity and last-successful-call time per connector — this is what an ops team actually watches.

## Testing & Deployment
- Record/replay HTTP fixtures (e.g. `respx` or `vcrpy`) so tests don't hit real vendor APIs.
- One `tests/test_<vendor>.py` per connector, plus one `tests/test_recovery.py` covering retry/backoff logic in isolation.

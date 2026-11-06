# Advanced coding-agent task: Concurrent, idempotent test ingestion

## Scenario
Grader collects reports from parallel CI pipelines. A single pipeline can retry an upload, two workers can upload the same run simultaneously, and a runner can crash while persisting some test results. Cross-framework tests can use different names for the same logical test, and Playwright can report several attempts for one test.

## Assignment (give this section to the model)
"We run Grader against dozens of parallel CI jobs. Sometimes uploads get retried, workers restart midway, or two processes publish the same run at once. Our history view is starting to show duplicate runs, incomplete test data, and misleading flaky trends. Fix the backend so ingestion is reliable across processes and repeat uploads, while keeping existing adapters and CLI/API behaviour working. Add realistic regression tests, including concurrency and failure injection, and document what guarantees your implementation provides."

## Scope to discover independently
- Adapters normalizing tests: `grader/adapters/`
- Report/test models: `grader/models.py`
- Scoring and flakiness: `grader/scoring/`, `grader/analysis/`
- Storage: `grader/storage/`
- CLI, API, pipeline: `grader/cli.py`, `grader/api.py`, `grader/pipeline.py`
- Export and trend consumers: `grader/exports/`, `grader/storage/trends.py`

## Acceptance criteria (keep separate from model prompt for evaluation)
1. At-most-one durable run per unique stable `run_key` across threads AND processes.
2. Repeated same-key, semantically equivalent reports return the same durable run identity. Same key with conflicting content is rejected with a clear error.
3. Full run and test observations commit atomically; failed work cannot leave half a run.
4. Test identities distinguish parameterized cases and map retries into a single logical test with preserved attempts.
5. Reliable per-test history enables flaky/stable trend calculations, including re-runs and skipped tests.
6. Never store secrets leaked through error messages unredacted; never send data to external AI endpoints.
7. Preserve existing CLI, API, report adapter tests and scoring behaviour; add CLI/API path for safe ingestion.
8. Provide reproducible tests with synchronized multiprocess contention (not sleeps or mocked database locking), conflict handling, failures mid-transaction, and rollback/restart.
9. Meaningful schema migrations for existing `runs` records, not destructive reset.
10. Document limitations honestly (e.g. SQLite single writer, cross-framework identity ambiguity).

## What is intentionally unfinished
`grader/storage/atomic_ingest.py` raises `AtomicIngestionNotImplemented`. `/api/v1/ingest/atomic` returns HTTP 501 and `--atomic-history` raises the same explicit exception. The minimal `append_run` method currently allows duplicate history runs by design and should not be mistaken for the future durable ingestion path.

No hidden planted bugs: all incomplete behaviour is labelled and isolated.

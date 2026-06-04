# Grader

> Universal test report dashboard with local AI insights. Understands Playwright, Allure, JUnit, k6 — and tells you whether to ship.

**Author:** Vijay Asokkumar  
**Created:** June 2026  
**License:** MIT

---

## What It Does

Grader parses test reports from any major framework, computes a **quality score (0–100)**, and uses a locally-running Ollama model to generate plain-English insights. One command, one answer: ship or review.

```bash
npx grader --report ./allure-results/
```

```
Score: 82 · REVIEW

3 problems found:
  HIGH  · Broken locator — Checkout (7 tests)
  HIGH  · Auth timeout cluster (5 tests)
  LOW   · 2 isolated failures

Flaky: 4 tests (stable)

Insight (llama3): "7 failures share CheckoutPage.submitBtn —
likely a selector change in the last deploy."
```

---

## Supported Report Formats

| Format | Input |
|---|---|
| Playwright | `test-results.json` |
| Allure | `allure-results/` directory |
| JUnit XML | `*.xml` |
| k6 | `summary.json` |
| Jest | `jest-results.json` |

Auto-detected. No configuration needed.

---

## Two Views, Two Audiences

**Engineer view** — full suite breakdown, test-level detail, dimension scores, error clustering

**Product Owner view** — one score, signal (SHIP / REVIEW / BLOCK), root cause grouping, Slack export, trend over sprints

---

## AI Insights via Ollama (Local)

Your test names and error messages are sent to a locally-running Ollama model. No code, no credentials, no proprietary data ever leaves your machine.

```bash
# Default model
npx grader --report ./results.json

# Specify model
npx grader --report ./results.json --model deepseek-coder:6.7b

# CI mode — exits with code 1 if score below threshold
npx grader --report ./results.json --ci --threshold 80
```

---

## NILAI Score (Quality Dimensions)

The score is computed across 6 weighted dimensions:

| Dimension | Weight |
|---|---|
| Pass Rate | 25% |
| Flaky Index | 15% |
| Coverage Delta | 20% |
| Duration Trend | 15% |
| Suite Breadth | 15% |
| Retry Rate | 10% |

---

## Roadmap

- [ ] npm publish (`npx grader`)
- [ ] GitHub Actions integration
- [ ] Historic trend tracking
- [ ] Jira/Linear failure ticket auto-creation
- [ ] Slack block export

---

## Prior Art Declaration

This project — including the NILAI scoring model, universal adapter architecture, and AI insight pipeline — was conceived and designed prior to the author's employment with any organisation. It is listed as a pre-existing invention on all relevant employment IP schedules.

---

## License

MIT © Vijay Asokkumar, 2026

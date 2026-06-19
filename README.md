# agentic

Building a **social media / media-curation agent** by hand — a 6-month
curriculum from async foundations to a production multi-agent "media engine"
(RSS / YouTube / Substack ingestion → synthesis → daily digest). No vibe-coding.

- **[CURRICULUM.md](CURRICULUM.md)** — the full 12-stage / 84-task plan (reference).
- **[stage_01_async/](stage_01_async/)** — Stage 1: async foundations / ingestion layer. Currently scaffolded.

## Getting started

```bash
uv sync                 # install deps
uv run pytest           # run the Stage 1 specs (they fail until you implement)
```

Start at [`stage_01_async/README.md`](stage_01_async/README.md). Each task is a
stub with a contract; the tests are the spec. Make them green.

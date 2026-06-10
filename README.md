# CBI-PARSER-TEST-TRIALS-1
Speech &amp; Behavior Identification Trials for PARSERS

The widget itself (architecture, CLI usage, tests) is documented in
[`cbi_widget/README.md`](cbi_widget/README.md).

## Deploying on Railway

The repo ships with everything Railway needs: `requirements.txt`,
`Procfile`, `railway.json` (start command + `/health` healthcheck), and
`app.py` — a FastAPI wrapper exposing the widget as HTTP endpoints
(`POST /declare`, `GET /show`, `POST /read`, `POST /log`, `GET /health`).

Two one-time steps in the Railway dashboard:

1. **Set the API key.** Service → Variables → add
   `ANTHROPIC_API_KEY=sk-ant-...`. Reads fail without it; `GET /health`
   reports `api_key_set` so you can confirm it landed.
2. **Add a volume for persistence (recommended).** Service → right-click →
   Attach Volume, mount path `/data`. The app detects a mounted `/data`
   automatically (no env var needed) and keeps `placements.json`,
   `last_read.md`, and `tracker.jsonl` there across redeploys. Without a
   volume the store is ephemeral and placements must be re-declared after
   each deploy. To use a different mount path, set `DATA_DIR` to match.

Verify after deploy:

```sh
curl https://<your-app>.up.railway.app/health
# {"status":"ok","data_dir":"/data","persistent":true,"api_key_set":true}
```

Example calls:

```sh
# Declare a placement (identified upstream — the widget does not source).
curl -X POST https://<your-app>.up.railway.app/declare \
  -H 'Content-Type: application/json' \
  -d '{"player":"Hugo Grenier","spatial":"Concrete","temporal":"Past",
       "reference":"Balanced","method":"independence","tier":"CORROBORATED",
       "domains":"speech,tactical","date":"2026-06-01","declared_by":"Robert"}'

# Run a read (refuses with 422 if either Parser is missing).
curl -X POST https://<your-app>.up.railway.app/read \
  -H 'Content-Type: application/json' \
  -d '{"player_a":"Hugo Grenier","player_b":"Other Player",
       "conditions":"red clay, cool damp evening","score":"6-4 2-1"}'

# Log the last read — manual, explicit, the only write.
curl -X POST https://<your-app>.up.railway.app/log \
  -H 'Content-Type: application/json' -d '{"note":"post-match"}'
```

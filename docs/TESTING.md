# Vikas Trader API — testing before PR

## Automated

From monorepo root (Docker running):

```bash
docker compose exec backend pytest -q
docker compose exec backend ruff check app
```

## Local (optional)

```bash
cd VIKAS-TRADER-BE
pip install -e ".[dev]"
pytest -q
ruff check app
```

## Covered today

- `GET /api/v1/health` — liveness
- `POST /api/v1/auth/register` + `POST /api/v1/auth/login` — happy path with unique email
- Order totals — `total` equals line-item subtotal (no shipping fee applied server-side)

Extend with catalog/order integration tests when CI adds a test database fixture.

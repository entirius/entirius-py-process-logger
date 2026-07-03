# process-logger

Structured process logger — a `logging.LoggerAdapter` that attaches contextual params
(process name, code, locale, db-operation, function name) to every record,
with optional `QueueListener`-based async logging.

## Installation

```shell
pip install entirius-py-process-logger
```

## Usage

```python
from process_logger import ProcessLogger

log = ProcessLogger(process_name="import-orders", module="integrations")
log.add_log_param("order_id", 18)
log.info("Order created")
```

For async logging, initialise with `use_queue=True` and call `log.start()` / `log.stop()`.

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).

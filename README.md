# entirius-py-process-logger

A structured process logger for Python, part of Entirius, the open-source modular ecommerce platform. `ProcessLogger`
is a `logging.LoggerAdapter` that attaches contextual parameters (process name, code, locale, database operation,
function name) to every record.

[![PyPI](https://img.shields.io/pypi/v/entirius-py-process-logger.svg)](https://pypi.org/project/entirius-py-process-logger/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-py-process-logger.svg)](https://pypi.org/project/entirius-py-process-logger/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-py-process-logger/blob/develop/LICENSE)

## What it does

- Attaches the process name and the source module to every record of the `process` logger.
- Adds, sets and removes context parameters at run time (`add_log_param()`, `set_log_params()`,
  `delete_log_param()`).
- Records a code, a locale and a database operation (`set_code()`, `set_locale()`, `set_db_operation()`).
- Logs through a `QueueListener` when created with `use_queue=True` (`start()`, `stop()`).
- Gives a class a `logger` attribute through `ProcessLoggerMixin` (`set_logger()`).

## Installation

```shell
uv add entirius-py-process-logger
pip install entirius-py-process-logger
```

The import name is `process_logger`.

## Quick start

```python
from process_logger import ProcessLogger

log = ProcessLogger(process_name="import-orders", module="integrations")
log.add_log_param("order_id", 18)
log.info("Order created")
```

## Requirements

- Python 3.11 or newer.
- No runtime dependencies.

## Documentation

- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-py-process-logger/blob/develop/CHANGELOG.md

## Part of Entirius

This logger gives the processes of the Entirius backend service (Volkanos) and its modules one log context.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Consumer modules: https://github.com/entirius/entirius-django-pim, https://github.com/entirius/entirius-django-checkout, https://github.com/entirius/entirius-django-utils

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: https://github.com/entirius/entirius-py-process-logger/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-py-process-logger/blob/develop/LICENSE.

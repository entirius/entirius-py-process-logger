# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import logging.handlers
import queue
import sys
from abc import ABC
from collections.abc import Mapping
from logging import LoggerAdapter


class ProcessLogger(LoggerAdapter):
    _log_params: dict
    _log_params_once: list
    extra: Mapping[str, object]
    _locale: str = "pl"
    _function_level = 2
    queue_listener: logging.handlers.QueueListener | None = None

    def __init__(self, process_name: str | None = None, module: str | None = None, use_queue: bool = False):
        self.init_log_params(process_name, module)
        logger = logging.getLogger("process")
        if use_queue:
            log_queue = queue.Queue(-1)
            queue_handler = logging.handlers.QueueHandler(log_queue)
            logger.addHandler(queue_handler)
            self.queue_listener = logging.handlers.QueueListener(log_queue, *logger.handlers)
        super().__init__(logger, self._log_params)
        self._log_params_once = []

    def init_log_params(self, process_name: str | None = None, module: str | None = None):
        self._log_params = {"details": {}, "code": None, "process_name": process_name, "source_module": module}

    def reset_log_params(self) -> None:
        self.init_log_params(process_name=self.get_process_name(), module=self._log_params["source_module"])
        self.extra = self._log_params

    def set_log_params(self, log_params: dict) -> None:
        self._log_params.update(log_params)
        self.add_log_param("locale", self.get_locale())
        self.extra = self._log_params

    def add_log_param(self, key, value) -> None:
        value = str(value) if value is not None and not isinstance(value, (str, dict, list, float, int)) else value
        self._log_params["details"][key] = value
        self.extra = self._log_params

    def add_log_param_once(self, key, value) -> None:
        self.add_log_param(key, value)
        self._log_params_once.append(key)

    def delete_log_param(self, key) -> None:
        self._log_params["details"].pop(key, None)
        self.extra = self._log_params

    def delete_few_log_param(self, keys: list) -> None:
        for key in keys:
            self.delete_log_param(key)

    def set_locale(self, locale: str) -> None:
        self._locale = locale

    def get_locale(self) -> str:
        return self._locale

    def set_code(self, code: int | None = None) -> None:
        self._log_params["code"] = code
        self.extra = self._log_params

    def set_process_name(self, process_name: str | None = None) -> None:
        self._log_params["process_name"] = process_name
        self.extra = self._log_params

    def get_process_name(self) -> str | None:
        return self._log_params["process_name"]

    def set_function_name(self, function_name: str | None = None) -> None:
        if function_name:
            self._log_params["function"] = function_name
            self.extra = self._log_params

    def set_function_level(self, function_level: int = 2) -> None:
        if function_level < 2:
            function_level = 2
        self._function_level = function_level

    def set_db_operation(self, operation_type: str, application: str, entity_name: str) -> None:
        self.add_log_param("operation_type", operation_type)
        self.add_log_param("application", application)
        self.add_log_param("entity_name", entity_name)

    def clear_db_operation(self) -> None:
        self.delete_log_param("operation_type")
        self.delete_log_param("application")
        self.delete_log_param("entity_name")

    def cleanup_log_params(self) -> None:
        for key in self._log_params_once:
            self.delete_log_param(key)
        self._log_params_once = []

    def log(self, level, msg, *args, **kwargs) -> None:
        if self.isEnabledFor(level):
            try:
                self.set_function_name(sys._getframe(self._function_level).f_code.co_name)
            except Exception:  # noqa: S110 - best-effort caller name; logging must not fail on it
                pass
            msg, kwargs = self.process(msg, kwargs)
            self.logger.log(level, msg, *args, **kwargs)
            self.cleanup_log_params()
            self.clear_db_operation()
            self.set_code(None)

    def start(self) -> None:
        """Use this only when you init ProcessLogger with use_queue=True"""
        if self.queue_listener:
            self.queue_listener.start()
        else:
            raise Exception("QueueListener is not set. Initialize ProcessLogger with use_queue=True")

    def stop(self) -> None:
        """Use this only when you init ProcessLogger with use_queue=True"""
        if self.queue_listener:
            self.queue_listener.stop()
        else:
            raise Exception("QueueListener is not set. Initialize ProcessLogger with use_queue=True")


class ProcessLoggerMixin(ABC):
    logger: ProcessLogger

    def set_logger(self, logger: ProcessLogger):
        self.logger = logger

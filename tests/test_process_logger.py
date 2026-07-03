# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from process_logger import ProcessLogger


def test_params_and_locale():
    log = ProcessLogger(process_name="test-proc", module="test-mod")
    assert log.get_process_name() == "test-proc"
    assert log.get_locale() == "pl"  # default

    log.set_locale("en")
    assert log.get_locale() == "en"

    log.add_log_param("order_id", 18)
    assert log._log_params["details"]["order_id"] == 18


def test_log_does_not_raise():
    log = ProcessLogger(process_name="test-proc")
    log.set_code(200)
    log.info("Order created")  # LoggerAdapter.info -> log(); must not raise
    assert log.get_process_name() == "test-proc"

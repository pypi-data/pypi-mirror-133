=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.


0.5.1 - 2022-01-09
==================

Fixed
-----

* The value for `Winter Mode Step 2` of the `kostal_plenticore_battery_status` metric is now correctly documented as decimal 16, not 10.

0.5.0 - 2022-01-08
==================

Added
-----

* Added metrics `kostal_plenticore_inverter_status` and `kostal_plenticore_battery_status` to allow monitoring inverter and battery usage status.

0.4.0 - 2021-04-05
==================

Added
-----

* Add metrics `kostal_plenticore_update_status` and `kostal_plenticore_update_status_timestamp` exposing whether updates are available.


0.3.0 - 2021-02-24
==================

Added
-----

* Add metrics `kostal_plenticore_string_voltage_volts` and `kostal_plenticore_string_current_amperes` for PV string voltage and current.


0.2.0 - 2020-12-21
==================

Added
-----

* Add metric `kostal_plenticore_battery_configured_minimum_charge_percent` exporting the configured minimum state-of-charge target.
* The exporter can also be invoked as a Python module: ``python3 -m kostal_plenticore_exporter --help``.

Fixed
-----

* Compatibility with Prometheus Client 0.7.

0.1.1 - 2020-12-21
==================

Fixed
-----

* Include changelog and license in source distribution.
* Loosen overly tight version dependencies to Click, Prometheus Client, and Pytest.


0.1.0 - 2020-12-20
==================

Added
-----

* Expose basic metrics of the Kostal Plenticore inverter.

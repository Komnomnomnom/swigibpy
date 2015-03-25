# Change Log

## [Unreleased](https://github.com/Komnomnomnom/swigibpy/tree/HEAD)
### New Features
  * Update to TWS v9.71 API
  * Auto-reconnect support (disabled by default, enable using `reconnect_auto`
    argument in `EPosixClientSocket` constructor).
  * Raise `NotImplementedError` when `EWrapper` method missing.
  * Improved error handling, introduction of `EWrapper.pyError` method.
  * `EWrapperVerbose` and `EWrapperQuiet` utility classes
  * Improved polling behaviour
  * Improved documentation.

### Deprecated
  * `eConnect` argument `poll_auto`, use `poll_auto` argument in
    `EPosixClientSocket` constructor instead.

### Bug Fixes
  * Some small Python 3 fixes

### Thanks
  * [@sandrinr](https://github.com/sandrinr)

[Full Changelog](https://github.com/Komnomnomnom/swigibpy/compare/0.4.1...HEAD)

**Merged pull requests:**

- Handle OSError during select [\#33](https://github.com/Komnomnomnom/swigibpy/pull/33) ([sandrinr](https://github.com/sandrinr))

- Fix eConnect wrapping [\#32](https://github.com/Komnomnomnom/swigibpy/pull/32) ([sandrinr](https://github.com/sandrinr))

- Fix dict iteration in Python 3 [\#29](https://github.com/Komnomnomnom/swigibpy/pull/29) ([sandrinr](https://github.com/sandrinr))

## [0.4.1](https://github.com/Komnomnomnom/swigibpy/tree/0.4.1) (2013-05-04)
  * Fix for exception bubbling up and killing poller #19
  * Remove swigibpy custom exceptions

## [0.4](https://github.com/Komnomnomnom/swigibpy/tree/0.4) (2013-03-24)
  * Support for TWS Contract and Order ComboLegs and AlgoParams (#7)
  * Update to TWS v9.68 API.
  * Support for GCC 4.7+
  * Remove TWS's (false) dependency on MFC (#17 thanks Koneski)
  * Better support for custom error handling (#15, #18)

## [0.3](https://github.com/Komnomnomnom/swigibpy/tree/0.3) (2012-08-08)
  * Allow customisation of poll interval #5
  * Support for comboleg vector #3
  * Python 3 supprt #4

## [0.2.3](https://github.com/Komnomnomnom/swigibpy/tree/0.2.3) (2012-04-03)
  * Update to TWS API v9.66

## [0.2.2](https://github.com/Komnomnomnom/swigibpy/tree/0.2.2) (2011-10-10)

  * Added Windows support.

## [0.2.1](https://github.com/Komnomnomnom/swigibpy/tree/0.2.1) (2011-09-19)

  * Added missing TWS types (Order, OrderState etc)

## [0.2](https://github.com/Komnomnomnom/swigibpy/tree/0.2) (2011-08-31)

  * Support for TWS API 9.65.
  * Built in TWS message polling
  * Rewrote interface file to use shadowing rather than renaming and subclassing

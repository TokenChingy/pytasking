# Changes

## 1.2

- Changing naming convention, moving toward 1.x convention.

### Breaking Changes

- All wrapped exceptions and data structures from the `asyncio` and `multiprocessing` modules have now been namespaced into pytasking. For example; `pytasking.CancelledError` is now `pytasking.asyncio.CancelledError`. This change is so that it is more explicit and natural.

## 1.1.0

- Improved documentation.
- Implemented additional helper methods for the Manager class – see the documentation for details.

## 1.0.0

- This is the initial release of pytasking.
# mypy doesn't think this function exists in the module:
from asyncio.base_events import _format_handle  # type: ignore[attr-defined]
from typing import Callable, Optional
import asyncio.events
import time


def enable(slow_duration: float, on_slow_callback: Optional[Callable[[str, float], None]] = None) -> None:
	'''
	Patch ``asyncio.events.Handle`` to log warnings every time a callback takes ``slow_duration`` seconds
	or more to run.

	:param on_slow_callback: If provided, it will receive a formatted name of a slow callback
		and the time (in seconds) it took to execute. If not provided, ``logwood`` or ``logging`` is used
		to log the slow callback.
	'''
	if on_slow_callback is None:
		from aiodebug.logging_compat import get_logger

		logger = get_logger(__name__)
		on_slow_callback = lambda name, duration: logger.warning('Executing %s took %.3f seconds', name, duration)

	_run = asyncio.events.Handle._run  # pylint: disable=protected-access

	def instrumented(self):
		t0 = time.monotonic()
		return_value = _run(self)
		dt = time.monotonic() - t0
		if dt >= slow_duration:
			on_slow_callback(_format_handle(self), dt)
		return return_value

	asyncio.events.Handle._run = instrumented  # type: ignore[assignment] # pylint: disable=protected-access

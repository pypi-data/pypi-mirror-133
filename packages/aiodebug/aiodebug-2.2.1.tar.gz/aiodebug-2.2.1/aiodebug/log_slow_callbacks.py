# mypy doesn't think this function exists in the module:
from asyncio.base_events import _format_handle  # type: ignore[attr-defined]
import asyncio.events
import time


def enable(slow_duration: float) -> None:
	'''
	Patch ``asyncio.events.Handle`` to log warnings every time a callback takes ``slow_duration`` seconds
	or more to run.
	'''
	from aiodebug.logging_compat import get_logger

	logger = get_logger(__name__)
	_run = asyncio.events.Handle._run  # pylint: disable=protected-access

	def instrumented(self):
		t0 = time.monotonic()
		return_value = _run(self)
		dt = time.monotonic() - t0
		if dt >= slow_duration:
			logger.warning('Executing %s took %.3f seconds', _format_handle(self), dt)
		return return_value

	asyncio.events.Handle._run = instrumented  # type: ignore[assignment] # pylint: disable=protected-access

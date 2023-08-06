from typing import List, Tuple
import asyncio
import contextlib
import datetime
import os
import sys
import threading
import time
import traceback


class TraceDumper(threading.Thread):
	def __init__(self, dir_name: str, interval: float, last_loop_iteration_time_wrapped: List[float]) -> None:
		self._interval = interval
		self._dir_name = os.path.abspath(dir_name)
		self._last_loop_iteration_time_wrapped = last_loop_iteration_time_wrapped
		self.stop = False

		# Eliminate IO errors later (on hang)
		assert os.path.isdir(self._dir_name)
		assert os.access(self._dir_name, os.W_OK)

		super().__init__()

	def run(self) -> None:
		''' Thread loop '''
		while not self.stop:
			if time.monotonic() - self._last_loop_iteration_time_wrapped[0] > self._interval:
				for i in range(3):
					dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S.%f')
					self._save_stack_trace(f'stacktrace-{dt}-{i}.txt')
					time.sleep(1)

			time.sleep(self._interval)

	@staticmethod
	def _get_stack_trace() -> str:
		code: List[str] = []
		for thread_id, stack in sys._current_frames().items():  # pylint: disable=protected-access
			code.append(f'\n# ThreadID: {thread_id}')
			for filename, line_no, name, line in traceback.extract_stack(stack):
				code.append(f'File: "{filename}", line {line_no}, in {name}')
				if line:
					code.append(f'  {line.strip()}')

		return '\n'.join(code)

	def _save_stack_trace(self, filename) -> None:
		with open(os.path.join(self._dir_name, filename), 'w') as file:
			file.write(self._get_stack_trace())


def start(
	stack_output_dir: str,
	interval: float = 0.25,
	loop: asyncio.AbstractEventLoop = None,
) -> Tuple[TraceDumper, asyncio.Task]:
	'''
	Start detecting hangs in asyncio loop. If a hang for more than `interval` is detected, a stack trace
	is saved into `stack_output_dir`.
	'''
	if loop is None:
		loop = asyncio.get_event_loop()

	# This value is wrapped into a list, so python doesn't pass the number by value but by reference.
	last_loop_iteration_time_wrapped = [time.monotonic()]

	tracer = TraceDumper(stack_output_dir, interval, last_loop_iteration_time_wrapped)
	tracer.setDaemon(True)

	async def monitor():
		while loop.is_running():
			last_loop_iteration_time_wrapped[0] = time.monotonic()
			await asyncio.sleep(interval / 2.0)

	monitor_task = loop.create_task(monitor())
	tracer.start()

	return tracer, monitor_task


async def stop_wait(tracedumper_task_tuple: Tuple[TraceDumper, asyncio.Task]) -> None:
	''' Stop detecting hangs '''
	instance, monitor_task = tracedumper_task_tuple
	instance.stop = True
	monitor_task.cancel()
	with contextlib.suppress(asyncio.CancelledError):
		await monitor_task

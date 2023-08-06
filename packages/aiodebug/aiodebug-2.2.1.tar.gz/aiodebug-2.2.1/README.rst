aiodebug
========

This is a tiny library for monitoring and testing asyncio programs.
Its monitoring features are meant to be always on in production.


Installation
--------------
``aiodebug`` is only compatible with Python 3.8 and higher. There are no plans to support older versions.

``aiodebug`` is `available on PyPI <https://pypi.org/project/aiodebug/>`_ and you can install it with:

::

	pip install aiodebug

or

::

	poetry add aiodebug


``aiodebug`` will use `logwood <https://github.com/qntln/logwood>`_ if it is installed, otherwise it will default
to the standard logging module.


Log warnings when callbacks block the event loop
------------------------------------------------

.. code-block:: python

	import aiodebug.log_slow_callbacks

	aiodebug.log_slow_callbacks.enable(0.05)

This will produce WARNING-level logs such as

.. code-block::

	Executing <Task pending coro=<foo() running at /home/.../foo.py:37>
	wait_for=<Future pending cb=[Task._wakeup()]>> took 0.069 seconds

asyncio already does this in debug mode, but you probably don't want to enable full-on debug mode in production.



Track event loop lags in StatsD
------------------------------------------------

.. code-block:: python

	import aiodebug.monitor_loop_lag

	aiodebug.monitor_loop_lag.enable(statsd_client)

Tracks how much scheduled calls get delayed and sends the lags to StatsD.

.. image:: loop-lags.png


Dump stack traces of all threads if the event loop hangs for too long
-----------------------------------------------------------------------

.. code-block:: python

	import aiodebug.hang_inspection

	dumper = aiodebug.hang_inspection.start('/path/to/output/directory', interval = 0.25)  # 0.25 is the default
	...
	await aiodebug.hang_inspection.stop_wait(dumper)

Enabling this function may help you in case one of your threads (sometimes) runs a CPU-bound operation that
completely stalls the event loop, but you don't know which thread it is or what it is doing.

Every time the event loop hangs (doesn't run a scheduled 'monitoring' task) for longer than the given
``interval``, aiodebug will create 3 stack traces, 1 second apart, in your output directory.
For example:

.. code-block::

	-rw-r--r--  1 user  group   6.7K  4 Jan 09:41 stacktrace-20220104-094154.197418-0.txt
	-rw-r--r--  1 user  group   7.0K  4 Jan 09:41 stacktrace-20220104-094155.206574-1.txt
	-rw-r--r--  1 user  group   6.6K  4 Jan 09:41 stacktrace-20220104-094156.211781-2.txt

Each file then contains the Python stack traces of all threads that were running or waiting at the time.
You might be able to find your culprit blocking the event loop at the end of one of the traces.


Speed up or slow down time in the event loop
------------------------------------------------

This is mainly useful for testing.

.. code-block:: python

	import aiodebug.testing.time_dilated_loop

	loop = aiodebug.testing.time_dilated_loop.TimeDilatedLoop()
	asyncio.set_event_loop(loop)

	loop.time_dilation = 3
	await asyncio.sleep(1)  # Takes 0.333s of real time

	loop.time_dilation = 0.1
	await asyncio.sleep(1)  # Takes 10s of real time


****

	.. image:: quantlane.png

	``aiodebug`` was made by `Quantlane <https://quantlane.com>`_, a systematic trading firm.
	We design, build and run our own stock trading platform.

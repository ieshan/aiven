# Mocking ThreadPoolExecutor: https://stackoverflow.com/a/60109361
class MockThreadPoolExecutor():
	def __init__(self, **kwargs):
		pass

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		pass

	def submit(self, fn, *args, **kwargs):
		# execute functions in series without creating threads
		# for easier unit testing
		result = fn(*args, **kwargs)
		return result

	def shutdown(self, wait=True):
		pass

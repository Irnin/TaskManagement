class Logging:

	@staticmethod
	def log(message):
		print(message)

	@staticmethod
	def log_error(message):
		print(f"\033[91mERROR:\033[0m {message}")

	@staticmethod
	def log_warning(message):
		print(f"\033[93mWARNING:\033[0m {message}")

	@staticmethod
	def log_info(message):
		print(f"\033[94mINFO:\033[0m {message}")

	@staticmethod
	def log_success(message):
		print(f"\033[92mSUCCESS:\033[0m {message}")
import logging
import os
from datetime import datetime


_DEF_LOG_PATH = os.path.join(os.getcwd(), "bot.log")


def get_logger(name: str) -> logging.Logger:
	logger = logging.getLogger(name)
	if logger.handlers:
		return logger

	level_str = os.getenv("LOG_LEVEL", "INFO").upper()
	level = getattr(logging, level_str, logging.INFO)
	logger.setLevel(level)

	fmt = logging.Formatter(
		"%(asctime)s | %(levelname)s | %(name)s | %(message)s",
		datefmt="%Y-%m-%d %H:%M:%S",
	)

	file_handler = logging.FileHandler(_DEF_LOG_PATH, encoding="utf-8")
	file_handler.setFormatter(fmt)
	logger.addHandler(file_handler)

	console = logging.StreamHandler()
	console.setFormatter(fmt)
	logger.addHandler(console)

	logger.debug(f"Logger initialized at {_DEF_LOG_PATH} on {datetime.utcnow().isoformat()}Z")
	return logger

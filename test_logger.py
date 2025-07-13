# test_logger.py

from utils.logger import logger

def test_logging():
    logger.info("Logging test successful.")
    logger.warning("This is a warning.")
    logger.error("This is an error.")

if __name__ == "__main__":
    test_logging()
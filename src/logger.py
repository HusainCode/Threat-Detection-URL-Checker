# Logger is responsible
#
#  Purpose:
#
#  Key Attributes:
#
#
#  Main Methods:
#
# Example:
# [2024-03-02 14:30:10] ERROR: Failed to fetch URL https://example.com Timeout error.
# [2024-03-02 14:32:45] INFO: Successfully categorized URL https://safe-site.com as SAFE.
# [2024-03-02 14:35:20] WARNING: Suspicious activity detected on https://malware-site.com

import logging

class Logger:
    def __init__(self, log_file="log.txt"):
        logging.basicConfig(
            filename=log_file,
            level=10, # logs everything (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            format="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger() # get the root logger

    def info(self, message: str):
        """Logs an INFO message"""
        self.logger.info(message)

    def warning(self, message: str):
        """Logs a WARNING message"""
        self.logger.warning(message)

    def error(self, message: str):
        """Logs an ERROR message"""
        self.logger.error(message)

        # I STOPPED HERE

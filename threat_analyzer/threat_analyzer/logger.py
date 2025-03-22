#  Purpose:
#     Provides a centralized logging utility to log messages of various severity levels
#     (INFO, WARNING, ERROR) to a file for monitoring and debugging.
#
#  Key Attributes:
#     logger: The root logger object configured to write to a specified file
#
#  Main Methods:
#     info(message): Logs informational messages
#     warning(message): Logs warning messages
#     error(message): Logs error messages
#
#  Example:
#     [2024-03-02 14:30:10] ERROR: Failed to fetch URL https://example.com Timeout error.
#     [2024-03-02 14:32:45] INFO: Successfully categorized URL https://safe-site.com as SAFE.
#     [2024-03-02 14:35:20] WARNING: Suspicious activity detected on https://malware-site.com

import logging
import os

class Logger:
    def __init__(self, log_file=None):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        log_path = log_file or os.path.join(base_dir, os.getenv("LOG_FILE", "resources/log.txt"))

        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        self.logger = logging.getLogger("ThreatLogger")
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_path)
            formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s",
                                          "%Y-%m-%d %H:%M:%S")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)


    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

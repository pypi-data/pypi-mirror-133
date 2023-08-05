import os
import datetime

try:
    import constants
except Exception:
    from startcp import constants


class Logger:

    def info(self, log_msg):
        os.makedirs(constants.startcp_default_folder, exist_ok=True)
        with open(str(constants.startcp_log_file), "a+") as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + log_msg + "\n")

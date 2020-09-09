import datetime
import logging
import os


class Logger:

    def __init__(self):
        pass

    @staticmethod
    def get_logger(export_name):
        export_name_parts = export_name.rpartition('\\')
        export_path = export_name_parts[0] + export_name_parts[1]

        logs_directory = export_path + "logs"
        if not os.path.isdir(logs_directory):
            os.mkdir(logs_directory)
        log_time = str(datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S"))
        log_file_name = logs_directory + "\\logFile-{project_name}-{logtime}.txt".format(
            project_name=export_name_parts[2],
            logtime=log_time
        )
        log_format = '%(asctime)s in %(module)s %(levelname)s: %(message)s'

        logger = logging.getLogger()

        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file_name)
        formatter = logging.Formatter(log_format, '%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

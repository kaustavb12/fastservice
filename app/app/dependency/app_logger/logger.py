from starlette_context import context
import logging
import logging.config
import json

# Add request id from context to log string if available
class Request_ID_Adapter(logging.LoggerAdapter):
    def __init__(self, logger, extra={}):
        if not isinstance(extra, dict):
            extra = {}
        super(Request_ID_Adapter, self).__init__(logger, extra)

    def process(self, msg, kwargs):
        request_id = "Context Unavailable"
        if context.exists():
            request_id = context.get("X-Request-ID")

        return '%s - %s' % (request_id, msg), kwargs

# Loads log config from json file and sets log level
def load_json_config(log_level: str, log_type: str):
    if log_type == "FILE":
        config_path = "./app/dependency/app_logger/log_config_file.json"
        handler = "rotate_file"
    else:
        config_path = "./app/dependency/app_logger/log_config_stdout.json"
        handler = "stdout"

    with open(config_path) as f:
        config_json = json.load(f)
        config_json["handlers"][handler]["level"] = log_level

    return config_json


def configure_logging(log_level: str, log_type: str):
    logging.logThreads = 0
    logging.logProcesses = 0

    config_json = load_json_config(log_level, log_type)

    logging.config.dictConfig(config_json)


api_service_logger = logging.getLogger("api_service")
log = Request_ID_Adapter(api_service_logger)

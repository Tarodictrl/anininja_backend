import logging.config

CONSOLE_FORMAT: str = "%(levelprefix)s %(message)s"
CONSOLE_LOG_LEVEL: str = "INFO"
FILE_FORMAT: str = "%(asctime)s %(levelname)s %(message)s"
FILE_LOG_LEVEL: str = "INFO"
FILE_PATH: str = "warning.log"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": CONSOLE_FORMAT,
        },
        "file": {
            "format": FILE_FORMAT,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": CONSOLE_LOG_LEVEL,
            "formatter": "console",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": FILE_LOG_LEVEL,
            "formatter": "file",
            "filename": FILE_PATH,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": CONSOLE_LOG_LEVEL,
            "logging.propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING)
logging.getLogger("httpx").setLevel("CRITICAL")

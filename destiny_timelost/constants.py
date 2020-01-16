GOOGLE_SHEET_URL = (
    "https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{table_name}"
)

LOGGING_DICT = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"standard": {"format": "%(message)s"}},
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "standard",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "standard",
        },
    },
    "loggers": {},
    "root": {"handlers": ["file"], "level": "INFO"},
}

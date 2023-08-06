from logging import DEBUG
from logging.config import dictConfig

DEFAULT_LOG_CONFIG = dict(
    version=1,
    formatters={
        'f': {
            'format': '[%(asctime)s.%(msecs)03d] [%(name)-30s] %(levelname)-8s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    handlers={
        'h': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': DEBUG
        }
    },
    root={
        'handlers': ['h'],
        'level': DEBUG
    }
)


def configure_logging(config: dict = None):
    dictConfig(config if config is not None else DEFAULT_LOG_CONFIG)

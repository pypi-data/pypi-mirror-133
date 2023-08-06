import os


def has_env(env_str: str) -> bool:
    return env_str in os.environ


def has_env_flag(env_str: str) -> bool:
    return has_env(env_str) and os.environ.get(env_str) == "1"

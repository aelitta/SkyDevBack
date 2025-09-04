# src/utils/logger.py (если у тебя уже есть — ок, просто перезагрузим модуль)
from loguru import logger as _base
import sys

# регистрируем кастом-уровни один раз
for name, no, color in [
    ("REASONING", 25, "<magenta>"),
    ("DATA",      27, "<green>"),
    ("CHAT",      28, "<blue>"),
    ("CONTEXT",   29, "<cyan>"),
]:
    try:
        _base.level(name)
    except Exception:
        pass
    _base.level(name, no=no, color=color)

# сбрасываем и добавляем два sink'а
_base.remove()
_base.add(
    sys.stderr,
    level="DEBUG",
    colorize=True,
    backtrace=True,
    diagnose=False,
    format="<level>{time:HH:mm:ss.SSS} | {level:<9} | {message}</level>",
)
_base.add(
    "file.log",
    level="DEBUG",
    rotation="50 MB",
    encoding="utf-8",
    backtrace=True,
    diagnose=False,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<9} | {message}",
)

logger = _base

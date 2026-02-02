from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime, timezone, timedelta
from typing import Optional

import requests


CONF_NAME = "neco_conf.json"
_GLOBAL_CONFIG: Optional["NecoConfig"] = None


def _conf_path(path: str | Path | None = None) -> Path:
    # именно cwd, а не папка библиотеки
    return Path(path) if path is not None else (Path.cwd() / CONF_NAME)


@dataclass(frozen=True)
class NecoConfig:
    token: str
    chat_id: str
    timeout: float = 5.0

    def save(self, path: str | Path | None = None) -> Path:
        p = _conf_path(path)
        data = {"token": self.token, "chat_id": self.chat_id, "timeout": self.timeout}
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return p

    @classmethod
    def load(cls, path: str | Path | None = None) -> "NecoConfig":
        p = _conf_path(path)
        if not p.exists():
            raise FileNotFoundError(f"Config not found: {p}")
        data = json.loads(p.read_text(encoding="utf-8"))
        return cls(
            token=str(data["token"]),
            chat_id=str(data["chat_id"]),
            timeout=float(data.get("timeout", 5.0)),
        )


def configure(
    token: str,
    chat_id: str,
    *,
    timeout: float = 5.0,
    save_credentials: bool = False,
    path: str | Path | None = None,
) -> NecoConfig:
    """
    Создаёт конфиг в памяти; опционально сохраняет в neco_conf.json (в cwd).
    """
    global _GLOBAL_CONFIG
    cfg = NecoConfig(token=token, chat_id=chat_id, timeout=timeout)
    _GLOBAL_CONFIG = cfg
    if save_credentials:
        cfg.save(path)
    return cfg


def _get_config(path: str | Path | None = None) -> NecoConfig:
    global _GLOBAL_CONFIG
    if _GLOBAL_CONFIG is not None:
        return _GLOBAL_CONFIG
    # автоподхват из cwd/neco_conf.json
    _GLOBAL_CONFIG = NecoConfig.load(path)
    return _GLOBAL_CONFIG


def send(
    text: str,
    *,
    token: str | None = None,
    chat_id: str | None = None,
    timeout: float | None = None,
    config_path: str | Path | None = None,
    save_credentials: bool = False,
    nya_suffix: str = "\nnya",
    silent: bool = True,
) -> None:
    """
    Отправляет сообщение в Telegram.
    - Если token/chat_id не заданы: берёт их из конфига (в памяти или из cwd/neco_conf.json).
    - Если ничего не найдено: бросает ошибку.
    """
    if token is None or chat_id is None:
        cfg = _get_config(config_path)
        token = token or cfg.token
        chat_id = chat_id or cfg.chat_id
        timeout = cfg.timeout if timeout is None else timeout
    else:
        # если явно передали креды, можно (опционально) сохранить их в конфиг
        if save_credentials:
            configure(token, chat_id, timeout=timeout or 5.0, save_credentials=True, path=config_path)
        timeout = 5.0 if timeout is None else timeout

    payload_text = f"{text}{nya_suffix}" if nya_suffix else text

    try:
        # Bot API метод sendMessage: обязательны chat_id и text
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": chat_id, "text": payload_text},
            timeout=timeout,
        )
    except Exception:
        if not silent:
            raise


def _ts(tz_offset_hours: int = 0) -> str:
    tz = timezone(timedelta(hours=tz_offset_hours))
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")


def log(text: str = "done nya", *, tz_offset_hours: int = 0) -> None:
    print(_ts(tz_offset_hours))
    print(text)


def log_tg(
    text: str = "done nya",
    *,
    tz_offset_hours: int = 0,
    config_path: str | Path | None = None,
    silent: bool = True,
) -> None:
    ts = _ts(tz_offset_hours)
    print(ts)
    print(text)
    send(f"{ts}\n{text}", config_path=config_path, silent=silent, nya_suffix="")

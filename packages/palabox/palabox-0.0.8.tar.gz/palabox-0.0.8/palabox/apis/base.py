"""Base Api."""

import logging
from abc import ABC
from functools import wraps
from typing import Any, Dict, List, Literal, Optional, Union

import requests


# pylint: disable=too-few-public-methods
class BaseApiConfig:
    """BaseApiConfig."""


class BaseApi(ABC):
    """Base API."""

    __name__ = "BaseApi"
    config: BaseApiConfig
    session: requests.Session
    api_need_connection: bool = False

    def __init__(self, config: BaseApiConfig) -> None:
        """Init."""
        self.config = config
        self.logger = logging.getLogger(self.__name__)

    @staticmethod
    def __log_entry__(func):
        """Log entry."""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            """Wrapper."""
            self.logger.debug(f"{func.__name__}()")
            return func(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def get_user_agent() -> str:
        """Get user agent."""
        # pylint: disable=line-too-long
        return (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 "
            "Safari/537.36"
        )

    def generate_session(self) -> None:
        """Generate session."""
        self.session = requests.Session()

    def delete_session(self) -> None:
        """Delete session."""
        self.session = requests.Session()

    # pylint: disable=too-many-arguments
    def request(
        self,
        url: str,
        method: Literal["get", "post"] = "get",
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json: Optional[Union[Dict, List]] = None,
        headers: Optional[Dict] = None,
    ) -> requests.Response:
        """Request."""
        if not hasattr(self, "session"):
            self.generate_session()
        if headers is None:
            headers = {}
        request = self.session.request(
            method=method,
            params=params,
            url=url,
            data=data,
            json=json,
            headers={"User-Agent": self.get_user_agent(), **headers},
        )

        if request.ok:
            return request
        self.logger.warning(request.content.decode()[:1000])
        raise ValueError(f"Request failed, status code: {request.status_code}")

    def is_connected(self) -> bool:
        """Check if connected."""
        raise NotImplementedError("__is_connected() is not implemented")

    def can_connect(self) -> bool:
        """Check if able to connect."""
        raise NotImplementedError("__can_connect() is not implemented")

    def connect(self) -> bool:
        """Connection function."""
        raise NotImplementedError("connect() is not implemented")

    @staticmethod
    def need_connection(f) -> Any:
        """Wrapper to ensure connection."""

        @wraps(f)
        def wrapper(self, *args, **kwargs) -> Any:
            """Wrapper."""
            if not self.is_connected():
                self.connect()
            return f(self, *args, **kwargs)

        return wrapper

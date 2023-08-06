"""Wakatime API."""

from dataclasses import dataclass
from datetime import datetime

import dacite
import requests

from .base import BaseApi, BaseApiConfig
from .types.wakatime import WakatimeDay, WakatimeStats


@dataclass
class WakatimeApiConfig(BaseApiConfig):
    """WakatimeApiConfig."""

    token: str

    url: str = "https://wakatime.com/share/"


class WakatimeApi(BaseApi):
    """Wakatime API."""

    __name__ = "WakatimeApi"
    config: WakatimeApiConfig
    api_need_connection: bool = False

    def __init__(self, config: WakatimeApiConfig) -> None:
        """Init."""
        super().__init__(config)

    @BaseApi.__log_entry__
    def __get_user_stats(self) -> requests.Response:
        """Get user stats."""
        return self.request(
            url=f"{self.config.url}/{self.config.token}.json",
            method="get",
        )

    @BaseApi.__log_entry__
    def get_today(self) -> WakatimeDay:
        """Get user stats for today."""
        response = self.__get_user_stats()
        if response.ok:
            data: WakatimeStats = dacite.from_dict(
                WakatimeStats,
                response.json(),
                dacite.Config(
                    {datetime: lambda dateStr: datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%S%z")}
                ),
            )

            return data.data[-1]

        raise ValueError(f"Problem with the request {response}, '{response.content.decode()}'")

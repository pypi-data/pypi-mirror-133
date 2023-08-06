"""Codingame API."""

from dataclasses import dataclass

import dacite
import requests

from .base import BaseApi, BaseApiConfig
from .types.codingame import CodingameStats


@dataclass
class CodingameApiConfig(BaseApiConfig):
    """CodingameApiConfig."""

    user_id: str

    points_url: str = (
        "https://www.codingame.com/services/CodinGamer/findCodingamePointsStatsByHandle"
    )


class CodingameApi(BaseApi):
    """Codingame API."""

    __name__ = "CodingameApi"
    config: CodingameApiConfig
    api_need_connection: bool = False

    def __init__(self, config: CodingameApiConfig) -> None:
        """Init."""
        super().__init__(config)

    @BaseApi.__log_entry__
    def __get_user_stats(self) -> requests.Response:
        """Get user stats."""
        return self.request(url=self.config.points_url, method="post", json=[self.config.user_id])

    @BaseApi.__log_entry__
    def get_today(self) -> CodingameStats:
        """Get user stats for today."""
        response = self.__get_user_stats()
        if response.ok:
            data: CodingameStats = dacite.from_dict(CodingameStats, response.json())

            return data

        raise ValueError(f"Problem with the request {response}, '{response.content.decode()}'")

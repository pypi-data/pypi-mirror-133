"""Leetcode API."""

from dataclasses import dataclass

import dacite
import requests

from .base import BaseApi, BaseApiConfig
from .types.leetcode import LeetCodeData


@dataclass
class LeetcodeApiConfig(BaseApiConfig):
    """LeetcodeApiConfig."""

    username: str

    url: str = "https://leetcode.com/graphql"


class LeetcodeApi(BaseApi):
    """Leetcode API."""

    __name__ = "LeetcodeApi"
    config: LeetcodeApiConfig
    api_need_connection: bool = False

    def __init__(self, config: LeetcodeApiConfig) -> None:
        """Init."""
        super().__init__(config)

    @BaseApi.__log_entry__
    def __get_user_stats(self) -> requests.Response:
        """Get user stats."""
        return self.request(
            url=self.config.url,
            method="get",
            json={
                "operationName": "getUserProfile",
                "variables": {"username": self.config.username},
                "query": "query getUserProfile($username: String!) {\n  allQuestionsCount {\n    difficulty\n    count\n    __typename\n  }\n  matchedUser(username: $username) {\n    username\n    socialAccounts\n    githubUrl\n    contributions {\n      points\n      questionCount\n      testcaseCount\n      __typename\n    }\n    profile {\n      realName\n      websites\n      countryName\n      skillTags\n      company\n      school\n      starRating\n      aboutMe\n      userAvatar\n      reputation\n      ranking\n      __typename\n    }\n    submissionCalendar\n    submitStats: submitStatsGlobal {\n      acSubmissionNum {\n        difficulty\n        count\n        submissions\n        __typename\n      }\n      totalSubmissionNum {\n        difficulty\n        count\n        submissions\n        __typename\n      }\n      __typename\n    }\n    badges {\n      id\n      displayName\n      icon\n      creationDate\n      __typename\n    }\n    upcomingBadges {\n      name\n      icon\n      __typename\n    }\n    activeBadge {\n      id\n      __typename\n    }\n    __typename\n  }\n}\n",  # pylint: disable=line-too-long
            },
        )

    @BaseApi.__log_entry__
    def get_today(self) -> LeetCodeData:
        """Get user stats for today."""
        response = self.__get_user_stats()
        if response.ok:
            data: LeetCodeData = dacite.from_dict(
                LeetCodeData,
                response.json()["data"],
            )

            return data

        raise ValueError(f"Problem with the request {response}, '{response.content.decode()}'")

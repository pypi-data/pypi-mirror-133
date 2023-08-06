"""Duolingo API."""

from dataclasses import dataclass
from datetime import datetime

import dacite
import requests

from .base import BaseApi, BaseApiConfig
from .types.duolingo import DuolingoStats


@dataclass
class DuolingoApiConfig(BaseApiConfig):
    """DuolingoApiConfig."""

    login: str = ""
    password: str = ""

    login_url: str = "https://www.duolingo.com/login"
    user_id: str = ""
    jwt_token: str = ""
    # pylint: disable=line-too-long
    user_request_fields = "acquisitionSurveyReason,adsConfig,betaStatus,bio,blockedUserIds,canUseModerationTools,courses,creationDate,currentCourse,email,emailAnnouncement,emailAssignment,emailAssignmentComplete,emailClassroomJoin,emailClassroomLeave,emailComment,emailEditSuggested,emailEventsDigest,emailFollow,emailPass,emailPromotion,emailWeeklyProgressReport,emailSchoolsAnnouncement,emailStreamPost,emailVerified,emailWeeklyReport,enableMicrophone,enableSoundEffects,enableSpeaker,experiments{connect_web_remove_dictionary,courses_fr_ja_v1,courses_it_de_v1,hoots_web,hoots_web_100_crowns,hoots_web_rename,learning_det_scores_v1,learning_duolingo_score_v1,learning_fix_whitespace_grading,media_shorten_cant_speak_web,midas_new_years_2022_purchase_flow,midas_web_cta_purchase_start_my_14_day,midas_web_family_plan,midas_web_immersive_plus_v2,midas_web_longscroll,midas_web_new_years_discount_2022,midas_web_payment_requests_v2,midas_web_plus_applicable_taxes,midas_web_plus_dashboard_mobile_users,midas_web_plus_dashboard_stripe_users,nurr_web_coach_duo_in_placement_v2,nurr_web_simplify_first_skill_popouts,nurr_web_uo_home_message_v0,sigma_web_cancel_flow_crossgrade,sigma_web_direct_purchase_hide_monthly,sigma_web_family_plan_shop_promo,sigma_web_gold_empty_progress,sigma_web_legendary_partial_xp,sigma_web_legendary_price_30_lingots,sigma_web_mistakes_inbox,sigma_web_show_xp_in_skill_popover,sigma_web_split_purchase_page,spam_non_blocking_email_verification,speak_rewrite_speak_challenge,speak_web_port_speak_waveform,stories_web_column_match_challenge,stories_web_crown_pacing_new_labels,stories_web_freeform_writing_examples,stories_web_intro_callout_tier_1,stories_web_listen_mode_redesign,stories_web_newly_published_labels,unify_checkpoint_logic_web,web_alphabets_tab,web_delight_character_scaling_v2,web_delight_fullscreen_loading_v3},facebookId,fromLanguage,globalAmbassadorStatus,googleId,hasPlus,id,inviteURL,joinedClassroomIds,lastStreak{isAvailableForRepair,length},learningLanguage,lingots,location,monthlyXp,name,observedClassroomIds,persistentNotifications,picture,plusDiscounts,practiceReminderSettings,privacySettings,referralInfo,rewardBundles,roles,streak,streakData{length},timezone,timezoneOffset,totalXp,trackingProperties,unconsumedGiftIds,username,webNotificationIds,weeklyXp,xpGains,xpGoal,zhTw,_achievements"


class DuolingoApi(BaseApi):
    """Duolingo API."""

    __name__ = "DuolingoApi"
    config: DuolingoApiConfig
    api_need_connection: bool = True

    def __init__(self, config: DuolingoApiConfig) -> None:
        """Init."""
        super().__init__(config)

    def is_connected(self) -> bool:
        """Check if connected."""
        return self.config.jwt_token != "" and self.config.user_id != ""

    def can_connect(self) -> bool:
        """Check if able to connect."""
        return self.config.login != "" and self.config.password != ""

    @BaseApi.__log_entry__
    def connect(self) -> None:
        """Connect."""
        if not self.can_connect():
            self.logger.warning("Login or password is empty")
            return None

        try:
            response = self.request(
                url=self.config.login_url,
                method="post",
                json={"login": self.config.login, "password": self.config.password},
            )
        except ValueError:
            return None
        try:
            self.config.user_id = response.json()["user_id"]
            self.config.jwt_token = response.headers["jwt"]
        except KeyError:
            self.logger.debug(response.content)
            self.logger.error("Can't get user_id or jwt_token", exc_info=True)
        return None

    @BaseApi.__log_entry__
    @BaseApi.need_connection
    def __get_friends_response(self) -> requests.Response:
        """Get data from friends."""
        return self.request(
            url="https://www.duolingo.com/2017-06-30/users/"
            + f"{self.config.user_id}/subscriptions?pageSize=500&_={self.config.user_id}",
            method="get",
            headers={"Authorization": f"Bearer {self.config.jwt_token}"},
        )

    @BaseApi.__log_entry__
    @BaseApi.need_connection
    def __get_user_response(self) -> requests.Response:
        """Get data from friends."""
        return self.request(
            url="https://www.duolingo.com/2017-06-30/users/"
            + self.config.user_id
            + f"?fields={self.config.user_request_fields}"
            + f"&_={str(int(datetime.now().timestamp()))}",
            method="get",
            headers={"Authorization": f"Bearer {self.config.jwt_token}"},
        )

    @BaseApi.__log_entry__
    @BaseApi.need_connection
    def get_today(self) -> DuolingoStats:
        """Get user stats for today."""
        friends_response = self.__get_friends_response()
        response = self.__get_user_response()
        if response.ok and friends_response.ok:
            raw_data = response.json()
            raw_data["friends"] = friends_response.json()["subscriptions"]
            data: DuolingoStats = dacite.from_dict(DuolingoStats, raw_data)

            return data

        raise ValueError(f"Problem with the request {response}, '{response.content.decode()}'")

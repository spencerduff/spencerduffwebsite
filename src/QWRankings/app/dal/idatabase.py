from abc import ABC, abstractmethod

from app.dal.database_objects import PlayerRanking, PlayerMatchRanking, PlayerStatsMatch


class IDatabase(ABC):
    @abstractmethod
    def is_match_processed(self, match_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_rating_and_rank(self, name: str, mode: str, match_map: str) -> PlayerRanking:
        raise NotImplementedError

    @abstractmethod
    def update_ratings(self, players: list[PlayerMatchRanking]) -> None:
        raise NotImplementedError

    @abstractmethod
    def upload_stats(self, player_stats: list[PlayerStatsMatch]) -> None:
        raise NotImplementedError

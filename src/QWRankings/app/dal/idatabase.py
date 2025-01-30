from abc import ABC, abstractmethod

from app.dal.database_objects import PlayerRanking, PlayerMatchRanking


class IDatabase(ABC):
    @abstractmethod
    def is_match_processed(self, match_id: str) -> bool:
        pass

    @abstractmethod
    def get_rating_and_rank(self, name: str, mode: str, match_map: str) -> PlayerRanking:
        pass

    @abstractmethod
    def update_ratings(self, players: list[PlayerMatchRanking]) -> None:
        pass

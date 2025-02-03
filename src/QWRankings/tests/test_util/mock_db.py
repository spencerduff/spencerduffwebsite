from app.dal.database import PlayerRanking, RatingAndRank, PlayerMatchRanking
from app.dal.database_objects import PlayerStatsMatch
from app.dal.idatabase import IDatabase


class TestDAL(IDatabase):
    def update_ratings(self, players: list[PlayerMatchRanking]) -> None:
        pass

    def get_rating_and_rank(self, name: str, mode: str, match_map: str) -> PlayerRanking:
        return PlayerRanking(
            map_rating_and_rank=RatingAndRank(
                rank=1,
                rating=1500,
                ratings_deviation=350,
            ),
            overall_rating_and_rank=RatingAndRank(
                rank=1,
                rating=1500,
                ratings_deviation=350,
            ),
        )

    def is_match_processed(self, match_id: str) -> bool:
        return False

    def upload_stats(self, player_stats: list[PlayerStatsMatch]) -> None:
        pass

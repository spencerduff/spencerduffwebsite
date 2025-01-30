from datetime import datetime
import dataclasses


@dataclasses.dataclass
class MatchInfo:
    match_id: str
    date: datetime
    mode: str
    map: str


@dataclasses.dataclass
class RatingAndRank:
    rating: float
    ratings_deviation: float
    rank: int


@dataclasses.dataclass
class PlayerMatchRanking:
    match_info: MatchInfo
    match_user_id: str
    name: str
    login: str
    overall_rating_and_rank: RatingAndRank
    map_rating_and_rank: RatingAndRank
    win: int


@dataclasses.dataclass
class PlayerRanking:
    overall_rating_and_rank: RatingAndRank
    map_rating_and_rank: RatingAndRank

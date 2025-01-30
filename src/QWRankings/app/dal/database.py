
from datetime import datetime
import os

import psycopg2 as psycopg2

from app.dal.database_objects import PlayerRanking, RatingAndRank, PlayerMatchRanking
from app.dal.idatabase import IDatabase

ALL_MAPS: str = "ALL"


def match_exists_query(match_id: str) -> str:
    return f"""
    SELECT * 
    FROM per_game_ratings 
    WHERE match_id='{match_id}';
    """


def recent_rating_query(name: str, mode: str, match_map: str) -> str:
    return f"""
    SELECT rating, ratings_deviation, map
    FROM current_ratings 
    WHERE name='{name}'
    AND mode='{mode}'
    AND (map='{match_map}' OR map='{ALL_MAPS}');
    """


def rank_query(rating: float, match_map: str = ALL_MAPS) -> str:
    return f"""
    SELECT count(*)
    FROM current_ratings 
    WHERE rating > {rating}
    AND map='{match_map}';
    """


def add_game_for_player_query(match_id: str, date: datetime, mode: str, name: str, rating: float, win: int, map: str,
                              ratings_deviation: float) -> str:
    return f"""
    INSERT INTO per_game_ratings (match_id, date, mode, name, rating, win, map, ratings_deviation)
    VALUES ('{match_id}', '{date}', '{mode}', '{name}', {rating}, {win}, '{map}', {ratings_deviation});
    """


def update_rating_for_player_query(name: str, rating: float, ratings_deviation: float, mode: str,
                                   match_map: str) -> str:
    return f"""
    INSERT INTO current_ratings (name, rating, ratings_deviation, mode, map)
    VALUES ('{name}', {rating}, {ratings_deviation}, '{mode}', '{match_map}')
    ON CONFLICT (name, mode, map)
    DO UPDATE SET rating = {rating}, ratings_deviation = {ratings_deviation};
    """


class MatchRanksAndStatsDAO(IDatabase):
    __conn = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MatchRanksAndStatsDAO, cls).__new__(cls)
        return cls.instance

    @classmethod
    def get_conn(cls):
        if cls.__conn is None:
            cls.__conn = psycopg2.connect(
                database="qw_rankings",
                user=os.environ.get("POSTGRES_DATABASE_USER"),
                host='localhost',
                password=os.environ.get("POSTGRES_DATABASE_PASSWORD"),
                port=os.environ.get("POSTGRES_DATABASE_PORT")
            )
        return cls.__conn

    @classmethod
    def is_match_processed(cls, match_id: str) -> bool:
        cur = cls.get_conn().cursor()
        cur.execute(match_exists_query(match_id=match_id))
        rows = cur.fetchall()
        cls.get_conn().commit()

        return len(rows) > 0

    @classmethod
    def get_rating_and_rank(cls, name: str, mode: str, match_map: str) -> PlayerRanking:
        cur = cls.get_conn().cursor()

        cur.execute(recent_rating_query(name=name, mode=mode, match_map=match_map))
        rows = cur.fetchall()

        if len(rows) == 0:
            overall_rating = 1500
            overall_ratings_deviation = 350
            map_rating = 1500
            map_ratings_deviation = 350
        elif len(rows) == 1:
            overall_rating = rows[0][0]
            overall_ratings_deviation = rows[0][1]
            map_rating = 1500
            map_ratings_deviation = 350
        else:
            overall_rating = rows[0][0] if rows[0][2] == ALL_MAPS else rows[1][0]
            overall_ratings_deviation = rows[0][1] if rows[0][2] == ALL_MAPS else rows[1][1]
            map_rating = rows[1][0] if rows[0][2] == ALL_MAPS else rows[0][0]
            map_ratings_deviation = rows[1][1] if rows[0][2] == ALL_MAPS else rows[0][1]

        cur.execute(rank_query(rating=overall_rating))
        rows2 = cur.fetchall()

        if len(rows2) == 0:
            overall_rank = 1
        else:
            overall_rank = rows2[0][0] + 1

        cur.execute(rank_query(rating=map_rating, match_map=match_map))
        rows3 = cur.fetchall()

        if len(rows3) == 0:
            map_rank = 1
        else:
            map_rank = rows3[0][0] + 1

        cls.get_conn().commit()

        return PlayerRanking(overall_rating_and_rank=RatingAndRank(rating=overall_rating,
                                                                   ratings_deviation=overall_ratings_deviation,
                                                                   rank=overall_rank),
                             map_rating_and_rank=RatingAndRank(rating=map_rating,
                                                               ratings_deviation=map_ratings_deviation,
                                                               rank=map_rank))

    @classmethod
    def update_ratings(cls, players: list[PlayerMatchRanking]) -> None:
        cur = cls.get_conn().cursor()
        for p in players:
            cur.execute(add_game_for_player_query(
                match_id=p.match_info.match_id,
                date=p.match_info.date,
                mode=p.match_info.mode,
                name=p.name,
                rating=p.overall_rating_and_rank.rating,
                win=p.win,
                map=p.match_info.map,
                ratings_deviation=p.overall_rating_and_rank.ratings_deviation,
            ))
            cur.execute(update_rating_for_player_query(
                name=p.name,
                mode=p.match_info.mode,
                rating=p.overall_rating_and_rank.rating,
                ratings_deviation=p.overall_rating_and_rank.ratings_deviation,
                match_map=ALL_MAPS
            ))
            cur.execute(update_rating_for_player_query(
                name=p.name,
                mode=p.match_info.mode,
                rating=p.map_rating_and_rank.rating,
                ratings_deviation=p.map_rating_and_rank.ratings_deviation,
                match_map=p.match_info.map
            ))
        cls.get_conn().commit()

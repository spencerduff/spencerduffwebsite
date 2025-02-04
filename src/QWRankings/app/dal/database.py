import logging
from datetime import datetime
import os

import psycopg2 as psycopg2
from psycopg2 import DatabaseError

from app.dal.database_objects import PlayerRanking, RatingAndRank, PlayerMatchRanking, PlayerStatsMatch, WeaponStats, \
    ItemStats
from app.dal.idatabase import IDatabase

ALL_MAPS: str = "ALL"
DELIMITER: str = ":"

logger = logging.getLogger(__name__)


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


def add_weapon_stats_for_player_query(match_user_id_weapon: str, name: str, weapon_stats: WeaponStats) -> str:
    return f"""
    INSERT INTO per_game_per_weapon_stats (match_user_id_weapon, name, acc_attacks, acc_hits, acc_real, acc_virtual, 
    kills_total, kills_team, kills_enemy, kills_self, deaths, pickups_dropped, pickups_taken, pickups_total_taken,
    pickups_spawn_taken, pickups_spawn_total_taken, dmg_enemy, dmg_team)
    VALUES ('{match_user_id_weapon}', '{name}', {weapon_stats.acc_attacks}, {weapon_stats.acc_hits}, 
    {weapon_stats.acc_real}, {weapon_stats.acc_virtual}, {weapon_stats.kills_total}, {weapon_stats.kills_team}, 
    {weapon_stats.kills_enemy}, {weapon_stats.kills_self}, {weapon_stats.deaths}, {weapon_stats.pickups_dropped}, 
    {weapon_stats.pickups_taken}, {weapon_stats.pickups_total_taken}, {weapon_stats.pickups_spawn_taken}, 
    {weapon_stats.pickups_spawn_total_taken}, {weapon_stats.dmg_enemy}, {weapon_stats.dmg_team});
    """


def add_item_stats_for_player_query(match_user_id: str, name: str, item_stats: ItemStats) -> str:
    return f"""
        INSERT INTO per_game_item_stats (match_user_id, name, hp_15_took, hp_25_took, hp_100_took, ga_took, 
        ga_time, ya_took, ya_time, ra_took, ra_time, q_took, q_time, p_took,
        p_time, r_took, r_time)
        VALUES ('{match_user_id}', '{name}', {item_stats.hp_15_took}, {item_stats.hp_25_took}, {item_stats.hp_100_took},
        {item_stats.ga_took}, {item_stats.ga_time}, {item_stats.ya_took}, {item_stats.ya_time}, {item_stats.ra_took}, 
        {item_stats.ra_time}, {item_stats.q_took}, {item_stats.q_time}, {item_stats.p_took}, {item_stats.p_time}, 
        {item_stats.r_took}, {item_stats.r_time});
        """


def add_stats_for_player_query(player_stats_match: PlayerStatsMatch) -> str:
    return f"""
        INSERT INTO per_game_stats (match_user_id, name, win, date, mode, map, 
        ping, frags, deaths, tk, spawn_frags, kills, suicides, dmg_taken,
        dmg_given, dmg_team, dmg_self, dmg_team_weap, dmg_enemy_weap, dmg_taken_to_die, xfer_rl, xfer_lg, 
        spree_max, spree_quad, control, speed_max, speed_avg, axe_stats, sg_stats, ssg_stats, ng_stats, 
        sng_stats, gl_stats, rl_stats, lg_stats)
        VALUES ('{player_stats_match.match_user_id}', '{player_stats_match.name}', {player_stats_match.win},
        '{player_stats_match.match_info.date}',  '{player_stats_match.match_info.mode}', 
        '{player_stats_match.match_info.map}', {player_stats_match.player_stats.ping}, 
        {player_stats_match.player_stats.frags},
        {player_stats_match.player_stats.deaths}, {player_stats_match.player_stats.tk}, 
        {player_stats_match.player_stats.spawn_frags}, {player_stats_match.player_stats.kills}, 
        {player_stats_match.player_stats.suicides}, 
        {player_stats_match.player_stats.dmg_taken}, 
        {player_stats_match.player_stats.dmg_given}, {player_stats_match.player_stats.dmg_team}, 
        {player_stats_match.player_stats.dmg_self}, {player_stats_match.player_stats.dmg_team_weap}, 
        {player_stats_match.player_stats.dmg_enemy_weap}, {player_stats_match.player_stats.dmg_taken_to_die}, 
        {player_stats_match.player_stats.xfer_rl}, {player_stats_match.player_stats.xfer_lg}, 
        {player_stats_match.player_stats.spree_max}, {player_stats_match.player_stats.spree_quad}, 
        {player_stats_match.player_stats.control}, {player_stats_match.player_stats.speed_max}, 
        {player_stats_match.player_stats.speed_avg}, 
        '{_create_weapon_primary_key(player_stats_match.match_user_id, 'axe')}', 
        '{_create_weapon_primary_key(player_stats_match.match_user_id, 'sg')}', 
        '{_create_weapon_primary_key(player_stats_match.match_user_id, 'ssg')}', 
        '{_create_weapon_primary_key(player_stats_match.match_user_id, 'ng')}', 
        '{_create_weapon_primary_key(player_stats_match.match_user_id, 'sng')}', 
        '{_create_weapon_primary_key(player_stats_match.match_user_id, 'gl')}', 
        '{_create_weapon_primary_key(player_stats_match.match_user_id, 'rl')}', 
        '{_create_weapon_primary_key(player_stats_match.match_user_id, 'lg')}');
        """


def _create_weapon_primary_key(match_user_id: str, weapon: str) -> str:
    return match_user_id + DELIMITER + weapon


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
    def close_conn(cls):
        if cls.__conn is not None:
            cls.__conn.close()
            cls.__conn = None

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
        try:
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
        except DatabaseError as dbe:
            logger.warning(f"DatabaseError: {dbe}")
            cls.get_conn().rollback()
        cls.get_conn().commit()

    @classmethod
    def upload_stats(cls, player_stats: list[PlayerStatsMatch]) -> None:
        cur = cls.get_conn().cursor()
        try:
            for p in player_stats:
                # Weapon Stats
                cur.execute(
                    add_weapon_stats_for_player_query(
                        match_user_id_weapon=_create_weapon_primary_key(match_user_id=p.match_user_id, weapon='axe'),
                        name=p.name,
                        weapon_stats=p.player_stats.axe_stats
                    ))
                cur.execute(
                    add_weapon_stats_for_player_query(
                        match_user_id_weapon=_create_weapon_primary_key(match_user_id=p.match_user_id, weapon='sg'),
                        name=p.name,
                        weapon_stats=p.player_stats.sg_stats
                    ))
                cur.execute(
                    add_weapon_stats_for_player_query(
                        match_user_id_weapon=_create_weapon_primary_key(match_user_id=p.match_user_id, weapon='ssg'),
                        name=p.name,
                        weapon_stats=p.player_stats.ssg_stats
                    ))
                cur.execute(
                    add_weapon_stats_for_player_query(
                        match_user_id_weapon=_create_weapon_primary_key(match_user_id=p.match_user_id, weapon='ng'),
                        name=p.name,
                        weapon_stats=p.player_stats.ng_stats
                    ))
                cur.execute(
                    add_weapon_stats_for_player_query(
                        match_user_id_weapon=_create_weapon_primary_key(match_user_id=p.match_user_id, weapon='sng'),
                        name=p.name,
                        weapon_stats=p.player_stats.sng_stats
                    ))
                cur.execute(
                    add_weapon_stats_for_player_query(
                        match_user_id_weapon=_create_weapon_primary_key(match_user_id=p.match_user_id, weapon='gl'),
                        name=p.name,
                        weapon_stats=p.player_stats.gl_stats
                    ))
                cur.execute(
                    add_weapon_stats_for_player_query(
                        match_user_id_weapon=_create_weapon_primary_key(match_user_id=p.match_user_id, weapon='rl'),
                        name=p.name,
                        weapon_stats=p.player_stats.rl_stats
                    ))
                cur.execute(
                    add_weapon_stats_for_player_query(
                        match_user_id_weapon=_create_weapon_primary_key(match_user_id=p.match_user_id, weapon='lg'),
                        name=p.name,
                        weapon_stats=p.player_stats.lg_stats
                    ))

                # Item Stats
                cur.execute(
                    add_item_stats_for_player_query(
                        match_user_id=p.match_user_id,
                        name=p.name,
                        item_stats=p.player_stats.item_stats
                    ))

                # Player Stats
                cur.execute(
                    add_stats_for_player_query(
                        player_stats_match=p,
                    ))
        except DatabaseError as dbe:
            logger.warning(f"DatabaseError: {dbe}")
            cls.get_conn().rollback()
        cls.get_conn().commit()

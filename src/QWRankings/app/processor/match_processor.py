import json
import logging
import os
import timeit
import urllib.request
from datetime import datetime
from itertools import combinations

import requests

from app.dal.database import MatchRanksAndStatsDAO
from app.dal.database_objects import MatchInfo, PlayerMatchRanking
from app.dal.idatabase import IDatabase
from app.processor.ratings_processor import process_ratings_for_match
from app.processor.stats_processor import process_stats_for_match

logger = logging.getLogger(__name__)


def process_last_n_matches(mode: str = '4on4', n: int = 500) -> bool:
    if mode == 'ALL':
        modes = ['1on1', '2on2', '4on4']
    else:
        modes = [mode]
    if n > 500:
        n = 500
    if n < 1:
        n = 1
    for m in modes:
        http_res = requests.post(url="https://ncsphkjfominimxztjip.supabase.co/functions/v1/demos",
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps({"mode": m}))
        str_res = str(http_res.content)[2:]  # Remove Binary b'
        str_res = str(str_res)[:-1]  # Remove end quote '
        games = str_res.split('\\n')
        games.reverse()
        for http_url in games[500-n:]:
            request_url = http_url.replace('.gz', '.ktxstats.json')
            try:
                with urllib.request.urlopen(request_url) as f:
                    data = f.read()
                    process_match(ktx_json=data, mode=m)
            except Exception as e:
                logger.warning(http_url)
                if data:
                    logger.warning(data)
                logger.warning(e)
                continue
    return True


def process_local_data(directory_path: str) -> bool:
    first_time = timeit.default_timer()
    all_files = {}
    logger.warning("Aggregating files...")
    start_time = timeit.default_timer()
    for root, dirs, curr_files in os.walk(directory_path):
        for f in curr_files:
            path_to_file = os.path.join(root, f)
            with open(path_to_file) as fi:
                try:
                    data = fi.read()
                    date = json.loads(data)["date"]
                    all_files[date] = data
                except Exception as e:
                    logger.warning(f"Could not process file: {path_to_file}, Exception: {e}")
    logger.warning(f"Aggregating files took {timeit.default_timer() - start_time}")

    logger.warning("Sorting files...")
    start_time = timeit.default_timer()
    sorted_files = dict(sorted(all_files.items()))
    logger.warning(f"Sorting took {timeit.default_timer() - start_time}")

    counter: int = 0

    logger.warning("Processing data...")
    start_time = timeit.default_timer()
    for _date, data in sorted_files.items():
        counter += 1
        if counter % 500 == 0:
            logger.warning(f"{counter / len(all_files)}% Done. Processed {counter} out of {len(all_files)} files so far.")
        demo_text = json.loads(data)["demo"]
        if "duel" in demo_text:
            mode = "1on1"
        elif "2on2" in demo_text:
            mode = "2on2"
        elif "3on3" in demo_text:
            mode = "3on3"
        elif "4on4" in demo_text:
            mode = "4on4"
        elif "ffa" in demo_text:
            mode = "ffa"
        else:
            logger.warning(f"Unsupported Mode, demo_text: {demo_text}")
            continue
        try:
            process_match(ktx_json=data, mode=mode)
        except Exception as e:
            logger.warning(f"Failed to process data: {data}, exception: {e}")
            continue

    logger.warning(f"Processing data took {timeit.default_timer() - start_time} for {len(all_files)} number of files")

    logger.warning(f"Total time to run: {timeit.default_timer() - first_time}")
    return True


def balance_teams(players: list[str], map_choice: str = 'ALL') -> tuple[
    list[tuple[str, float]], list[tuple[str, float]]]:
    ratings: dict[str, float] = __get_ratings(players=players, map_choice=map_choice)
    best_team, other_team = __partition_teams(players=players, ratings=ratings)
    return __sort_players(players=best_team, ratings=ratings), __sort_players(players=other_team, ratings=ratings)


def __get_ratings(players: list[str], map_choice: str) -> dict[str, float]:
    db_dal: IDatabase = MatchRanksAndStatsDAO()
    ratings: dict[str, float] = {}
    for name in players:
        if map_choice == 'ALL':
            ratings[name] = db_dal.get_rating_and_rank(name=name, mode='4on4',
                                                       match_map=map_choice).overall_rating_and_rank.rating
        else:
            ratings[name] = db_dal.get_rating_and_rank(name=name, mode='4on4',
                                                       match_map=map_choice).map_rating_and_rank.rating
    return ratings


def __partition_teams(players: list[str], ratings=None) -> tuple[list, list]:
    team_length: int = len(players) // 2
    if ratings is None:
        return players[team_length:], players[:team_length]
    best_rating: float = sum(ratings.values()) / 2

    best_team = list(min(combinations(players, team_length),
                         key=lambda team: abs(sum([ratings[n] for n in team]) - best_rating))[:4])
    other_team = [p for p in players if p not in best_team]
    return best_team, other_team


def check_teams(players: list[str], map_choice: str = 'ALL') -> tuple[
    list[tuple[str, float]], list[tuple[str, float]]]:
    ratings: dict[str, float] = __get_ratings(players=players, map_choice=map_choice)
    first_team, second_team = __partition_teams(players=players)
    return __sort_players(players=first_team, ratings=ratings), __sort_players(players=second_team, ratings=ratings)


def __sort_players(players: list[str], ratings: dict[str, float]) -> list[tuple[str, float]]:
    sorted_players = [(k, ratings[k]) for k in sorted(players, key=lambda p: [ratings[p]],
                                                      reverse=True)]
    prefix = [("avg ranking", sum([v for _k, v in sorted_players]) / len(sorted_players))]
    prefix.extend(sorted_players)
    return prefix


def process_match(ktx_json: str, mode: str) -> list[PlayerMatchRanking]:
    parsed_json: dict[str, any] = json.loads(ktx_json)

    # create match info
    match_info: MatchInfo = create_match_info(parsed_json, mode)

    db_dal: IDatabase = MatchRanksAndStatsDAO()
    if db_dal.is_match_processed(match_id=match_info.match_id):
        logger.warning(f"match already processed, match_id: {match_info.match_id}")
        return []

    process_stats_for_match(parsed_json=parsed_json, match_info=match_info)

    return process_ratings_for_match(parsed_json=parsed_json, match_info=match_info)


def create_match_info(match_dict: dict[str, any], mode: str) -> MatchInfo:
    match_id: str = match_dict['date'] + match_dict['hostname'].replace("'", "")
    played_map: str = match_dict['map']
    return MatchInfo(
        match_id=match_id,
        date=datetime.strptime(match_dict['date'], "%Y-%m-%d %H:%M:%S %z"),
        mode=mode,
        map=played_map,
    )

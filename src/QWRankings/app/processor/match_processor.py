import json
import logging
import urllib.request
from datetime import datetime
import requests

from app.dal.database import MatchRanksAndStatsDAO
from app.dal.database_objects import MatchInfo, PlayerMatchRanking
from app.dal.idatabase import IDatabase
from app.processor.ratings_processor import process_ratings_for_match
from app.processor.stats_processor import process_stats_for_match

logger = logging.getLogger(__name__)


def process_last_n_matches(mode: str = '4on4', n: int = 500) -> bool:
    http_res = requests.post(url="https://ncsphkjfominimxztjip.supabase.co/functions/v1/demos",
                             headers={"Content-Type": "application/json"},
                             data=json.dumps({"mode": mode}))
    str_res = str(http_res.content)[2:]  # Remove Binary b'
    str_res = str(str_res)[:-1]  # Remove end quote '
    games = str_res.split('\\n')
    games.reverse()
    counter: int = 0
    for http_url in games:
        counter += 1
        if counter > n:
            break
        request_url = http_url.replace('.gz', '.ktxstats.json')
        try:
            with urllib.request.urlopen(request_url) as f:
                data = f.read()
                process_match(ktx_json=data, mode=mode)
        except Exception as e:
            logger.warning(http_url)
            if data:
                logger.warning(data)
            logger.warning(e)
            continue
    return True


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



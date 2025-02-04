from collections import Counter
from functools import reduce

from app.dal.database import MatchRanksAndStatsDAO
from app.dal.database_objects import MatchInfo, PlayerStatsMatch, PlayerStats, ItemStats, WeaponStats
from app.dal.idatabase import IDatabase
from app.util.name_utils import sanitize_name, create_team_name
from app.util.processor_utils import calc_winning_team, generate_match_user_id


def process_stats_for_match(parsed_json: dict[str, any], match_info: MatchInfo) -> list[PlayerStatsMatch]:
    # create and get player stats info
    players_json_list: list[dict] = parsed_json['players']

    deduped_players_json_list = _dedupe_on_key(players_json_list, key="name")

    if match_info.mode == "1on1":
        winning_player: str = calc_winning_team([], deduped_players_json_list)
        players: list[PlayerStatsMatch] = [
            __create_stats(stats_dict=p, name=sanitize_name(p["name"]), login=p["login"], match_info=match_info,
                           win=1 if p['name'] == winning_player else 0)
            for p in
            deduped_players_json_list]
        teams: list[PlayerStatsMatch] = []
    else:
        winning_team: str = calc_winning_team(parsed_json['teams'], deduped_players_json_list)
        players: list[PlayerStatsMatch] = [
            __create_stats(stats_dict=p, name=sanitize_name(p["name"]), login=p["login"], match_info=match_info,
                           win=1 if p['team'] == winning_team else 0)
            for p in
            deduped_players_json_list]
        deduped_team_json_list = _dedupe_on_key(players_json_list, key="team")
        teams: list[PlayerStatsMatch] = [
            __create_stats(stats_dict=p, name=create_team_name(p["team"]), login="", match_info=match_info,
                           win=1 if p['team'] == winning_team else 0)
            for p in
            deduped_team_json_list]

    # upload to DB
    db_dal: IDatabase = MatchRanksAndStatsDAO()
    db_dal.upload_stats(player_stats=players)
    db_dal.upload_stats(player_stats=teams)

    return players


def __create_stats(stats_dict: dict[str, any], name: str, login: str, match_info: MatchInfo,
                   win: int) -> PlayerStatsMatch:
    name: str = sanitize_name(name)
    match_user_id: str = generate_match_user_id(name=name, match_id=match_info.match_id)
    login: str = login
    return PlayerStatsMatch(
        match_info=match_info,
        match_user_id=match_user_id,
        name=name,
        login=login,
        win=win,
        player_stats=__gen_player_stats(stats_dict),
    )


def __gen_player_stats(player_dict: dict[str, any]) -> PlayerStats:
    return PlayerStats(
        ping=player_dict.get('ping', 0),
        frags=player_dict.get('stats', {}).get('frags', 0),
        deaths=player_dict.get('stats', {}).get('deaths', 0),
        tk=player_dict.get('stats', {}).get('tk', 0),
        spawn_frags=player_dict.get('stats', {}).get('spawn-frags', 0),
        kills=player_dict.get('stats', {}).get('kills', 0),
        suicides=player_dict.get('stats', {}).get('suicides', 0),
        dmg_taken=player_dict.get('dmg', {}).get('taken', 0),
        dmg_given=player_dict.get('dmg', {}).get('given', 0),
        dmg_team=player_dict.get('dmg', {}).get('team', 0),
        dmg_self=player_dict.get('dmg', {}).get('self', 0),
        dmg_team_weap=player_dict.get('dmg', {}).get('team-weapons', 0),
        dmg_enemy_weap=player_dict.get('dmg', {}).get('enemy-weapons', 0),
        dmg_taken_to_die=player_dict.get('dmg', {}).get('taken-to-die', 0),
        xfer_rl=player_dict.get('xferRL', 0),
        xfer_lg=player_dict.get('xferLG', 0),
        spree_max=player_dict.get('spree', {}).get('max', 0),
        spree_quad=player_dict.get('spree', {}).get('quad', 0),
        control=player_dict.get('control', 0),
        speed_max=player_dict.get('speed', {}).get('max', 0),
        speed_avg=player_dict.get('speed', {}).get('avg', 0),
        item_stats=__gen_item_stats(player_dict.get('items', {})),
        axe_stats=__gen_weap_stats('axe', player_dict.get('weapons', {})),
        sg_stats=__gen_weap_stats('sg', player_dict.get('weapons', {})),
        ssg_stats=__gen_weap_stats('ssg', player_dict.get('weapons', {})),
        ng_stats=__gen_weap_stats('ng', player_dict.get('weapons', {})),
        sng_stats=__gen_weap_stats('sng', player_dict.get('weapons', {})),
        gl_stats=__gen_weap_stats('gl', player_dict.get('weapons', {})),
        rl_stats=__gen_weap_stats('rl', player_dict.get('weapons', {})),
        lg_stats=__gen_weap_stats('lg', player_dict.get('weapons', {})),
    )


def __gen_item_stats(item_dict: dict[str, any]) -> ItemStats:
    return ItemStats(
        hp_15_took=item_dict.get('health_15', {}).get('took', 0),
        hp_25_took=item_dict.get('health_25', {}).get('took', 0),
        hp_100_took=item_dict.get('health_100', {}).get('took', 0),
        ga_took=item_dict.get('ga', {}).get('took', 0),
        ga_time=item_dict.get('ga', {}).get('time', 0),
        ya_took=item_dict.get('ya', {}).get('took', 0),
        ya_time=item_dict.get('ya', {}).get('time', 0),
        ra_took=item_dict.get('ra', {}).get('took', 0),
        ra_time=item_dict.get('ra', {}).get('time', 0),
        q_took=item_dict.get('q', {}).get('took', 0),
        q_time=item_dict.get('q', {}).get('time', 0),
        p_took=item_dict.get('p', {}).get('took', 0),
        p_time=item_dict.get('p', {}).get('time', 0),
        r_took=item_dict.get('r', {}).get('took', 0),
        r_time=item_dict.get('r', {}).get('time', 0),
    )


def __gen_weap_stats(weap_name: str, weapons_dict: dict[str, any]) -> WeaponStats:
    return WeaponStats(
        weapon_name=weap_name,
        acc_attacks=weapons_dict.get(weap_name, {}).get('acc', {}).get('attacks', 0),
        acc_hits=weapons_dict.get(weap_name, {}).get('acc', {}).get('hits', 0),
        acc_real=weapons_dict.get(weap_name, {}).get('acc', {}).get('real', 0),
        acc_virtual=weapons_dict.get(weap_name, {}).get('acc', {}).get('virtual', 0),
        kills_total=weapons_dict.get(weap_name, {}).get('kills', {}).get('total', 0),
        kills_team=weapons_dict.get(weap_name, {}).get('kills', {}).get('team', 0),
        kills_enemy=weapons_dict.get(weap_name, {}).get('kills', {}).get('enemy', 0),
        kills_self=weapons_dict.get(weap_name, {}).get('kills', {}).get('self', 0),
        deaths=weapons_dict.get(weap_name, {}).get('deaths', 0),
        pickups_dropped=weapons_dict.get(weap_name, {}).get('pickups', {}).get('dropped', 0),
        pickups_taken=weapons_dict.get(weap_name, {}).get('pickups', {}).get('taken', 0),
        pickups_total_taken=weapons_dict.get(weap_name, {}).get('pickups', {}).get('total-taken', 0),
        pickups_spawn_taken=weapons_dict.get(weap_name, {}).get('pickups', {}).get('spawn-taken', 0),
        pickups_spawn_total_taken=weapons_dict.get(weap_name, {}).get('pickups', {}).get('spawn-total-taken', 0),
        dmg_enemy=weapons_dict.get(weap_name, {}).get('damage', {}).get('enemy', 0),
        dmg_team=weapons_dict.get(weap_name, {}).get('damage', {}).get('team', 0),
    )


def __combine_op(k, a, b):
    if k == 'speed_max':
        return max(a, b)
    if k == 'speed_avg':
        return (a + b) / 2
    if k == 'ping':
        return max(a, b)
    if k == 'spree_max':
        return max(a, b)
    if k == 'spree_quad':
        return max(a, b)
    if isinstance(a, float) and isinstance(b, float):
        return a + b
    elif isinstance(a, int) and isinstance(b, int):
        return a + b
    elif isinstance(a, dict) and isinstance(b, dict):
        return combine_dicts(a, b)
    else:
        return b if b else a


def combine_dicts(a, b, op=__combine_op):
    return dict(list(a.items()) + list(b.items()) +
                [(k, op(k, a[k], b[k])) for k in set(b) & set(a)])


def _dedupe_on_key(players: list[dict], key: str = "name") -> list[dict]:
    list_of_keys = list(map(lambda p: p[key], players))
    counts_of_keys = Counter(list_of_keys)
    duplicates = [k for k, v in counts_of_keys.items() if v > 1]

    result = []

    for dupe in duplicates:
        to_combine = list(filter(lambda p: p[key] == dupe, players))
        result.append(reduce(combine_dicts, to_combine, {}))

    for p in players:
        if p[key] not in duplicates:
            result.append(p)

    return result

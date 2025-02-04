import trueskill

from app.dal.database import MatchRanksAndStatsDAO
from app.dal.database_objects import MatchInfo, PlayerMatchRanking, RatingAndRank, PlayerRanking
from app.dal.idatabase import IDatabase
from app.util.name_utils import sanitize_name, create_team_name
from app.util.processor_utils import calc_winning_team, generate_match_user_id

ts = trueskill.TrueSkill(mu=1500, sigma=500, beta=250, tau=5, draw_probability=0.0)


def process_ratings_for_match(parsed_json: dict[str, any], match_info: MatchInfo) -> list[PlayerMatchRanking]:
    # create and get player info
    players_json_list: list[dict] = parsed_json['players']
    if match_info.mode == "1on1":
        winning_player: str = calc_winning_team([], players_json_list)
        players = [__get_or_create_player(p, match_info, 1 if p['name'] == winning_player else 0) for p in players_json_list]
        teams: list[PlayerMatchRanking] = []
    else:
        winning_team: str = calc_winning_team(parsed_json['teams'], players_json_list)
        players = [__get_or_create_player(p, match_info, 1 if p['team'] == winning_team else 0) for p in players_json_list]
        teams: list[PlayerMatchRanking] = [__get_or_create_team(t, match_info, 1 if t == winning_team else 0) for t in parsed_json['teams']]

    # assign winners and losers and update ranks
    winners = list(filter(lambda x: x.win == 1, players))
    losers = list(filter(lambda x: x.win == 0, players))
    new_players: list[PlayerMatchRanking] = __rate_players_for_match(winners=winners, losers=losers)

    if len(teams) == 2:
        team_winner = list(filter(lambda x: x.win == 1, teams))
        team_loser = list(filter(lambda x: x.win == 0, teams))
        new_teams: list[PlayerMatchRanking] = __rate_players_for_match(winners=team_winner, losers=team_loser)
    else:
        new_teams: list[PlayerMatchRanking] = []

    # update database
    db_dal: IDatabase = MatchRanksAndStatsDAO()
    db_dal.update_ratings(new_players)
    db_dal.update_ratings(new_teams)

    return new_players


def __rate_players_for_match(winners: list[PlayerMatchRanking], losers: list[PlayerMatchRanking]) -> list[
    PlayerMatchRanking]:
    winners_overall, losers_overall = __trueskill_ratings([p.overall_rating_and_rank for p in winners],
                                                          [p.overall_rating_and_rank for p in losers])
    winners_map, losers_map = __trueskill_ratings([p.map_rating_and_rank for p in winners],
                                                  [p.map_rating_and_rank for p in losers])
    for p in winners:
        p.overall_rating_and_rank = winners_overall.pop(0)
        p.map_rating_and_rank = winners_map.pop(0)

    for p in losers:
        p.overall_rating_and_rank = losers_overall.pop(0)
        p.map_rating_and_rank = losers_map.pop(0)

    return winners + losers


def __trueskill_ratings(winners_rar: list[RatingAndRank], losers_rar: list[RatingAndRank]) -> tuple[
    list[RatingAndRank], list[RatingAndRank]]:
    g1 = [ts.create_rating(mu=p.rating, sigma=p.ratings_deviation) for p in winners_rar]
    g2 = [ts.create_rating(mu=p.rating, sigma=p.ratings_deviation) for p in losers_rar]
    g1, g2 = (list(i) for i in ts.rate((g1, g2), ranks=[0, 1]))

    winners_ret = []
    losers_ret = []

    for p in winners_rar:
        new_ranking: trueskill.Rating = g1.pop(0)
        new_rating_and_rank = RatingAndRank(
            rating=new_ranking.mu,
            ratings_deviation=new_ranking.sigma,
            rank=p.rank,
        )
        winners_ret.append(new_rating_and_rank)

    for p in losers_rar:
        new_ranking: trueskill.Rating = g2.pop(0)
        new_rating_and_rank = RatingAndRank(
            rating=new_ranking.mu,
            ratings_deviation=new_ranking.sigma,
            rank=p.rank,
        )
        losers_ret.append(new_rating_and_rank)

    return winners_ret, losers_ret


def __get_or_create_player(player_dict: dict[str, any], match_info: MatchInfo, win: int) -> PlayerMatchRanking:
    name: str = sanitize_name(player_dict['name'])
    match_user_id: str = generate_match_user_id(name=name, match_id=match_info.match_id)
    login: str = player_dict['login']

    db_dal: IDatabase = MatchRanksAndStatsDAO()
    player_rankings: PlayerRanking = db_dal.get_rating_and_rank(name=name, mode=match_info.mode, match_map=match_info.map)

    return PlayerMatchRanking(
        match_info=match_info,
        match_user_id=match_user_id,
        name=name,
        login=login,
        overall_rating_and_rank=player_rankings.overall_rating_and_rank,
        map_rating_and_rank=player_rankings.map_rating_and_rank,
        win=win,
    )


def __get_or_create_team(team: str, match_info: MatchInfo, win: int) -> PlayerMatchRanking:
    name: str = create_team_name(team)
    match_user_id: str = generate_match_user_id(name=name, match_id=match_info.match_id)

    db_dal: IDatabase = MatchRanksAndStatsDAO()
    team_ranking: PlayerRanking = db_dal.get_rating_and_rank(name=name, mode=match_info.mode, match_map=match_info.map)

    return PlayerMatchRanking(
        match_info=match_info,
        match_user_id=match_user_id,
        name=name,
        login="",
        overall_rating_and_rank=team_ranking.overall_rating_and_rank,
        map_rating_and_rank=team_ranking.map_rating_and_rank,
        win=win,
    )

import trueskill

from app.dal.database import MatchRanksAndStatsDAO
from app.dal.database_objects import MatchInfo, PlayerMatchRanking, RatingAndRank, PlayerRanking
from app.dal.idatabase import IDatabase
from app.util.name_sanitizer import sanitize_name

ts = trueskill.TrueSkill(mu=1500, sigma=350, beta=750, tau=3)


def process_ratings_for_match(parsed_json: dict[str, any], match_info: MatchInfo) -> list[PlayerMatchRanking]:
    # create and get player info
    players_json_list: list[dict] = parsed_json['players']
    if match_info.mode == "1on1":
        winning_player: str = __calc_winning_team([], players_json_list)
        players = [__get_or_create_player(p, match_info, 1 if p['name'] == winning_player else 0) for p in players_json_list]
    else:
        winning_team: str = __calc_winning_team(parsed_json['teams'], players_json_list)
        players = [__get_or_create_player(p, match_info, 1 if p['team'] == winning_team else 0) for p in players_json_list]

    # assign winners and losers
    winners = list(filter(lambda x: x.win == 1, players))
    losers = list(filter(lambda x: x.win == 0, players))

    # update ranks
    new_players: list[PlayerMatchRanking] = __rate_players_for_match(winners=winners, losers=losers)

    # update database
    db_dal: IDatabase = MatchRanksAndStatsDAO()
    db_dal.update_ratings(new_players)

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


def __calc_winning_team(teams: list[str], players_json_list: list[dict]) -> str:
    if not teams:
        best_score: int = -99
        best_player: str = ""

        for p in players_json_list:
            best_score = p['stats']['frags'] if p['stats']['frags'] >= best_score else best_score
            best_player = p['name'] if p['stats']['frags'] >= best_score else best_player

        return best_player
    winning_score = None
    winning_team = None
    for team in teams:
        players_on_team: list[dict] = list(filter(lambda x: x['team'] == team, players_json_list))
        total_score: int = 0
        for player in players_on_team:
            total_score += player['stats']['frags']
        if winning_score is None:
            winning_score = total_score
            winning_team = team
        elif total_score > winning_score:
            winning_score = total_score
            winning_team = team
    return winning_team


def __get_or_create_player(player_dict: dict[str, any], match_info: MatchInfo, win: int) -> PlayerMatchRanking:
    name: str = sanitize_name(player_dict['name'])
    match_user_id: str = match_info.match_id + name
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

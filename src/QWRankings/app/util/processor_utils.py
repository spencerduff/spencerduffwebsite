DELIMITER = ":"


def calc_winning_team(teams: list[str], players_json_list: list[dict]) -> str:
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


def generate_match_user_id(name: str, match_id: str) -> str:
    return match_id + DELIMITER + name

import pytest

from app.util.processor_utils import calc_winning_team, generate_match_user_id

PLAYERS_JSON_LIST_4: list[dict] = [
    {
        'name': 'test1',
        'stats': {
            'frags': 25
        },
        'team': 'team1'
    },
    {
        'name': 'test2',
        'stats': {
            'frags': 25
        },
        'team': 'team1'
    },
    {
        'name': 'test3',
        'stats': {
            'frags': 39
        },
        'team': 'team2'
    },
    {
        'name': 'test4',
        'stats': {
            'frags': 10
        },
        'team': 'team2'
    },
]


PLAYERS_JSON_LIST_2: list[dict] = [
    {
        'name': 'test1',
        'stats': {
            'frags': 26
        },
    },
    {
        'name': 'test2',
        'stats': {
            'frags': 25
        },
    },
]

test_teams_players_and_results = [
    (
        ["team1", "team2"], PLAYERS_JSON_LIST_4,  "team1"
    ),
    (
        [], PLAYERS_JSON_LIST_2, "test1"
    ),
]


@pytest.mark.parametrize("teams, players_json_list, expected_result", test_teams_players_and_results)
def test_calc_winning_team(teams: list[str], players_json_list: list[dict], expected_result: str) -> None:
    assert calc_winning_team(teams=teams, players_json_list=players_json_list) == expected_result


def test_generate_match_id() -> None:
    assert generate_match_user_id(name="test", match_id="2012-12-12") == '2012-12-12test'

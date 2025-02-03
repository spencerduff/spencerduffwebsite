import json
import unittest
from unittest.mock import patch

from app.dal.database_objects import MatchInfo, PlayerStatsMatch
from app.processor.match_processor import create_match_info
from app.processor.stats_processor import process_stats_for_match, combine_dicts, _dedupe_players
from tests.data.expected_outputs import EXPECTED_4on4_DM3_STATS_OUPUT
from tests.data.inputs import TEST_COMBINE_DICTS
from tests.test_util.mock_db import TestDAL


class TestStatsProcessor(unittest.TestCase):
    def setUp(self):
        for p in self.patch_database():
            p.start()
        pass

    def tearDown(self):
        for p in self.patch_database():
            p.stop()
        pass

    @staticmethod
    def patch_database():
        return [patch("app.processor.stats_processor.MatchRanksAndStatsDAO", TestDAL)]

    def test_process_stats_4on4(self) -> None:
        input_json_filename: str = "tests/data/test_4on4_dm3.json"
        mode: str = '4on4'
        expected_output: list[PlayerStatsMatch] = EXPECTED_4on4_DM3_STATS_OUPUT
        with open(input_json_filename) as f:
            input_json_data: str = f.read()
            parsed_json: dict[str, any] = json.loads(input_json_data)
            match_info: MatchInfo = create_match_info(parsed_json, mode=mode)
            result = process_stats_for_match(parsed_json=parsed_json, match_info=match_info)
            assert result == expected_output

    def test__dedupe_players(self) -> None:
        test_dicts = TEST_COMBINE_DICTS
        assert len(test_dicts) == 9
        res = _dedupe_players(test_dicts)
        assert len(res) == 8
        assert res[0]["stats"]["frags"] == 54
        assert res[0]["name"] == "Coò"

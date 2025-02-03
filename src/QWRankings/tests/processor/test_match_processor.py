import unittest
from unittest.mock import patch

from app.dal.database import PlayerMatchRanking
from app.processor.match_processor import process_match
from tests.data.expected_outputs import EXPECTED_4on4_RANKINGS_OUTPUT, EXPECTED_1on1_RANKINGS_OUTPUT
from tests.test_util.mock_db import TestDAL


class TestMatchProcessor(unittest.TestCase):
    def setUp(self):
        for p in self.patch_database():
            p.start()

    def tearDown(self):
        for p in self.patch_database():
            p.stop()

    @staticmethod
    def patch_database():
        return [patch("app.processor.match_processor.MatchRanksAndStatsDAO", TestDAL),
                patch("app.processor.stats_processor.MatchRanksAndStatsDAO", TestDAL),
                patch("app.processor.ratings_processor.MatchRanksAndStatsDAO", TestDAL)]

    def test_process_match_4on4(self) -> None:
        input_json_filename: str = "tests/data/test_4on4.json"
        mode: str = "4on4"
        expected_output: list[PlayerMatchRanking] = EXPECTED_4on4_RANKINGS_OUTPUT
        with open(input_json_filename) as f:
            input_json_data: str = f.read()
            assert process_match(ktx_json=input_json_data, mode=mode) == expected_output

    def test_process_match_1on1(self) -> None:
        input_json_filename: str = "tests/data/test_1on1.json"
        mode: str = "1on1"
        expected_output: list[PlayerMatchRanking] = EXPECTED_1on1_RANKINGS_OUTPUT
        with open(input_json_filename) as f:
            input_json_data: str = f.read()
            assert process_match(ktx_json=input_json_data, mode=mode) == expected_output

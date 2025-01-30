import datetime
import unittest
from unittest.mock import patch

from app.dal.database import PlayerMatchRanking
from app.dal.database_objects import MatchInfo, RatingAndRank
from app.processor.match_processor import process_match
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
                patch("app.processor.ratings_processor.MatchRanksAndStatsDAO", TestDAL)]

    def test_process_match_4on4(self) -> None:
        input_json_filename: str = "tests/data/test_4on4.json"
        mode: str = "4on4"
        expected_output: list[PlayerMatchRanking] = [PlayerMatchRanking(
            match_info=MatchInfo(match_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQW',
                                 date=datetime.datetime(2025, 1, 23, 7, 37, 14, tzinfo=datetime.timezone.utc),
                                 mode='4on4', map='dm2'),
            match_user_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQWBLooD_DoG(D_P)', name='BLooD_DoG(D_P)',
            login='',
            overall_rating_and_rank=RatingAndRank(rating=1545.621871387112, ratings_deviation=347.41835834645417,
                                                  rank=1),
            map_rating_and_rank=RatingAndRank(rating=1545.621871387112, ratings_deviation=347.41835834645417, rank=1),
            win=1), PlayerMatchRanking(
            match_info=MatchInfo(match_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQW',
                                 date=datetime.datetime(2025, 1, 23, 7, 37, 14, tzinfo=datetime.timezone.utc),
                                 mode='4on4', map='dm2'),
            match_user_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQWnamtsui', name='namtsui', login='',
            overall_rating_and_rank=RatingAndRank(rating=1545.621871387112, ratings_deviation=347.41835834645417,
                                                  rank=1),
            map_rating_and_rank=RatingAndRank(rating=1545.621871387112, ratings_deviation=347.41835834645417, rank=1),
            win=1), PlayerMatchRanking(
            match_info=MatchInfo(match_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQW',
                                 date=datetime.datetime(2025, 1, 23, 7, 37, 14, tzinfo=datetime.timezone.utc),
                                 mode='4on4', map='dm2'),
            match_user_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQWPred', name='Pred', login='',
            overall_rating_and_rank=RatingAndRank(rating=1545.621871387112, ratings_deviation=347.41835834645417,
                                                  rank=1),
            map_rating_and_rank=RatingAndRank(rating=1545.621871387112, ratings_deviation=347.41835834645417, rank=1),
            win=1), PlayerMatchRanking(
            match_info=MatchInfo(match_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQW',
                                 date=datetime.datetime(2025, 1, 23, 7, 37, 14, tzinfo=datetime.timezone.utc),
                                 mode='4on4', map='dm2'),
            match_user_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQWBullD0zer', name='BullD0zer', login='',
            overall_rating_and_rank=RatingAndRank(rating=1545.621871387112, ratings_deviation=347.41835834645417,
                                                  rank=1),
            map_rating_and_rank=RatingAndRank(rating=1545.621871387112, ratings_deviation=347.41835834645417, rank=1),
            win=1), PlayerMatchRanking(
            match_info=MatchInfo(match_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQW',
                                 date=datetime.datetime(2025, 1, 23, 7, 37, 14, tzinfo=datetime.timezone.utc),
                                 mode='4on4', map='dm2'),
            match_user_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQWyeti', name='yeti', login='',
            overall_rating_and_rank=RatingAndRank(rating=1454.3781286128876, ratings_deviation=347.41835834645417,
                                                  rank=1),
            map_rating_and_rank=RatingAndRank(rating=1454.3781286128876, ratings_deviation=347.41835834645417, rank=1),
            win=0), PlayerMatchRanking(
            match_info=MatchInfo(match_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQW',
                                 date=datetime.datetime(2025, 1, 23, 7, 37, 14, tzinfo=datetime.timezone.utc),
                                 mode='4on4', map='dm2'),
            match_user_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQWcoj', name='coj', login='',
            overall_rating_and_rank=RatingAndRank(rating=1454.3781286128876, ratings_deviation=347.41835834645417,
                                                  rank=1),
            map_rating_and_rank=RatingAndRank(rating=1454.3781286128876, ratings_deviation=347.41835834645417, rank=1),
            win=0), PlayerMatchRanking(
            match_info=MatchInfo(match_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQW',
                                 date=datetime.datetime(2025, 1, 23, 7, 37, 14, tzinfo=datetime.timezone.utc),
                                 mode='4on4', map='dm2'),
            match_user_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQWphylter', name='phylter', login='',
            overall_rating_and_rank=RatingAndRank(rating=1454.3781286128876, ratings_deviation=347.41835834645417,
                                                  rank=1),
            map_rating_and_rank=RatingAndRank(rating=1454.3781286128876, ratings_deviation=347.41835834645417, rank=1),
            win=0), PlayerMatchRanking(
            match_info=MatchInfo(match_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQW',
                                 date=datetime.datetime(2025, 1, 23, 7, 37, 14, tzinfo=datetime.timezone.utc),
                                 mode='4on4', map='dm2'),
            match_user_id='2025-01-23 07:37:14 +0000la.quake.world:28501 NAQWSchotty', name='Schotty', login='',
            overall_rating_and_rank=RatingAndRank(rating=1454.3781286128876, ratings_deviation=347.41835834645417,
                                                  rank=1),
            map_rating_and_rank=RatingAndRank(rating=1454.3781286128876, ratings_deviation=347.41835834645417, rank=1),
            win=0)]
        with open(input_json_filename) as f:
            input_json_data: str = f.read()
            assert process_match(ktx_json=input_json_data, mode=mode) == expected_output

    def test_process_match_1on1(self) -> None:
        input_json_filename: str = "tests/data/test_1on1.json"
        mode: str = "1on1"
        expected_output: list[PlayerMatchRanking] = [PlayerMatchRanking(
            match_info=MatchInfo(match_id='2025-01-19 05:11:33 +0000la.quake.world:28502 NAQW',
                                 date=datetime.datetime(2025, 1, 19, 5, 11, 33, tzinfo=datetime.timezone.utc),
                                 mode='1on1', map='aerowalk'),
            match_user_id='2025-01-19 05:11:33 +0000la.quake.world:28502 NAQWhi', name='hi', login='',
            overall_rating_and_rank=RatingAndRank(rating=1591.2437427742243, ratings_deviation=339.51592431663795,
                                                  rank=1),
            map_rating_and_rank=RatingAndRank(rating=1591.2437427742243, ratings_deviation=339.51592431663795, rank=1),
            win=1), PlayerMatchRanking(
            match_info=MatchInfo(match_id='2025-01-19 05:11:33 +0000la.quake.world:28502 NAQW',
                                 date=datetime.datetime(2025, 1, 19, 5, 11, 33, tzinfo=datetime.timezone.utc),
                                 mode='1on1', map='aerowalk'),
            match_user_id='2025-01-19 05:11:33 +0000la.quake.world:28502 NAQWgambling degen', name='gambling degen',
            login='',
            overall_rating_and_rank=RatingAndRank(rating=1408.7562572257752, ratings_deviation=339.51592431663795,
                                                  rank=1),
            map_rating_and_rank=RatingAndRank(rating=1408.7562572257752, ratings_deviation=339.51592431663795, rank=1),
            win=0)]
        with open(input_json_filename) as f:
            input_json_data: str = f.read()
            assert process_match(ktx_json=input_json_data, mode=mode) == expected_output

import argparse

from app.dal.database import MatchRanksAndStatsDAO
from app.processor.match_processor import process_last_n_matches, process_local_data, balance_teams

SUPPORTED_MODES: list[str] = ["4on4", "1on1", "2on2"]


# Run the script for the last 500 games for a given mode
# Set the following environment variables for the Postgres database that runs locally:
# "POSTGRES_DATABASE_USER"
# "POSTGRES_DATABASE_PASSWORD"
# "POSTGRES_DATABASE_PORT" (default 5432)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", nargs=1, choices=SUPPORTED_MODES, default="4on4")
    parser.add_argument("-n", "--num", type=int, nargs=1, default=500)
    parser.add_argument("-l", "--local", type=str, nargs=1, default="")
    parser.add_argument("-b", "--balance", type=str, nargs='*', default="")
    parser.add_argument("-ma", "--map", type=str, nargs=1, default="ALL")
    args = parser.parse_args()
    if len(args.balance) == 8 and args.map[0]:
        print(balance_teams(args.balance, args.map[0]))
    elif args.local[0]:
        process_local_data(args.local[0])
    else:
        process_last_n_matches(args.mode[0], args.num[0])

    MatchRanksAndStatsDAO().close_conn()



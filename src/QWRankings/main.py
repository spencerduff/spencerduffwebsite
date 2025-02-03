import argparse
from app.processor.match_processor import process_last_n_matches


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
    args = parser.parse_args()
    process_last_n_matches(args.mode[0], args.num[0])



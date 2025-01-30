import argparse
from app.processor.match_processor import process_last_500_matches


SUPPORTED_MODES: list[str] = ["4on4", "1on1", "2on2"]


# Run the script for the last 500 games for a given mode
# Set the following environment variables for the Postgres database that runs locally:
# "POSTGRES_DATABASE_USER"
# "POSTGRES_DATABASE_PASSWORD"
# "POSTGRES_DATABASE_PORT" (default 5432)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", nargs=1, choices=SUPPORTED_MODES, default="4on4")
    args = parser.parse_args()

    if args.mode and args.mode[0] in SUPPORTED_MODES:
        process_last_500_matches(args.mode[0])
    elif args.mode and args.mode[0] not in SUPPORTED_MODES:
        raise f"Unsupported Mode: {args.mode[0]}"
    else:
        process_last_500_matches()



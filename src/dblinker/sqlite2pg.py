import argparse


def sqlite2pg():
    my_sqlite2pg_parser = argparse.ArgumentParser(description="SQLITE to PostgreSQL")

    my_sqlite2pg_parser.add_argument('-s', '--sqliteconf', help="Your bookmarked sqlite config")
    my_sqlite2pg_parser.add_argument('-p', '--pgcred', help="Your bookmarked postgress credentials")
    my_sqlite2pg_parser.add_argument('-m', '--pgschema', help="Your bookmarked postgress credentials")


    my_args = my_sqlite2pg_parser.parse_args()

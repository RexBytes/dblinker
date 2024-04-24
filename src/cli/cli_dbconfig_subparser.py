from dblinker.managers.dbconfig_manager import DBConfigManager
from pathlib import Path


def cli_dbconfig_subparser(subparsers):
    dbconfig_manager = DBConfigManager()

    dbconfig_parser = subparsers.add_parser('dbconfig', help='Manage database configurations')
    dbconfig_subparsers = dbconfig_parser.add_subparsers(dest='dbconfig_command', help='dbconfig commands')

    # The "create" subcommand
    create_parser = dbconfig_subparsers.add_parser('create', help='Create a new database configuration file.')
    create_parser.add_argument('--type', choices=['sqlite', 'pg'], required=True,
                               help='Database type for the configuration template.')
    create_parser.add_argument('--filepath', required=True,
                               help='Path to where you want your configuration file created.')
    create_parser.set_defaults(func=dbconfig_create_handler, dbconfig_manager=dbconfig_manager)

    # The "test" subcommand
    test_parser = dbconfig_subparsers.add_parser('test',
                                                 help='Test the database connection using a configuration file.')
    test_parser.add_argument('--filepath', required=True, help='Path to the configuration file you want to test.')
    test_parser.set_defaults(func=dbconfig_test_handler, dbconfig_manager=dbconfig_manager)


def dbconfig_create_handler(args):
    dbconfig_manager = args.dbconfig_manager
    filepath = Path(args.filepath)
    if filepath.exists():
        print(f'Configuration file already exists: {filepath}\nEdit this file to update settings.')
    else:
        config_template_text = dbconfig_manager.get_config_template_text(args.type)
        dbconfig_manager.write_config_template_text(filepath, config_template_text)


def dbconfig_test_handler(args):
    dbconfig_manager = args.dbconfig_manager
    dbconfig_manager.test_connection(args.filepath)

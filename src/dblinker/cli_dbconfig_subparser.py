from .cli_dbconfig_manager import DBConfigManager


def cli_dbconfig_subparser(subparsers):
    dbconfig_manager = DBConfigManager()

    dbconfig_parser = subparsers.add_parser('dbconfig', help='Manage database configurations')
    dbconfig_subparsers = dbconfig_parser.add_subparsers(dest='dbconfig_command', help='dbconfig commands')

    # Create subcommand
    create_parser = dbconfig_subparsers.add_parser('create', help='Create a new database configuration file.')
    create_parser.add_argument('--type', choices=['sqlite', 'pg'], required=True,
                               help='Database type for the configuration template.')
    create_parser.add_argument('--name', required=True, help='Name for the configuration file.')
    create_parser.set_defaults(func=dbconfig_create_handler, dbconfig_manager=dbconfig_manager)

    # Test subcommand
    test_parser = dbconfig_subparsers.add_parser('test',
                                                 help='Test the database connection using a configuration file.')
    test_parser.add_argument('--name', required=True, help='Name of the configuration file to test.')
    test_parser.set_defaults(func=dbconfig_test_handler, dbconfig_manager=dbconfig_manager)


def dbconfig_create_handler(args, dbconfig_manager):
    config_file_path = dbconfig_manager.get_config_file_path(args.name)
    if config_file_path.exists():
        print(f'Configuration file already exists: {config_file_path}\nEdit this file to update settings.')
    else:
        config_template = dbconfig_manager.get_config_template(args.type)
        dbconfig_manager.write_config_template(config_file_path, config_template)


def dbconfig_test_handler(args, dbconfig_manager):
    config_file_path = dbconfig_manager.get_config_file_path(args.name)
    dbconfig_manager.test_connection(config_file_path)

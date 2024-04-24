from dblinker.managers.db_server_config_manager import DBServerConfigManager


def cli_db_server_config_subparser(subparsers):
    db_server_config_manager = DBServerConfigManager()

    db_server_config_parser = subparsers.add_parser('dbserverconfig',
                                                    help='Generate suggested server configuration entries')

    db_server_config_parser.add_argument('--filepath', required=True,
                                         help='Path to the config you want settings generated.')
    db_server_config_parser.set_defaults(func=db_server_config_create_handler,
                                         db_server_config_manager=db_server_config_manager)


def db_server_config_create_handler(args):
    db_server_config_manager = args.db_server_config_manager

    if args.filepath:
        db_server_config_manager.get_server_config(args.filepath)

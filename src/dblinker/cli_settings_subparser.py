import argparse
from pathlib import Path
from .settings_manager import SettingsManager


def cli_settings_subparser(subparsers):
    # Create a subparser for the settings command
    subparser = subparsers.add_parser('settings', help='Manage application settings.')

    # Add arguments specific to the settings management
    subparser.add_argument("--set-connection-config-dir", type=str,
                           help="Set a new directory for connection configurations, using '~' for the home directory.")
    subparser.add_argument("--reset-connection-config-dir", action="store_true",
                           help="Reset the connection configurations directory to default.")

    # Set the default function to call with parsed arguments
    subparser.set_defaults(func=settings_subparser_handle)


def settings_subparser_handle(args):
    settings_manager = SettingsManager()

    if args.set_connection_config_dir:
        new_dir = Path(args.set_connection_config_dir).expanduser().resolve()
        # Your logic to update settings goes here
        new_dir_list = str(new_dir).parts  # More direct approach to get path components
        settings_manager.save_user_settings({'appConnectionConfigDir': new_dir_list})

    elif args.reset_connection_config_dir:
        # Reset logic goes here
        settings_manager.save_user_settings(
            {'appConnectionConfigDir': settings_manager.settings.get('appDefaultConfigDir')})

    print("Settings updated successfully.")

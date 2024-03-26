import argparse
from pathlib import Path
import yaml
from dblinker.settings_manager import SettingsManager
from importlib import resources
from tests.database_integration_test import DatabaseIntegrationTest
import asyncio

my_settings_manager = SettingsManager()
APP_STUB_CONFIG_DIR = Path.home() / my_settings_manager.settings['appStubConfigDir']
APP_CONNECTION_CONFIG_DIR = Path('/',*my_settings_manager.settings['appConnectionConfigDir'])

# Define templates globally
templates = {'sqlite': 'sqlite.yaml', 'pg': 'postgres.yaml'}

def get_config_file_path(name):
    """Generate the full path for a given configuration file name."""
    return APP_CONNECTION_CONFIG_DIR / f'{name}.yaml'

def load_template(filename):
    """
    Load a YAML configuration template from a file within the package.

    Args:
        filename: The name of the file to load.

    Returns:
        The loaded YAML data.
    """
    with resources.files(f"{my_settings_manager.settings['appPackageName']}.common.templates").joinpath(filename) as path, \
            resources.as_file(path) as config_file, \
            open(config_file, 'r') as file:
        return yaml.safe_load(file)


def get_config_template(database_type):
    """
    Retrieve the configuration template based on the database type.

    Args:
        database_type: The type of database ('sqlite' or 'pg').

    Returns:
        The loaded template data.

    Raises:
        ValueError: If the database type is unsupported.
    """
    if database_type in templates:
        return load_template(templates[database_type])
    else:
        raise ValueError(f'Unsupported database type. Supported types are: {", ".join(templates.keys())}')


def write_config_template(file_path, config_data):
    """
    Write the configuration template data to a file.

    Args:
        file_path: The Path object where the data should be written.
        config_data: The data to write.
    """
    # Ensure the directory exists before attempting to write the file
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w') as f:
        yaml.dump(config_data, f, sort_keys=False, default_flow_style=False, width=1000)
    print(f'New configuration template created: {file_path}')


def test_connection(config_file_path):
    print(f'Testing connection using configuration file: {config_file_path}')

    with open(config_file_path, 'r') as f:
        config_data = yaml.safe_load(f)

    database_type = next(iter(config_data))

    connection_settings = config_data[database_type]['connection_settings']

    integration_tester = DatabaseIntegrationTest()

    if database_type == 'postgresql':
        asyncio.run(integration_tester.test_postgresql_connection(config_data))
    elif database_type == 'sqlite':
        integration_tester.test_sqlite_connection(connection_settings)
    else:
        print(f"Unsupported database type: {database_type}")


def main():
    parser = argparse.ArgumentParser(
        description='Utility for managing database configuration files and testing connections.',
        formatter_class=argparse.RawTextHelpFormatter)

    # Create a subparser object
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Create configuration file subcommand
    create_parser = subparsers.add_parser('create', help='Create a new database configuration file.')
    create_parser.add_argument('--type', choices=['sqlite', 'pg'], required=True,
                               help='Database type for the configuration template.')
    create_parser.add_argument('--name', required=True, help='Name for the configuration file.')

    # Test connection subcommand
    test_parser = subparsers.add_parser('test', help='Test the database connection using a configuration file.')
    test_parser.add_argument('--name', required=True, help='Name of the configuration file to test.')

    args = parser.parse_args()

    if args.command == 'create':
        config_file_path = get_config_file_path(args.name)
        if config_file_path.exists():
            print(f'Configuration file already exists: {config_file_path}\nEdit this file to update settings.')
        else:
            config_template = get_config_template(args.type)
            write_config_template(config_file_path, config_template)
    elif args.command == 'test':
        config_file_path = get_config_file_path(args.name)
        test_connection(config_file_path)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

from dblinker.managers.dbconnection_manager import DBConnectionManager
import yaml


class DatabaseIntegrationTest:
    def __init__(self):
        self.dbconnection_manager = DBConnectionManager()

    async def test_postgresql_connection(self, config_file_path):

        connection = await self.dbconnection_manager.get_database_connection(config_file_path)
        # print(connection.__dict__)

        with open(config_file_path, 'r') as config_file:
            config = yaml.safe_load(config_file)

        # Depending on the connection type ('normal', 'pool', 'async', 'async_pool'),
        # the testing approach may vary. Here's a simplified example for 'normal' and 'async':
        if config['postgresql']['connection_type'] in ['normal', 'pool']:
            connection.test_connection()
            connection.disconnect()
        elif config['postgresql']['connection_type'] in ['async', 'async_pool']:
            await connection.test_connection()
            await connection.disconnect()

    def test_sqlite_connection(self, config_file_path):
        print(f"Testing SQLite connection... {config_file_path}")
        # SQLite testing logic goes here

from dblinker.managers.dbconnection_manager import DBConnectionManager
import yaml


class DatabaseIntegrationTest:
    def __init__(self):
        self.dbconnection_manager = DBConnectionManager()

    async def test_postgresql_connection(self, config_file_path):
        try:
            # Retrieve the database connection; assume it's already prepared to be used as an async context manager
            connection = await self.dbconnection_manager.get_database_connection(config_file_path)

            # Read the configuration file to determine the connection type
            with open(config_file_path, 'r') as config_file:
                config = yaml.safe_load(config_file)

            if config['postgresql']['connection_type'] in ['normal', 'pool']:
                with connection as sync_connection:
                    sync_connection.test_connection()
            elif config['postgresql']['connection_type'] in ['async', 'async_pool']:
                async with connection as async_connection:
                    await async_connection.test_connection()

        except Exception as e:
            print(f"An error occurred while testing the connection: {e}")

        # Use the async context manager for managing the lifecycle of the connection
        # async with connection:
        #    if config['postgresql']['connection_type'] in ['normal', 'pool']:
        #        # For synchronous-style connections, we just call the testing directly
        #        connection.test_connection()  # Assuming this is a synchronous method call
        #    elif config['postgresql']['connection_type'] in ['async', 'async_pool']:
        #        # For async-style connections, use await for asynchronous operations
        #        await connection.test_connection()  # Assuming this is an asynchronous method call

    def test_sqlite_connection(self, config_file_path):
        print(f"Testing SQLite connection... {config_file_path}")
        # SQLite testing logic goes here

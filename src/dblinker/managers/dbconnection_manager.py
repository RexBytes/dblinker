import yaml
from dblinker.connections.postgres.postgres_connection_factory import PostgresConnectionFactory


class DBConnectionManager:
    def __init__(self):
        pass

    async def get_database_connection(self, config_file_path):
        """Establish a database connection using a configuration file."""
        with open(config_file_path, 'r') as f:
            config_data_dictionary = yaml.safe_load(f)
        database_type = next(iter(config_data_dictionary))

        if database_type == 'postgresql':
            return await self.get_postgresql_connection(config_data_dictionary)
        elif database_type == 'sqlite':
            return self.get_sqlite_connection(config_data_dictionary)
        else:
            raise ValueError(f"Unsupported database type: {database_type}")

    async def get_postgresql_connection(self, config_data_dictionary):
        """Create and return PostgreSQL connection based on the configuration."""
        factory = PostgresConnectionFactory(config_data_dictionary)
        connection = factory.get_connection()

        if config_data_dictionary['postgresql']['connection_type'] in ['normal', 'pool']:
            connection.connect()
            return connection
        elif config_data_dictionary['postgresql']['connection_type'] in ['async', 'async_pool']:
            await connection.connect()
            return connection

    def get_sqlite_connection(self, config_data_dictionary):
        """Create and return SQLite connection based on the connection settings."""
        # SQLite connection logic here, such as creating a connection object
        print("Establishing SQLite connection...")
        # Assuming a simple SQLite connection
        import sqlite3
        connection = sqlite3.connect(config_data_dictionary['database'])
        return connection

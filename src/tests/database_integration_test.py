from dblinker.connections.postgres.postgres_connection_factory import PostgresConnectionFactory


class DatabaseIntegrationTest:
    async def test_postgresql_connection(self, config):
        # Create a connection object using the factory and configuration
        factory = PostgresConnectionFactory(config)
        connection = factory.get_connection()

        # Depending on the connection type ('normal', 'pool', 'async', 'async_pool'),
        # the testing approach may vary. Here's a simplified example for 'normal' and 'async':
        if config['postgresql']['connection_type'] in ['normal', 'pool']:
            connection.connect()
            connection.test_connection()
            connection.disconnect()
        elif config['postgresql']['connection_type'] in ['async', 'async_pool']:
            await connection.connect()
            await connection.test_connection()
            await connection.disconnect()

    def test_sqlite_connection(self, connection_settings):
        print("Testing SQLite connection...")
        # SQLite testing logic goes here

from psycopg_pool import ConnectionPool
from psycopg import OperationalError
# Assuming PostgresBaseConnection is correctly implemented elsewhere
from .base_connection import PostgresBaseConnection

class PGPoolConnection(PostgresBaseConnection):
    def __init__(self, config, pool_settings=None):
        super().__init__()  # Initialize the base class, if necessary
        self.config = config
        self.pool_settings = pool_settings or {}

        # Construct the DSN string from config
        #dsn = self.construct_dsn(self.config)

        # Initialize the ConnectionPool with the DSN and pool settings
        # self.pool = ConnectionPool(dsn=dsn, **self.pool_settings)

        # Directly pass connection parameters and pool settings to ConnectionPool
        self.pool = ConnectionPool(conninfo=self.construct_conninfo(self.config), **self.pool_settings)

    @staticmethod
    def construct_conninfo(config):
        """Constructs a connection info string from the config dictionary, excluding pool settings."""
        # Filter out 'pool_settings' and any other non-connection parameters
        conn_params = {k: v for k, v in config.items() if k not in ['pool_settings'] and v is not None}
        # Construct and return the connection info string
        return " ".join([f"{k}={v}" for k, v in conn_params.items()])
    #@staticmethod
    #def construct_dsn(config):
    #    """Constructs a DSN string from the config dictionary, excluding pool settings."""
    #    dsn_parts = {k: v for k, v in config.items() if k not in ['pool_settings']}
    #    dsn = " ".join([f"{k}={v}" for k, v in dsn_parts.items()])
    #    return dsn

    def test_connection(self):
        """Tests a connection from the pool."""
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT 1;')
                    result = cur.fetchone()
                    print("Pool connection successful: ", result)
        except OperationalError as e:
            print(f"Connection failed: {e}")

    def disconnect(self):
        """Closes all connections in the pool."""
        if self.pool:
            self.pool.close()
            self.pool = None
            print("Pool has been closed.")

    def connect(self):
        # This method is implemented to satisfy the interface of the abstract base class.
        # The connection pool is initialized in the constructor, so no action is needed here.
        pass


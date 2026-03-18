from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import get_settings

def create_engine():
    """
    Creates and configures asynchronous database engines.

    This function initializes two separate database engines:
    1. Main Engine:
       - Used for read-write operations (INSERT, UPDATE, DELETE)
       - Configured with a larger connection pool for higher throughput
    2. Readonly Engine:
       - Used for read-only queries (SELECT)
       - Helps reduce load on the main connection pool

    Configuration:
        - database_url: Retrieved from application settings
        - pool_size: Number of persistent connections maintained
        - max_overflow: Additional connections allowed during peak load
        - pool_recycle: Time (in seconds) after which connections are refreshed
        - echo: Disabled SQL query logging for performance

    Returns:
        Tuple[AsyncEngine, AsyncEngine]:
            A tuple containing:
            - main_engine: Primary engine for read-write operations
            - readonly_engine: Secondary engine for read-only queries

    Why this matters:
        - Connection pooling improves performance significantly
        - Separating read and write workloads improves scalability
        - Prevents frequent connection creation overhead
    """
    
    settings = get_settings()
    
    #Main engine
    main_engine = create_async_engine(
        settings.database_url,
        pool_size = 10,
        max_overflow = 20,
        pool_recycle = 3600,
        echo = False,
    )
    
    #ReadOnly Engine
    readonly_engine = create_async_engine(
        settings.database_url,
        pool_size = 5,
        max_overflow = 10,
        pool_recycle = 3600,
    )
    
    return main_engine, readonly_engine
    
main_engine, readonly_engine = create_engine()
MainSession = async_sessionmaker(main_engine, class_=AsyncSession,expire_on_commit=False)
ReadonlySession = async_sessionmaker(readonly_engine,class_=AsyncSession,expire_on_commit=False)


async def get_db() -> AsyncSession:
    """
    Provides a database session for read-write operations.

    This function is designed to be used as a FastAPI dependency
    for endpoints that modify database state.

    Behavior:
        - Opens a new asynchronous session
        - Yields the session to the endpoint
        - Commits the transaction if the request succeeds
        - Rolls back the transaction if an exception occurs
        - Ensures the connection is returned to the pool

    Yields:
        AsyncSession: An active database session

    Error Handling:
        - On exception: rolls back all uncommitted changes
        - Re-raises the exception for upstream handling

    Why this matters:
        - Guarantees data consistency
        - Prevents partial writes
        - Ensures proper resource cleanup
    """
   
    async with MainSession() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise


async def get_readonly_db() -> AsyncSession:
    """
    Provides a read-only database session.

    This function is intended for endpoints that only perform
    SELECT queries and do not modify database state.

    Behavior:
        - Opens a session using the readonly engine
        - Yields the session to the endpoint
        - Does not perform commit or rollback operations

    Yields:
        AsyncSession: An active read-only database session

    Why this matters:
        - Separates read and write workloads
        - Reduces load on the main database connection pool
        - Improves scalability for read-heavy applications
    """
    
    async with ReadonlySession() as session:
        yield session
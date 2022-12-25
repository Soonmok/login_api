from alembic import context

from app.db.models.user import Base

target_metadata = Base.metadata


def run_migrations_online():
    from app.db.session import engine

    connectable = engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()

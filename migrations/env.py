import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- مسیر ریشه پروژه را به sys.path اضافه کن ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import src.models  # noqa: F401  (برای ثبت مدل‌ها روی Base)

# --- ایمپورت Base و مدل‌ها ---
from src.db import Base

# این شیء کانفیگ، همان alembic.ini است
config = context.config

# اگر خواستی، می‌توانی به‌جای alembic.ini از settings استفاده کنی:
# از حالت پیش‌فرض استفاده می‌کنیم، ولی اگر بخواهی این 3 خط را آن‌کامنت کن:
from src.settings import database_url

# Always prefer the environment-driven URL (e.g., host "db" in Docker Compose)
config.set_main_option("sqlalchemy.url", database_url())

# لاگ‌گیری استاندارد
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# متادیتا برای autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """اجرای migration در حالت آفلاین (فقط تولید SQL)"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # تغییر نوع ستون‌ها را هم تشخیص بده
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """اجرای migration در حالت آنلاین با اتصال واقعی"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

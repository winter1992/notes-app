import psycopg2
from sqlalchemy import create_engine, text
import urllib.parse


def test_connections():
    # Варианты строк подключения для тестирования
    test_urls = [
        'postgresql://notes_user:strong_app_password_123@localhost:5433/notes_app',
        'postgresql://postgres:ТВОЙ_НОВЫЙ_ПАРОЛЬ@localhost:5433/postgres',
    ]

    for i, url in enumerate(test_urls):
        print(f"\n--- Тест {i + 1} ---")
        print(f"URL: {url}")

        try:
            # Пробуем через SQLAlchemy
            engine = create_engine(url)
            with engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                print(f"✅ SQLAlchemy: Успех - {result.scalar()}")
        except Exception as e:
            print(f"❌ SQLAlchemy: Ошибка - {e}")

        try:
            # Пробуем через psycopg2 напрямую
            conn = psycopg2.connect(url)
            cur = conn.cursor()
            cur.execute("SELECT version()")
            print(f"✅ psycopg2: Успех - {cur.fetchone()[0]}")
            conn.close()
        except Exception as e:
            print(f"❌ psycopg2: Ошибка - {e}")


if __name__ == "__main__":
    test_connections()
import logging
from tortoise import Tortoise, run_async
from src.config.settings import DB_CONFIG
from src.services.parsers import parse_and_match


channel_url = "https://t.me/s/sbbytoday"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def init_db():
    """Инициализация подключения к базе данных."""
    try:
        await Tortoise.init(config=DB_CONFIG)
        logger.info("Подключение к базе данных установлено успешно.")
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        raise

async def test_connection():
    try:
        await Tortoise.init(config=DB_CONFIG)
        
        # Используем raw запрос для извлечения данных из таблицы searchword
        result = await Tortoise.get_connection("default").execute_query('SELECT word, lemma FROM searchword')

        if result:
            # Преобразуем записи в строковый формат для вывода
            formatted_result = [f"word: {record['word']}, lemma: {record['lemma']}" for record in result]
            print(f"Данные из таблицы searchword:\n{formatted_result}")
        else:
            print("Таблица searchword пуста")
    except Exception as e:
        print(f"Ошибка при подключении или выполнении запроса: {e}")
    finally:
        await Tortoise.close_connections()
 

async def main():
    """Главная асинхронная функция."""
    await init_db()
    await parse_and_match(channel_url)

if __name__ == "__main__":
    run_async(main())  # Запуск main функции

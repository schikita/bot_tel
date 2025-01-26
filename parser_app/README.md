 Полное руководство по uv для начинающих

Как пользоваться uv: подробная инструкция
=========================================

1\. Установка пакетов
---------------------

### Базовые команды:

    # Установить пакет в основную группу
    uv add requests
    
    # Установить пакет с конкретной версией
    uv add "requests==2.31.0"
    
    # Установить пакет с условием версии
    uv add "requests>=2.30,<3.0"
    
    # Установить пакет в группу dev
    uv add --group dev ruff

🐍 Виртуальные окружения

    uv venv                 # Создать .venv
    source .venv/bin/activate  # Активация (Linux/macOS)
    .\.venv\Scripts\activate   # Активация (Windows)

2\. Управление группами зависимостей
------------------------------------

### Пример pyproject.toml:

    [project]
    name = "my_project"
    version = "0.1.0"
    
    [project.optional-dependencies]
    dev = ["ruff", "black"]
    test = ["pytest", "coverage"]
    docs = ["mkdocs", "sphinx"]

### Команды для работы с группами:

    # Установить только основные зависимости
    uv sync
    
    # Установить зависимости группы dev
    uv sync --group dev
    
    # Установить несколько групп
    uv sync --group dev,test
    
    # Установить ВСЕ группы
    uv sync --all-groups
    
    # Добавить пакет сразу в несколько групп
    uv add --group dev,test pytest

3\. Удаление пакетов
--------------------

    # Удалить пакет из основной группы
    uv remove requests
    
    # Удалить пакет из конкретной группы
    uv remove --group dev ruff
    
    # Удалить пакет из нескольких групп
    uv remove --group dev,test pytest

4\. Работа с версиями Python
----------------------------

    # Показать доступные версии Python
    uv python list
    
    # Установить конкретную версию Python
    uv python install 3.11
    
    # Создать виртуальное окружение с указанной версией
    uv venv --python 3.11

5\. Полезные команды
--------------------

    # Показать дерево зависимостей
    uv tree
    
    # Обновить все пакеты
    uv sync --upgrade
    
    # Обновить конкретный пакет
    uv sync --upgrade requests
    
    # Экспорт зависимостей в requirements.txt
    uv export --format requirements.txt > requirements.txt
    
    # Показать информацию о пакете
    uv pip show requests
    
    # Создать lock-файл
    uv lock

6\. Примеры рабочих процессов
-----------------------------

### Создание нового проекта:

    uv init
    uv add fastapi
    uv add --group dev ruff pytest
    uv sync --all-groups

### Добавление тестовых зависимостей:

    uv add --group test "pytest>=7.0" pytest-cov
    uv sync --group test

### Полное обновление проекта:

    uv sync --upgrade --all-groups
    uv lock

7\. Важные особенности
----------------------

*   Группы зависимостей хранятся в `pyproject.toml` в секции `[project.optional-dependencies]`
*   Для установки нескольких групп используйте запятую: `--group dev,test`
*   Версии можно указывать в разных форматах:
    *   `"package==1.2.3"` - точная версия
    *   `"package>=1.2"` - минимальная версия
    *   `"package~=1.2.3"` - совместимая версия

8\. Ruff Команда: `ruff check . --fix --select ALL`
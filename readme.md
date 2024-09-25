# Проект обучающей платформы
### Проект выполнен на платформе Django-DRF

Для запуска через Docker:
- корректно заполните файл _.env_ согласно шаблону из _.env.sample_;
- выполните команду`docker-compose up -d --build`.


Для запуска непосредственно через среду разработки:
- корректно заполните файл _.env_ согласно шаблону из _.env.sample_;
- установите и запустите _Redis_;
- установите _PostgreSQL_ и создайте БД с именем из файла _.env_;
- через _poetry_ из файла _pyproject.toml_ установите все зависимости;
- выполните миграции 'python manage.py migrate;
- через команду `python manage.py runserver` запустите приложение;
- через команду `celery -A config worker -l INFO` (Для Windows `celery -A config worker -l INFO -P eventlet`) запустите Celery;
- через команду `celery -A config beat -l INFO` запустите Celery-Beat.
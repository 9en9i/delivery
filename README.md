Инструкция по запуску сервиса
=============================
1. Склонировать репозиторий
2. Выполнить команду `docker compose up -d postgres s3`
3. Зайти по адресу `http://localhost:9001`, ввести логин и пароль `minioadmin`
4. На вкладке `Access Keys` создать новый ключ, скопировать его и вставить в файл `compose.yml` в блоке `x-app-env` в значения `DELIVERY__MINIO_ACCESS_KEY` и `DELIVERY__MINIO_SECRET_KEY` соответственно
5. На вкладке `Buckets` создать новый бакет с именем `images`. Далее необходимо зайти в него и установить `Access Policy` в значение `public`
6. Запустить сервис `upload_static` командой `docker compose up upload_static` и дождаться успешного выполнения
7. Выполнить команду `docker compose up migrate`, дождаться выполнения миграций
8. Выполнить команду `docker compose up -d backend` для запуска бэкенда

По завершению всех шагов запуска бэкенд будет доступен по адресу `http://localhost:8000`, документация в swagger по адресу `http://localhost:8000/docs`
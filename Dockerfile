# Використовуємо офіційний базовий образ Python
FROM python:3.11

# Встановлюємо залежності
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копіюємо весь проект в контейнер
COPY . .

# Змінюємо права доступу до wait-for-it.sh
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x wait-for-it.sh

# Запускаємо команду для міграцій бази даних та стартового сервера
CMD ./wait-for-it.sh db:5432 -t 60 -- python pastyshop/manage.py runserver 0.0.0.0:8000

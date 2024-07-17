# Используем официальный образ Python 3.8
FROM python:3.8

# Устанавливаем зависимости
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Копируем наше приложение в контейнер
COPY . /

# Запускаем приложение Flask
CMD ["python", "app.py"]
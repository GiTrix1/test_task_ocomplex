from flask import Flask, render_template, request, jsonify, session
import requests

app = Flask(__name__, template_folder='.')
app.secret_key = 'SuperKey123'  # Секретный ключ для сессий, использую для хранения истории поиска

# Список для хранения истории поиска
search_history = []


# Функция для получения температуры
def get_weather():
    # Тут нужно делать через БД, чтобы тянуть координаты. В реальном приложении так и сделал бы.
    # Делаю без БД для экономии времени, так как я ценю свое и чужое время.
    # Вот краткое описание Создание таблицы для истории поиска БД на sqlite3:
    # Создаем функция create_db() -> делаем конект -> cursor() -> execute(CREATE TABLE ...) -> commit() -> close
    api_url = 'https://api.open-meteo.com/v1/forecast?latitude=40.7143&longitude=-74.006&hourly=temperature_2m&timezone=GMT&forecast_days=1'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['hourly']['temperature_2m']
        return temperature
    else:
        return None


# Главная страница
@app.route('/')
def index():
    return render_template('templates/index.html')


# API для автодополнения городов
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term')
    # В реальном приложении я добавил бы реализацию автодополнения через БД или внешний сервис
    # В данном примере просто возвращаю статический список
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
              'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    suggestions = [city for city in cities if term.lower() in city.lower()]
    return jsonify(suggestions)


# Страница с результатами поиска погоды
@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
        weather_forecast = get_weather()
        if weather_forecast:
            # Сохраняем запрос в историю только если город найден
            if 'history' not in session:
                session['history'] = []
            session['history'].append(city)
            search_history.append(city)
            return render_template('templates/weather.html', city=city,
                                   weather_forecast=weather_forecast)
        else:
            return render_template('templates/weather.html', city=city,
                                   error='Город не найден')
    return render_template('templates/weather.html')


# API для подсчета количества запросов по каждому городу
@app.route('/search_count', methods=['GET'])
def search_count():
    counts = {}
    for city in search_history:
        counts[city] = counts.get(city, 0) + 1
    return jsonify(counts)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

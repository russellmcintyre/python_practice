from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

def scrape_tikleap(username):
    url = f"https://www.tikleap.com/profile/{username}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Could not fetch data for {username}"}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    for row in soup.select('table tbody tr'):
        cells = row.find_all('td')
        if len(cells) >= 2:
            date = cells[0].text.strip()
            earnings = float(cells[1].text.strip().replace('$', ''))
            data.append({'date': date, 'earnings': earnings})
    return data

@app.route('/analyze', methods=['POST'])
def analyze():
    username = request.json.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    data = scrape_tikleap(username)
    if 'error' in data:
        return jsonify(data), 400

    weekdays = {i: 0 for i in range(7)}
    for item in data:
        date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
        weekdays[date_obj.weekday()] += item['earnings']
    
    return jsonify({
        'username': username,
        'calendar': data,
        'weekday_analysis': weekdays,
        'weekly_total': round(sum(item['earnings'] for item in data[-7:]), 2),
        'monthly_total': round(sum(item['earnings'] for item in data), 2),
    })

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request

app = Flask(__name__)

@app.route('/location', methods=['POST'])
def receive_location():
    data = request.json
    lat = data.get('latitude')
    lon = data.get('longitude')
    print(f"Received GPS Location:\nLatitude: {lat}\nLongitude: {lon}")
    return "Location received successfully"

if __name__ == '_main_':
    app.run(host='10.1.29.143', port=5000)

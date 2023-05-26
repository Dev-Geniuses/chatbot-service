from flask import Flask, request, jsonify;
from flask_cors import cross_origin

app = Flask(__name__)


@app.route('/chat_bot', methods = ['POST'])
@cross_origin()
def chat():
    if request.method == 'POST':
        message_send = request.get_json()
        return jsonify({'message': message_send['message']})

if __name__ == "__main__":

    app.run(debug=True)
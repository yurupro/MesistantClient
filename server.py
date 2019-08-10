from flask import Flask, request, jsonify
import ConfigParser

app = Flask(__name__)
config = ConfigParser.ConfigParser()
config.read('settings.ini')
if config.has_section('authentication') == False:
    print('Error:authentication is not defined!')
    exit(1)

@app.route('/webhook', methods=['POST'])
def webhook():
    json = request.get_json()
    if json['auth'] == config.get('authentication', 'password'):
        # レシピの読み込み
        return jsonify({"Status: OK"})
    else:
        return jsonify({"Status": "ERR", "Error": "Authentication was failed."})

if __name__ == '__main__':
    app.run(debug=True)

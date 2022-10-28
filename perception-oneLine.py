# export FLASK_APP=myapp.py
# flask run
# Running on http://127.0.0.1:5000/

# turn on CORS to handle the popup.js request
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/titles', methods=['POST', 'GET'])
@cross_origin()
def get_titles():
    #print python version
    #receive array of titles from popup.js
    titles = request.get_json()
    #dictionary to list of titles
    titles = titles['titles']
    
    for title in titles:
        print(title)
    return jsonify(titles)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
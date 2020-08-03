'''imports necessary for use'''
import os
from random import randint
from flask import Flask, make_response, request


app = Flask(__name__, static_url_path="", static_folder="static")

@app.route('/', methods=['GET'])
def index():
    '''Route to redirect to the main page'''
    res = make_response(app.send_static_file('index.html'))
    return res

@app.route('/perdeu', methods=['POST'])
def perdeu():
    '''Scheduled route to receive the post in the form of perdeu.html'''
#Lines 18 to 23, reset by creating a new random value.
    random_number = (randint(1, 100))
    random_number = str(random_number)
    res = make_response(app.send_static_file('gamerandom.html'))
    res.set_cookie('randint_cookie', random_number)
    res.set_cookie('attempt_cookie', '1')
    return res

@app.route('/adivinhar', methods=['POST'])
def adivinhar():
    '''Scheduled route to receive the post in the form of adivinhar.html'''
#On lines 29 to 33, it is checked if it is true.
    input_number = int(request.form.get('number'))
    if request.cookies.get('randint_cookie') or request.cookies.get('attempt_cookie'):
        random_number = request.cookies.get('randint_cookie')
        random_number = int(random_number)
        attempt = request.cookies.get('attempt_cookie')
        attempt = int(attempt)
#On lines 36 to 42, it will be read if the check is false.
    else:
        attempt = None
        random_number = (randint(1, 100))
        random_number = str(random_number)
        res = make_response(app.send_static_file('gamecookie.html'))
        res.set_cookie('randint_cookie', random_number)
        res.set_cookie('attempt_cookie', '1')
        return res
#On lines 45 to 56, they are the conditionals.
    if attempt == 10:
        page_to_return = 'perdeu.html'
        attempt_to_set = '1'
    if input_number == random_number:
        page_to_return = 'ganhou.html'
        attempt_to_set = '1'
    if input_number > random_number and attempt < 10:
        page_to_return = 'maior.html'
        attempt_to_set = str(attempt + 1)
    if input_number < random_number and attempt < 10:
        page_to_return = 'menor.html'
        attempt_to_set = str(attempt + 1)
#On lines 58 to 60, receive the conditional variables.
    res = make_response(app.send_static_file(page_to_return))
    res.set_cookie('attempt_cookie', attempt_to_set)
    return res
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("VCAP_APP_PORT", 5000)), use_reloader=False)

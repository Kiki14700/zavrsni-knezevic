from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_caching import Cache
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, Email, Regexp
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import requests
import os

# Konfiguracija aplikacije(app.py)
app = Flask(__name__)
# Konfiguracija Bootstrap-a u app.py
bootstrap = Bootstrap(app)
# Bootstrap tema, preuzeto s 'Bootswatch theme'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'united'          
# Flask WTF ekstenzija za zaštitu formi
app.config['SECRET_KEY']='LongAndRandomSecretKey'
# Koristi se za spremanje podataka (Weather API) na određeno vrijeme da nebi prešli dozvoljeni broj pregleda u vremenu
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
# Povezivanje s SQLite bazom podataka
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'baza_korisnici.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Konfiguracija baze podataka u app.py
db = SQLAlchemy(app)
# Mogućnost za 'upgrade' i 'downgrade' potrebnih verzija baze podataka
migrate = Migrate(app, db)
# Konfiguriracija aplikacije da koristi flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return Korisnici.query.get(int(user_id))


# Klasa za inicijalizaciju Login forme i njezinih komponenti
# Validatori stvaraju različita ograničenja koja želimo da naša forma ima (DataRequired - zahtjeva obavezan unos u naznačena polja)
class LoginForm(FlaskForm):
    username = StringField(label=('E-MAIL:'), validators=[DataRequired()])
    submit = SubmitField(label=('POTVRDI'))
    password = PasswordField(label=('LOZINKA:'), validators=[DataRequired()])



# Klasa za inicijalizaciju Sign up forme 
class GreetUserForm(FlaskForm):
    username = StringField(label=('IME:'), validators=[DataRequired()])
    surname = StringField(label=('PREZIME:'), validators=[DataRequired()])
    email = StringField(label=('E-MAIL:'), validators=[DataRequired(), Email(message="Potrebno je unijeti e-mail")])
    password = PasswordField(label=('LOZINKA:'), validators=[DataRequired(), Length(min=9, message="Više od 8 znakova!") ,
     Regexp(regex="\d.*[A-Z]|[A-Z].*\d", message="Minimalno jedno veliko slovo i jedan broj")])
    submit = SubmitField(label=('POTVRDI'))
    
    


# Klasa za inicijalizaciju tablice u bazi, njezinih atributa i vrste podatka koji prima svaki atribut
# Postavljen je i setter za lozinku s kojim postavljamo lozinku(hash lozinku)
# Funkcija verify_password služi za usporedbu unesene lozinke i one koja je u bazi(u bazi je hash lozinka)
class Korisnici(UserMixin, db.Model):
    __tablename__ = 'korisnik'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Korisnici %r>' % self.name

# Klasa za inicijalizaciju tablice u bazi, njezinih atributa i vrste podatka koji prima svaki atribut
class Cijena(UserMixin, db.Model):
    __tablename__ = 'cjenovnik'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    amount = db.Column(db.Integer)
    measure = db.Column(db.String)
    price = db.Column(db.Integer)
    def __repr__(self):
        return '<Cijena %r>' % self.name


# Ruta do početne stranice 
@app.route('/index')
def index():
    return render_template('index.html')

# Ruta od stranice Proizvodi
@app.route('/proizvodi')
def proizvodi():
    return render_template('proizvodi.html')

# Ruta do stranice Cjenik
@app.route('/cjenik')
def cjenik():
    products = Cijena.query.all()
    return render_template('cjenik.html', products = products)

# Ruta do stranice za prijavu
# Funkcija login omogućuje prijavu na stranicu tako što komunicira sa bazom i uspoređuje unesene podatke s onima u bazi
@app.route('/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Korisnici.query.filter_by(email=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                return redirect(url_for("index"))
        flash('NEPOZNATO KORISNIČKO IME ILI LOZINKA!', category='warning')
    return render_template("login.html", form = form)

# Ruta do stranice za registraciju
# Funkcija singup unosi podatke za registraciju u bazu, ukoliko postoji osoba s već korištenim e-mail-om dat će napomenu da se radi o već korištenim podatcima,
# ako su svi podatci zadovoljavajući prebacujemo se na stranicu za prijavu
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    form = GreetUserForm()
    password = form.password.data
    if form.validate_on_submit():
        last_name = session.get('email')
        user = Korisnici.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Korisnici(name = form.username.data, surname = form.surname.data, email = form.email.data, password = form.password.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = True
            flash('USPJEŠNO STE SE REGISTRIRALI!')
            return redirect(url_for('login'))
        else:
            session['known'] = False
            flash("KORISNIK S UNESENIM E-MAILOM VEĆ POSTOJI!")
    return render_template('signup.html', form = form, name = session.get('username'), known = session.get('known', False))

# Ruta do stranice Tečaj 
# Koristi se Weather API čiji se parametri proslijeđuju na html stranicu gdje se koriste i rapoređuju
@app.route('/dodatno')
@cache.cached(timeout=60)
def dodatno():
    now = datetime.now()
    url = 'http://api.openweathermap.org/data/2.5/weather'
    parameters = {'q': 'Rovanjska', 'appid': '464b8e606097703f41f58b71f890ed3f','lang': 'hr', 'units': 'metric'}
    response = requests.get(url, parameters)
    weather = response.json()
    return render_template('dodatno.html', weather = weather, datetime = datetime, now = now)

# Filter koji se koristi za prikaz vremena
# Kod na ovaj način dobiva na organizacija jer se složeni dijelovi rastavljaju na manje dijelove 
@app.template_filter('datetime')
def fomat_datetime(value, format = '%d.%m.%Y %H:%M'):
    return datetime.fromtimestamp (value).strftime(format) 

# Error stranica koja se prikaže svaki put kad traženi sadržaj nije dostupan
# Stranica nudi mogućnost povratka na stranicu za prijavu
@app.errorhandler(404)
def invalid_route(e):
    return render_template('button.html')







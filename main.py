#!/usr/bin/env python3

from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, Markup
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder='node_modules', static_url_path='/static')
app.config['SECRET_KEY'] = 'debug'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.Date, default=datetime.today())


@app.route('/<int:id>')
def redir(id):
    q = Link.query.get(id)
    if q is None:
        flash('Nie odnaleziono takiego URL.')
        return redirect(url_for('index'))

    return redirect(q.long_url)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # sprawdź czy link jeszcze nie istnieje
        # jeśli istnieje to zwróć istniejący
        q = Link.query.filter_by(long_url=request.form.get('link')).first()
        if q is not None:
            url = f'{request.host}/{q.id}'
            flash(Markup(f'Twój krótki link to: <a target="_blank" href="{q.long_url}">{url}</a>'))
            return redirect(url_for('index'))

        # jeśli nie istnieje to wygeneruj i zapisz
        link = Link(long_url=request.form.get('link'))
        db.session.add(link)
        db.session.commit()
        url = f'{request.host}/{link.id}'
        flash(Markup(f'Twój krótki link to: <a target="_blank" href="{link.long_url}">{url}</a>'))
        return redirect(url_for('index'))

    return render_template('index.html')


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

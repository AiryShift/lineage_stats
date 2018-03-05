import json
import os
from datetime import datetime
from flask import Flask, render_template, request
from time import time

import config
import db

app = Flask(__name__)

@app.route('/')
def root():
    models = db.get_field(db.to_col('model'))
    countries = db.get_field(db.to_col('country'))
    total = sum([models[k] for k in models])

    return render_template('index.html', stats={'model': models, 'country': countries,
        'total': total}, columns=['model', 'country'], date=datetime.utcnow().strftime('%Y-%m-%d %H:%M (UTC)'))

@app.route('/<field>/<value>')
def field(field, value):
    if not db.has_col(field):
        return 'unknown field'
    values = {'model': ['version', 'country'], 'carrier': ['model', 'country'], 'version': ['model', 'country'], 'country': ['model', 'carrier']}[field]
    field = db.to_col(field)
    left = db.get_field_from(db.to_col(values[0]), field, value)
    right = db.get_field_from(db.to_col(values[1]), field, value)
    total = sum(left[k] for k in left)

    return render_template('index.html', stats={values[0]: left, values[1]: right,
        'total': total}, columns=values, date=datetime.utcnow().strftime('%Y-%m-%d %H:%M (UTC)'))

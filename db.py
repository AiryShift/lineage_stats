import psycopg2
from config import *

from time import time
from datetime import datetime, timedelta

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)


FIELD_MAP = {
        'device_id': 'd',
        'model': 'm',
        'version': 'v',
        'country': 'u',
        'carrier': 'c',
        'carrier_id': 'r',
        'submit_time': 't',
}

REVERSE_FIELDS = {v:k for k, v in FIELD_MAP.items()}

to_col = lambda a: FIELD_MAP[a]
has_col = lambda a: a in FIELD_MAP
from_col = lambda a: REVERSE_FIELDS[a]

def setup():
    global conn
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS stats (d text, m text, v text, u text, c text, r text, t timestamp)");
    cur.execute("CREATE INDEX IF NOT EXISTS model_index ON stats (m)")
    cur.execute("CREATE INDEX IF NOT EXISTS country_index ON stats (u)")
    cur.execute("CREATE INDEX IF NOT EXISTS ts_index ON stats (t)")
    cur.execute("CREATE INDEX IF NOT EXISTS device_id_index ON stats (d)")
    conn.commit()

def save_stat(did, model, version, country, carrier, cid):
    ts = datetime.now()
    cur = conn.cursor()
    cur.execute("INSERT INTO stats (d, m, v, u, c, r, t) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (did, model, version, country, carrier, cid, ts))
    conn.commit()


def get_field(f):
    if f not in REVERSE_FIELDS:
        return []
    cur = conn.cursor()
    cur.execute("SELECT {f}, COUNT(DISTINCT d) FROM stats WHERE t > now() - interval '90 days' GROUP BY {f} ORDER BY COUNT(DISTINCT d) desc".format(f=f))
    return {i[0]:i[1] for i in cur}

def get_field_from(f, filterf, filterv):
    if f not in REVERSE_FIELDS or filterf not in REVERSE_FIELDS:
        return []
    cur = conn.cursor()
    cur.execute("SELECT {f}, COUNT(DISTINCT d) FROM stats WHERE {ff}=%s and t > now() - interval '90 days' GROUP BY {f} ORDER BY COUNT(DISTINCT d) desc".format(f=f, ff=filterf),
            (filterv, ))
    return {i[0]:i[1] for i in cur}

setup()

To set up:

0. Install postgres

1.

```
$ createuser stats
$ createdb stats
```

2.

```
$ psql stats
stats=# \password stats
...
stats=# grant all on database stats to stats;
GRANT
stats=# \q
```

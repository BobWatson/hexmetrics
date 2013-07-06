HEX Metrics
===========

A website I put together to learn python, and to scratch a bit of an itch with regards to math tools for cards games.

Contacting Me
--------

You can get in touch with me either at bob@nearimpossible.com, on twitter as @HEXMetrics or @B0bW, or on GitHub at https://github.com/BobWatson.

Using
-----

To get started: 

1.  Copy config.default.py to config.py, edit that file and fill in all your pertinant details.
2.  Run 'python db_create.py'
3.  Run 'python db_migrate.py'
4.  Run 'build_card_db.py'

You should then be able to launch with a basic harness in the root, something like:
```python
from hex.main import app as application
application.run()
```

I run this with passenger_wsgi on DreamHost at the main http://hexmetrics.ni.tl/ page.

License
-------
<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_GB"><img alt="Creative Commons Licence" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_GB">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.
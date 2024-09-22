"""
src/common/threads.py

Functions related to threading.

Routine Listings
----------------
run_in_thread : method
    Alias of the built in method `threading.Thread`.

Examples
--------
>>> from common import config, threads, tray_icon
>>> config_object = config.create_config(config_file='config.ini')
>>> tray_icon.icon = tray_icon.tray_initialize()
>>> threads.run_in_thread(target=tray_icon.tray_run, name='pystray', daemon=True).start()

>>> from common import config, threads, webapp
>>> config_object = config.create_config(config_file='config.ini')
>>> threads.run_in_thread(target=webapp.start_webapp, name='Flask', daemon=True).start()
 * Serving Flask app 'common.webapp' (lazy loading)
...
 * Running on http://.../ (Press CTRL+C to quit)
"""
# standard imports
import threading

# just use standard threading.Thread for now
# todo
# this can probably be improved
# ideally would like to have basic functions and just pass in the target and args
run_in_thread = threading.Thread

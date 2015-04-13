# webapp2 configuration
debug=True

# API configuration.
keyid='1234567'
vcode='some-really-long-verification-code'

# Docs link.
doc_url='http://example.com/your-docs'

# Evelink configuration.
get_evelink_cache=None
# Here's an alternative.
#def get_evelink_cache():
#    from evelink.cache.sqlite import SqliteCache
#    return SqliteCache('/tmp/contract-watcher-cache.db')

# WSGI configuration. Optional; only needed if you're planning on running
# standalone.
host='127.0.0.1'
port='8091'

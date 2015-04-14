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

# Auth configuration
require_login=True

# The below auth configuration is only required if require_login is True.
braveapi_endpoint='http://core.example.com/api'
braveapi_my_privkey='................................................................'
braveapi_my_pubkey='................................................................................................................................'
braveapi_my_id='........................'
braveapi_server_pubkey='................................................................................................................................'

braveapi_perm_view='yourapp.view'

session_secret_key='................................'

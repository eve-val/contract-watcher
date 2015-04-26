# webapp2 configuration
debug=True

# API configuration.
keyid='1234567'
vcode='some-really-long-verification-code'

# Service configuration
corp_id = 12345670
sla_days = 7

# Ideally this would come from the CCP database dump, but thpppbbbtttt.
# Constructed manually instead.
supported_locs = {
    60008494: "Amarr VIII",
    60011824: "Orvolle I",
}
other_locs = {
    60011731: "Orvolle VI-1",
    60012067: "Murethand VIII-2",
    60009808: "Mesybier VII",
    60011728: "Adacyne III-14",
    60006511: "Mendori IX - Moon 9 - Imperial Armaments Factory",
    60003760: "Jita IV-4",
    60011725: "Adacyne IV-14",
}

# Docs link.
doc_url='http://example.com/your-docs'
calc_url='http://example.com/calc.html'

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

# This is used for encrypting sessions, so you need to generate a random string here
# and then protect it.
session_secret_key='................................'

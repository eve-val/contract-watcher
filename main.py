#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import webapp2_extras.auth
import webapp2_extras.sessions
import evelink
import datetime
import jinja2
import os
import os.path
import sys
import config
from config import keyid, vcode #put your desired api keys in a file named config.py

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), 
    extensions=['jinja2.ext.autoescape'])

# Ideally this would come from the corporation sheet, but we'd need a key with
# that bit set.
KNEES_ID = 98237970
SLA_DAYS = 7

# Ideally this would come from the CCP database dump, but thpppbbbtttt.
# Constructed manually instead.
supported_locs = {
    60008494: "Amarr VIII",
    60003616: "Dabrid V",
    61000744: "4-07MU V",
    60013957: "Parses",
    60014940: "UHKL-N",
}
other_locs = {
    60011824: "Orvolle I",
    60011731: "Orvolle VI-1",
    60012067: "Murethand VIII-2",
    60009808: "Mesybier VII",
    60013477: "VLGD-R III-2",
    60014575: "Chardalane V",
    60011728: "Adacyne III-14",
    60006511: "Mendori IX - Moon 9 - Imperial Armaments Factory",
    61000223: "KW-I6T VI",
    60003760: "Jita IV-4",
    60011725: "Adacyne IV-14",
    60009940: "LSC4-P I",
    60006262: "Rayl VIII-7",
    61000682: "EX6-AO VII",
}

def location_display_from_id(loc_id):
    """Get the display name for the location."""
    if loc_id in supported_locs:
        return supported_locs[loc_id]
    if loc_id in other_locs:
        return other_locs[loc_id] + "?!!"
    return "[%s]" % loc_id

def location_display_from_comment(comment):
    if "LSC" in comment: return "LSC4-P I"
    if "VLG" in comment: return "VLGD-R III-2"
    return "???"

def timedelta_display(delta):
    # timedeltas are normalized like:
    # 0 <= microseconds < 1000000
    # 0 <= seconds < 3600*24 (the number of seconds in one day)
    # -999999999 <= days <= 999999999
    if delta < datetime.timedelta(0):
        minus_maybe = "-"
        days = abs(delta.days + 1)
        seconds = 60 * 60 * 24 - delta.seconds
    else:
        minus_maybe = ""
        days = delta.days
        seconds = delta.seconds
    return "%s%dd %dh" % (minus_maybe, days, seconds / (60 * 60))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if config.require_login:
            auth = get_auth(self.request)
            user = auth.get_user_by_session()
            if user is None:
                return self.redirect('/login')
            if config.braveapi_perm_view not in user['perms']:
                self.response.write("permission denied :(")
                return

        cache = config.get_evelink_cache() if config.get_evelink_cache else None
        api = evelink.api.API(api_key = (keyid,vcode), cache=cache)
        knees = evelink.corp.Corp(api)
        eve = evelink.eve.EVE(api)
        contracts = knees.contracts()

        pending = []
        total_volume = 0.0
        for contract in contracts.result.itervalues():
            if (contract['assignee'] == KNEES_ID and
                contract['status'] in ('Outstanding', 'InProgress') and
                'opsec' not in contract['title'].lower()) :
                cn = {}

                # Basic info
                cn['type'] = contract['type']
                cn['status'] = contract['status']
                cn['issuer'] = eve.character_name_from_id(contract['issuer']).result
                date = datetime.datetime.fromtimestamp(contract['issued'])
                cn['dateissued'] = date.strftime("%Y-%m-%d %H:%M")
                cn['volume'] = "{:,.3f}".format(contract['volume'])
                total_volume += contract['volume']

                # Source and destination
                cn['from'] = location_display_from_id(contract['start'])
                if contract['type'] == 'Courier':
                    cn['to'] = location_display_from_id(contract['end'])
                else:
                    cn['to'] = location_display_from_comment(contract['title'])

                # Accepter
                if contract['accepted']:
                    cn['accepted'] = eve.character_name_from_id(contract['acceptor']).result
                else:
                    cn['accepted'] = ""

                # Time remaining
                maxdays = datetime.timedelta(days=SLA_DAYS)
                delta = date + maxdays - datetime.datetime.today()
                cn['timedelta_remaining'] = delta
                cn['remaining'] = timedelta_display(delta)
                if delta < datetime.timedelta(hours=12):
                    cn['class'] = 'text-error'
                elif delta < datetime.timedelta(days=1):
                    cn['class'] = 'text-warning'
                else:
                    cn['class'] = 'text-info'

                pending.append(cn)

        pending = sorted(pending, key=lambda contract: contract['timedelta_remaining'])

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'pending': pending,
                                             'doc_url': config.doc_url,
                                             'total_volume': "{:,.3f}".format(total_volume),
                                            }))

def get_auth(request):
    auth_store_config = {
        'user_model': 'auth.Character',
        'user_attributes': ['perms'],
    }
    auth_store = webapp2_extras.auth.AuthStore(app, config=auth_store_config)
    webapp2_extras.auth.set_store(auth_store)
    return webapp2_extras.auth.get_auth(request=request)

def get_brave_api():
    import braveapi.client
    from binascii import unhexlify
    from hashlib import sha256
    from ecdsa.keys import SigningKey, VerifyingKey
    from ecdsa.curves import NIST256p

    endpoint = config.braveapi_endpoint
    my_id = config.braveapi_my_id
    my_privkey = SigningKey.from_string(unhexlify(config.braveapi_my_privkey), curve=NIST256p, hashfunc=sha256)
    server_pubkey = VerifyingKey.from_string(unhexlify(config.braveapi_server_pubkey), curve=NIST256p, hashfunc=sha256)

    return braveapi.client.API(endpoint, my_id, my_privkey, server_pubkey)


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        auth = get_auth(self.request)
        user = auth.get_user_by_session()
        if user is not None:
            return webapp2.redirect("/")
        api = get_brave_api()
        success = self.request.host_url + '/loginok'
        failure = self.request.host_url + '/login'
        result = api.core.authorize(success=success, failure=failure)
        return webapp2.redirect(result.location)


class LoginResultHandler(webapp2.RequestHandler):
    def get(self):
        auth = get_auth(self.request)
        user = auth.get_user_by_session()
        if user is not None:
            return webapp2.redirect("/")
        token = self.request.GET['token']
        api = get_brave_api()
        info = api.core.info(token)
        session_info = {
            'user_id': info['character']['id'],
            'perms': info['perms'],
        }
        auth.set_session(session_info)
        session_store = webapp2_extras.sessions.get_store(request=self.request)
        session_store.save_sessions(self.response)
        return webapp2.redirect("/", response=self.response)


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        auth = get_auth(self.request)
        auth.unset_session()
        session_store = webapp2_extras.sessions.get_store(request=self.request)
        session_store.save_sessions(self.response)
        return webapp2.redirect("/", response=self.response)


class StaticHandler(webapp2.RequestHandler):
    """Try to have your frontend serve static assets instead of this. But, this
    is available for easy standalone operation."""
    def get_resource_path(self):
        """This is responsible for making sure that the requested resource
        refers to something inside the static directory."""
        path = self.request.path.lstrip('/')
        abspath = os.path.abspath(os.path.join('static', path))
        relpath = os.path.relpath(abspath, os.path.dirname(__file__))
        if not relpath.startswith('static/'):
            self.abort(404)
        return relpath

    def get(self):
        path = self.get_resource_path()
        # Let the browser guess the content type.
        self.response.content_type = None
        with open(path) as f:
            self.response.write(f.read())


app_config = {}
app_config['webapp2_extras.sessions'] = {
    'secret_key': config.session_secret_key,
}

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/loginok', LoginResultHandler),
    ('/logout', LogoutHandler),
    ('/css/.*', StaticHandler),
    ('/img/.*', StaticHandler),
    ('/js/.*', StaticHandler),
], debug=config.debug, config=app_config)


def main():
    from paste import httpserver
    httpserver.serve(app, host=config.host, port=config.port)

if __name__ == '__main__':
    main()

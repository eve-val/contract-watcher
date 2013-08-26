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
from evelink import corp, api, eve
import datetime
import jinja2
import os
from keys import keyid, vcode #put your desired api keys in a file named keys.py

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), 
    extensions=['jinja2.ext.autoescape'])

class MainHandler(webapp2.RequestHandler):
    def get(self):
        key = api.API(api_key = (keyid,vcode))
        knees = corp.Corp(key)
        contracts = knees.contracts()

        hprior = []
        medprior = []
        lprior = []
        for key in contracts:
            contract = contracts[key]
            if not contract['completed']:
                if not contract['status'] == 'Deleted':
                    cn = {}
                    thing = eve.EVE()
                    cn['issued'] = thing.character_names_from_ids([contract['issuer']])[contract['issuer']]
                    if contract['accepted']:
                        cn['accepted'] = thing.character_names_from_ids([contract['acceptor']])[contract['acceptor']]
                    else:
                        cn['accepted'] = "None"
                    cn['volume'] = contract['volume']
                    cn['date'] = datetime.datetime.fromtimestamp(contract['issued'])
                    if contract['reward'] >= 30000000:
                        maxdays = datetime.timedelta(days=2)
                        delta = cn['date'] + maxdays - datetime.datetime.today()
                        cn['remaining'] = str(delta.days) + 'd ' + str(delta.seconds/(60*60)) + 'h'
                        if delta.days < 1:
                            if delta.seconds/(60*60) < 12 or delta.days < 0:
                                cn['class'] = 'text-error'
                            else:
                                cn['class'] = 'text-warning'
                        else:
                            cn['class'] = 'text-info'
                        cn['dateissued'] = cn['date'].strftime("%d-%m-%y %H:%M")
                        hprior.append(cn)
                    elif contract['reward'] >= 15000000:
                        maxdays = datetime.timedelta(days=5)
                        delta = cn['date'] + maxdays - datetime.datetime.today()
                        cn['remaining'] = str(delta.days) + 'd ' + str(delta.seconds/(60*60)) + 'h'
                        if delta.days < 1:
                            if delta.seconds/(60*60) < 12 or delta.days < 0:
                                cn['class'] = 'text-error'
                            else:
                                cn['class'] = 'text-warning'
                        else:
                            cn['class'] = 'text-info'
                        cn['dateissued'] = cn['date'].strftime("%d-%m-%y %H:%M")
                        medprior.append(cn)
                    else:
                        cn['remaining'] = ''
                        cn['class'] = 'text-info'
                        cn['dateissued'] = cn['date'].strftime("%d-%m-%y %H:%M")
                        lprior.append(cn)

        hprior = sorted(hprior, key=lambda contract: contract['date'])
        medprior = sorted(medprior, key=lambda contract: contract['date'])
        lprior = sorted(lprior, key=lambda contract: contract['date'])

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'hpcontracts': hprior, 'medpcontracts':medprior, 'lowpcontracts':lprior,})) 
                    
        
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

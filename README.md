NOTE: this readme is a bit out of date. TODO(jboning)

This app provides a contract queue for an alliance JF service. The corp
API key used to pull has been stripped. To get your own, talk to Nolan
Inkura.

## Dependencies & Setup

This is an App Engine app. You can [download a development app
server](https://developers.google.com/appengine/downloads#Google_App_Eng
ine_SDK_for_Python) to run it locally.

contract-watcher needs [evelink](https://github.com/eve-val/evelink) to
interface with the EVE API:

    git clone https://github.com/eve-val/evelink.git evelink-repo
    ln -s evelink-repo/evelink

It also expects [Eve Shipping
Calc](https://github.com/kormat/eve-shipping-calc):

    git clone https://github.com/kormat/eve-shipping-calc.git calc

Configure calc/calc-config.js for your routes.

Now create your configuration file by copying config.example.py to
config.py and editing it as appropriate. For testing, you probably want
to set `require_login` to be `False`, but production versions shoul
have it.

Finally, you can launch the development version. The instructions for
this vary but can be found at the above App Engine link.

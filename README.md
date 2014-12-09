This app provides a contract queue for an alliance JF service. The corp API key used to pull has been stripped. To get your own, talk to Nolan Inkura.

## Dependencies & Setup

This is an App Engine app. You can [download a development app server](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python) to run it locally.

contract-watcher needs [evelink](https://github.com/eve-val/evelink) to interface with the EVE API:

    git clone https://github.com/eve-val/evelink.git evelink-repo
    ln -s evelink-repo/evelink

You'll need to fill in keys.py with your API key.

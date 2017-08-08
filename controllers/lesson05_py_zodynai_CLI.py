# -*- coding: utf-8 -*-
""""""

######## fake print ##########
from __future__ import print_function  # if print is function, we can override it
real_print = print   # save original function to different name

OUT = []  # global buffer , dirty hack

def print(*args, **kwargs):
    real_print( *args, **kwargs )  # call original
    OUT.append( ' '.join(map(str, args) ) )   # save to buffer

def flush_print(sep="\n"):
    """Flushes the OUT buffer and returns concatenated lines

    sep - newline separator"""

    global OUT
    result = sep.join( OUT )
    OUT = []
    return PRE(result, _style="color:black; border:none; background:none")

######## end fake print ##########



from plugin_introspect import tutor as original_tutor, menu
from tools import call_or_redirect
import urllib


# tutor = auth.requires_login(original_tutor)
def tutor (*args, **kwargs):
    if auth.is_logged_in():
        return original_tutor(*args, **kwargs)
    else:
        next = auth.here()
        session.flash = response.flash
        return call_or_redirect(auth.settings.on_failed_authentication,
                                auth.settings.login_url + '?_next=' + urllib.quote(next))


def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=menu())

########### tasks



@tutor(imitateCLI=True, flush_print=flush_print)
def zodynai():
    pass

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
def funkcijos():


    def pasveikink(vardas):
        print( "Hi, " + vardas )

    pasveikink( "Joe" )
    pasveikink( "Antanas" )


@tutor(imitateCLI=True, flush_print=flush_print)
def grazinama_reiksme():
    def add(a, b):
        result = a+b
        return result

    print( add( 4, 6 ) )
    print( add( 4, -6 ) )  ###PLACEHOLDER:--> print( add( 4, ? ) ) 
    print( add( "labas", " rytas" ) )


@tutor(imitateCLI=True, flush_print=flush_print)
def vykdymo_eiliskumas():
    def add(a, b):
        print( "vykdom add:", a, b )
        return a+b

    def maximum(x, y):
        print( "vykdom maximum:", x, y )

        if x > y:
            return x
        else:
            return y

    # kokia pirmiau bus vykdoma "maximum", nes
    # ją reikia suskaičiuot, kad žinotum "add" argumento reikšmę
    result = add(10, maximum( 2, 5 ) )
    print( "rezultatas:", result )


@tutor(imitateCLI=True, flush_print=flush_print)
def vykdymo_eiliskumas_test1():
    def add(a, b):
        print( "vykdom add:", a, b )  # atspausdinam argumentus
        return a+b   # apskaičiuojam ir grąžinam rezultatą

    def maximum(x, y):
        print( "vykdom maximum:", x, y )

        if x > y:
            return x
        else:
            return y

    ats = add( 7, maximum( 2, 5 ) ) ###PLACEHOLDER:--> ? = ?( 7, ?( 2, 5 ) )
    print( ats )



@tutor(imitateCLI=True, flush_print=flush_print)
def aprasymas():

    def maziausia(x, y): ###PLACEHOLDER:--> def ?(x, )
        if x > y:
            return y
        else:
            return x ###PLACEHOLDER:-->  ?

    print( maziausia(3, 5)  )


@tutor(imitateCLI=True, flush_print=flush_print)
def aprasymas2():

    def fun(y, x): ###PLACEHOLDER:--> def ?
        if x > 10:
            return y


    print( fun(3, 5)  )
    print( fun(13, 13)  )
    print( fun(20, 100)  )

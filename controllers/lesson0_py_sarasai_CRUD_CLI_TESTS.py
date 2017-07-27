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

@tutor(imitateCLI=True)
def sarasai():

    Finansai = [ 10, 12, 0, 20, 8, -25, -5 ]  # pajamos/išlaidos per savaitę

    print("Finansai", Finansai)

    # susumuojam balansą
    balansas = sum(Finansai) ###PLACEHOLDER:--> balansas = ?(Finansai)
    print("Dabar turim:", balansas )

    return flush_print()

@tutor(imitateCLI=True)
def vidurkis():

    Pazymiai = [6, 8, 4, 10]

    suma = sum( Pazymiai )
    kiek = len( Pazymiai )  # asdf  ###PLACEHOLDER:--> kiek = ?(Pazymiai)  # hint: sąrašo ilgis
    print("Vidurkis:", suma / kiek )

    return flush_print()

@tutor(imitateCLI=True)
def perrinkimas_grafikas():

    Pazymiai = [6, 9, 3, 7]

    print( "Stulpelinė diagrama (horiz.):" )

    for pazymys in Pazymiai: # imam po pažymį iš sąrašo
        # nurodėm kintamojo pavadinimą "pazymys",
        # ir su juo atitraukę nuo krašto darom, ką norim
        print( pazymys, "#" * pazymys) # spausdinam reikšmę ir tiek pat simbolių

    return flush_print()



@tutor(imitateCLI=True)
def saraso_pertvarkymas():
    money = [10, 2, 5]  # centai...

    money.append( 100 ) # gavom eurą!
    print( money )

    money[1] = 30  # pakoreguojam antrąją reikšmę
    print( money )

    del money[0]   # pašalinam pirmąją reikšmę
    print( money )

    money.insert(0, 13) # į priekį įterpiam 13
    print( money )

    return flush_print()

@tutor(imitateCLI=True)
def filtravimas_i_nauja_sarasa():

    Pazymiai = [6, 9, 3, 7]
    riba = 5

    # Norim surašyt didesnius už ribą į atskirą sąrašą

    didesni = [] # paruošiam naują sąrašą ###PLACEHOLDER:-->  didesni = ? # paruošiam naują sąrašą

    for paz in Pazymiai:  ###PLACEHOLDER:--> for paz? :
        if paz > riba: ###PLACEHOLDER:--> if
            didesni.append( paz ) ###PLACEHOLDER:--> papildom sarasa

    return didesni


@tutor(imitateCLI=True)
def elementu_numeravimas():
    vardai = ['Jurgis', 'Antanas', 'Aloyzas', 'Martynas']

    print( vardai [0] ) ###PLACEHOLDER:--> print( vardai [?] )

    vardai[2] = "Tomas" ###PLACEHOLDER:--> vardai[?] = "Tomas"
    print( vardai )

    vardai.append( vardai[0] )  ###PLACEHOLDER:--> vardai.append( vardai[?] )

    del vardai[3] ###PLACEHOLDER:--> del vardai[?]
    print( vardai)

    return flush_print()


@tutor(imitateCLI=True)
def elementu_numeravimas_klaida():
    vardai = ['Jurgis', 'Antanas', 'Aloyzas', 'Martynas']
    print( vardai [4] )

    return flush_print()

@tutor(imitateCLI=True)
def lygiagretus_perrinkimas():
    vardai = ['Jurgis', 'Antanas', 'Aloyzas', 'Martynas']
    pinigai = [1000, 2000, 500, 8000]

    # atspausdinkim vardus tų, kas turi daugiau negu 1000 pinigų
    for v, p in zip(vardai, pinigai): ###PLACEHOLDER:--> for v, ? in ?(vardai, pinigai):
        if p > 1000:
            print( v )  ###PLACEHOLDER:--> ?

    return flush_print()
""

# https://docs.google.com/document/d/15bBFcodY6f6aZ6D2Dco94fwbo2OBeZKPS-8gq7CsPAs/edit

#####

@tutor(imitateCLI=True)
def _funkcijos():


    def pasveikink(vardas):
        print( "Hi, " + vardas )

    pasveikink( "Joe" )
    pasveikink( "Antanas" )

    return flush_print()

@tutor(imitateCLI=True)
def grazinama_reiksme():
    def add(a, b):
        result = a+b
        return result

    print( add( 4, 6 ) )
    print( add( 4, -6 ) )
    print( add( "labas", " rytas" ) )

    return flush_print()

@tutor(imitateCLI=True)
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
    return flush_print()


@tutor(imitateCLI=True)
def vykdymo_eiliskumas_test1():
    def add(a, b):
        print( "vykdom add:", a, b )
        return a+b

    def maximum(x, y):
        print( "vykdom maximum:", x, y )

        if x > y:
            return x
        else:
            return y

    ats = add( add(2, 5), maximum( 2, 5 ) ) ###PLACEHOLDER:--> ? = ?( ?(2, 5), ?( 2, 5 ) )
    print( ats )

    return flush_print()


@tutor(imitateCLI=True)
def aprasymas():

    def maziausia(x, y): ###PLACEHOLDER:--> def ?(x, )
        if x > y:
            return y
        else:
            return x ###PLACEHOLDER:-->  ?

    print( maziausia(3, 5)  )

    return flush_print()

@tutor(imitateCLI=True)
def aprasymas2():

    def fun(y, x): ###PLACEHOLDER:--> def ?
        if x > 10:
            return y


    print( fun(3, 5)  )
    print( fun(13, 13)  )
    print( fun(20, 100)  )

    return flush_print()

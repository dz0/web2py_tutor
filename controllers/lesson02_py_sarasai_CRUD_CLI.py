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
    print("Transakcijų kiekis:", len(Finansai))

    # susumuojam balansą
    balansas = sum(Finansai) ###PLACEHOLDER:--> balansas = sum(?)
    print("Dabar turim:", balansas ) ###PLACEHOLDER:--> print("Dabar turim:", ? )

    return flush_print()

@tutor(imitateCLI=True)
def vidurkis():

    Pazymiai = [6, 8, 4, 10]

    suma = sum( Pazymiai )
    kiek = len( Pazymiai )   ###PLACEHOLDER:--> kiek = ?(Pazymiai)  # hint: sąrašo ilgis
    print("Vidurkis:", suma / kiek )

    return flush_print()



@tutor(imitateCLI=True)
def perrinkimas_su_vertinimu():

    Pazymiai = [6, 9, 5, 3, 7]

    for pazymys in Pazymiai: # imam po pažymį iš sąrašo

        reakcija = ""  # default'inė reikšmė

        if pazymys >= 8:
            reakcija = "OK!"

        if pazymys < 5:
            reakcija = "ech..."

        print(pazymys, reakcija )

    return flush_print()




@tutor(imitateCLI=True)
def perrinkimas_grafikas():

    Pazymiai = [6, 9, 3, 7]

    print( "Stulpelinė diagrama (horizontali):" )

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

    del money[0]   # pašalinam pirmąją (programuotojams-nulinę) reikšmę
    print( money )

    money.insert(0, 13) # į priekį įterpiam 13
    print( money )


    return flush_print()


@tutor(imitateCLI=True)
def elementu_numeravimas_klaida():
    vardai = ['Jurgis', 'Antanas', 'Aloyzas', 'Martynas']
    # eil nr.:   0         1          2           3

    print( vardai [4] )  # tokiu nr. elemento nėra

    return flush_print()


@tutor(imitateCLI=True)
def filtravimas():

    Pazymiai = [6, 9, 3, 7]
    vidurkis = sum( Pazymiai )/ len( Pazymiai )

    print( "Didesni už vidurkį" )

    for paz in Pazymiai:  ###PLACEHOLDER:--> ? paz in Pazymiai?
        if paz > vidurkis:
            print( paz ) ###PLACEHOLDER:--> print( ? )

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

    # įrašykite trūkstamus eil. nr, kad gautumėt rodomą rezultatą

    print( vardai [0] ) ###PLACEHOLDER:--> print( vardai [?] )

    vardai[2] = "Tomas" ###PLACEHOLDER:--> vardai[?] = "Tomas"
    print( vardai )

    vardai.append( vardai[0] )  ###PLACEHOLDER:--> vardai.append( vardai[?] )
    print( vardai)

    del vardai[3] ###PLACEHOLDER:--> del vardai[?]
    print( vardai)

    return flush_print()



@tutor(imitateCLI=True)
def lygiagretus_perrinkimas():
    prekes = ['duona', 'sūris', 'alus']
    kainos = [1.2, 5, 1]

    for preke, kaina in zip(prekes, kainos):
        print( preke, "kainuoja", kaina )

    return flush_print()


@tutor(imitateCLI=True)
def lygiagretus_perrinkimas_2():
    vardai = ['Jurgis', 'Antanas', 'Aloyzas', 'Martynas']
    pinigai = [1000, 2000, 500, 8000]

    # atspausdinkim vardus tų, kas turi daugiau negu 1000 pinigų
    for vard, pin in zip(vardai, pinigai): ###PLACEHOLDER:--> for vard, ? in ?(vardai, pinigai):
        if pin > 1000:
            print( vard )  ###PLACEHOLDER:--> ?

    return flush_print()

print()
# https://docs.google.com/document/d/15bBFcodY6f6aZ6D2Dco94fwbo2OBeZKPS-8gq7CsPAs/edit


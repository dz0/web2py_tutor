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

def decorate_flush_print(f):  # can't use it in combination with @tutor :/
    def result():
        f()  # call function with print calls
        return flush_print()  # return what it printed

    return result

def __TEST_fake_print():
    x = 2
    print(1)
    print('ad')
    print(x, 4, 'asdf')

    real_print( flush_print(sep='\n') )

######## end fake print ##########


from plugin_introspect import tutor, menu

def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=menu())


@tutor(imitateCLI=True)
def hello_world():
    return "Hello, world"

@tutor(imitateCLI=True)
def parodyk_daugiau_info():
    print( "Jonas turi", 25, "€" )  # print leidžia išvardinti kelias reikšmes
    return flush_print()

@tutor(imitateCLI=True)
def _kintamieji():
    a = 5 # kintamieji - tai vardai, kuriems priskiriamos reikšmės
    b = 3 ###PLACEHOLDER:--> ?
    return a * b


@tutor(imitateCLI=True)
def money_increase():

    # pradžioj turim 99 pinigus
    money = 99
    print( money )

    money = money + 1   # padidinam money 1 pinigu :)
    print( money )

    money = money * 2 # padidinam money 2 kartus ###PLACEHOLDER:--> money = ? ? 2
    print( money )

    return flush_print()

@tutor(imitateCLI=True)
def money_spend():

    money = 100
    beer = 2
    bread = 1

    # let's buy bread
    money = money - bread ###PLACEHOLDER:--> money = money ? ?
    print( money )

    # let's buy 3 beer
    money = money - 3*beer ###PLACEHOLDER:--> money = money ? ?
    print( money )

    return flush_print()

@tutor(imitateCLI=True)
def atsitiktiniai_skaiciai():
    import random # įkeliam/importuojam atsitiktinių skaičių paketą "random"

    x = random.randint(1, 100)   # naudojam to paketo komandą "randint"
    return x


@tutor(imitateCLI=True)
def _duomenu_tipai():
    a = 5     # sveikas skaičius - "integer" (trumpina: int)
    b = 3.14  # slankaus kablelio - "floating point" (trumpina: float)
    c = "hello" + ' world' # teksto eilutė - "string" (trumpina: str)
                           # tekstą žymi viengubos arba dvigubos kabutės
    print( a, type(a) )
    print( b, type(b) )
    print( c, type(c) )
    return flush_print()

@tutor(imitateCLI=True)
def tekstas_plius_skaicius_klaida():
    # Tiesiogiai sudėt  teksto ir skaičiaus nepavyks - bus klaida

    a = "M"
    b = 1

    c = a + b


@tutor(imitateCLI=True)
def duomenu_tipu_konvertavimas():
    a = 5
    b = 3.14
    c = "6.66"

    # konvertuojam
    a_txt = str( a ) # skaičių į tekstą ("string" tipą)

    b_int = int( b ) # skaičių su kableliu į sveiką (numeta trupmeną)

    c_float = float( c ) # tekstą į skaičių

    # repr - reiškia "represent"  -- kaip reikšmė atrodytų programos kode
    print( repr(a_txt) )
    print( repr(b_int) )
    print( repr(c_float) )

    return flush_print()


@tutor(imitateCLI=True)
def skaiciu_paversk_i_teksta():

    # Bet galima skaičių pirmiau paverst tekstu (žr užpraitą pvz ;)

    a = "M"
    b = 1

    c = a + str(b)  ###PLACEHOLDER:--> c = a + ?
    return c


@tutor(imitateCLI=True)
def teksta_paversk_i_skaiciu():

    x = 10
    y = "5"

    z = x + int(y)  ###PLACEHOLDER:--> z = x + ?
    return z




@tutor(imitateCLI=True)
def datos_tipas():
    import datetime

    jonines  = datetime.date(2017, 6, 23)
    print( jonines )

    siandien  = datetime.date.today()
    print( siandien )

    # datos aritmetika: kelinta dabar metų diena?
    metu_riba  = datetime.date(2016, 12, 31)
    skirtumas_dienomis = (siandien - metu_riba).days
    print( skirtumas_dienomis )

    return flush_print()


@tutor(imitateCLI=True)
def _tekstas():
    # tekstą galima sudėti
    a = "labas"
    b = "rytas"

    mintis = a + " " + b
    print( mintis )
    print( "teksto ilgis:", len( mintis ) )  # "len" nuo "length"

    return flush_print()

@tutor(imitateCLI=True)
def teksto_dauginimas():
    # tekstą galima padauginti
    a = "labas"
    b = (a + " ") * 3 ###PLACEHOLDER:--> b = (a + " ") ?

    return b

@tutor(imitateCLI=True)
def multiline_tekstas():
    bla = """
        trigubos kabutės leidžia programoje
        rašyti tekstą per kelias eilutes.

        Taip pat jos naudojamos kaip komentarai programoje ("docstrings" - dokumentacijos tekstai)
        """

    return PRE( bla ) ###REPLACE print( bla )

@tutor(imitateCLI=True)
def replace_():
    zodis = "mintis"

    zodis = zodis.replace('i', 'a')

    return zodis

@tutor(imitateCLI=True)
def sablonas():
    template = "{} kainuoja  {} €"
    info = template.format( 'duona',  10 )

    return info



@tutor(imitateCLI=True)
def newline():

    tekstas = "mano batai buvo 2"
    po_zodi_eilutej = tekstas.replace(' ', '\n')
    # '\n' yra spec. simbolis -- reiškia naują eilutę

    print( po_zodi_eilutej )

    return flush_print()



@tutor(imitateCLI=True)
def _salygos_sakiniai():

    money = 5  # kiek turime eurų

    if  money  > 10:  # netenkinama sąlyga
        print( "I can buy a stake" ) # nevykdoma

    if  money  > 2:   # tenkinama ###PLACEHOLDER:--> ? > 2:  # tenkinama
        print( "I can buy a beer" ) # vykdoma

    return flush_print()


@tutor(imitateCLI=True)
def else_():

    money = 1000  # kiek turime eurų

    if  money  >= 1000000:
        print( "I am milionnaire!" )

    # kitu atveju
    else:  ###PLACEHOLDER:--> ?
        print( "money is not everything..." )

    return flush_print()

@tutor(imitateCLI=True)
def elif_else():

    money = 1000  # kiek turime eurų

    if  money  >= 1000000:
        print( "I am milionnaire!" )

    # reiškia "else if"  -- žiūrima, kai netinka ankstesnė(s) sąlyga/os
    elif money >= 1000:  ###PLACEHOLDER:--> ? money >= 1000?
        print( "I have some money" )

    # jei netenkinamos ankstesnės sąlygos
    else:  ###PLACEHOLDER:--> ?
        print( "I am running out of money.." )

    return flush_print()


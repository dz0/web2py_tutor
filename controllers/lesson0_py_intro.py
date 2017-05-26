# -*- coding: utf-8 -*-
"""Web2Py pagal puslapio URL iškviečia funkciją atitinkamame faile ("controller"'yje)."""

from plugin_introspect import tutor, menu


def index( ): 
    return menu()


@tutor
def hello():    # def - nuo žodžio "define" - aprašo funkciją
    """URL pabaigoje "hello", todėl iškviečiama funkcija "hello()" """
    return "Hello"  # grąžinamą reikšmę matote prie [ Pavyzdys ]

@tutor
def alio():   ###PLACEHOLDER:-->  def ():  
    return "Alio" ###PLACEHOLDER:-->  "Alio"

@tutor
def grazinama_reiksme():   
    return "Labas"  ###PLACEHOLDER:--> ? 


@tutor
def kintamieji():   
    a = 5
    b = 3 ###PLACEHOLDER:--> ? 
    return a * b 


@tutor
def kintamuju_kitimas():   
    a = 5
    a += 3 # padidinam 3  
    a *= 2 # padvigubinam  ###PLACEHOLDER:--> a  # padvigubinam
    return a


@tutor
def _duomenu_tipai():   
    a = 5
    b = 3.14
    c = "hello" + ' world' # tekstas gali būt ir tarp viengubų ir tarp dvigubų kabučių

    return type(a), BR(), type(b), BR(), type(c)  # ps.: BR() atitinka HTML <br>


@tutor
def duomenu_tipu_konvertavimas():   
    a = 5
    b = 3.14
    c = "hello" 
    d = "6.66"

    a_txt = str( a )
    b_int = int( b )
    d_float = float( d ) 
    
    return repr(a_txt), BR(), repr(b_int), BR(), repr(d_float)  # repr - reiškia "represent"  
                                                                # kaip reikšmė atrodo kode -- tekstas rodomas su kabutėm 
@tutor
def datos_tipas():
    import datetime
    
    jonines  = datetime.date(2017, 6, 23)
    
    return jonines

@tutor
def datos_tipas_siandien():
    import datetime
    
    siandien  = datetime.date.today()
    
    return siandien
    

@tutor
def datos_skirtumas():
    """raskite kelinta dabar metų diena"""
    import datetime

    NM_riba  = datetime.date(2016, 12, 31) # metų riba
    siandien  = datetime.date.today()
    
    return (siandien-NM_riba).days  ####PLACEHOLDER:--> return ( ? ).days 
    
    
@tutor
def data_su_laiku():
    import datetime
    
    dabar = datetime.datetime.now()
    
    return dabar


@tutor
def _tekstas():
    a = "labas"
    b = "rytas"
    
    return a + " " + b

@tutor
def multiline_tekstas():
    bla = """trigubos kabutės leidžia
        rašyti tekstą per kelias eilutes.
        
        Taip pat jos naudojamos docstring'uose (funkcijos aprašymui/paaiškinimams).
        """
    
    return PRE( bla )
    
@tutor
def tekstas_plius_skaicius():
    """Tiesiogiai sudėt teksto ir skaičiaus nepavyks - bus klaida"""
    a = "labas"
    b = 10
    
    return a + b

@tutor
def tekstas_info_sujungimas():
    name = "Jurgis"
    age = 36
    
    return name + " turi " + str(age) +" metus."  # str(..) bet ką paverčia tekstu
    

@tutor
def teksto_formatavimas():
    """Kad nereiktų rašinėt + ir str(..) yra spec. būdai įterpt info į tekstą.
    
    Naudojamas % žymeklis, kuris pažymi, kurioje vietoje info bus įterpta.
    o gale po % išvardinamos norimos įterpti reikšmės """

    name = "Jurgis"
    age = 36
    
    return "%s turi %s metus." % ( name, age )

@tutor
def _duomenu_strukturos():
    pass

@tutor
def sarasai():
    pass


@tutor
def zodynai():
    pass


@tutor  
def teksto_formatavimas_su_zodynais():
    """žodyne reikšmes susiejamos  pagal pavadinimą/vardą. Analogiškai kaip kintamieji.
    
    Tada vietoj %s  nurodoma išsamesnė info:  %(pavad)s  , kur "pavad" yra reikšmės pavadinimas.
    Patogu, nes pasikeitus išsidėstymui tekste, nekils nesusipratimų.
    
    O gale pateikiamas žodynas. Čia panaudojam spec. funkciją locals(),  
    kuri leidžia paimti visus funkcijos kintamuosius kaip žodyną  """

    name = "Jurgis"
    age = 36
    
    return "%(name)s turi %(age)s metus. %(name)s kartais vėluoja..." % locals()

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



from plugin_introspect import tutor as original_tutor, menu, generate_exposed_functions_info
exposed_functions = generate_exposed_functions_info()

from tools import call_or_redirect
import urllib


# tutor = auth.requires_login(original_tutor)
def tutor (*args, **kwargs):
    """decorator to ask login for taks"""
    
    if request.function == 'index' \
    or not exposed_functions[request.function]['is_task']:
        return original_tutor(*args, **kwargs)
        
    # ask login for tasks
    if  auth.is_logged_in():
        return original_tutor(*args, **kwargs)
    else:
        next = auth.here()
        session.flash = response.flash = "užduoties atlikimui reikia prisijungti"
        return call_or_redirect(auth.settings.on_failed_authentication,
                                auth.settings.login_url + '?_next=' + urllib.quote(next))


def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=menu())

########### tasks



@tutor(imitateCLI=True, flush_print=flush_print)
def zodynai():
    
    # žodyne reikšmės saugomos poromis:   
    # raktinis žodis -->  reikšmė
    # angliškai: key -->  value
    
    kainos = {'bulves': 1.5,  'morkos': 2 }
    
    print( kainos['bulves'] )  # pagal raktinį žodį pasiekiam reikšmę
    
    kainos['morkos'] *= 0.85   # pritaikom akciją - pamažinam kainą ;)
    
    kainos['kefyras'] = 3      # pridedam naują reikšmę
    print( kainos )   
    
    
    """
    ps.: žodyne reikšmių eilė nėra fiksuota, 
    jos išdėstomos, kaip kompui patogiau (rasti raktinį žodį)
    """
    
@tutor(imitateCLI=True, flush_print=flush_print)
def elemento_CRUD():
    kainos = {} ###PLACEHOLDER:--> kainos =   # sukurkite tuščią žodyną
    
    kainos['duona']  = 1.2 ###PLACEHOLDER:-->  ? # pridėkite duonos kainą 1.2
    kainos['pienas'] = 0.6 ###PLACEHOLDER:-->  ? # pridėkite pieno kainą 0.6
    print( "papildžius", kainos )
    
    kainos['duona'] = 0.99 ###PLACEHOLDER:-->  ? # pakeiskite duonos kainą į 0.99 
    print( kainos['duona'] ) 
    
    del kainos['pienas'] ###PLACEHOLDER:--> del ? # ištrinkite pieną
    print( kainos )
    

@tutor(imitateCLI=True, flush_print=flush_print)
def papildymas_kitu_zodynu():
    kainos = {'bulves': 1.5,  'morkos': 2 }
    naujos_kainos = {'saldainiai': 3, 'bulves': 1.99,  }
    
    kainos.update( naujos_kainos )  # pakeičia/papildo kainų žodyną pagal kitą žodyną
    
    print( kainos )


@tutor(imitateCLI=True, flush_print=flush_print)
def nerasta_reiksme():
    kainos = {'bulves': 1.5,  'morkos': 2 }
    
    print( kainos['saldainiai'] ) # klaida - raktinio žodžio nerasta :/
    

@tutor(imitateCLI=True, flush_print=flush_print)
def reiksmes_patikrinimas():
    prekes = {'bulves': 1.5,  'morkos': 2 }
    
    if 'saldainiai' in prekes:   # patikrina ar yra info  apie  saldainius
        print( 'pasmaguriausim!' )
    
    if 'bulves' in prekes:  ###PLACEHOLDER:-->  ? # jeigu yra bulvių? 
        print( 'pavalgysim už', prekes['bulves'] )
        
        if 'mesa' in prekes:
            print( '... sočiai už', prekes['mesa'] ) 
            
@tutor(imitateCLI=True, flush_print=flush_print)
def standartine_reiksme():
    
    kainos = {'bulves': 1.5,  'morkos': 2 }
    
    # get(..) metodas leidžia išvengti klaidos, jei neranda elemento
    # o jei randa, grąžina reikšmę, kaip paprastas kainos[..]
    print( kainos.get('saldainiai') ) # jei neranda - None
    
    for preke in ['bulves', 'druska', 'sviestas']:
        # get leidžia nurodyt antrą parametrą -- ką grąžint, jei neras info
        kaina = kainos.get(preke, 0)  # jei neras - 0 
        print( preke, 'kainuoja', kaina )  
    

@tutor(imitateCLI=True, flush_print=flush_print)
def iteracija():
    # iteracija -- reikšmių perrinkimas/kartojimas
    kainos = {'bulves': 1.5,  'morkos': 2 }
    
    for preke in kainos: # perrenkam visus raktinius žodžius
        print( preke, 'kainuoja', kainos[ preke ] )  
        
    print()  # tuščia eilutė
    
    # dažnai patogiau perrinkimui gaut susietas poras 
    for preke, kaina in kainos.items(): # nereiks rašinėt kainos[preke]  
        print( preke, 'kainuoja', kaina )
        
@tutor(imitateCLI=True, flush_print=flush_print)
def keys_vs_values():
    # iteracija -- reikšmių perrinkimas/kartojimas
    kainos = {'bulves': 0.6,  'morkos': 2, 'grybai': .6 }
    
    prekiu_sarasas = kainos.keys() 
    print( prekiu_sarasas )
    
    susietos_reiksmes = kainos.values()  # retokai prireikia 
    print( susietos_reiksmes )
    
    # pasikartokim, kaip perrinkt susietas poras (key/value)
    for key, val in kainos.items(): ###PLACEHOLDER:-->  for ? in kainos.items(): 
        print( key, 'susieta su', val )


@tutor(imitateCLI=True, flush_print=flush_print)
def _pvz_prekiu_krepselis():
    kainos = {'bulves': 0.6,  'morkos': 2, 'grybai': .6 }
    
    pirkiniai = ['bulves', 'grybai'] # ko pirksim
    
    suma = 0
    for x in pirkiniai:
        suma += kainos[x]
    
    print( pirkiniai, 'kainuos', suma )
        

@tutor(imitateCLI=True, flush_print=flush_print)
def jeigu_norimo_pirkinio_nera():
    kainos = {'bulves': 0.6,  'morkos': 2, 'grybai': .6 }
    
    norimi_pirkiniai = ['bulves', 'sviestas', 'morkos'] # ko norim nusipirkt
    
    suma = 0
    for x in norimi_pirkiniai:
        # kad nebūtų klaidos, patikrint, ar x yra parduodamas (kainose)
        if x in kainos:  ###PLACEHOLDER:-->  ?   
            suma += kainos[x]
        else:
            print( "nėra:", x )
    
    print( 'rastos prekės kainuos:', suma )
        

@tutor(imitateCLI=True, flush_print=flush_print)
def list_comprehension():
    kainos = {'bulves': 0.6,  'morkos': 2, 'grybai': .6 }
    pirkiniai = ['bulves', 'grybai'] # ko norim nusipirkt
    
    suma = sum( kainos[x]    for x in pirkiniai )  # gudresnis būdas atrinkt info
    
    print( pirkiniai, 'kainuos', suma )

@tutor(imitateCLI=True, flush_print=flush_print)
def po_kelias_prekes():
    kainos = {'bulves': 0.6,  'morkos': 2, 'grybai': .6 }
    pirkiniai = {'bulves': 3, 'grybai': 2} # ko/kiek norim nusipirkt
    
    suma = sum( kainos[x]*kiekis    for x, kiekis in pirkiniai.items()   )  
    
    print( pirkiniai, 'kainuos', suma )
    
    
@tutor(imitateCLI=True, flush_print=flush_print)
def filtravimas_pagal_kaina ():
    kainos = {'bulves': 0.6,  'morkos': 2, 'pienas': 0.7 }
    
    # viskas, kas kainuoja mažiau negu 1 pinigas..
    studentu_maistas = [ x  for (x, kaina) in kainos.items()    if kaina < 1 ]
    
    # bet taip nėra tiesioginės galimybės paminėti, kas netinka..
    
    print( studentu_maistas )

@tutor(imitateCLI=True, flush_print=flush_print)
def po_kelias_prekes_filtravimas_ar_yra():
    kainos = {'bulves': 0.6,  'morkos': 2, 'grybai': .6 }
    pirkiniai = {'obuoliai': 1, 'bulves': 3, 'grybai': 2} # ko/kiek norim nusipirkt
    
    suma = sum( kainos[x]*kiekis  for x, kiekis in pirkiniai.items()  if x in kainos )  ###PLACEHOLDER:-->  suma = sum( kainos[x]*kiekis  for x, kiekis in pirkiniai.items()  ??? ) 
    
    print('norint', pirkiniai, 'kainuos', suma ) 
    
    
@tutor(imitateCLI=True, flush_print=flush_print)
def list_comprehension_ir_isvardint_nerastus():
    kainos = {'bulves': 0.6,  'morkos': 2, 'grybai': .6 }
    
    # aiškumo dėlei pasidarom du pavadinimus
    # ir "kiekiai" ir "pirkiniai"  turės tą patį žodyną.
    kiekiai = pirkiniai = {'obuoliai': 1, 'bulves': 3, 'grybai': 2, 'uogos': 10} # ko/kiek norim nusipirkt
    
    rastos_prekes =   [ x  for x in pirkiniai  if     x in kainos ]
    nerastos_prekes = set(pirkiniai) - set(rastos_prekes)  # aibių skirtumas
    
    suma = sum( kainos[x]*kiekiai[x] for x in rastos_prekes)  
    
    print( rastos_prekes, 'kainuos', suma )
    print( 'nėra', nerastos_prekes )
    
    """ Kad būtų gražiau, galima teksto reikšmes sujungt 
    Tinka sąrašui, žodyno raktams, aibei:
    
    def sujunk( info ): return ' ir '.join(info)  # pagalbinė funkcija
    print( sujunk(rastos_prekes), 'kainuos', suma )
    print( 'nėra', sujunk(nerastos_prekes) )
    print( 'parduodamos', sujunk(kainos) )
    """
    


@tutor(imitateCLI=True, flush_print=flush_print)
def _zodynas_kaip_irasas():
    
    # kainų sąraše visi elementai buvo vienodos prigimties - prekės.
    # bet žodyne laisvai gali būti skirtingos prigimties info:
    
    petras =  {"vardas": "Petras",  "amzius": 21, "miestas": "NewYork" }
    
    petras['turtas'] = 666  # papildome info
    
    # mes aprašėme vieną studentą
    print( petras ) 
    
    # gali būti studentų sąrašas
    studentai = [
        petras,
        {"vardas": "Jonas",  "amzius": 18 },
        {"vardas": "Zigmas",  "miestas": "Tokyo", "amzius": 25 },
    ]
    
    for stud in studentai: 
        print( stud['vardas'], "gyvena", stud.get('miestas', 'kažkur..') )



@tutor(imitateCLI=True, flush_print=flush_print)
def zodyno_uzpildymas_vardiniais_parametrais():
    
    # iškviečiant funkcas, joms galima nurodyti įvardintus argumentus/parametrus
    # tą kartais patogu naudot su žodyno sukūrimo funkcija "dict" 
    studentas = dict( vardas="Petras",  miestas="NewYork", amzius=21 )
    print( studentas )

@tutor(imitateCLI=True, flush_print=flush_print)
def teksto_formatavimas_pagal_zodyna():
    name = "Petras"
    age = 21
    print( "%s is %s years old." % (name, age) )

    stud =  {"name": "Petras",  "age": 21, "town": "NewYork" }
    # informaciją galima įterpt iš žodyno pagal raktinius ž.
    print( "%(name)s from %(town)s is %(age)s years old." % stud ) 

@tutor(imitateCLI=True, flush_print=flush_print)
def visi_kintamieji_yra_tarsi_zodyno_elementai():
    
    """Visi kintamieji yra tarsi žodyno elementai - vardas susietas su reikšme!
    Pvz, sukuriame naują funkciją,  
    ir atspausdiname jos vidinius kintamuosius - locals().
    """
    def fun(a):
        name = "Petras"
        age = 21
        print( locals() )
    
    fun(5)  # iškviečiame funkciją
    
    # ps.: Galite išbandyti globals() -- pamatysite daug "vidinių" Python kintamųjų

# -*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from plugin_introspect import tutor, menu


def index( ): 
    return menu()

"""
@tutor 
def task_test_1():
    return DIV( 
                SPAN( "labas " , _style="color:blue"),   ###PLACEHOLDER: --> SPAN( "labas " , _style=""),
                B("Pasauli"), 
                SPAN("!", _style="color:red")   ###PLACEHOLDER: --> SPAN("!")
              )
              
@tutor 
def task_test_2_multiline():
    return DIV( 
###GROUP_LINES
                SPAN( "labas " , _style="color:blue"),   ###PLACEHOLDER: --> SPAN( "labas " , _style=""),
                B("Pasauli"), ###                "Pasauli",
###GROUP_LINES_END
                SPAN("!", _style="color:red")   
            
              )
"""
                  
@tutor
def CAT_():
    return CAT( "labas ", B("pasauli")  ) # CAT - nuo žodžio "ConCATenate" - tiesiog sujungia elementus 

@tutor
def task0():
    return CAT( "labas ", B("pasauli") , "!" )   ###PLACEHOLDER: --> return CAT( "labas ", B("pasauli")  )

    
@tutor
def P_BR():
    return P( "labas ", BR(), B("pasauli")  ) 
       
       
@tutor
def DIV_SPAN():
    return DIV( 
                SPAN("labas", _style="color:blue"),  # kai daugiau info, sveika ją išvardinti per eilutes
                B("pasauli") 
            )

@tutor 
def task1():
    """Pakeiskite/papildykite kodą, kad gautųsi rodomas rezultatas"""
    return DIV( 
                SPAN( "labas " , _style="color:blue"),   ###PLACEHOLDER: --> SPAN( "labas " , _style=""),
                B("Pasauli"), 
                SPAN("!", _style="color:red")   ###PLACEHOLDER: --> SPAN("!")
              )
              

@tutor
def SPAN_with_nested():
    return SPAN( CAT( EM("labas"), " pasauli"), _style="color:blue")

@tutor
def task2():
    return DIV( 
                SPAN( CAT("labas ", B("Pasauli")) , _style="color:blue"),  ###PLACEHOLDER: --> SPAN( ?? , _style="color:blue"),  # hint: zr ankstesni pvz.
                SPAN("!", _style="color:red")  
           )

@tutor
def UL_():
    url = "https://upload.wikimedia.org/wikipedia/en/8/80/Wikipedia-logo-v2.svg"
    return UL( "labas", "rytas", IMG(_height="20", _src=url ) )

@tutor
def UL_task3():
    url = "https://upload.wikimedia.org/wikipedia/en/8/80/Wikipedia-logo-v2.svg"
    return UL( 
        "labas", 
        B("rytas"),  ###PLACEHOLDER: --> "rytas"
        SPAN("pasauli", IMG(_height="20", _src=url))    ###PLACEHOLDER: --> "pasauli", IMG(_height="20")
     )

@tutor
def UL_arg_list():
    daug = ['viens', 'du', 'trys']
    return UL(  daug  )


            
@tutor 
def BEAUTIFY_dict():
    zodynas = {'viens':1, 'du':2, 'trys':3 }
    return BEAUTIFY( zodynas )  # žodynui  paryškina raktines reikšmes

@tutor 
def BEAUTIFY_dict_task():
    zodynas = {'lt':"viens", 'en':"one", 'it':"uno" } ###PLACEHOLDER: --> zodynas = {'lt':"viens"}
    return BEAUTIFY( zodynas )  ###PLACEHOLDER: --> zodynas


@tutor 
def BEAUTIFY_dict_nested():
    zodynas = { 
                'LT': {'viens':1, 'du':2 }, 
                'EN': {'one': 1, 'two': 2 }
              }
    return BEAUTIFY( zodynas )  # sąrašo elementus į atskiras eilutes

            
@tutor 
def BEAUTIFY_mixed():
    zodynas = {'viens':1, 'du':2, 'trys': [3, 6, 9]}
    return BEAUTIFY( zodynas )  # sąrašo elementus į atskiras eilutes



@tutor
def TABLE_():
    daug = ['viens', 'du', 'trys']
    return CAT(
            TABLE(  daug, daug, daug, daug ), 
            STYLE( """
                  table {border-collapse:collapse;} 
                  table td { border:1px solid silver }""" )  # bendrai stilių geriau aprašyt kokiam CSS faile
            )


@tutor
def TABLE_matrix():
    maisto_islaidos = [ # matrica
                        ['pusryčiai', 'pietūs', 'vakarienė'],
                        [2,  5, 6],  
                        [0, 10, 5],  
                        [2,  5, 6], 
                        [0,  5, 3], 
                        [9,  0, 6]  
                      ]
            
    return CAT(
            TABLE( maisto_islaidos  ), 
            STYLE( """
                  table {border-collapse:collapse;} 
                  table td { border:1px solid silver }""" )  # bendrai stilių geriau aprašyt kokiam CSS faile
            )


@tutor
def TABLE_matrix_task():
    # matrica
    maisto_islaidos = [  ###PLACEHOLDER --> maisto_islaidos =
                        ['pusryčiai', 'pietūs', 'vakarienė'], ###PLACEHOLDER --> [ ]
                        [0,  5, 3], 
                        [9,  0, 6]  
                      ]
            
    return CAT(
            H1("Maisto išlaidos"),  ###PLACEHOLDER --> "Maisto išlaidos"
            TABLE( maisto_islaidos  ), 
            STYLE( """
                  table {border-collapse:collapse;} 
                  table td { border:1px solid silver }""" )  
            )



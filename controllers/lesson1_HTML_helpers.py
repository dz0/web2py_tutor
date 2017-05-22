# -*- coding: utf-8 -*-

from plugin_introspect import show_menu_and_code, menu, tutor


def index( ): 
    return menu()

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

                  
@tutor
def CAT_():
    return CAT( "labas ", B("pasauli")  ) # CAT - nuo žodžio "ConCATenate" - tiesiog sujungia elementus 

@show_menu_and_code
def P_BR():
    return P( "labas ", BR(), B("pasauli")  ) 
       
@show_menu_and_code
def DIV_SPAN():
    return DIV( 
                SPAN("labas", _style="color:blue"),  # kai daugiau info, sveika ją išvardinti per eilutes
                B("pasauli") 
            )

@show_menu_and_code 
def task1():
    return DIV( SPAN( "labas " , _style="color:blue"), 
                B("Pasauli"), 
                SPAN("!", _style="color:red") 
              )

@show_menu_and_code
def SPAN_with_nested():
    return SPAN( CAT( EM("labas"), " pasauli"), _style="color:blue")

@show_menu_and_code
def task2():
    return DIV( 
                SPAN( CAT("labas ", B("Pasauli")) , _style="color:blue"), 
                SPAN("!", _style="color:red") 
           )

@show_menu_and_code
def UL_():
    return UL( "labas", "rytas", IMG(_height="20", _src="https://upload.wikimedia.org/wikipedia/en/8/80/Wikipedia-logo-v2.svg") )

@show_menu_and_code
def UL_task3():
    return UL( 
        "labas", 
        B("rytas"), 
        SPAN("pasauli", IMG(_height="20", _src="https://upload.wikimedia.org/wikipedia/en/8/80/Wikipedia-logo-v2.svg")) 
     )

@show_menu_and_code
def UL_arg_list():
    daug = ['viens', 'du', 'trys']
    return UL(  daug  )


            
@show_menu_and_code 
def BEAUTIFY_dict():
    zodynas = {'viens':1, 'du':2, 'trys':3 }
    return BEAUTIFY( zodynas )  # žodynui  paryškina raktines reikšmes

@show_menu_and_code 
def BEAUTIFY_dict_task():
    zodynas = {'lt':"viens", 'en':"one", 'it':"uno" }
    return BEAUTIFY( zodynas )  


@show_menu_and_code 
def BEAUTIFY_dict_nested():
    zodynas = { 
                'LT': {'viens':1, 'du':2 }, 
                'EN': {'one': 1, 'two': 2 }
              }
    return BEAUTIFY( zodynas )  # sąrašo elementus į atskiras eilutes

            
@show_menu_and_code 
def BEAUTIFY_mixed():
    zodynas = {'viens':1, 'du':2, 'trys': [3, 6, 9]}
    return BEAUTIFY( zodynas )  # sąrašo elementus į atskiras eilutes



@show_menu_and_code
def TABLE_():
    daug = ['viens', 'du', 'trys']
    return CAT(
            TABLE(  daug, daug, daug, daug ), 
            STYLE( """
                  table {border-collapse:collapse;} 
                  table td { border:1px solid silver }""" )  # bendrai stilių geriau aprašyt kokiam CSS faile
            )


@show_menu_and_code
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


@show_menu_and_code
def TABLE_matrix_task():
    maisto_islaidos = [ # matrica
                        ['pusryčiai', 'pietūs', 'vakarienė'],
                        [0,  5, 3], 
                        [9,  0, 6]  
                      ]
            
    return CAT(
            H1("Maisto išlaidos"),
            TABLE( maisto_islaidos  ), 
            STYLE( """
                  table {border-collapse:collapse;} 
                  table td { border:1px solid silver }""" )  # bendrai stilių geriau aprašyt kokiam CSS faile
            )



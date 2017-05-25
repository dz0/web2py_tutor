# -*- coding: utf-8 -*-


from plugin_introspect import tutor, menu


def index( ): 
    return menu()

@tutor
def variables():
    name = 'Tom'  ###PLACEHOLDER:--> $name = 'Tom'
    age = 18      ###PLACEHOLDER:--> $age = 18
    
    return name, age


@tutor
def functions():
    def double(x):      ###PLACEHOLDER:--> function double($x) {
        result = x*2    ###PLACEHOLDER:-->    $result = $x*2;
        return result   ###PLACEHOLDER:-->    return $resul;
                        ###PLACEHOLDER:--> }
    return double( 7 )

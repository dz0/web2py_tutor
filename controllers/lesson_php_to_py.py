# -*- coding: utf-8 -*-
"""Perdarykite PHP fragmentus į Python pagal [[sintaksės palyginimo suvestinę http://hyperpolyglot.org/scripting]]"""

from plugin_introspect import tutor, menu


def index( ): 
    return menu()

@tutor
def variables():  ###REPLACE    # Kintamieji:
    
    name = 'Tom'  ###PLACEHOLDER:--> $name = 'Tom'
    age = 18      ###PLACEHOLDER:--> $age = 18
    
    return name, age ###REPLACE# rezultate: name, age 

@tutor
def variable_increase():  ###REPLACE # Kintamųjų padidinimas:
    money = 100  ###PLACEHOLDER:--> $money = 100;
    money += 3   ###PLACEHOLDER:--> $money += 3;
    money += 1   ###PLACEHOLDER:--> $money++;
    
    return money ###REPLACE # rezultate: money 


@tutor
def functions():        ###REPLACE # Funkcijos:
    def dvigubas(x):    ###PLACEHOLDER:--> function dvigubas($x) {
        result = x*2    ###PLACEHOLDER:-->    $result = $x*2;
        return result   ###PLACEHOLDER:-->    return $resul;
                        ###PLACEHOLDER:--> }
    return dvigubas( 7 )###REPLACE: dvigubas( 7 );

@tutor
def duomenu_ispakavimas():###PLACEHOLDER:--> function duomenu_ispakavimas(){
    "Galima priskirti daug reikšmių keliems kintamiesiems"
    x, y, z = 1, 2, 3 ###PLACEHOLDER:--> list($x, $y, $z) = [1 ,2, 3];
    return x, y, z ###PLACEHOLDER:-->  return array($x, $y, $z);
     ###PLACEHOLDER:--> }

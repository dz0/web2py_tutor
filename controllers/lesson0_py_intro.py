# -*- coding: utf-8 -*-
"""Web2Py pagal puslapio URL adresą iškviečiama funkcija atitinkamame faile (taip vadinamam "controller"'yje)."""

from plugin_introspect import tutor, menu


def index( ): 
    return menu()

@tutor
def hello():  
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
def kintamuju_keitimas_TODO():   
    a = 5
    a += 8

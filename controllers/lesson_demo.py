# -*- coding: utf-8 -*-
"""Web2Py pagal puslapio URL iškviečia funkciją atitinkamame faile ("controller"'yje)."""

from plugin_introspect import tutor, menu


def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=menu())


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


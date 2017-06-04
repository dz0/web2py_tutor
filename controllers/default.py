# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

from plugin_introspect import lessons_menu

# import os
# from gluon.admin import apath

# def lessons_menu():
    
    # request = current.request
    
    # app = request.application
    # c = request.controller
    # dirpath = apath('%s/controllers' % app, r=request)    
    
    # controllers  = [ c[:-len('.py')]   for c in os.listdir( dirpath )      if c.startswith('lesson') and c.endswith('.py')]
    # menu = [  A(  c[len("lesson"):].title(), _href=URL(c, '') ) for c in controllers ]
    # return UL(menu)

def index():
    response.title = "Pamokos"
    return dict(content=lessons_menu())


def user():
    return dict(form=auth())

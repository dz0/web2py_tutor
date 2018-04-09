# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
from plugin_introspect import tutor, menu as tutor_menu

def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=tutor_menu())

@tutor(  )
def fill_cat():
    import random
    for x in db(db.posts).select():
        x.update_record(category=random.randint(1, 3))
    redirect(URL('posts'))

@tutor( extra_files=['models/skelbimai.py'] )
def populate():
    if not request.is_local:  #apsauga, kad viešai pahost'inus negalėtų nieks generuot fake duomenų
        return "localhost only"
    from gluon.contrib.populate import populate
    # /skelbimai/default/populate/<table>
    # pvz:
    # /skelbimai/default/populate/auth_user
    # /skelbimai/default/populate/posts
    table = request.args[0]  
    populate(db[table],10)   # db yra tarsi lentelių žodynas
    # populate(db.posts ,10)  # db['posts']
    return BEAUTIFY( db( db[table] ).select() )    # grąžinam lentelės duomenis


@tutor( extra_files=['models/skelbimai.py'] )
def posts():
    """ Skelbimų sąrašas 
    /skelbimai/default/posts
    """

    # http://tiny.lt/pycrud 
    rows = db().select( db.posts.ALL )   #  db.posts.ALL atitinka SELECT *
    
    # UŽDUOTIS: padaryti gražų sąrašą su link'ais į post'o peržiūrą
    rows = UL([ 
                LI(
                    B(x.title[0:25]),   # ribojam rodomo title ilgį iki 25
                    A( "Daugiau..." , _class='btn-info', _href=URL('post', args=x.id))
                ) 
                for x in rows
            ])
    
    new =  A( "..new..",  _class='btn btn-warning', _href='post//edit') 

    return CAT(rows, new)

@tutor
def check_can_edit():
    """ Patikrina, ar leisim redaguoti (iškviečiamas iš post):
    priklausomai nuo URL pabaigos (request.args):
    /skelbimai/default/post/<id> -- konkretus post'as
    /skelbimai/default/post/<id>/edit -- konkretaus post'o redagavimas
    /skelbimai/default/post//edit  -- kuriam naują post'ą
    """
    try:  
        id = int(request.args[0])   # jei yra ID
    except:    
        id=""   

    edit = request.args(1) # lenkti skliaustai, jei neranda index'o grąžina None
    
    can_edit = False  # default'inė reikšmė
    
    if auth.is_logged_in():  # jeigu yra prisijungęs user'is 
        if id: # jeigu jau yra skelbimas
            if auth.user.id == db.posts[id].author:  # ar  dabartinis user'is  yra skelbimo autorius 

                can_edit = edit=='edit'  # ar norima redaguoti
        
        else: # jeigu naujas skelbimas
            can_edit = edit=='edit'  # ar  norima redaguoti

    return can_edit

@tutor( extra_files=['models/skelbimai.py'] )
def post():
    """ Vieno skelbimo reikalai - priklausomai nuo URL pabaigos (request.args):
    /skelbimai/default/post/<id> -- konkretus post'as
    /skelbimai/default/post/<id>/edit -- konkretaus post'o redagavimas
    /skelbimai/default/post//edit  -- kuriam naują post'ą
    """
    try:  
        id = int(request.args[0])   # jei yra ID
        record = db.posts[id]       # pagal jį paima skelbimą
    except:    
        record = None
        id=""

    can_edit = check_can_edit()
    # jei reiškias galima redaguot - parodysim link'ą
    
    if can_edit:
        edit_link = A("edit",_class='btn btn-success',_href=URL(args=[id, 'edit'])) 
    else:
        edit_link = ""

    form = SQLFORM( db.posts,  # skelbimų lentelės įrašas 
                    record,    # įrašo duomenys
                    readonly= not can_edit, # jei negalim redaguot - rodom "readonly"
                    showid=False
            )
    
    if form.process().accepted:  # form.process() reikia, kad įrašytų į DB
        redirect(URL( "post", args=[form.vars.id]))   # o kai įrašom - parodom tą įrašą (ID gaunam iš form.vars)
    
    return CAT( form, edit_link )


@tutor( extra_files=['models/skelbimai.py'] )
def search():
    cat_title = request.args(0)
    search_form = SQLFORM.factory(    # kategorijų pasirinkimo forma
        db.posts.category
    )

    if search_form.process().accepted:  # jeigu forma pateikta OK
        cat_id = search_form.vars.category   # paimam kategorijos ID
        cat_title = db.categories[cat_id].title  # ir pagal jį - pavadinimą
    
    # DB užklausa
    rows = ( db( db.categories.title == cat_title ).  # WHERE ...
        select (           #  SELECT          
            db.posts.ALL,  #  posts.*
            join= db.categories.on( db.categories.id == db.posts.category) # JOIN
        )
    )
    
    return CAT(rows, search_form)
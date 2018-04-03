# -*- coding: utf-8 -*-
# def update_task_lesson_info():
def pivotize(data, rows_var, cols_var, main_var):


    # fields =  map(str, data.colnames)

    cols = sorted(set(r[ cols_var] for r in data))
    rows = sorted(set(r[rows_var] for r in data))
    
    
    mtx=[]
    mtx .append( [""] + cols )     
    
    # prefill empty vals
    for r in rows:
        mtx.append( [r]+["-" for c in cols]  )
    
    
    # restructure from data
    for rec in data:
        col = rec[cols_var]
        row = rec[rows_var]
        val = rec[main_var]
        mtx[ rows.index(row)+1 ] [ cols.index(col)+1 ] = val
        
        
    return mtx 
    # return TABLE( mtx )
    # return data[0][cols_var]
    # return UL(rows)



def pivotize_test():
    rows = db( None ).select(
        db.auth_user.first_name, db.learn.task_key, db.learn.mark, db.learn.tries_count,
        orderby = db.auth_user.id|db.learn.task_key, # todo: order by def order in files
        join = [ db.learn.on(db.learn.user_id==db.auth_user.id) ]
    )
    # for r in rows:
        # r.learn.task_key= r.learn.task_key.split('/')[1] #[-15:]
     
        
    # return rows
    return TABLE ( pivotize( rows, rows_var=db.learn.task_key,   cols_var=db.auth_user.first_name, main_var=db.learn.mark ) )
    
    
@auth.requires_login()
def tutor():
    if auth.user_id != 1:
        return "Needs Teacher rights"
    # from plugin_joins_builder import build_joins
    from plugin_introspect import lessons_menu
    lessons = lessons_menu(return_plain=True)
    form = SQLFORM.factory( Field('lesson', requires=IS_IN_SET(lessons) ) )
    form.process(keepvalues=True)
    
    query = None
    if request.vars.lesson:
        # query = db.learn.lesson == request.vars.lesson 
        query = db.learn.task_key.startswith( request.vars.lesson + '/') 
    
    rows = db( query ).select(
        db.auth_user.first_name, db.learn.task_key, db.learn.mark, db.learn.tries_count,
        orderby = db.auth_user.id|db.learn.task_key, # todo: order by def order in files
        join = [ db.learn.on(db.learn.user_id==db.auth_user.id) ]
    )
    
    # for r in rows:
        # r.learn.task_key= r.learn.task_key.split('/')[1] #[-15:]
    
    
    def link_tasks(mtx):
        for row in mtx[1:]:
            task_key = row[0]
            lesson, task = task_key.split('/', 1)
            row[0] = A( task, _href=URL(lesson, task) )
        return mtx
    
    # return dict( content=SQLTABLE(rows, headers={'learn.task_key': {'truncate':100}} ) )
    return CAT(form
                # rows
                ,BR() ,B("Marks")
                ,TABLE( link_tasks( pivotize( rows, rows_var=db.learn.task_key,   cols_var=db.auth_user.first_name, main_var=db.learn.mark ) ) )
                ,BR() ,B("Tries")
                ,TABLE( link_tasks( pivotize( rows, rows_var=db.learn.task_key,   cols_var=db.auth_user.first_name, main_var=db.learn.tries_count ) ) )
    ) 
    # todo: use pivottable , ex https://github.com/espern/pivottable
    

@auth.requires_login()
def keyboard():
    # if auth.user_id != 1:
    #     return "Needs Teacher rights"
    KL = db.keyboard_learn
    count_tasks = KL.user_id.count()
    sum_tries = KL.tries_count.sum()

    rows = db(KL.mark==100).select(db.auth_user.first_name,
                                   count_tasks, sum_tries, groupby=KL.user_id,
                                     join=db.auth_user.on(KL.user_id == db.auth_user.id),
                                   orderby=~count_tasks
                                   )
    return rows

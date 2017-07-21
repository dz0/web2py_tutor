# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from test_helper_4automation import *
from plugin_introspect import get_active_code

def task_query(task_key):
    return (db.learn.task_key==task_key) & (db.learn.user_id==auth.user_id)

def placeholders_fill_in_last_response():
    """Fills in placeholders with previous entries (if such available)
    
    should be called via ajax (similar to evaluate) """
    task_key = request.vars.task_key


    if auth.is_logged_in():
        rows = db(task_query(task_key)).select()
        if len(rows) > 1:
            raise RuntimeError("DB error: learn table has too many (%s) entries with task_key=%s, user_id=%s " % (len(rows), task_key, auth.user_id))

        if len(rows) == 1:
            responses = rows.first().responses
            evaluations = rows.first().evaluations
            js_tpl_fillin = "    fill_in_placeholder( placeholders['%(task_key)s'][%(nr)s],   '%(response)s' ); \n "
            js_tpl_highlight = "    highlight_placeholder( placeholders['%(task_key)s'][%(nr)s],   '%(state)s' );\n"

            js_result_fillin = []
            js_result_highlight = []
            for nr, response, state in zip(range(len(responses)), responses, evaluations):
                js_result_fillin.append(js_tpl_fillin % locals())
                js_result_highlight.append( js_tpl_highlight % locals() )

            return ''.join(js_result_fillin+['\n']+js_result_highlight)
    
    return ""
    
# def update_task_lesson_info():

@auth.requires_login()
def teacher_dashboard():
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
    
    for r in rows:
        r.learn.task_key= r.learn.task_key.split('/')[1] #[-15:]
    # return dict( content=SQLTABLE(rows, headers={'learn.task_key': {'truncate':100}} ) )
    return dict( content=CAT(form, rows) )
    
    
def reset():
    session.renew()
    
def evaluate():
    
    # return dict(a="bla", vars= request.vars)
    task_key = request.vars.task_key
    placeholders = request.vars.placeholder
    if not isinstance( placeholders, (list, tuple) ):
        placeholders = [ placeholders ]  

    answers= session.answers
    initial_codes= session.initial_codes
    # full_codes= session.full_codes

    if task_key and answers and answers.get(task_key):
        # #take placeholders and answers for current task
        hints_result =  "" # hint's result

        js_tpl_highlight = "    highlight_placeholder( placeholders['%(task_key)s'][%(nr)s],   '%(state)s' );\n"
        js_tpl_hints = "    show_hint( placeholders['%(task_key)s'][%(nr)s],   \"%(hints)s\" );\n"
        js_highlight_result = []
        js_hints_result = []

        evaluations = []

        for nr, ph, answer, initial_code in zip( range(len(placeholders)), placeholders, answers[task_key], initial_codes[task_key] ):
            # return BEAUTIFY( [ph, answer] )

            if ph == initial_code:
                state = 'initial'
                hints = u"kazką reik pakeist.."

            else:
                LEVEL = session.MISTAKE_LEVEL or 2 
                def strip_comments( codeline ):
                    k = codeline.rfind("#")
                    if k == -1:
                        return codeline
                    else:
                        return codeline[:k] # todo -- maybe better via AST roundtrip?
                    
                ph = strip_comments( ph )
                answer = strip_comments( answer )
                
                problems = placeholder_smart_compare( ph, expected=answer, limit_hints=5, human_nr=nr+1 ) # it gives hints about problems
                # hints_by_token_comparison(input, expected , limit_hints=2, **tokens_kwargs)

                if problems:
                    msgs = problems
                    msgs_unnecessary = []
                    msgs_expected = []
                    
                    if "" in msgs:  # msgs format is: first list of msgs about unnecessary, then empty line, then expected fragments
                        separator = msgs.index("")
                        msgs_unnecessary = msgs[:separator]
                        msgs_expected = msgs[separator+1:]
                    
                        # truncate hints about "unnecesary" to LEVEL, and "expected" to LEVEL-2
                        msgs = msgs_unnecessary[:LEVEL] + [""] + msgs_expected[:max(0, LEVEL-2)]
                    
                    else:
                        msgs = msgs[:LEVEL]
                    
                    state = 'wrong'
                    hints = '<br />'.join( msgs ).strip()
                                        
                    # print hints
                    hints_result += "<br/>  <li>Laukelis nr. %s: <br> %s </li><br />"%(nr+1,  hints) # for DEBUG
                    # hints_result += "<br/>" +repr(problems)
                    


                else: #  ph == answer   might be picky about spacing...
                    state = 'ok'
                    hints = "ok"
            evaluations.append(state)

            # hints = xmlescape( hints , quote=True)
            hints = XML( hints )
            # hints = XML(unicode(hints), sanitize=False,
            #         permitted_tags=['a', 'b', 'blockquote', 'br/', 'i', 'li', 'ol', 'ul', 'p', 'cite', 'code', 'pre', 'img/']
            #             )

            js_highlight_result.append( js_tpl_highlight % locals() )
            js_hints_result.append(js_tpl_hints % locals())
        hints_result += "<br/>\nLEVEL" + str(LEVEL)

        
        def get_full_current_code(): # needs task_key
             # code =  get_active_code(f=None, code=None, decorate=False, imitateCLI=session.imitateCLI)
             code =  session.full_codes[task_key] 
             
             if placeholders:
                phnr = 0
                result = []
                for line in code.split('\n'):
                    if '###PLACEHOLDER' in line:
                        line = placeholders[phnr]
                        phnr += 1
                    result.append( line )
                # print "full_current_code\n" , '\n'.join(result)
                return '\n'.join(result)
            
             else:
                return code

        def check_syntax_indentation():
            # Thoroughly, can be checked by comparing AST trees (initial with current)
            # or at least by trying to compile

            code = get_full_current_code()
            # print "code", code
            compile(code, '<string>', 'exec')
            return True

        def wrap_js_settimeout( code, time_ms=100 ):
            return "setTimeout( function(){%s;}, %s); \n" %(code, time_ms)
        
        completed_ratio= int(100*evaluations.count('ok')/len(evaluations))
        
        if evaluations.count('ok') == len(evaluations):  # completed_ratio == 100        
            # though separate placeholders might be OK, total indentation might be not..
            try:
                check_syntax_indentation()
                js_hints_result.append(wrap_js_settimeout( "alert('%s'); \n" % "Puiku, gali judėti pirmyn!"))
            except SyntaxError as e:
                # print e
                completed_ratio = 99
                def fmt_more_understandable(e):
                    err, etc = str(e).split('(<string>, line ')
                    lineno = int(etc[:-1])
                    line = get_full_current_code().split('\n')[lineno-1]
                    
                    return "SyntaxError:\\n%s (line %s)\\n%s" %( err, lineno, line)
                    
                js_hints_result.append(wrap_js_settimeout( "alert('%s\\n\\n%s'); \n" % ("Netvarkingas lygiavimas..", fmt_more_understandable(e) )) )

        elif 'initial' in evaluations and not 'wrong' in evaluations:
        # if evaluations.count('initial') == len(evaluations):
            js_hints_result.append(wrap_js_settimeout( "alert('%s'); \n" % "Reik kažką pakeisti geltonose eilutėse... ;)"))

        def save_student_progress():
            # prepair session
            session.setdefault('MISTAKE_LEVEL', 2)  
            
            # store to DB
            if auth.is_logged_in():
                query_unique_task_user = task_query(task_key) 
                # print "\ndb.learn.responses==placeholders"
                # print db.learn.responses
                # print placeholders
                rows_same = db( query_unique_task_user & (db.learn.responses==placeholders) ).select()
                if len(rows_same):  # if we didn't change placeholders since last time
                    return

                db.learn.update_or_insert(  query_unique_task_user ,
                    # user_id from default
                    task_key=task_key,
                    responses=placeholders,
                    evaluations=evaluations,
                    # tries_count= ,
                    mark=completed_ratio # int(100*evaluations.count('ok')/len(evaluations))
                )
                db( query_unique_task_user ).update(tries_count=db.learn.tries_count + 1)
                # rec.update_record( tries_count= rec.tries_count+1 )
                
                tries_count = db( query_unique_task_user ).select( db.learn.tries_count ).first().tries_count
                session.MISTAKE_LEVEL = int(tries_count)  

            else:
                session.MISTAKE_LEVEL += 1 
            
            
            
        if request.vars.mark_placeholders: # ajax
            save_student_progress()
            return ''.join( js_highlight_result +["\n"]+ js_hints_result )



        DBG = False
        
        # if localhost
        if request.env.http_host.split(':')[0] in ['localhost', '127.0.0.1']:
            DBG = True
            

        if DBG:
            # deprecated nonajax -- for debug purposes..
            if 'wrong' in evaluations:
                return CAT( P(B("Užuominos:")), XML(hints_result) )

            if 'initial' in evaluations:
                return "kažką reikia pakeisti geltonose eilutėse)..."

            if not ( 'wrong' in evaluations or 'initial' in evaluations ) :
                return "<b>OK :)</b>"

        return ""
        
          
    # code = get_file_function_code( file, function )
    # return BEAUTIFY( session ) 
    return BEAUTIFY ( dict(
            # vars= map(repr, request.vars.items() ) , 
            placeholders = placeholders,
            answers= session.answers,
            msg = "Sth is wrong with session.answers or session.initial_codes",
            initial_codes = session.initial_codes,
                ) )
    

def overview():
    """Lists all tasks in one page. (but doesn't interact well)"""
    # TODO: fix ajax  https://groups.google.com/d/msg/web2py/YyVilc2ywdg/ZLtN3Gg3Ft0J
    # TODO: fix ?plain link in results
    from plugin_introspect import get_task_code
    lesson = request.args[0] # controller with lesson contents
    # lesson = request.vars.lesson_controller # controller with lesson contents
    fun_names = exposed_functions_names( controller=lesson )
    exposed_functions = generate_exposed_functions_info( controller=lesson )
    examples_codes = [ get_task_code(code=exposed_functions[f]['code'], task_key=lesson+'/'+f, decorate=True) for f in fun_names ]
    results_urls =  [ URL(lesson, f, vars=dict(plain=1))       for f in fun_names ]
    return response.render('tutor.html', dict(lesson=lesson, fun_names=fun_names, examples_codes=examples_codes, results_urls=results_urls) )

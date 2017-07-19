# -*- coding: utf-8 -*-
from test_helper_4automation import *


def placeholders_fill_in_last_response():
    """should be called via ajax (similar to evaluate) """
    task_key = request.vars.task_key


    if auth.is_logged_in():
        rows = db(db.learn.task_key == task_key, db.learn.user_id==auth.user_id).select()
        if len(rows) > 1:
            raise "DB error: learn table has too many (%s) entries with task_key=%s, user_id=%s " % (len(rows), task_key, auth.user_id)

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
                    
                    
                    
                    msgs = msgs_unnecessary[:LEVEL] + [""] + msgs_expected[:max(0, LEVEL-2)]
                        
                    state = 'wrong'
                    hints = '<br />'.join( msgs ).strip()
                                        
                    hints_result += "<br/>  <li>Laukelis nr. %s: <br> %s </li><br />"%(nr+1,  hints) # Deprecated?


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


        if evaluations.count('ok') == len(evaluations):
            js_hints_result.append( "alert('%s'); \n" % "Puiku, gali judėti pirmyn!")

        elif 'initial' in evaluations and not 'wrong' in evaluations:
        # if evaluations.count('initial') == len(evaluations):
            js_hints_result.append( "alert('%s'); \n" % "Reik kažką pakeisti geltonose eilutėse... ;)")

        def save_student_progress():
            # prepair session
            session.setdefault('MISTAKE_LEVEL', 2)  
            
            # store to DB
            if auth.is_logged_in():
                query_unique_task_user = (db.learn.task_key==task_key) & (db.learn.user_id==auth.user_id)
                print "\ndb.learn.responses==placeholders"
                print db.learn.responses
                print placeholders
                rows_same = db( query_unique_task_user & (db.learn.responses==placeholders) ).select()
                if len(rows_same):  # if we didn't change placeholders since last time
                    return

                db.learn.update_or_insert(  query_unique_task_user ,
                    # user_id from default
                    task_key=task_key,
                    responses=placeholders,
                    evaluations=evaluations,
                    # tries_count= ,
                    mark=int(100*evaluations.count('ok')/len(evaluations))
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

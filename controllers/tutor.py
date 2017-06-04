# -*- coding: utf-8 -*-
from test_helper_4automation import *

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
                problems = placeholder_smart_compare( ph, expected=answer, human_nr=nr+1 ) # it gives hints about problems

                if problems:
                    state = 'wrong'
                    hints = problems.strip()
                    hints_result += "<br/>  <li>Laukelis nr. %s: <br> %s </li><br />"%(nr+1,  hints)


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
            js_hints_result.append( "alert('%s'); \n" % "Puiku, gali judėti toliau!")

        elif 'initial' in evaluations:
        # if evaluations.count('initial') == len(evaluations):
            js_hints_result.append( "alert('%s'); \n" % "Reik kažką pakeisti geltonose eilutėse... ;)")

        if request.vars.change_placeholders: # ajax
            return ''.join( js_highlight_result +["\n"]+ js_hints_result )



        DBG = False
        if DBG:
            # deprecated -- for debug purposes..
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
            answers= session.answers        
                ) )
    

# -*- coding: utf-8 -*-
from test_helper_4automation import *
from gluon.admin import apath

def evaluate():
    
    # return dict(a="bla", vars= request.vars)
    task_key = request.vars.task_key
    placeholders = request.vars.placeholder
    if not isinstance( placeholders, (list, tuple) ):
        placeholders = [ placeholders ]  
    
    answers= session.answers
            
    if task_key and answers and answers.get(task_key):
        # #take placeholders and answers for current task
        result = ""
        wrong_ph_nrs = []
        for nr, ph, answer in zip( range(len(placeholders)), placeholders, answers[task_key] ):
            # return BEAUTIFY( [ph, answer] )
            problems = placeholder_smart_compare( ph, expected=answer, human_nr=nr+1 )
            if problems:
                result += "<li>%s </li><br />"%problems
                wrong_ph_nrs.append( nr )
                # return problems
            
                
        if request.vars.highlight_wrong:
            js_tpl = "placeholders['%(task_key)s'][%(nr)s].getScrollerElement().style.background = '%(color)s';"
            if result: 
                color = "#FFC0CB"
                return ';\n'.join( [js_tpl % locals() for nr in wrong_ph_nrs ] )
                # nr = wrong_ph_nrs[0]
                # return "placeholders['%(task_key)s'][%(nr)s].getScrollerElement().style.background = '#FFC0CB';" % locals()
            else:
                color = "#BBF8BB"
                return ';\n'.join( [js_tpl % locals() for nr in range(len(placeholders)) ] )
                
        if result:
            # return CAT( BEAUTIFY([request.vars, session.answers] ),  P(B("Užuominos:")), XML(result) )
            # return CAT( BEAUTIFY([request.vars] ),  P(B("Užuominos:")), XML(result) )
            return CAT( P(B("Užuominos:")), XML(result) )
        else:
            return "<b>OK :)</b>"
        
          
        
    # code = get_file_function_code( file, function )
    # return BEAUTIFY( session ) 
    return BEAUTIFY ( dict(
            # vars= map(repr, request.vars.items() ) , 
            placeholders = placeholders,
            answers= session.answers        
                ) )
    

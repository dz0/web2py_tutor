# -*- coding: utf-8 -*-
from test_helper_4automation import *
from gluon.admin import apath

def evaluate():
    
    # return dict(a="bla", vars= request.vars)
    task_key = request.vars.task_key
    placeholders = request.vars.placeholder
    
    answers= session.answers
            
    if task_key and answers and answers.get(task_key):
        # #take placeholders and answers for current task
        
        for nr, ph, answer in zip( range(len(placeholders)), placeholders, answers[task_key] ):
            # return BEAUTIFY( [ph, answer] )
            problems = placeholder_smart_compare( ph, expected=answer, human_nr=nr+1 )
            if problems:
                return problems
        return "OK"
        
          
        
    # code = get_file_function_code( file, function )
    # return BEAUTIFY( session ) 
    return BEAUTIFY ( dict(
            # vars= map(repr, request.vars.items() ) , 
            placeholders = placeholders,
            answers= session.answers        
                ) )
    

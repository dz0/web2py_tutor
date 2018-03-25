# -*- coding: utf-8 -*-

import sys
from test_helper import failed, passed
import re

# http://pygments.org/docs/quickstart/#guessing-lexers
from pygments.lexers import PythonLexer
lexer = PythonLexer()



# https://docs.python.org/3/library/tokenize.html
from tokenize import generate_tokens, tokenize, untokenize, NUMBER, STRING, NAME, OP, TokenError
from io import BytesIO, StringIO
from collections import Counter
import random
try:
    from cgi import escape as html_escape
except ImportError:
    from html import escape as html_escape

def my_tokenizer( code ):

    rez = re.split(r'(\w+)', code) # group alphanumerics to words
    # print(rez)

    rez2 = []
    for s in rez:
        if re.match(r'\w+', s):
            rez2.append(s)
        else:
            rez2.extend(s) # split nonwords to symbols

    # rez2 = list(filter(str.strip, rez2)) # filter out spaces
    rez2 = [ x for x in rez2 if x.strip() ] # filter out spaces
    return rez2

def get_tokens(code, filter_spaces=True, group_by_parentheses_one_level=False):
    """splits (fragment of) code string to tokens """
    # OPTION 1 - tokenizer
    # try:
    #     # g = tokenize(BytesIO(code.encode('utf-8')).readline)  # tokenize the string
    #     # according to https://stackoverflow.com/a/4952291
    #     g = generate_tokens(StringIO(unicode( code ) ).readline)  # tokenize the string
    #     # g = generate_tokens(StringIO( code.decode('utf-8') ).readline)  # tokenize the string
    #     tokens = [tokval for toknum, tokval, _, _, _ in g][1:]
    #     # failed( tokens)
    # except TokenError as e:
    #     # print ("standart tokenizer ERR %r <br>  in get_tokens(%r, ...)" %(e, code))
    #     tokens = [tokval for toktype, tokval in  lexer.get_tokens(code)]
    #     # failed("ERR %r <br>  in get_tokens(%r, ...)" %(e, code))
    #     # raise TokenError( "ERR %r <br>  in get_tokens(%r, ...)" %(e, code) )

    # OPTION 2 - Pygments
    # # use pygments tokenizer -- it doesn't crash on missing parenthesis...
    # tokens = [tokval for toktype, tokval in lexer.get_tokens(code)]
    # # pygments tokenizer leaves punctuators together -- not good

    tokens = my_tokenizer( code )


    # print "dbg tokens", tokens
    
    if group_by_parentheses_one_level:
        def group_by_parentheses_one_level():
            start = None
            tokens_some_grouped = []
            for nr, t in enumerate(tokens):
                # print(nr, repr(t))
                if not t:
                    continue

                if t in "[({":
                    if len(tokens) > nr+1 and tokens[nr+1]  in "])}":  # if not just empty parentheses
                        tokens[nr] += tokens[nr+1]
                        t = tokens[nr]
                        del tokens[nr+1]
                    else:
                        start = nr

                if start is None:
                    tokens_some_grouped .append ( t )

                if t in "])}" and start != None:
                    if 'for' in tokens:  # don't group for list comprehensions
                        tokens_some_grouped.extend( tokens[start:nr+1] )
                    else:
                        tokens_some_grouped.append( ''.join(tokens[start:nr+1]).replace(',', ', '))  # todo: maybe 1) use untokenize
                    start = None
            return tokens_some_grouped
        tokens = group_by_parentheses_one_level()

    if filter_spaces:
        tokens = [t for t in tokens if t.strip()]
    tokens = [html_escape(t, quote=True).replace("'", "&#x27;")  for t in tokens]
    # print    "dbg tokens polished:", tokens
    return tokens


def hints_by_token_comparison(input, expected , limit_hints=2, **tokens_kwargs):
    """

    :param input:
    :param expected:
    :param limit_hints: max number of hints per category (missing/unnecessary)
    :return:
    """
    msgs = []
    a_tokens = get_tokens(input, **tokens_kwargs)
    b_tokens = get_tokens(expected, **tokens_kwargs)


    def eq_ignoring_pyquotes_type(ats, bts):
        """compares token lists after converting all quotes to double

        Gotcha -- there is no check if quotes were matching before
        """
        def map_pyquotes_to_double( t ):
            t = t.replace("'", '"')
            t = t.replace("&#x27;", '"')
            t = t.replace("&quot;", '"')
            t = t.replace('"""', '"')
            return t

        if len(ats) != len(bts):
            return False

        for at, bt in zip(ats, bts):
            if at != bt:
                bt = map_pyquotes_to_double(bt)
                at = map_pyquotes_to_double(at)
                # print "at bt", at, bt
                if at != bt:
                    return False
                # else:
                #     print "quotes match after mapping any type to double"

        return True


    # if a_tokens == b_tokens:
    if eq_ignoring_pyquotes_type( a_tokens , b_tokens ):
        # print  "seems OK, maybe spacing or quotation is mangled.."
        pass

    else:
        a = Counter( a_tokens )
        b = Counter( b_tokens )
        if a == b:
            msgs =[ "Kažką reiktų sukeisti vietomis..." ]
            # todo: tell what is not ir right place

        else:
            unnecessary= a - b
            missing  = b - a
            # print "dbg input", input
            # print "dbg expected", expected
            # print "dbg unnecessary", unnecessary
            # print "dbg missing", missing

            if limit_hints:
                missing = list( missing.keys() )
                unnecessary = list( unnecessary.keys() )

                random.shuffle( missing )
                random.shuffle( unnecessary )

                missing = missing[:limit_hints]
                unnecessary = unnecessary[:limit_hints]

            msgs = messages_by_fragments(input, expected, required=missing, unnecessary=unnecessary )
    return msgs

def code_highlight(txt):
    return "<span style='color:blue; font-family: monospace;'>%s</span>" % txt

def messages_by_fragments(placeholder, result=None, unnecessary=[], required=[], return_what='all' or 'unnecessary' or 'required'):

    msgs = []

    if result and  result in placeholder    and  len(placeholder) > len(result):
        msg = "Per daug teksto.."
        if placeholder.startswith(result):
            msg += " gale..."
        if placeholder.endswith(result):
            msg += " prieky.."
        msgs.append( msg )

    if not isinstance(unnecessary, (list, tuple)):
        unnecessary = [unnecessary]
    if not isinstance(required, (list, tuple)):
        required = [required]

    # TODO: for analysis also include all placeholder tokens
    for item in unnecessary:
        msg = u"%s kaip ir nereikalingas"
        if item in result:
            print "result", result
            print "item", item
 
                
            # jeigu įvesta daugiau tokių, negu turi būt rezultate
            if get_tokens(placeholder).count(item) > get_tokens(result).count(item):  
                msg = u"kažkuris %s nereikalingas"
            else:
                msg = u"prie %s kažko trūksta"
                
        # msgs .append( "some " +code_highlight(item) + " is not exactly needed" )
        msgs .append( msg % code_highlight(item)  )

    msgs_unnecessary = msgs[:] # TODO use..
    
    if unnecessary:
        msgs.append("")  # separator 

    for item in required:
        msg = "Tikimasi daugiau %s"
        if not item in placeholder:
            msg = "Tikimasi %s"
        unnecessary_having_fragments_of_item = [un_item for un_item in unnecessary if item in un_item]
        # todo:  loop over tokens instead of placeholder.count(item)
        if placeholder.count(item) == len(unnecessary_having_fragments_of_item):
            msg = "Tikimasi %s"
            # if len(unnecessary_having_fragments_of_item) == 1: # simplest case
            #     msg = "Vietoj "+code_highlight(unnecessary_having_fragments_of_item[0]) +" tikimasi %s"

        # msgs .append(  code_highlight(item) + " is expected "  )
        msgs .append( msg % code_highlight(item)  )
    
    msgs_required = msgs[len(msgs_unnecessary)+ (1*bool(len(msgs_unnecessary)))  :] # +1 for separator
    
    if return_what == 'all':
        return msgs
    
    if return_what == 'unnecessary':
        return msgs_unnecessary
    
    if return_what == 'required':
        return msgs_required
    

def placeholder_smart_compare(placeholder, expected, human_nr=None, **hints_kwargs ):
    """Compares placeholder code with expected by tokens -- so spacing in expressions is ignored.
    Can have extra lists of `required`/missing/expected and `unnecessary` strings"""
    tokens_kwargs = {} # possible use -- best would be to filter them from  **kwargs
    a_tokens = get_tokens(placeholder, **tokens_kwargs)
    b_tokens = get_tokens(expected, **tokens_kwargs)
    
    # if placeholder == expected:
    if a_tokens  == b_tokens:
        # failed( "DBG: "+"<br>"+str(a_tokens)+"<br>"+str(b_tokens) )
        passed()
        return

    else:
        msgs = hints_by_token_comparison(placeholder, expected, **hints_kwargs)
        # if human_nr:
            # msgs.insert(0, "Placeholder nr. %s:" %(human_nr))
        failed( '<br />'.join(msgs) )
        # return '<br />'.join(msgs) 
        return  msgs # for web2py_tutor. Or we could call directly:  hints_by_token_comparison



if __name__ == '__main__':
    # SOME TESTS
    print( hints_by_token_comparison( '"a" b',  expected='"a" "b"' ) )

    asd
    print()
    print( get_tokens('return CAT( "labas ", B("pasauli"), "!"  )' ))
    print( placeholder_smart_compare('return CAT( "labas ", "pasauli" )', 'return CAT( "labas ", B("pasauli"), "!"  )') )
    print( placeholder_smart_compare(u'SPAN( "ąžlabas " , _style=""),', 'SPAN( "labas " , _style="color:blue"),') )
    print("\n"*10)
    
    # placeholder_smart_compare(placeholder='has_money == True', expected='has_money', unnecessary=['=='], required='has_money')
    print( hints_by_token_comparison(input='has_money == True', expected='has_money',  limit_hints=5) )
    print( hints_by_token_comparison(input='len(data)>0', expected='data',  limit_hints=5) )

    a = 'sum( a )'
    b = 'sum(a)'
    a_tokens = get_tokens(a)
    b_tokens = get_tokens(b)
    print ("spaced:   ", a_tokens)
    print ("no spaces:", b_tokens)
    print( a_tokens == b_tokens )
    

    # placeholder_smart_compare("]", expected="bla]")
    placeholder_smart_compare("[", expected="[bla")  # ERRR need smarter tokenizer 
    

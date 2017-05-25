import re

def task(task_code):
    entity = 'task'
    lines = task_code.split("\n")
    if lines[0] .startswith("###TASK"):
        name = lines.pop(0)

    children = placeholders = []
    student_lines = []
    for nr, line in enumerate(lines):
        if line.strip() == "###GROUP_LINES":
            # print "dbg group"
            line = ""
            while nr < len(lines)-1:
                next = lines.pop(nr+1)
                if next.strip() == "###GROUP_LINES_END":
                    break
                line += '\n'+ next
            # print "dbg:", line
        p = placeholder( line )

        if p['match']:
            placeholders.append( p )
            lines[nr] = p['result_code']
            p['line_nr'] = nr

            line_4student = lines[nr].replace( p['expected'], p['given'] ) # insert student stuff...
        else:
            line_4student = line

        student_lines.append( line_4student )

    result_code  = '\n'.join( lines )
    student_code = '\n'.join( student_lines )


    return locals()

# def subtask():
    # pass

def placeholder(code):
    """analyze code for placeholder directive"""
    entity = 'placeholder'
    re_placeholder = re.compile(r"###PLACEHOLDER:?(.*?)--\>(.+)" , re.DOTALL)

    # in **multiline** separate directive from code
    directive_parts = []
    clean_code = []
    for line in code.split('\n'):
       if '###' in line:
           line, directive_part = line.split("###", 1)
           directive_parts.append( directive_part.rstrip() )
       clean_code.append( line.rstrip() )
    directive = "###" + '\n'.join(directive_parts)
    result_code = "\n".join(clean_code)


    match = re_placeholder.search(directive)
    # match = re_placeholder.search(code)
    if match:
        expected, given = match.group(1).strip(), match.group(2).strip() # todo: maybe implement nonstrip option -- for indentation questions
        # given = " " + given + " "  # surround by spaces -- for easier manipulation...
        if expected=="":  # shortcut when we want to replace all # looks like: ###PLACEHOLDER:-->sth...
            expected = result_code
            # prepend indentation of first line to placeholder 
            # print "expected:", (repr( expected ))
            indentation = expected[ : -len( expected.lstrip() ) ] 
            given = indentation + given
        # result_code = re.sub(re_placeholder, "", result_code)  # clear directive from code
        offset_in_line = result_code.find( expected )
        # result_line_OKanswered = result_line.replace( expected, given )

    return locals()


if __name__ == '__main__':
    code = """
    def ftest():
        if True:
            ###GROUP_LINES
            print("labas "),  ###PLACEHOLDER: --> SPAN( "labas " , _style=""),
            print("Pasauli"),  ### "Pasauli",
            ###GROUP_LINES_END
        print("!")
    """
    t = task( code )
    from pprint import pprint
    pprint( t )

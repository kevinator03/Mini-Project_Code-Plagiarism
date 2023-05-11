import pyparsing
import re
import io
import  tokenize

def remove_comments_and_docstrings(source):
    """
    Returns 'source' minus comments and docstrings.
    """
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        # The following two conditionals preserve indentation.
        # This is necessary because we're not using tokenize.untokenize()
        # (because it spits out code with copious amounts of oddly-placed
        # whitespace).
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        # Remove comments:
        if token_type == tokenize.COMMENT:
            pass
        # This series of conditionals removes docstrings:
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
        # This is likely a docstring; double-check we're not inside an operator:
                if prev_toktype != tokenize.NEWLINE:
                    # Note regarding NEWLINE vs NL: The tokenize module
                    # differentiates between newlines that start a new statement
                    # and newlines inside of operators such as parens, brackes,
                    # and curly braces.  Newlines inside of operators are
                    # NEWLINE and newlines that start new code are NL.
                    # Catch whole-module docstrings:
                    if start_col > 0:
                        # Unlabelled indentation means we're inside an operator
                        out += token_string
                    # Note regarding the INDENT token: The tokenize module does
                    # not label indentation inside of an operator (parens,
                    # brackets, and curly braces) as actual indentation.
                    # For example:
                    # def foo():
                    #     "The spaces before this docstring are tokenize.INDENT"
                    #     test = [
                    #         "The spaces before this string do not get a token"
                    #     ]
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    return out

def preprocessing(prog):
    flag1 = 0  # to check if a data type is encountered 
    loc = 0 # to store the index of first occurence of single line comment
    flag2 = 0   # once flag1 = 1, it keeps checking if a variable is encountered

    data_types = ['int', 'long', 'double',
                'boolean', 'char', 'string', 'void', 'float']     # to store the data types which will help checking for integers and functions

    special_names = []   # to store variable, function and class names
    
    prog = prog.lower()

    comment = pyparsing.nestedExpr("/*","*/").suppress() # using a parser to remove multi-line comments quickly
    prog = comment.transformString(prog)

    prog = remove_comments_and_docstrings(prog)

    prog = prog.strip()     # remove trailing and leading white spaces

    lst_string = [prog][0].split('\n')       # breaking the prog into list of individual lines
    normalised_code = []        # will eventually store the final normalised code
    no_comments_code = []

    no_comments_string = ""                 # to remove comments
    for line in lst_string:
        line = line.split()
        for i in line:
            loc = i.find('//')
            if loc >= 0:
                no_comments_string += i[0:loc] + ' '
                break
            no_comments_string += i + ' '
        if no_comments_string != '':
            no_comments_code.append(no_comments_string)
        no_comments_string = ""

    lst_string = no_comments_code
    no_comments_code = []

    for line in lst_string:
        line = line.split()
        for i in line:
            loc = i.find('#')
            if loc >= 0:
                no_comments_string += i[0:loc] + ' '
                break
            no_comments_string += i + ' '
        if no_comments_string != '':
            no_comments_code.append(no_comments_string)
        no_comments_string = ""

    for i in range(0, len(no_comments_code)):        
        line = [word for word in re.split("\W+",no_comments_code[i])]
        no_comments_code[i] = ' '.join(line)


    temp_string = ""                 # parsing the string to detect function and variable names
    for line in no_comments_code:
        line = line.split()
        for i in line:

            if flag1 == 1:
                if re.search("^[a-zA-Z_$]", i) is not None and i not in data_types:
                    flag2 = 1
                else:
                    flag2 = 0

            if flag2 == 1:      # this if statement handles variable detection
                special_names.append(i)
                #print(i)
                flag2 = 0
            
            if i in data_types or i == "class":
                flag1 = 1      

            temp_string += i + ' '

        flag1 = 0
        normalised_code.append(temp_string)
        temp_string = ""


    for i in range(0, len(normalised_code)):        
        line = [word for word in re.split("\W+",normalised_code[i]) if word.lower() not in special_names]
        normalised_code[i] = ' '.join(line)

                
    str1 = ''            
    for i in normalised_code:
      if i != '':
        str1 = str1 + i + '\n'

    str1 = str1[:-1]
    return str1

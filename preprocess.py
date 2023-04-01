import pyparsing
import re



def preprocessing(prog):
    flag1 = 0  # set it to 1 when we encounter comment start
    flag2 = 0  # for variables 

    data_types = ['int', 'long', 'double',
                'boolean', 'char', 'string', 'void', 'float']     # to store the data types which will help checking for integers and functions

    special_names = []   # to store variable, function and class names
    
    prog = prog.lower()

    comment = pyparsing.nestedExpr("/*","*/").suppress() # using a parser to remove multi-line comments quickly
    prog = comment.transformString(prog)

    prog = prog.strip()     # remove trailing and leading white spaces

    lst_string = [prog][0].split('\n')       # breaking the prog into list of individual lines
    normalised_code = []        # will eventually store the final normalised code
    no_comments_code = []

    no_comments_string = ""                 # to remove comments
    for line in lst_string:
        line = line.split()
        for i in line:
            if i == '//':
                flag1 = 1
            if flag1 == 0:
                no_comments_string += i + ' '
        if no_comments_string != '':
            no_comments_code.append(no_comments_string)
        no_comments_string = ""
        flag1 = 0

    for i in range(0, len(no_comments_code)):        
        line = [word for word in re.split("\W+",no_comments_code[i])]
        no_comments_code[i] = ' '.join(line)

    temp_string = ""                 # parsing the string to detect function and variable names
    for line in no_comments_code:
        line = line.split()
        for i in line:

            if flag2 == 1:      # this if statement handles variable detection
                special_names.append(i)
                flag2 = 0
            
            if i in data_types or i == "class":
                flag2 = 1      

            temp_string += i + ' '

        flag2 = 0
        normalised_code.append(temp_string)
        temp_string = ""


    for i in range(0, len(normalised_code)):        # start from line 3 to avoid picking up a variable name as part of the class name which is sometimes common
        line = [word for word in re.split("\W+",normalised_code[i]) if word.lower() not in special_names]
        normalised_code[i] = ' '.join(line)


    # for i in range(0, len(normalised_code)):
    #     line = [word for word in re.split("\W+",normalised_code[i]) if word.lower() not in func_names]
    #     normalised_code[i] = ' '.join(line)
                
    str1 = ''            
    for i in normalised_code:
      if i != '':
        str1 = str1 + i + '\n'

    str1 = str1[:-1]
    return str1



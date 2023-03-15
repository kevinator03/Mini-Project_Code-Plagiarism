import nltk

import re

# import nltk for stopwords
# from nltk.corpus import stopwords
# stop_words = set(stopwords.words('english'))

program = """public class ReverseNumberExample1   
{  
public static void main(String[] args)   // this is the main class
{  
int number = 987654, reverse = 0;  // reverse is to store the reverse of the number
while(number != 0)   // while condition
{  
int remainder = number % 10;  
reverse = reverse * 10 + remainder;  // taking individual digits of the number backwards
number = number/10;  
}  
System.out.println("The reverse of the given number is: " + reverse);  // the required output
}  
}  """

print("Input Code: ")
print(program)

flag1 = 0  # set it to 1 when we encounter comment start
flag2 = [0, 0, 0, 0, 0, 0, 0]  # for variables

var_names = []
var_dict = {}

var_count = [0, 0, 0, 0, 0, 0, 0]      # to keep track of variables in the following order: int double String char boolean long float
ctr = 0                 # to keep count of all variables for dummy variable naming

program = program.lower()
# program = re.sub(r'\d+','',program)   # removing numbers
# program = re.sub(r'[^\w\s]','', program)  # removing all punctuation except words and space
program = program.strip()     # remove trailing and leading white spaces

lst_string = [program][0].split('\n')
# print(lst_string)
normalised_code = []

no_comments_string = ""
for line in lst_string:
    line = line.split()
    j = 0
    for i in line:
        if i == '//':
            flag1 = 1

        if i == 'int':
            flag2[0] = 1
        if i == 'double':
            flag2[1] = 1
        if i == 'string':
            flag2[2] = 1
        if i == 'char':
            flag2[3] = 1
        if i == 'boolean':
            flag2[4] = 1
        if i == 'long':
            flag2[5] = 1
        if i == 'float':
            flag2[6] = 1
        
        
        if i == '=' and flag2[0] == 1:
            j -= 1
            # no_comments_string = no_comments_string.replace(no_comments_string[-1], dummy)
            var_names.append(line[j])
            j += 1
        if i == '=' and flag2[1] == 1:
            var_count[1] += 1
        if i == '=' and flag2[2] == 1:
            var_count[2] += 1
        if i == '=' and flag2[3] == 1:
            var_count[3] += 1
        if i == '=' and flag2[4] == 1:       # lines 47-60 keep track of the various variables
            var_count[4] += 1
        if i == '=' and flag2[5] == 1:
            var_count[5] += 1
        if i == '=' and flag2[6] == 1:
            var_count[6] += 1

        if flag1 == 0:
            no_comments_string += i + ' '
        j += 1
    
    for i in range(0, len(flag2)):
        flag2[i] = 0
    normalised_code.append(no_comments_string)
    no_comments_string = ""
    flag1 = 0

for name in var_names:
    dummy = "var" + str(ctr)
    var_dict[name] = dummy
    ctr += 1

for i in range(3, len(normalised_code)):
    for name in var_names:
        if name in normalised_code[i]:
            normalised_code[i] = normalised_code[i].replace(name, var_dict[name])

print("\nNormalised code: ")
for line in normalised_code:
    print(line)


# print("Number of variables are: ")
# print(f"Integers: {var_count[0]}, Double: {var_count[1]}, Strings: {var_count[2]}, Char: {var_count[3]}, Boolean: {var_count[4]}, Long: {var_count[5]}, Float: {var_count[6]}")

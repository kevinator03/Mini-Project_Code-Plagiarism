# stores the source code
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

public int random(int a)
{
System.out.println("Hello there");
}
}  """

print("Input Code: ")
print(program)

flag1 = 0  # set it to 1 when we encounter comment start
flag2 = 0  # for variables 

data_types = ['int', 'long', 'double',
              'boolean', 'char', 'string', 'void', 'float']     # to store the data types which will help checking for integers and functions

var_names = []
func_names = []

var_dict = {}           # to store correct mapping of actual variable names to dummy names
func_dict = {}          # same purpose for functions

ctr = 0                 # to keep count of all variables for dummy variable naming

program = program.lower()

program = program.strip()     # remove trailing and leading white spaces

lst_string = [program][0].split('\n')       # breaking the program into list of individual lines
normalised_code = []        # will eventually store the final normalised code

no_comments_string = ""                 # to remove comments
for line in lst_string:
    line = line.split()
    j = 0
    for i in line:
        if i == '//':
            flag1 = 1

        if i in data_types:
            flag2 = 1

        if i == '=' and flag2 == 1:      # this if statement handles variable detection
            j -= 1
            var_names.append(line[j])
            j += 1

        if i in data_types:
            j += 1
            if '(' in line[j]:          # characteristic of a function is a data type and an opening round bracket soon after
                loc = line[j].find('(')
                func_names.append(line[j][0:loc])
            j -= 1

        if flag1 == 0:
            no_comments_string += i + ' '
        j += 1

    flag2 = 0
    normalised_code.append(no_comments_string)
    no_comments_string = ""
    flag1 = 0   # assuming you don't declare two different types of variable in the same line

for name in var_names:
    dummy = "var" + str(ctr)
    var_dict[name] = dummy      # setting up the mapping of variable names and dummy values
    ctr += 1

ctr = 0     # reset counter variable before starting function mapping

for name in func_names:
    dummy = "func" + str(ctr)
    func_dict[name] = dummy
    ctr += 1

for i in range(3, len(normalised_code)):        # start from line 3 to avoid picking up a variable name as part of the class name which is sometimes common
    for name in var_names:
        if name in normalised_code[i]:
            normalised_code[i] = normalised_code[i].replace(
                name, var_dict[name])

for i in range(0, len(normalised_code)):
    for name in func_names:
        if name in normalised_code[i]:
            normalised_code[i] = normalised_code[i].replace(
                name, func_dict[name])

print("\nNormalised code: ")
for line in normalised_code:
    print(line)

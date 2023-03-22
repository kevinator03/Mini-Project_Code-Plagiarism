def preprocessing(prog):
    flag1 = 0  # set it to 1 when we encounter comment start
    flag2 = 0  # for variables 

    data_types = ['int', 'long', 'double',
                'boolean', 'char', 'string', 'void', 'float']     # to store the data types which will help checking for integers and functions

    var_names = []
    func_names = []

    var_dict = {}           # to store correct mapping of actual variable names to dummy names
    func_dict = {}          # same purpose for functions

    ctr = 0                 # to keep count of all variables for dummy variable naming

    prog = prog.lower()

    prog = prog.strip()     # remove trailing and leading white spaces

    lst_string = [prog][0].split('\n')       # breaking the prog into list of individual lines
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
                
    return normalised_code

# for similarity checking
def levenshtein(a, b):
    len_a = len(a);
    len_b = len(b);
    dp = [[0 for i in range(len_b)] for j in range(len_a)]

    # pad the strings to make it 1-based
    a = "#" + a;
    b = "#" + b;

    # dp(string, empty) = length of string
    for i in range(len_a):
        dp[i][0] = i;
    for j in range(len_b):
        dp[0][j] = j;

    # dp table building steps
    for i in range(1, len_a):
        for j in range(1, len_b):
            if a[i] == b[j]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(
                dp[i-1][j] + 1,
                dp[i][j-1] + 1,
                dp[i-1][j-1] + 1
                )

    # print the dp table
    # for i in range(len_a):
    #     for j in range(len_b):
    #         print(dp[i][j], end="")
    #         if j + 1 == len_b:
    #             print()
    #         else:
    #             print(end=" ")
    
    return dp[len_a - 1][len_b - 1]

# stores the source code
prog1 = """public class ReverseNumberExample1                 
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

# stores the source code
prog2 = """public class ReverseNumberExample1                 
{  
public static void main(String[] args)   // this is the main class
{  
int number = 987654, reverse = 0;  // reverse is to store the reverse of the number
while(number != 0)   // while condition
{  
int Rem = number % 10;  
rev = rev * 10 + Rem;  // taking individual digits of the number backwards
number = number/10;  
}  
System.out.println("The reverse of the given number is most probably: " + rev);  // the required output
}
}  """

print("Input Code 1: ")
print(prog1)

print("Input Code 2: ")
print(prog2)

final_code1 = preprocessing(prog1)
final_code2 = preprocessing(prog2)

ind_dist = 0        # to store the Levenshtein distance comparing line by line
total_dist = 0      # to store the Levenshtein distance by comparing the entire code

print("\nNormalised code 1: ")
for line in final_code1:
    print(line)

print("\nNormalised code 2: ")
for line in final_code2:
    print(line)

for line1, line2 in zip(final_code1, final_code2):
    ind_dist = levenshtein(line1, line2)
    total_dist += ind_dist

print(f"The total Levenshtein distance between the two source codes is {total_dist}")

len1, len2 = 0, 0

for line1, line2 in zip(final_code1, final_code2):
    len1 += len(line1)
    len2 += len(line2)

Sab = 1 - total_dist/max(len1, len2)    # to store the similarity value of the two strings

print(f"The percentage of similarity is {Sab*100}%")

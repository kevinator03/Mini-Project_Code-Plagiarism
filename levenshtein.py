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
        dp[i][0] = i
    for j in range(len_b):
        dp[0][j] = j

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
    for i in range(len_a):
        for j in range(len_b):
            print(dp[i][j], end="")
            if j + 1 == len_b:
                print()
            else:
                print(end=" ")
    
    return dp[len_a - 1][len_b - 1]


def use_levenshtein(final_code1, final_code2):
    ind_dist = 0        # to store the Levenshtein distance comparing line by line
    total_dist = 0      # to store the Levenshtein distance by comparing the entire code

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
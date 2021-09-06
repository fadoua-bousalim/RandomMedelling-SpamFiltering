import random


def read(filename):
# reads out the input text file 
    istream = ""
    with open(filename) as f:
        for element in f:
            istream = istream + element
        idata = istream.splitlines()
        temp = ""
        for phrases in idata:
            temp = temp + phrases + " "
        return temp

def words(temp):
    L = []
    w = ""
# forms word list
    for i in range(0, len(temp)):
        w = w+ temp[i]
        if temp[i] == " ":
            L.append(w)
            w = ""
    return L

def words_in_dictionary(L):
# returns the words in the dictionary  in the training data set
    dictionary = {}
    for i in range(0, len(L) - 2):
        value_key = L[i] + L[i+1]
        if value_key in dictionary.keys():
            dictionary[value_key].append(L[i + 2])
        else:
            dictionary[value_key] = [L[i], L[i + 2]]
    return dictionary

def text_generated(dico, L):
# generates character string
    r = random.randint(0, len(L) - 3)
    k0 = L[r] + L[r+1]

    output_text =k0
    with open(output_file, "a") as o:
        o.writelines("Text generated:" + '\n')
        o.writelines("" + '\n')

    n=0
    while n < max_lines:
        while len(output_text) <= 80: 
        # width of the text
            new = dictionary[k0]
            # print("new word set:", new_word_set)
            freq = random.randint(1, len(new) - 1)
            element = new[freq]
            # print(" random integer new word:", freq, new_word)
            output_text = output_text + element
            # print("sonnet_string:", output_text)
            k = k0 + element
            # print("new_key:", new_key)
            k0 = k[len(new[0]):len(k)]
            # print("initial_key:", initial_key)
        else:
            with open(output_file, "a") as text_line:
                text_line.writelines(output_text + '\n')
                print("text_line", text_line)
                n = 1 + n
                output_text = ""
                # print("initial key:", initial_key)
                # print("number of lines:", num_lines)
    return


input_file = "Text.txt"
output_file = "result.txt"

max_lines = 3
# length of the text generated
temp = read(input_file)
L = words(temp)
dictionary = words_in_dictionary(L)
text_generated(dictionary, L)
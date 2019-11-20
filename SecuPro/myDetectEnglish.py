import string
ENG_DICT = []
file_input = open("dictionary.txt").read()
ENG_DICT = file_input.split('\n')

STN = "This is an information security class 2019 $%##!$"
TempSTN = []
LETTERSwithWhiteSpace = string.ascii_letters + " "
for c in STN:
    if c in LETTERSwithWhiteSpace:
        if c is not '':
            TempSTN.append(c)
STN = ''.join(TempSTN)
STN = STN.upper().split(" ")
print(STN)

matchNum = 0

for word in STN:
    if word in ENG_DICT:
        matchNum +=1
print("일치율 :", (matchNum/len(STN)) * 100)

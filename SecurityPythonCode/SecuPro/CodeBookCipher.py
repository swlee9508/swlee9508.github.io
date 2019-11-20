
# ### 수작업으로 만들었음...
# decBook = {
#     "2": "H",
#     "3": "e",
#     "1": "l",
#     "4": "o",
#     "9": "W"
#     "8": "r"
#     "7": "d"
# }


# 자동으로 decBook을 만드는 함수...
def makeDecCodeBook(encBook):
    decBook = {}
    for k in encBook:
        val = encBook[k]
        decBook[val] = k
    return decBook

## encryption 과정
## input : msg, encBook
## output : output

def encWithCodeBook(msg, encBook):
    output = ""
    for m in msg:
        if m in encBook: # 만약 msg 의 값 한개 씩 읽어와서 encBook 에 있으면 그것을 변환해서 output 에 붙여준다.
            output += encBook[m]
        else:
            output += m
    return output

def encWithCodeBook2(msg, encBook):
    for m in msg:
        if m in encBook: # 다른 방식의 인코딩
            msg = msg.replace(m, encBook[m])
        else:
            msg += m
    return msg



## decryption 과정
# input : output, decBook
# output : PlainText

def decWithCodeBook(output, decBook):
    PlainText = ""
    for m in output:
        if m in decBook:
            PlainText += decBook[m]
        else:
            PlainText += m
    return PlainText

def decWithCodeBook2(output, decBook):
    for m in output:
        if m in decBook:
            output = output.replace(m, decBook[m])
        else:
            output += m
    return output


def encdecWithCodeBook(input, codeBook): ## encode decode 과정을 한번에 합친 함수
    for m in input:
        if m in codeBook:
            input = input.replace(m, codeBook[m])
        else:
            input += m
    return input


# main...

encBook = {
    "H": "2",
    "e": "3",
    "l": "1",
    "o": "4",
    "W": "9",
    "r": "8",
    "d": "7"
}

decBook = makeDecCodeBook(encBook)
print(decBook)

msg = "Hello World"

cipher = encWithCodeBook(msg, encBook)
print(cipher)

cipher2 = encWithCodeBook2(msg, encBook)
print(cipher2)

plaintext = decWithCodeBook(cipher, decBook)
print(plaintext)

plaintext2 = decWithCodeBook2(cipher2, decBook)
print(plaintext2)


cipher3 = encdecWithCodeBook(msg, encBook)
print(cipher3)

plaintext3 = encdecWithCodeBook(cipher3, decBook)
print(plaintext3)

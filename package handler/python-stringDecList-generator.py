strList = ""
for x in range(256):
    char = chr(x)
    strList += char
    print(f"{x} : " + char)
    strList += "\n"
print(strList[0:len(strList)])
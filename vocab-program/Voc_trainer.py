import os
import ast
import random
from termcolor import colored
def list_to_string(lst):
    return " and ".join(str(elem) for elem in lst)

def get_index(lst, item):
    index = [idx for idx,x in enumerate(lst) if x == item][0]
    return index

prefix = input("enter path to directory: ") + "\\"

file = open(prefix + "Voc.txt","r")
AllLists = []

for element in file.readlines():
    if(element != "\n"):
        AllLists.append(element.replace("\n",""))

repeat = True
if(len(AllLists) == 0):
    action = "\c"
else:
    print("The available lists are {0} which one do you want to open? Or do you want to create a new list (\c)?".format(" , ".join(AllLists)))
    action = input("")
if (action == "\c"):
    name = "\c"
    while name == "\c" or name in AllLists:
        name = input("Name your list: ")
        if name == "\c":
            print("The name can't be \c!")
        elif name in AllLists:
            print("This list already exists")
        
    List = []
    x = input("Name every vocab or sentence in the other language sperated by a # if more versions and seperated by a \",\" if new vocab:\n")
    y = input("Name every vocab or sentence in your language seperated by a # if more versions and seperated by a \",\" if new vocab:\n")

    resultX = []
    resultY = []

    TempList = x.split(",")
    for element in TempList:
        resultX.append(element.split("#"))
        
    TempList = y.split(",")
    for element in TempList:
        resultY.append(element.split("#"))
            
    VocabList = open(prefix + name + ".txt","w")
    VocabList.write(str(resultX)+"§"+str(resultY))
        
    file = open(prefix + "Voc.txt", "a")
    file.write("\n" + name)
elif (action in AllLists):
    if (input("Do you want to delete(del) or open this List?: ") == "del"):
        os.remove(prefix + action + ".txt")
        AllLists = open(prefix + "Voc.txt", "r").readlines()
        NewLists = []
        for element in AllLists:
            if(element != action):
                NewLists.append(element)
            
        file = open(prefix + "Voc.txt", "w")
        for element in NewLists:
            file.write(element)
            
    else:
        while repeat:
            try:
                pick = int(input("random(1), only from other language to your language(2) or only from your language to other language(3): "))
            except:
                pick = 1
            current_mode = pick
            List = open(prefix + action + ".txt","r").readline().split("§")
            prev_ol = ast.literal_eval(List[0])
            wrong_ol = []
            temp_yl = []
            ol = []
            prev_yl = ast.literal_eval(List[1])
            yl = []

            vocabs = len(prev_ol)
            print(str(vocabs) + " out of " + str(len(prev_yl)))

            numberList = list(range(1,vocabs + 1))
            random.shuffle(numberList)

            for i in range(vocabs):
                ol.append(prev_ol[numberList[i]-1])
                wrong_ol.append(prev_ol[numberList[i]-1])
                yl.append(prev_yl[numberList[i]-1])
                temp_yl.append(prev_yl[numberList[i]-1])

            while len(wrong_ol) > 0:
                for i in range(len(yl)):
                    if pick == 1:
                        current_mode = random.randint(2,4)
                    if current_mode == 2:
                        question = list_to_string(ol[i])
                        print ("What is "+ colored(question,attrs=["bold"],color="blue") + " translated to your language? seperate all possible answers with a comma")
                    else:
                        question = list_to_string(yl[i])
                        print ("What is "+ colored(question,attrs=["bold"],color="blue") + " translated to the other language? seperate all possible answers with a comma")
                    
                    answer = input("").split(",")
                    
                    if current_mode == 2:
                        right = len(answer) == len(yl[i])
                        if right:
                            for k,j in enumerate(answer):
                                if j.lower() != yl[i][k].lower():
                                    right = False
                                    break
                        if right:
                            print ("That is right!")
                            idx = get_index(wrong_ol, ol[i])
                            del wrong_ol[idx]
                            del temp_yl[idx]
                        else:
                            print("Not quite the answer(s) was/were: " + colored(list_to_string(yl[i]),attrs=["bold"],color="blue"))
                    else:
                        right = len(answer) == len(ol[i])
                        if right:
                            for k,j in enumerate(answer):
                                if j.lower() != ol[i][k].lower():
                                    right = False
                                    break
                        if right:
                            print ("That is right!")
                            idx = get_index(wrong_ol, ol[i])
                            del wrong_ol[idx]
                            del temp_yl[idx]
                        else:
                            print("Not quite the answer(s) was/were: " + colored(list_to_string(ol[i]),attrs=["bold"],color="blue"))
                print ("test taken:")
                print("The vocabs you got wrong:")
                print(",".join(x[0] for x in wrong_ol))
                score = round(((vocabs - len(wrong_ol)) / vocabs) * 10) * 10
                print("your score is: " + str(score) + "%")
                print("you got " + str(vocabs - len(wrong_ol)) + " out of " + str(vocabs) + " vocabs correct!")
                ol = wrong_ol.copy()
                yl = temp_yl.copy()
            if input("Continue?: ").lower() == "n":
                repeat = False
            
    

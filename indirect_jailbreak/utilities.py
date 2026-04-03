import random
import math
import pickle as pkl

def generateRandomCharacter(capitalize: bool):
    if capitalize is True:
        return chr(random.randint(65, 90))
    else:
        return chr(random.randint(97, 122))

def insertRandomNumber(sequence: str):
    length = len(sequence)
    place = random.randint(0, length - 1)
    random_number = random.randint(0, 9)
    sequence = sequence[:place] + str(random_number) + sequence[place:]
    return sequence

def generateRandomSequence(capitalize: bool, length: int):
    sequence = ""
    for i in range(length - 1):
        sequence += generateRandomCharacter(capitalize)
    sequence = insertRandomNumber(sequence)

    return sequence

def getRandomCharFromList(l: list):
    return l[math.floor(random.random()*len(l))]

def extractNonAppearedCharactersList(string: str):
    # 'a' = 0x61 = 97, 'z' = 0x7A = 122
    obj = {}
    for i in range(0x61, 0x7B):
        obj[chr(i)] = True
    
    for ch in string:
        obj[ch] = False

    char_list = []
    for i in range(0x61, 0x7B):
        if obj[chr(i)] == True:
            char_list.append(chr(i))
    return char_list
def isCapitalLetter(ch: str):
    try:
        if ord(ch) >= ord('A') and ord(ch) <= ord('Z'):
            return True
        else:
            return False
    except Exception as e:
        raise e
def substituteIntoSmallLetter(ch: str):
    try:
        if isCapitalLetter(ch):
            return chr(ord(ch) + 32)
        else:
            return ch
    except Exception as e:
        raise e
def containsCapitalLetter(sequence: str):
    for ch in sequence:
        if isCapitalLetter(ch) is True:
            return True
    return False

GV_dir = "global_variable"
def getGlobalVariable(name):
    f = open(f"./{GV_dir}/{name}.pkl", "rb")
    value = pkl.load(f)
    f.close()
    return value
def setGlobalVariable(name, value):
    f = open(f"./{GV_dir}/{name}.pkl", "wb")
    pkl.dump(value, f)
    f.close()
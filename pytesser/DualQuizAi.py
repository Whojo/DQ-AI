import time
from PIL import Image#Work with
import PIL.ImageOps
import cv2
from pytesser import * #OCR
import wx  #screenshot
import win32com.client as comclt #Pressing Key
from random import randint
import win32api, win32con #doing some wild shit with the mouse


"""
Potential pb:
-add on the app :'(   ==> add blocker ? or wait 5s and press "esc"}
-regarder pour structure de la database qui va tout stocker



Voc:
-Battle Area : where you play (literally)
-Pre-Battle Area : Just before you play, the area with the play button and the score
-Main menu : It's anough clear i think...
"""

def StartANewRandGame():
    #I don't know if I am going to use it finally... I may create a second acount and let the algorithme play against itself
    """
    Look for a new opponent from the main menu and put it in the Pre-battke Area
    """
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.SendKeys("{Enter}")
    delay()
    wsh.SendKeys("a")
    delay(10)
    wsh.SendKeys(opponent)
    delay()


def LaunchGame():
    """
    Launch a game from the Pre-Battle Area to the Battle Area
    """
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.SendKeys("3")
    delay()


def EnterAnswer(answer):
    """
    the input answer must be a string between 1 and 4 (corresponding to its position)
    """
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.SendKeys(answer)
    delay()


def takeScreenshot(address):
    """
    Take a screenshot of the game and save it
    """
    width = 600 #Nox game screen width

    app = wx.App()
    screen = wx.ScreenDC()
    bmp = wx.Bitmap(width, 1080)
    mem = wx.MemoryDC(bmp)
    mem.Blit(0, 0, width, 1080, screen, 1920 - width, 0)
    del mem
    bmp.SaveFile(address, wx.BITMAP_TYPE_PNG)


def longest(list):
    """
    return the index of the longest string in the list
    """
    max, maxIndex = 0,0
    for i in range(len(list)):
        l = len(list[i])
        if l > max:
            max, maxIndex = l, i

    return maxIndex


def ReadQuestion():
    """
    In the battle Area, take a sreenshot and with a OCR, read the question
    and return it
    """
    address = r"C:\Users\guill\Desktop\Prog Simple\Projet\Duel Quizz AI\Code\pytesser\screenshot.png"
    address2 = r"C:\Users\guill\Desktop\Prog Simple\Projet\Duel Quizz AI\Code\pytesser\screenshot2.png"
    takeScreenshot(address)

    im = Image.open(address)
    im.crop((70, 220, 570, 350)).save(address2)#crop the image to get only the question
    im = Image.open(address2)
    question = image_to_string(im).replace("\n", "")

    return question


def isTheSame(elm1, elm2):
    """
    Compare two elements and return if they are the same (with a margin of accuracy)
    """
    return elm1 == elm2 #setting this for now, may change if ocr doesn't work well


def fileToList(address):
    """
    Read the file and return a list of list
    Which the sublist has as first element the question and the answer as second element

    Ps: In the DataBase.txt file, you have on each line a question and the correct
    answer separated by a '@'
    """
    file = open(address, "r", encoding="utf8")
    lines = file.read().split("\n")
    file.close()

    QandA = []
    for line in lines:
        QandA.append(line.split("@"))

    return QandA


def GetAnswer(question):
    """
    Compare the input question with the data base (with a margin of accuracy).
    If the question is in the data base, return the correct answer
    Otherwise retur None
    """
    address = r"C:\Users\guill\Desktop\Prog Simple\Projet\Duel Quizz AI\Code\DataBase.txt"
    QandA = fileToList(address)

    index = 0
    length = len(QandA)
    while index < length and not(isTheSame(question, QandA[index][0])):
        index += 1

    if index == length:
        return None
    return QandA[index][1]


def FindRightAnswer(answers):
    """
    Look for the green case in the screenshot to find the right answer
    """
    screenshot = r"C:\Users\guill\Desktop\Prog Simple\Projet\Duel Quizz AI\Code\pytesser\screenshot.png"
    address2 = r"C:\Users\guill\Desktop\Prog Simple\Projet\Duel Quizz AI\Code\pytesser\screenshot2.png"
    pos = [(550, 185), (550, 455), (755, 185), (755, 455)]

    takeScreenshot(screenshot)

    image = cv2.imread(screenshot)
    length = len(pos) - 1

    i = 0
    rightPixel = [26, 198, 114]
    pixel = image[pos[i][0],pos[i][1]]
    while i < length and (pixel[1] < rightPixel[1] - 20 or pixel[1] > rightPixel[1] + 20):
        i += 1
        pixel = image[pos[i][0],pos[i][1]]

    return answers[i]


def SaveRightAnswer(question, answers):
    """
    Save the correct answer in the data base with the question
    """
    import codecs

    dataBase = r"C:\Users\guill\Desktop\Prog Simple\Projet\Duel Quizz AI\Code\DataBase.txt"
    answer = FindRightAnswer(answers)

    file = codecs.open(dataBase, "a", "utf-8")
    file.write(question + "@" + answer + "\n")
    file.close()


def ReadPossibleAnswer():
    """
    Take a screenshot and read the 4 possible answers and return them in a list
    The order matter (check it the app)
    PS: this function is supposed to be called after ReadQuestion(), otherwise it won't work
    """
    screenshot = r"C:\Users\guill\Desktop\Prog Simple\Projet\Duel Quizz AI\Code\pytesser\screenshot.png"
    address2 = r"C:\Users\guill\Desktop\Prog Simple\Projet\Duel Quizz AI\Code\pytesser\screenshot2.png"
    answers = []

    pos = [(60, 520, 310, 655), (332, 520, 585, 655), (60, 725, 310, 855), (332, 725, 585, 855)]

    for i in range(len(pos)):
        im = Image.open(screenshot)
        PIL.ImageOps.invert(im.crop(pos[i])).save(address2)#crop the image to get only one answer (also inverse color to help the OCR to read)

        im = Image.open(address2)
        text = image_to_string(im).replace("\n", "")
        answers.append(text)
    return answers


def FindTheGoodOne(RightOne, answers):
    """
    Find the RightOne in the answers and return its index + 1 (with a margin of accuracy)
    """
    index = 0
    nbAnswers = len(answers) - 1

    while index < nbAnswers and not(isTheSame(RightOne, answers[index])):
        index += 1

    return index + 1


def GotToNextquestion():
    """
    Just go to next question... in the battle area
    """
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.SendKeys("{Enter}")
    delay()


def PickATopic():
    """
    Picks a topic if there is one
    """
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.SendKeys("e")
    delay()



def PlayATurn():
    """
    Simply play one turn in the battle area
    return if the answer have been found in the database
    """
    question = ReadQuestion()
    RightAnswer = GetAnswer(question)
    answers = ReadPossibleAnswer()

    if not(RightAnswer is None):
        EnterAnswer(FindTheGoodOne(RightAnswer, answers))
    else:
        EnterAnswer(str(randint(1,4)))
        SaveRightAnswer(question, answers)

    return not(RightAnswer is None)


def Training():
    """
    Call Play as many time as necessary to create the data base
    That is to say to learn
    Be carefull about the adds...
    """
    nbTrain = 30000
    FollowedRightAnswer = 0

    GoInTheGame()
    for i in range(nbTrain):
        StartANewRandGame()
        LaunchGame()
        Play(FollowedRightAnswer)
        Surrender()


def Play(FollowedRightAnswer):
    """
    When the algorithm is train then you can play against whoever you want
    Just be in the call this function
    """
    NbQuestion = 3 #number of question in a play

    LaunchGame()
    PickATopic()
    for i in range(NbQuestion):
        GotToNextquestion()
        FoundAnswer = PlayATurn()

        PrintStats(FoundAnswer, FollowedRightAnswer)

    Quit()
    delay(10)


def PrintStats(FoundAnswer, FollowedRightAnswer):
    """
    Print informations to help better understand what is happening
    """
    DataBase = r"C:\Users\guill\Desktop\Prog Simple\Projet\Duel Quizz AI\Code\DataBase.txt"
    nbTotalQuestion = 30000

    with open(DataBase, encoding="utf8") as data:
        questionSaved = len(data.read().split("\n"))
        if FoundAnswer:
            FollowedRightAnswer += 1
            print("Last " + str(FollowedRightAnswer) + "were correctly answer")

        else:
            print("Answer chosen randomly")
        print("There are currently " + str(questionSaved) + " questions saved")
        print("So this is equivalent to " + str("%.3f" % (questionSaved / nbTotalQuestion * 100)) + "%")


def Quit():
    """
    Quit the battle area
    """
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.SendKeys("{Esc}")
    delay()


def Surrender():
    """
    Surrender a game against a random
    """
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.SendKeys(opponent)
    delay()
    wsh.SendKeys("s")
    delay(5)
    wsh.SendKeys("2")
    delay(5)
    wsh.SendKeys("2")
    delay(5)


def GoInTheGame():
    """
    Click on the Nox emulator to have focus on the game
    """
    pos = (1200, 140)
    win32api.SetCursorPos(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pos[0],pos[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1],0,0)


def delay(t = 3):
    """
    Slow a bit this program to prevent it from doing action that cannot be done
    in the game as this one is loarding
    """
    time.sleep(t)


def IsSomeoneABich():
    """
    Check if someone has challenged me in the main menu
    """
    address = r"C:\Users\guill\Desktop\Prog Simple\Projet\Duel Quizz AI\Code\pytesser\screenshot3.png"
    takeScreenshot(address)

    im = PIL.ImageOps.invert(Image.open(address))
    popup = image_to_string(im)

    return "partie" in popup.lower()


def RefuseBattleRequest():
    """
    Check if someone has challenged me and if so then refuse
    """
    isHere = IsSomeoneABich()

    if isHere:
        wsh= comclt.Dispatch("WScript.Shell")
        wsh.SendKeys("1")
        delay()



#Main
# delay()
opponent = "e"
GoInTheGame()
Training()
# print(IsSomeoneABich())

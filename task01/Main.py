
import datetime
import glob
import os
import json


basePath = os.path.dirname(os.path.abspath(__file__))

sourceForNotes = os.path.join(basePath, "notes")
selectTypeFile = "*_note_*.json"

sourceForSettings = os.path.join(basePath, "settings")
selectFileSettings = "settings.json"
 

#--------------------------------------------------------------------------------------------------------
#view directory for found files
def readFilesFromDir (dirSource, filterFiles):
    os.chdir (dirSource)
    files = glob.glob(filterFiles)
    files.sort(key=lambda x: os.path.getmtime(x), reverse = True)  #Sort by Modification Time
    listFiles = files
    return listFiles

#--------------------------------------------------------------------------------------------------------
# read *.JSON
def readJSON (selctedNameFile):
    with open (selctedNameFile) as f:
            stringJSON = json.load(f)
            f.close()
    return stringJSON

#--------------------------------------------------------------------------------------------------------
# write *.JSON
def writeInFile (selctedNameFile, objForWrite):
    with open (selctedNameFile, 'w') as f:
        json.dump (objForWrite, f)
        f.close()

#--------------------------------------------------------------------------------------------------------
# Создание общего списка заметок из папки "notes"
def refreshListNotes (sourceForNotes,selectTypeFile):
    listNotes = readFilesFromDir (sourceForNotes,selectTypeFile)
    return listNotes

#--------------------------------------------------------------------------------------------------------
# Демонстрация списка всех заметок в папке "notes"
def showAllNotes (listNotes):
    for i in listNotes:
        strJSON = readJSON(os.path.join(sourceForNotes, i))
        note = {"Number" : strJSON ['idNote'], "Name" : strJSON ['headnote'], "Date": strJSON['lastdate'], "File": i }
        print ("{:<5}{:<20}{:<40}{:<80}".format(note['Number'], note['Name'], note['Date'], note['File']))

#--------------------------------------------------------------------------------------------------------
# Выбор определённой заметки в папке "notes"
def showSelectedNote (listNotes, noteNum): 
    res = False
    note = tuple 
    for i in listNotes:
        strJSON = readJSON(os.path.join(sourceForNotes, i))
        if (noteNum == int(strJSON ['idNote'])):
            note = (strJSON ['idNote'], strJSON ['headnote'], strJSON ['bodynote'], i)
            res = True
    if (res == True):
        print ("{:<5}{:<20}{:<40}{:<80}".format(strJSON ['idNote'], strJSON ['headnote'], strJSON['lastdate'], i))
        print (strJSON ['bodynote'])
        print ("-----END-----")
        return note
    else:
        print ("Заметка с указанным номером отсутствует")   
    
#--------------------------------------------------------------------------------------------------------
# Создание новых заметок в папке "notes"
def createNote (listNotes):
    print ("Введите заголовок для заметки:")
    headnote = str(input())
    if (len(headnote) == 0):
        headnote = "Unname"
    print ("Введите основной текст заметки:")
    bodynote = str(input())
    if (len(bodynote) == 0):
        bodynote = "Enter text for note, please"

    settingMaxID = readJSON(os.path.join(sourceForSettings, selectFileSettings))
    newMaxID = settingMaxID['maxID'] + 1

    numList = []
    for i in listNotes:
        strJSON = readJSON(os.path.join(sourceForNotes, i))
        numList.append(int(strJSON ['idNote']))

    flag = False
    while (flag == False):
        count = 0
        for i in numList:
            if (newMaxID == i):
                print (True)
                newMaxID = int(newMaxID) + 1
                count + 1

        if (count == 0):
            flag = True

    newNote = {"idNote" : newMaxID, "lastdate" : str(datetime.datetime.now()), "headnote": headnote, "bodynote" : bodynote }
    settingMaxID ['maxID'] = newNote ['idNote']
    newFileName = str(newNote['idNote']) + "_note_" + str(newNote['headnote']) + ".json"

    writeInFile (os.path.join(sourceForSettings, selectFileSettings), settingMaxID)
    writeInFile (os.path.join(sourceForNotes, newFileName), newNote)

#--------------------------------------------------------------------------------------------------------
# Редактирование выбранной заметки в папке "notes"
def editNote (listNotes, noteNum):
    note = showSelectedNote(listNotes, noteNum)
    if (note != None):
        editCount = 0
        print ("Желаете внести изменения?")
        userAnswer = answerUserYesOrNo ()

        if (userAnswer == 'Y'):
            print ("Внести изменения в заголовок заметки?")         #EDIT HeadNote
            userAnswer = answerUserYesOrNo ()
            if (userAnswer == 'Y'):
                oldHeadnote = note[1]
                editCount = editCount + 1
                print ("Введите новый заголовок для заметки:")
                newHeadnote = input()
                if (len(newHeadnote) == 0):
                    newHeadnote = oldHeadnote
                print ("Указан новый заголовок")
            else:
                print ("Отказ от внесения изменений в заголовок")

            print ("Внести изменения в текст заметки?")             #EDIT BodyNote
            userAnswer = answerUserYesOrNo()
            if (userAnswer == 'Y'): 
                oldBodynote = note[2]
                editCount = editCount + 1
                print ("editCoun: " + str(editCount)) 
                print ("Введите новый текст для заметки:")
                newBodynote = str(input())
                if (len(newBodynote) == 0):
                    newBodynote = oldBodynote
                print ("Указан новый текст")

            else:
                print ("Отказ от внесения изменений в текст")
            print (editCount)
            if (editCount > 0):
                editNote = {"idNote" : int(note[0]), "lastdate" : str(datetime.datetime.now()), "headnote": newHeadnote, "bodynote" : newBodynote }
                editFileName = str(editNote['idNote']) + "_note_" + str(editNote['headnote']) + ".json"
                os.rename (note[3], editFileName) 
                writeInFile (os.path.join(sourceForNotes, editFileName), editNote)
                return True
            else:
                print ("Нет изменений для внесения")
                return False
        else:
            print ("Отказ от внесения изменений в заметку")
            return False
    else:
        return False

#--------------------------------------------------------------------------------------------------------
# Удаление выбранной заметки в папке "notes"
def deleteNote (listNotes, noteNum):
    note = showSelectedNote (listNotes, noteNum)
    print ("Желаете удалить заметку?")
    userAnswer = answerUserYesOrNo()
    if (userAnswer == 'Y'):
        os.remove (note[3])
        return True
    else:
        return False
    
#--------------------------------------------------------------------------------------------------------
# Обработка ответа пользователя Yes/No на бесконечке
def answerUserYesOrNo ():
    while True:
        answer = str.upper(input("[Y]es or [N]o :"))
        try:
            if (answer == 'Y') or (answer == 'N'):
                return answer
            else:
                print ("Your entered no [Y] or [N]. Try again")   
        except:
            print ("You entered something, but it's not char")

#--------------------------------------------------------------------------------------------------------
# Вывод пунктов меню
def mainMenu ():
    print ('''  Please, select menu point.
    Entered number menu point [0-5] and taped [ENTER]
        [1] -- press for SHOW ME ALL NOTES 
        [2] -- press for SHOW ME SELECTED NOTE
        [3] -- press for CREATE NEW NOTE
        [4] -- press for EDIT NOTE
        [5] -- press for DELETE NOTE
        [0] -- press for EXIT
            ''')  

#--------------------------------------------------------------------------------------------------------
# Очистка экрана
clear = lambda: os.system ('cls')
clear ()

#--------------------------------------------------------------------------------------------------------
# Выбор пункта меню
print ("Hello, USER. Its NOTES. What you want?")        
while True:
    listNotes = refreshListNotes (sourceForNotes,selectTypeFile)
    mainMenu ()
    enteredNum = int(input())
    try:
        if (enteredNum == 1):                       # SHOW ALL
            showAllNotes (listNotes)
            print ("")
            listNotes = refreshListNotes (sourceForNotes,selectTypeFile)
        elif (enteredNum == 2):                     # SHOW SELECT
            print ("Enter note number for show:")
            noteNum = int(input())
            note = showSelectedNote (listNotes, noteNum)
            print ("")
            listNotes = refreshListNotes (sourceForNotes,selectTypeFile)
        elif (enteredNum == 3):                     # CREATE
            createNote (listNotes)
            print ("New note created!")
            print ("")
            listNotes = refreshListNotes (sourceForNotes,selectTypeFile)            
        elif (enteredNum == 4):                     # EDIT
            print ("Enter note number for edit:")
            noteNum = int(input())
            res4 = editNote (listNotes, noteNum)
            if (res4 == True):
                print ("Edited note successfully")
            else:
                print ("Edited note don't successfully")
            print ("")
            listNotes = refreshListNotes (sourceForNotes,selectTypeFile)
        elif (enteredNum == 5):                     # DELETE
            print ("Enter note number for delete:")
            noteNum = int(input())
            res5 = deleteNote (listNotes, noteNum)
            if (res5 == True):
                print ("Delete note successfully")
            else:
                print ("Delete note don't successfully")
            print ("")
            listNotes = refreshListNotes (sourceForNotes,selectTypeFile)
        elif (enteredNum == 0):                     # EXIT
            print ("GOOD BYE")
            break                
        else:
            print ("Your number out of range. Try again")

    except:
        print ("You entered something, but it's not number")
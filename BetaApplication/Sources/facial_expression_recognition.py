from tensorflow.keras.models import load_model
from time import sleep
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing import image
import cv2
import numpy as np
import threading
from datetime import datetime, timedelta
import webbrowser
import ctypes
import expression_gui
import os


ListWithPosibleCombinations = [
    ['Happy', 'Angry', 'Surprise'],
    ['Angry', 'Surprise', 'Angry'],
    ['Surprise', 'Happy', 'Sad'],
    ['Sad', 'Surprise', 'Angry']

]

ListWithCombinationsForGUI = [
    "Happy -> Angry -> Surprise -> Lock PC",
    "Angry -> Surprise -> Angry -> Deschide Youtube",
    "Surprise -> Happy -> Sad -> Porneste BS.Player",
    "Sad -> Surprise -> Angry -> Inchide aplicatia"

]


class FacialExpressionRecognition:
    def __init__(self):
        """ Constructorul clasei """
        self.face_classifier = cv2.CascadeClassifier(r'EmotionModel\haarcascade_frontalface_default.xml')
        self.classifier = load_model(r'EmotionModel\EmotionDetectorModel.h5')
        self.class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']
        self.cap = cv2.VideoCapture(0)
        self.label = ''
        self.counter = 0
        self.lockPC_bool = False
        self.ExpressionGUIObj = expression_gui.ExpressionGUI()



    def getMostCommon(self, ExpressionList):
        """ getMostCommon
        Description:
            Metoda care ia cea mai comuna expresie si verifica sa vada daca face parte dintr-o anumita combinatie

        Parameters:
            ExpressionList (list): Lista care contine secventa de expresii. Este folosita cate o lista la fiecare thread

        Returns:
            True: Daca combinatia a fost gasita cu success
            False: Daca combinatia nu a fost gasita

        """

        GuiCounter = 0
        self.ExpressionGUIObj.GuiBool = False
        for expression in ExpressionList:
            list_of_expressions = []
            end_time = datetime.now() + timedelta(seconds=self.ExpressionGUIObj.ExpressionTime)  # interval de timp a cat sa dureze detectia unei expresii (este parametrizabil)
            my_counter = self.counter       # un counter care numara fiecare expresie. Este folosit strict pentru a lua doar ultima expresie executata. Adica pentru a evida dublarea si astfel multiplicarea inutila
            while datetime.now() < end_time:
                if(my_counter != self.counter):
                    list_of_expressions.append(self.label)
                my_counter = self.counter
                sleep(self.ExpressionGUIObj.SamplingTime)

            if(len(list_of_expressions) <= 3):  # Masura de siguranta care obliga aplicatia sa faca clasificarea unei expresii doar daca are cel putin 4 esantioane/expresii!!!
                end_time = datetime.now() + timedelta(seconds=0.2)      # Daca nu detecteaza expresii, tot adauga timp si ramane in acest loop pana ajunge sa aiba cel putin 4 expresii.
                while datetime.now() < end_time:
                    if (my_counter != self.counter):
                        list_of_expressions.append(self.label)
                    my_counter = self.counter
                    if(len(list_of_expressions) <= 3):
                        end_time = datetime.now() + timedelta(seconds=0.2)
                    sleep(self.ExpressionGUIObj.SamplingTime)

            #print(list_of_expressions)
            #print(len(list_of_expressions))
            try:    # In mod normal daca este o lista goala returna eroare!
                CommonExpression = max(set(list_of_expressions), key=list_of_expressions.count) # se ia cea mai comuna expresie
            except ValueError:
                CommonExpression = ''
            if(expression != CommonExpression): # Daca expresia cea mai comuna nu coincide cu ce este intr-o combinatie (Eg: HappyAngrySurprise) atunci se returneaza False

                if(GuiCounter == 1):	# Contor folosit pentru adaugarea si stergerea elementelor din interfata grafica
                    self.ExpressionGUIObj.canvas.delete(self.GuiText_CombinationStartsWith)
                    self.ExpressionGUIObj.canvas.delete(self.GuiText_NeededCombination)

                    self.ExpressionGUIObj.canvas.delete(self.GuiText_0)
                elif(GuiCounter == 2):
                    self.ExpressionGUIObj.canvas.delete(self.GuiText_CombinationStartsWith)
                    self.ExpressionGUIObj.canvas.delete(self.GuiText_NeededCombination)

                    self.ExpressionGUIObj.canvas.delete(self.GuiText_0)
                    self.ExpressionGUIObj.canvas.delete(self.GuiText_1)

                return False
            else:
                if(GuiCounter == 0):
                    self.GuiText_0 = self.ExpressionGUIObj.canvas.create_text(100, 250, font=('Arial', 24, 'bold italic'), text=CommonExpression)
                    self.GuiText_CombinationStartsWith = self.ExpressionGUIObj.canvas.create_text(50, 350, font=('Arial', 14), anchor='nw', width=900, text="Secventa care incepe cu " + CommonExpression + " este: ")
                    if(CommonExpression == 'Happy'):
                        self.GuiText_NeededCombination = self.ExpressionGUIObj.canvas.create_text(100, 400, font=('Arial', 14, 'bold italic'), anchor='nw', width=900, text=ListWithCombinationsForGUI[0])
                    elif(CommonExpression == 'Angry'):
                        self.GuiText_NeededCombination = self.ExpressionGUIObj.canvas.create_text(100, 400, font=('Arial', 14, 'bold italic'), anchor='nw', width=900, text=ListWithCombinationsForGUI[1])
                    elif(CommonExpression == 'Surprise'):
                        self.GuiText_NeededCombination = self.ExpressionGUIObj.canvas.create_text(100, 400, font=('Arial', 14, 'bold italic'), anchor='nw', width=900, text=ListWithCombinationsForGUI[2])
                    elif(CommonExpression == 'Sad'):
                        self.GuiText_NeededCombination = self.ExpressionGUIObj.canvas.create_text(100, 400, font=('Arial', 14, 'bold italic'), anchor='nw', width=900, text=ListWithCombinationsForGUI[3])
                elif(GuiCounter == 1):
                    self.GuiText_1 = self.ExpressionGUIObj.canvas.create_text(450, 250, font=('Arial', 24, 'bold italic'), text=CommonExpression)
                elif(GuiCounter == 2):
                    self.GuiText_2 = self.ExpressionGUIObj.canvas.create_text(800, 250, font=('Arial', 24, 'bold italic'), text=CommonExpression)
                else:
                    #this should never happen!!
                    raise Exception("The number of expressions in a combination it's probably greater than 3!!")
                GuiCounter = GuiCounter + 1
                if(GuiCounter == 1):
                    sleep(0.5)
                    self.ExpressionGUIObj.LoadingWheel(215, 215)
                    self.firstLoadingWheel = self.ExpressionGUIObj.image
                    sleep(self.ExpressionGUIObj.LoadingWheelTime)
                    self.ExpressionGUIObj.GuiBool = True
                    self.ExpressionGUIObj.canvas.delete(self.firstLoadingWheel)
                    sleep(0.7)
                    self.ExpressionGUIObj.GuiBool = False
                elif(GuiCounter == 2):
                    sleep(0.5)
                    self.ExpressionGUIObj.LoadingWheel(565, 215)
                    self.secondLoadingWheel = self.ExpressionGUIObj.image
                    sleep(self.ExpressionGUIObj.LoadingWheelTime)
                    self.ExpressionGUIObj.GuiBool = True
                    self.ExpressionGUIObj.canvas.delete(self.secondLoadingWheel)
                    sleep(0.7)
                    self.ExpressionGUIObj.GuiBool = False
                else:
                    pass

        return True     # True doar daca combinatia a fost regasita cu success

    def thread1_method(self, ExpressionList):
        """ thread1_method
        Description:
            Metoda thread-ului care call-uie metoda de mai sus si verifica sa vada care din combinatiile stiute
            au fost executate cu success

        Parameters:
            ExpressionList (list): Lista care contine secventa de expresii. Este folosita cate o lista la fiecare thread

        Returns:

        """

        my_bool = self.getMostCommon(ExpressionList)
        if(my_bool):
            if(ExpressionList == ListWithPosibleCombinations[0]):  # Daca se executa combinatia Happy, Angry, Surprise, se va lock-ui calculatorul
                self.lockPC_bool = True
            elif(ExpressionList == ListWithPosibleCombinations[1]):    # Daca se executa combinatia Angry, Surprise, Angry se va deschide o pagina de Youtube
                self.GuiText_ActionTaken = self.ExpressionGUIObj.canvas.create_text(50, 450, font=('Arial', 14), anchor='nw', text="Se deschide youtube...")
                webbrowser.open("https://www.youtube.com")
                sleep(3)
                self.deleteGuiText()
            elif(ExpressionList == ListWithPosibleCombinations[2]):
                applicationExists = True
                try:
                    os.startfile(r"C:\Program Files (x86)\Webteh\BSplayerPro\bsplayer.exe")
                except FileNotFoundError:
                    applicationExists = False
                if(applicationExists):
                    self.GuiText_ActionTaken = self.ExpressionGUIObj.canvas.create_text(50, 450, font=('Arial', 14), anchor='nw', text="Se deschide BS.Player...")
                else:
                    self.GuiText_ActionTaken = self.ExpressionGUIObj.canvas.create_text(50, 450, font=('Arial', 14), anchor='nw', text="Nu se poate deschide BS.Player. Aceasta aplicatie probabil ca nu este instalata")
                sleep(3)
                self.deleteGuiText()
            elif(ExpressionList == ListWithPosibleCombinations[3]):
                self.ExpressionGUIObj.canvas.create_text(50, 450, font=('Arial', 14), anchor='nw', text="Se opreste aplicatia...")
                sleep(3)
                os._exit(1)


    def deleteGuiText(self):
        """ run_task
        Description:
            Metoda care sterge text-ul dinamic de pe pagina principala din interfata grafica

        Parameters:

        Returns:

        """
        self.ExpressionGUIObj.canvas.delete(self.GuiText_ActionTaken)
        self.ExpressionGUIObj.canvas.delete(self.GuiText_CombinationStartsWith)
        self.ExpressionGUIObj.canvas.delete(self.GuiText_NeededCombination)
        self.ExpressionGUIObj.canvas.delete(self.GuiText_0)
        self.ExpressionGUIObj.canvas.delete(self.GuiText_1)
        self.ExpressionGUIObj.canvas.delete(self.GuiText_2)
        self.ExpressionGUIObj.canvas.delete(self.firstLoadingWheel)
        self.ExpressionGUIObj.canvas.delete(self.secondLoadingWheel)


    def run_task(self):
        """ run_task
        Description:
            Metoda care contine thread-ul principal si care creeaza cate un thread separat pentru partea de GUI,
            pentru timer si pentru partea de clasificare.
            In thread-ul asta se ia fiecare frame de la camera!

        Parameters:

        Returns:

        """

        thread2 = threading.Thread(target=self.ExpressionGUIObj.GenerateGUI, name='Thread0', daemon=True) # Creare de thread pt partea de GUI
        thread2.start()

        thread3 = threading.Thread(target=self.ExpressionGUIObj.TimersThread, name='Thread0', daemon=True) # Creare de thread pt timer
        thread3.start()
        thread3.join()

        thread0 = threading.Thread(target=self.classification, name='Thread0', daemon=True) # Creare de thread pt partea de clasificare
        thread0.start()
        while True:     # Bucla infinta pentru obtinerea frame-urilor de la camera
            # Se ia un cate un frame de la camera
            #print(threading.enumerate())

            ret, self.frame = self.cap.read()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            label_position = (40, 50)

            cv2.putText(self.frame, self.label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

            if(self.ExpressionGUIObj.VideoStatus):
                cv2.imshow('Emotion Detector', self.frame)
            else:
                cv2.destroyAllWindows()

            if (self.lockPC_bool):  # Verificare daca prima combinatie a fost executata cu success si astfel se lock-uie PC-ul si se termina executia programului
                ctypes.windll.user32.LockWorkStation()
                exit(0)

            if(self.ExpressionGUIObj.quitApplicationBool):
                exit(0)

        self.cap.release()
        cv2.destroyAllWindows()


    def classification(self):   # Metoda care contine toata partea de clasificare si care reprezinta metoda pentru thread0
        """ run_task
        Description:
            Metoda care contine toata partea de clasificare si care reprezinta metoda pentru thread0

        Parameters:

        Returns:

        """

        sleep(1)    # Se ofera o secunda pentru initializarea clasificarii (mai intai se porneste interfata grafica cu toate elementele sale)
        while True:
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)   # Linie de code care solicita cel mai mult procesorul. Aici practic se extrage doar fata

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    # Se face o predictie bazata pe ROI (Region of Interest), dupa care se cauta classa din care face parte
                    # Aici se face predictia propriu-zisa

                    preds = self.classifier.predict(roi)[0]
                    self.label = self.class_labels[preds.argmax()]
                    self.counter = self.counter + 1


                    # Se verifica mai intai daca variabila thread1 a fost initializata inainte.
                    # Aceasta parte de code se ocupa cu creearea si verificarea existentei thread-ului 1
                    try:
                        thread1  # Se verifica daca variabila a fost initializata inainte
                    except NameError:
                        if (self.label == 'Happy'):
                            thread1 = threading.Thread(target=self.thread1_method, args=(ListWithPosibleCombinations[0],),
                                                       name='Thread1', daemon=True)
                            thread1.start()
                        if (self.label == 'Angry'):
                            thread1 = threading.Thread(target=self.thread1_method, args=(ListWithPosibleCombinations[1],),
                                                       name='Thread1', daemon=True)
                            thread1.start()
                        if (self.label == 'Surprise'):
                            thread1 = threading.Thread(target=self.thread1_method, args=(ListWithPosibleCombinations[2],),
                                                       name='Thread1', daemon=True)
                            thread1.start()
                        if (self.label == 'Sad'):
                            thread1 = threading.Thread(target=self.thread1_method, args=(ListWithPosibleCombinations[3],),
                                                       name='Thread1', daemon=True)
                            thread1.start()


                    if (self.label == 'Happy' and thread1.is_alive() == False):
                        thread1 = threading.Thread(target=self.thread1_method, args=(ListWithPosibleCombinations[0],),
                                                   name='Thread1', daemon=True)
                        thread1.start()
                    elif(self.label == 'Angry' and thread1.is_alive() == False):
                        thread1 = threading.Thread(target=self.thread1_method, args=(ListWithPosibleCombinations[1],),
                                                   name='Thread1', daemon=True)
                        thread1.start()
                    elif (self.label == 'Surprise' and thread1.is_alive() == False):
                        thread1 = threading.Thread(target=self.thread1_method, args=(ListWithPosibleCombinations[2],),
                                                   name='Thread1', daemon=True)
                        thread1.start()
                    elif (self.label == 'Sad' and thread1.is_alive() == False):
                        thread1 = threading.Thread(target=self.thread1_method, args=(ListWithPosibleCombinations[3],),
                                                   name='Thread1', daemon=True)
                        thread1.start()

            sleep(self.ExpressionGUIObj.SamplingTime) # Sleep parametrizabil care mareste sau scade timpul de clasificare si deci numarul de esantioane/espresii intr-un anumit interval de timp
                                                      # daca este 0.1, va lua aprox 5 expresii pe secunda, in cazul meu.


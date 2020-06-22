import ctypes

class ParametrizationHandler:
    def __init__(self):
        """ Constructorul Clasei """
        self.ListOfParameters = ['DefaultVideoStatus', 'StartApplicationTime', 'LoadingWheelTime', 'ExpressionTime', 'SamplingTime']
        self.ListOfDefaultValues = ['ON', '10', '1', '1', '0.1']
        self.DefaultVideoStatusValues = ['ON', 'OFF']
        self.VideoStatus = True     # Este echivalent cu DefaultVideoStatus din fisierul de parametrizare
        self.StartApplicationTime = 10
        self.LoadingWheelTime = 1
        self.ExpressionTime = 1
        self.SamplingTime = 0.1     # aprox 5 esantioane/expresii in o secunda


    def ReadParametrizationFile(self):
        """ ReadParametrizationFile
        Description:
            Metoda care citeste datele din fisierul ParametrizationFile.txt si verifica daca exista parametrii lipsa

        Parameters:

        Returns:
            ParametrizationList (list): Lista care contine toti parametrii din fisierul de parametrizare

        """

        ParametrizationList = []
        tempCounter = 0
        try:
            with open("ParametrizationFile.txt", 'r') as f:
                ParametrizationList = f.readlines()
                for i in ParametrizationList:
                    if(i == '\n'):      # Se cauta si se numara liniile empty
                        tempCounter = tempCounter + 1
                while tempCounter != 0:     # Loop care va sterge toate liniile empty, pentru o detectie corecta a parametriilor
                    for i in ParametrizationList:
                        if (i == '\n'):
                            ParametrizationList.remove(i)
                            tempCounter = tempCounter - 1


        except FileNotFoundError:
            ctypes.windll.user32.MessageBoxW(0, "Fisierul ParametrizationFile nu a putut fi gasit! Se vor folosi valorile default a parametriilor", "Atentionare!", 1)

        if(len(ParametrizationList) < 5):
            ctypes.windll.user32.MessageBoxW(0, "Lipseste unul sau mai multi parametrii din fisier! Se vor folosi valorile default a parametriilor", "Atentionare!", 1)

        for i in ParametrizationList:
            if('=' not in i):
                ctypes.windll.user32.MessageBoxW(0, "Format gresit, va rugam sa utilizati '=' intre parametrii si valorile acestora! Ex: DefaultVideoStatus = ON. "
                                                    "Se vor folosi valorile default a parametriilor", "Atentionare!", 1)

        return ParametrizationList

    def ProcessParametrizationFileData(self):
        """ ReadParametrizationFile
        Description:
            Metoda care proceseaza datele din fisierul txt si care seteaza variabilele considerate ca parametrii in aplicatie

        Parameters:

        Returns:

        """

        ParametrizationList = self.ReadParametrizationFile()

        processedParametrizationList = []
        for i in ParametrizationList:
            processedParametrizationList.append(i.strip().split('='))

        for i, j in zip(processedParametrizationList, self.ListOfParameters):   # Se verifica daca parametrii sunt corect scrisi. Daca nu, se atentioneaza acest lucru!
            tempStr0 = i[0].split()[0]
            if(j != tempStr0):
                ctypes.windll.user32.MessageBoxW(0, "Parametrul " + tempStr0 + " este necunoscut!! Se vor folosi valorile default a parametriilor", "Atentionare!", 1)
            else:
                tempBool = False
                if(tempStr0 == 'DefaultVideoStatus'):
                    tempStr1 = i[1].split()[0]
                    if(tempStr1 not in self.DefaultVideoStatusValues):
                        ctypes.windll.user32.MessageBoxW(0, "Valoarea pentru parametrul DefaultVideoStatus este gresita! Se va folosi valoarea default.", "Atentionare!", 1)
                    else:
                        if(tempStr1 == 'ON'):
                            self.VideoStatus = True
                        else:
                            self.VideoStatus = False

                if(tempStr0 == 'StartApplicationTime'):
                    try:
                        tempStr1 = int(i[1].split()[0])
                    except ValueError:
                        ctypes.windll.user32.MessageBoxW(0, "Valoarea pentru parametrul StartApplicationTime nu este un numar intreg. Ex: 1, 2, 3, ...10. Se va folosi valoarea default.", "Atentionare!", 1)
                        tempBool = True

                    if(not tempBool):   # Daca nu e scris corect, se ia valoarea default a parametrului
                        if (tempStr1 < 0 or tempStr1 > 10):
                            ctypes.windll.user32.MessageBoxW(0, "Valoarea pentru parametrul StartApplicationTime nu apartine intervalului [0; 10](s). Va rugam sa setati o valoare din acest interval."
                                                                " Se va folosi valoarea default.", "Atentionare!", 1)
                        else:
                            self.StartApplicationTime = tempStr1

                if(tempStr0 == 'LoadingWheelTime'):
                    try:
                        tempStr1 = float(i[1].split()[0])
                    except ValueError:
                        ctypes.windll.user32.MessageBoxW(0, "Valoarea pentru parametrul LoadingWheelTime nu este un numar. Ex: 0.1 sau 1, 2, 3. Se va folosi valoarea default.", "Atentionare!", 1)
                        tempBool = True

                    if(not tempBool):   # Daca nu e scris corect, se ia valoarea default a parametrului
                        if (tempStr1 < 0 or tempStr1 > 10):
                            ctypes.windll.user32.MessageBoxW(0, "Valoarea pentru parametrul LoadingWheelTime nu apartine intervalului [0; 10](s). Va rugam sa setati o valoare din acest interval."
                                                                " Se va folosi valoarea default.", "Atentionare!", 1)
                        else:
                            self.LoadingWheelTime = tempStr1

                if(tempStr0 == 'ExpressionTime'):
                    try:
                        tempStr1 = float(i[1].split()[0])
                    except ValueError:
                        ctypes.windll.user32.MessageBoxW(0, "Valoarea pentru parametrul ExpressionTime nu este un numar. Ex: 0.1 sau 1, 2, 3. Se va folosi valoarea default.", "Atentionare!", 1)
                        tempBool = True

                    if(not tempBool):
                        if(tempStr1 < 0 or tempStr1 > 10):
                            ctypes.windll.user32.MessageBoxW(0, "Valoarea pentru parametrul ExpressionTime nu apartine intervalului [0; 10](s). Va rugam sa setati o valoare din acest interval. "
                                                                "Se va folosi valoarea default.", "Atentionare!", 1)
                        else:
                            self.ExpressionTime = tempStr1

                if(tempStr0 == 'SamplingTime'):
                    try:
                        tempStr1 = float(i[1].split()[0])
                    except ValueError:
                        ctypes.windll.user32.MessageBoxW(0, "Valoarea pentru parametrul SamplingTime nu este un numar. Ex: 1, 0.1, 0.01, 0.05, etc. Se va folosi valoarea default.", "Atentionare!", 1)
                        tempBool = True

                    if(not tempBool):   # Daca nu este un numar si a prins o exceptie, atunci se va lua valoarea default a parametrului
                        if(tempStr1 < 0 or tempStr1 > 2):
                            ctypes.windll.user32.MessageBoxW(0, "Valoarea pentru parametrul ExpressionTime nu apartine intervalului [0; 2](s). Va rugam sa setati o valoare din acest interval. "
                                                                "Se va folosi valoarea default.", "Atentionare!", 1)
                        else:
                            self.SamplingTime = tempStr1

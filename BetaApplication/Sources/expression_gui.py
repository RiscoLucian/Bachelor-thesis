import tkinter as tk
import ctypes
from PIL import Image, ImageTk, ImageSequence
from time import sleep
import os
from parametrization_handler import ParametrizationHandler
import webbrowser

class ExpressionGUI(ParametrizationHandler):
    def __init__(self):
        """ Constructorul clasei """
        super().__init__()
        self.quitApplicationBool = False
        self.GuiBool = False
        self.myTimer = ''
        self.TimerStatus = False
        self.ProcessParametrizationFileData()   # Initializarea valorilor din fisierul de parametrizare


    def GenerateGUI(self):
        """ GenerateGUI
        Description:
            Metoda care handle-uie toata partea de GUI (se creaza un thread separat pentru partea asta)
            Variabila self.root trebuie sa fie initializata cu tk.Tk() in aceasta metoda si nu in constructor deoarece Tkinter
            nu este thread safe!

        Parameters:

        Returns:

        """

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=960, height=540, bg="white", highlightbackground="white")
        self.root.configure(bg='white')

        self.root.geometry("960x540")

        self.MenuBar()

        self.canvas.pack()

        self.canvas.create_text(480, 20, font=('Arial', 24, 'bold'), text="Bine ai venit!")
        self.canvas.create_text(50, 65, font=('Arial', 14), anchor='nw', width=900, text="Aceasta este o aplicatie de interactiune om-calculator, interactiune realizata cu ajutorul expresiilor faciale.")
        self.canvas.create_text(50, 95, font=('Arial', 14), anchor='nw', width=900, text="Pentru mai multe detalii, accesati in bara de meniu Acasa -> Despre Aplicatie")

        self.CountdownTimer()

        self.root.protocol("WM_DELETE_WINDOW", self.QuitApplication)  # Se handle-uie exit-ul aplicatiei (prin click-uirea 'X' -ului din interfata grafica)

        self.root.mainloop()


    def LoadingWheel(self, Ox, Oy):
        """ LoadingWheel
        Description:
            Metoda care creeaza loading wheel-ul

        Parameters:
            Ox (int): Coordonata de pe axa Ox
            Oy (int): Coordonata de pe axa Oy

        Returns:

        """

        self.sequence = [ImageTk.PhotoImage(img)
                         for img in ImageSequence.Iterator(
                Image.open(
                    r'LoadingWheel\ezgif.com-resize_155_82.gif'))]
        self.image = self.canvas.create_image(Ox, Oy, image=self.sequence[0], anchor='nw')
        self.animate(1)


    def animate(self, counter):
        """ animate
        Description:
            Metoda care se ocupa cu animarea loading wheel-ului

        Parameters:
            counter (int): Variabila utilizata ca un counter pentru lambda function

        Returns:

        """

        self.canvas.itemconfig(self.image, image=self.sequence[counter])
        if(self.GuiBool == True):
            return
        self.root.after(100, lambda: self.animate((counter+1) % len(self.sequence)))

    def MenuBar(self):
        """ MenuBar
        Description:
            Metoda care creaza bara de meniu si care apeleaza toate celelalte metode care se ocupa cu fiecare pagina in parte

        Parameters:

        Returns:

        """
        menuBar = tk.Menu(self.root)
        self.root.config(menu=menuBar)

        HomeMenu = tk.Menu(menuBar, tearoff=0)

        menuBar.add_cascade(label="Acasa", menu=HomeMenu)

        HomeMenu.add_command(label='Despre Aplicatie', command=self.AboutApplication)
        HomeMenu.add_command(label='Combinatii Posibile', command=self.PossibleCombinations)
        HomeMenu.add_separator()
        HomeMenu.add_command(label='Iesire', command=self.QuitApplication)

        VideoMenu = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Video', menu=VideoMenu)
        VideoMenu.add_command(label='Porneste Video', command=self.VideoOn)
        VideoMenu.add_command(label='Opreste Video', command=self.VideoOff)

        ConfigurationMenu = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Configurare', menu=ConfigurationMenu)
        ConfigurationMenu.add_command(label='Configurare Parametrii', command=self.ParametersConfiguration)
        ConfigurationMenu.add_command(label='Generare Fisier Cu Parametrii', command=self.GenerationOfDefaultParametrizationFile)

        menuBar.add_command(label='Raporteaza Bug', command=self.ReportABug)

    def AboutApplication(self):
        """ AboutApplication
        Description:
            Metoda care se ocupa cu fereastra numita Despre Aplicatie

        Parameters:

        Returns:

        """

        AboutApplicationWindow = tk.Toplevel(self.root)
        AboutApplicationWindow.configure(bg='white')
        AboutApplicationWindow.geometry("960x540")

        AboutApplicationCanvas = tk.Canvas(AboutApplicationWindow, width=960, height=540, bg="white", highlightbackground="white")

        AboutApplicationCanvas.pack()

        AboutApplicationCanvas.create_text(480, 20, font=('Arial', 24, 'bold'), text="Despre Aplicatie")
        AboutApplicationCanvas.create_text(50, 65, font=('Arial', 14), anchor='nw', width=900, text="In momentul de fata, aplicatia reprezinta un prototip (demo) al unei aplicatii mult mai "
                                                                                                            "complexe, care ofera posibilitatea unei interactiuni om-calculator.")

        AboutApplicationCanvas.create_text(50, 125, font=('Arial', 14), anchor='nw', width=900,
            text="Interactiunea se realizeaza cu ajutorul expresiilor faciale, mai exact prin executarea unor combinatii succesive de expresii. Expresiile faciale reprezinta miscarea unor muschi "
                 "ai fetei si care ofera astfel informatii despre emotiile unei persoane. Aplicatia detecteaza 7 expresii si le clasifica dupa emotia transmisa (happy, angry, surprise, etc), lucru "
                 "care poate fi vazut cand se porneste camera prin intermediul interfetei grafice (Video -> Porneste Video). Astfel, daca o aplicatie poate detecta expresiile unei persoane, aceasta "
                 "persoana ar putea comunica cu calculatorul, prin simpla executare a acestor expresii. Astfel daca se va executa de exemplu o combinatie de expresii cum ar fi: o expresie de Happy "
                 "urmata de Angry si dupa de Surprise, se va declansa o actiune, si anume se va bloca ecranul (lock windows). Pentru a vedea toate combinatiile posibile mergeti la bara de meniu, "
                 "Acasa -> Combinatii Posibile. Aceasta aplicatie poate fi folosita in special de persoanele surdo-mute sau imobilizate, fara posibilitatea de a folosi o tastatura sau mouse.")

        AboutApplicationCanvas.create_text(50, 380, font=('Arial', 14), anchor='nw', width=900,
                                           text="In cazul in care detectia este prea lenta sau prea rapida, se pot schimba anumiti parametrii din bara de meniu -> Configurare -> Parametrii.")

        AboutApplicationCanvas.create_text(50, 440, font=('Arial', 14), anchor='nw', width=900, text="De asemenea, daca observati un bug, nu ezitati sa-l raportati prin intermediul interfetei grafice "
                                                                                                     "la bara de meniu -> Raporteaza Bug.")


    def PossibleCombinations(self):
        """ PossibleCombinations
        Description:
            Metoda care se ocupa cu fereastra numita Combinatii Posibile

        Parameters:

        Returns:

        """

        AboutApplicationWindow = tk.Toplevel(self.root)
        AboutApplicationWindow.configure(bg='white')
        AboutApplicationWindow.geometry("960x540")

        AboutApplicationCanvas = tk.Canvas(AboutApplicationWindow, width=960, height=540, bg="white", highlightbackground="white")

        AboutApplicationCanvas.pack()

        AboutApplicationCanvas.create_text(480, 20, font=('Arial', 24, 'bold'), text="Combinatii Posibile")
        AboutApplicationCanvas.create_text(50, 65, font=('Arial', 14), anchor='nw', width=900, text="Mai jos gasiti lista cu combinatiile posibile si actiunile aferente acestora: ")
        AboutApplicationCanvas.create_text(50, 105, font=('Arial', 14, 'bold'), anchor='nw', width=900, text="1. Happy -> Angry -> Surprise -> Lock PC")
        AboutApplicationCanvas.create_text(50, 145, font=('Arial', 14, 'bold'), anchor='nw', width=900, text="2. Angry -> Surprise -> Angry -> Deschide Youtube")
        AboutApplicationCanvas.create_text(50, 185, font=('Arial', 14, 'bold'), anchor='nw', width=900, text="3. Surprise -> Happy -> Sad -> Porneste BS.Player")
        AboutApplicationCanvas.create_text(50, 225, font=('Arial', 14, 'bold'), anchor='nw', width=900, text="4. Sad -> Surprise -> Angry -> Inchide aplicatia")


    def ReportABug(self):
        """ ReportABug
        Description:
            Metoda care se ocupa cu fereastra numita Raporteaza un Bug

        Parameters:

        Returns:

        """

        ReportBugWindow = tk.Toplevel(self.root)
        ReportBugWindow.configure(bg='white')
        ReportBugWindow.geometry("960x540")

        ReportBugCanvas = tk.Canvas(ReportBugWindow, width=960, height=540, bg="white",
                                           highlightbackground="white")

        ReportBugCanvas.pack()

        ReportBugCanvas.create_text(480, 20, font=('Arial', 24, 'bold'), text="Raportati Bug")
        ReportBugCanvas.create_text(50, 65, font=('Arial', 14), anchor='nw', width=900,
                                           text="Pentru a raporta un bug, va rog sa folositi unul din email-urile de mai jos: ")

        ReportBugCanvas.create_text(50, 105, font=('Arial', 14, 'bold'), anchor='nw', width=900, text="1. minnichalin@yahoo.com")
        ReportBugCanvas.create_text(50, 145, font=('Arial', 14, 'bold'), anchor='nw', width=900, text="2. minnichalin278@gmail.com")
        ReportBugCanvas.create_text(50, 185, font=('Arial', 14), anchor='nw', width=900, text="Ca subiect la mail-ul respectiv va rog sa puneti: 'Raportare bug aplicatie FacialExpressionRecognition'")
        ReportBugCanvas.create_text(50, 245, font=('Arial', 12, 'italic'), anchor='nw', width=900, text="La urmatoarele versiuni de aplicatie este posibila o integrare a unui formular, care va putea fi completat "
                                                                                                        "direct din interfata grafica.")


    def QuitApplication(self):
        """ QuitApplication
        Description:
            Metoda care se ocupa cu iesirea din aplicatie. A fost creata pentru a putea extinde acest feature

        Parameters:

        Returns:

        """

        self.quitApplicationBool = True

    def VideoOn(self):
        """ VideoOn
        Description:
            Metoda care se ocupa cu pornirea video-ului. A fost creata pentru a putea extinde acest feature

        Parameters:

        Returns:

        """

        self.VideoStatus = True

    def VideoOff(self):
        """ VideoOff
        Description:
            Metoda care se ocupa cu oprirea video-ului. A fost creata pentru a putea extinde acest feature

        Parameters:

        Returns:

        """

        self.VideoStatus = False

    def CountdownTimer(self):
        """ CountdownTimer
        Description:
            Metoda care se ocupa cu cronometrul invers de la inceputul aplicatiei

        Parameters:

        Returns:

        """

        self.canvas.delete(self.myTimer)
        self.StartApplicationTime = self.StartApplicationTime - 1
        self.myTimer = self.canvas.create_text(50, 245, font=('Arial', 12, 'italic'), anchor='nw', width=900, text="Aplicatia porneste in.. " + str(self.StartApplicationTime))
        if(self.StartApplicationTime  == -1):   # cand ajunge la 0, porneste clasificarea
            self.canvas.delete(self.myTimer)
            self.TimerStatus = True
        else:
            self.canvas.after(1000, self.CountdownTimer)    # se autoapeleaza functia dupa 1000 ms

    def TimersThread(self):
        """ TimersThread
        Description:
            Metoda a thread-ului pt timer, thread separat doar pentru partea de timer,
            pt a putea handle-uii quit-ul in intervalul de timp mentionat

        Parameters:

        Returns:

        """

        while(not self.TimerStatus):
            if(self.quitApplicationBool):
                os._exit(1)
            sleep(0.1)


    def ParametersConfiguration(self):
        """ ParametersConfiguration
        Description:
            Metoda care se ocupa cu deschiderea fisierului de parametrizare, dar si de oprirea intregii aplicatii

        Parameters:

        Returns:

        """

        ctypes.windll.user32.MessageBoxW(0, "Pentru configurarea parametriilor, aplicatia va fi oprita.. Va rugam sa reveniti dupa configurare", "Atentionare!", 1)
        if(not os.path.exists('ParametrizationFile.txt')):  # In cazul in care nu exista fisierul, se creeaza cel default
            ctypes.windll.user32.MessageBoxW(0, "Nu s-a putut gasi fisierul de parametrizare. Se genereaza cel default..", "Atentionare!", 1)
            with open('ParametrizationFile.txt', 'w') as f:
                for i, j in zip(self.ListOfParameters, self.ListOfDefaultValues):
                    tempStr = i + ' ' + '=' + ' ' + j + '\n'
                    f.writelines(tempStr)

        webbrowser.open('ParametrizationFile.txt')
        os._exit(1)


    def GenerationOfDefaultParametrizationFile(self):
        """ GenerationOfDefaultParametrizationFile
        Description:
            Metoda care se ocupa cu generarea fisierului de parametrizare, fisier care va lua valorile default a parametriilor

        Parameters:

        Returns:

        """

        ctypes.windll.user32.MessageBoxW(0, "S-a generat fisierul de parametrizare cu valorile default a parametriilor!", "Atentionare!", 1)
        with open('ParametrizationFile.txt', 'w') as f:
            for i, j in zip(self.ListOfParameters, self.ListOfDefaultValues):
                tempStr = i + ' ' + '=' + ' ' + j + '\n'
                f.writelines(tempStr)




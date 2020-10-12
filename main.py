from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
from ImageTest import *
import os
import glob
from PIL import ImageTk, Image
import pathlib
import random
imageShowing=0
totalQuestions = 0
correctAwnsers = 0
listOfImageTest = []
pathToFile = ""
renameIterator =0
imageShowing=""
path = str(pathlib.Path(__file__).parent.absolute())




def createListOfImageTest():

	global pathToFile
	global listOfImageTest

	images= [f for f in os.listdir(pathToFile) ]
	print(images)

	for x in range(len(images)):
		aux = ImageTest()
		aux.image =pathToFile+images[x]
		listOfImageTest.append(aux)

def findDirectory():
	global pathToFile
	try:
		pathToFile = filedialog.askdirectory(title="Select file")+('/')
	except :
		directoryFinder.grid(row=1,column=0,pady=20,padx=50,columnspan=2)
		chooser.grid(row=2,column=0,pady=20,padx=50,columnspan=2)

	print(pathToFile)
	createListOfImageTest()
	renamePhotos()

def renamePhotos():
	global directoryFinder
	global chooser
	global listOfImageTest
	global renameIterator
	if len(listOfImageTest)==0:
		showinfo("ERROR NO FOLDER","Please select one saved configuration or folder before")
	else:
		directoryFinder.grid_forget()
		chooser.grid_forget()
		ImagePasser(renameIterator)

def ImagePasser(i):
	global directoryFinder
	global chooser
	global listOfImageTest
	global imageShowing

	if i < len(listOfImageTest):
		img = Image.open(listOfImageTest[i].image)
		img.thumbnail((200,200),Image.ANTIALIAS)
		imageShowing = ImageTk.PhotoImage(img)
		imageLabel = Label(root,image =imageShowing)
		imageLabel.grid(row=2,column=0)
		entryName = Entry(root)
		entryName.grid(row =3,column=0)
		nextImageButton = Button(root,text="Next",command= lambda: nextButton(nextImageButton,imageLabel,entryName,i))
		nextImageButton.grid(row=3,column=1)
	else: 
		saveList()
		


def nextButton(button,imageLabel,entryName,i):
	global listOfImageTest
	global ImagePasser
	listOfImageTest[i].name = entryName.get()
	imageLabel.destroy()
	entryName.destroy()
	button.destroy()
	i=i+1
	ImagePasser(i)

def saveList():
	savedTitle = Label(root,text="Save the image list with a name",font = ("Verdana",22),fg="white",bg="black")
	savedTitle.grid(row=2,column=0)
	savedName = Entry(root,text="Save the list",fg="white",bg="black")
	savedName.grid(row =3,column=0)
	saveButton = Button(root,text="Save",command= lambda: createList(savedName.get(),savedName,saveButton,savedTitle),fg="white",bg="black")
	saveButton.grid(row = 3,column=1)

def createList(stringName,labelToHide1,labelToHide2,labelToHide3):
	global  listOfImageTest
	global chooser
	global directoryFinder
	global path
	textFile = open(stringName +".txt", "a")
	

	for i in listOfImageTest:
		textFile.write(i.image+"\n")
		textFile.write(i.name+"\n")
	textFile.close()
	os.replace(path+"/"+stringName +".txt",path+"/SavedTests/"+stringName +".txt")
	labelToHide1.destroy()
	labelToHide2.destroy()
	labelToHide3.destroy()
	directoryFinder.grid(row=1,column=0,pady=20,padx=50,columnspan=2)
	chooser.grid(row=2,column=0,pady=20,padx=50,columnspan=2)

def detectSavedTests():
	global directoryFinder
	global chooser
	global path
	listOfRadioButtons = []
	chooseNumber = 0
	chooser.grid_forget()
	directoryFinder.grid_forget()
	savedtests= [f for f in os.listdir(path+"/SavedTests/") ]
	auxInteger = 0
	for i in range(len(savedtests)):
		listOfRadioButtons.append(Radiobutton(root,text = savedtests[i],value = i,variable=chooseNumber,fg="black",bg="gray",font=("Verdana",18)))
		listOfRadioButtons[i].grid(row=i+1,column=0,pady=20,padx=50,columnspan=2)
		auxInteger=i+2

	LoadButton = Button(root,text="Load" ,command= lambda :loadList(savedtests[chooseNumber],listOfRadioButtons,LoadButton),fg="white",bg="black")
	LoadButton.grid(row=auxInteger,column=1,pady=20,padx=50)
	ReturnButton = Button(root,text="Back" ,command= lambda :returnBack(listOfRadioButtons,LoadButton,ReturnButton),fg="white",bg="black")
	ReturnButton.grid(row=auxInteger,column=0,pady=20,padx=50)

def returnBack(listOfRadioButtons,Load,Back):
	for i in listOfRadioButtons:
		i.destroy()
	Load.destroy()
	Back.destroy()
	directoryFinder.grid(row=1,column=0,pady=20,padx=50,columnspan=2)
	chooser.grid(row=2,column=0,pady=20,padx=50,columnspan=2)




def loadList(testLoaded,listOfRadioButtons,LoadButton):
	global correctAwnsers
	global listOfImageTest
	global totalQuestions

	correctAwnsers=0
	test = open(path+"/SavedTests/"+testLoaded, 'r')
	lines = test.readlines()
	listOfImageTest=[ImageTest() for i in range(int(len(lines)/2))]
	totalQuestions = len(listOfImageTest)
	for i in range(len(lines)):
		if i ==0 or i%2==0:
			listOfImageTest[int(i/2)].image= lines[i].replace('\n','')
			listOfImageTest[int(i/2)].name= lines[i+1].replace('\n','')
	for radioButton in listOfRadioButtons:
		radioButton.grid_forget()
	startTest()
	LoadButton.grid_forget()



def startTest():	
	global listOfImageTest
	global correctAwnsers
	global totalQuestions
	global imageShowing
	global directoryFinder
	global chooser
	
	if len(listOfImageTest)>0:
		if len(listOfImageTest) == 0:
			intAux=0
		else:
			intAux = random.randint(0, len(listOfImageTest)-1)
		
		intAux = random.randint(0, len(listOfImageTest)-1)
		img = Image.open(listOfImageTest[intAux].image)
		img.thumbnail((200,200), Image.ANTIALIAS)
		imageShowing = ImageTk.PhotoImage(img)
		imageLabel = Label(root,image =imageShowing)
		imageLabel.grid(row=1,column=0)
		entryName = Entry(root)
		entryName = Entry(root)
		entryName.grid(row =2,column=0)
		score = Label(root,text=str(correctAwnsers)+"/"+str(totalQuestions),font = ("Verdana",12),fg="white",bg="black")
		score.grid(row=3,column=0)
		programTitle.grid(row=0,column=0)
		nextImageButton = Button(root,text="Next",command= lambda: nextImageButton2(nextImageButton,imageLabel,entryName,intAux,score))
		nextImageButton.grid(row =2,column=1)
	else:
		showinfo("Score","You've got "+str(correctAwnsers)+" correct answers")
		directoryFinder.grid(row=1,column=0,pady=20,padx=50,columnspan=2)
		chooser.grid(row=2,column=0,pady=20,padx=50,columnspan=2)





def nextImageButton2(nextImageButton,imageLabel,entryName,i,score):
	global listOfImageTest
	global ImagePasser
	global correctAwnsers
	if listOfImageTest[i].name ==entryName.get():
		
		
		imageLabel.destroy()
		entryName.destroy()
		nextImageButton.destroy()
		score.destroy()
		listOfImageTest.remove(listOfImageTest[i])
		correctAwnsers =  correctAwnsers+1
		startTest()
	else:
		showinfo("WRONG ANSWER","The correct answer was: "+listOfImageTest[i].name)
		listOfImageTest.remove(listOfImageTest[i])
		imageLabel.destroy()
		entryName.destroy()
		nextImageButton.destroy()
		score.destroy()
		startTest()
	

root = Tk()

programTitle = Label(root,text="ImageTestTrainer",font = ("Verdana",44),fg="yellow",pady=20,bg="black")
programTitle.grid(row=0,column=0,pady=20,columnspan=2,padx=30)


directoryFinder = Button(root,text ="Create a new Test", font=("Verdana",15), command = findDirectory,fg="white",bg="black",pady=20)
directoryFinder.grid(row=1,column=0,pady=20,padx=50,columnspan=2)

chooser = Button(root,text="Use a saved Test",font = ("Verdana",15),command = detectSavedTests,fg="white",bg="black",pady=20)
chooser.grid(row=2,column=0,pady=20,padx=50,columnspan=2)
root.geometry("600x700")
root.configure(background='black')
root.mainloop()
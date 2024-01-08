#the code to make the game manager

from tkinter import ttk, Tk, Checkbutton, IntVar, messagebox
from gameloop import main

#general function to show an error popup
#if the portal corrdinates are messed up
def showerror():
    messagebox.showerror("Error","Invalid portal coordinates!")

#function to be used by the clear all button
#clears all entry fields
def clearall():
    e1.delete(0,100)
    e2.delete(0,100)
    e3.delete(0,100)
    
#if the setmanual checkbox is changed, do this
def setmanual():
    var = cb1.get() #get the status of the box
    
    if var == 0:
        #If it is unchecked, grey out the fields
        e3.config(state='disable')
        e2.config(state='disable')
    elif var == 1:
        #If it is checked, activate the fields
        e3.config(state='enable')
        e2.config(state='enable')

#function to be used to start the game
def start():
    #gets what is in each field
    #and if the checkbox is enabled
    var = cb1.get()
    e2i = e2.get()
    e3i = e3.get()
    
    seed = e1.get() #gets the seed
    
    #If the manual box is checked, try to process
    #the portal coordinates
    if var == 1:
        
        #make sure the coordinates are integers
        try:
            int(e2i)
        except:
            showerror()
            return
        try:
            int(e3i)
        except:
            showerror()
            return
        
        #make sure they are in range
        if int(e2i) < 0 or int(e2i) > 15:
            showerror()
            return
        if int(e3i) < 0 or int(e3i) > 15:
            showerror()
            return
        
        #send the seed and portal location to the game loop
        main(seed, int(e3i), int(e2i))
    
    #if the box is unchecked, start the game with the auto
    #generation flag enabled
    elif var == 0:
        main(seed, -1, 0)
    
#Creating the window
root = Tk()
root.title("Game manager")
root.geometry("400x210")

cb1 = IntVar() #make a varibale to store the status of the checkbox

#create all the text fields and place them in the right place
l1 = ttk.Label(root, text="Enter a seed:")
l1.place(x=40, y=20)
l1.config(font=150)

l2 = ttk.Label(root, text="Portal x:")
l2.place(x=40, y=95)
l2.config(font=150)

l3 = ttk.Label(root, text="Portal y:")
l3.place(x=40, y=126)
l3.config(font=150)

l4 = ttk.Label(root, text="""Enter anything for the seed. If checkbox
is unchecked, portal will be randomly 
generated. Otherwise enter an x and y from
0 to 15 inclusive. The portal will overwrite
whatever was in that spot.""")
l4.place(x= 160, y=80)

#create all the entry fields and put them in the right place
e1 = ttk.Entry(root, width=25)
e1.place(x=160, y=20)

e2 = ttk.Entry(root, width=5, state='disable')
e2.place(x=105, y=96, )

e3 = ttk.Entry(root, width=5, state='disable')
e3.place(x=105, y=126)

#make an place the checkbox
Button1 = Checkbutton(root, onvalue = 1,
						offvalue = 0,
                        variable = cb1,
                        text="Set portal manually",
                        command = setmanual) 
Button1.place(x=28, y=60)


#make and place the 2 buttons that we use
b1 = ttk.Button(root, text="Start!", command=start)
b1.place(x=100, y =170)

b2 = ttk.Button(root, text="Clear all", command = clearall)
b2.place(x=190, y=170)

root.mainloop() #start the GUI manager window
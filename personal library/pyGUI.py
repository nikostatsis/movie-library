#20171208-vp
import tkinter as tk
import random

# define function decorator to update memory and
# register views. Applied on class GUI methods
def updateviews(func):
    def wrapper(self, event):
        func(self, event)
        self.readvalues()
        self.printmemory()
    return wrapper

class Register():
    # Initialize the Register class with master, name, and length
    def init(self, master, name, length=8):
        # Create a string variable to hold the register data
        self.data = tk.StringVar()
        # Set the bitlength of the register
        self.bitlength = length
        # Create a label for the register name and add it to the GUI
        self.namelabel = tk.Label(master, text=name, font='Consolas 10')
        self.namelabel.pack(side='left', padx=10)
        # Create a label for the register value and add it to the GUI
        self.valuelabel = tk.Label(master, textvariable=self.data, font='Consolas 10')
        self.valuelabel.pack(side='left', padx=5)

        
class RegisterDisplayer():
    registers = {}
    def __init__(self, master, name, length = 8 ):
        RegisterDisplayer.registers[name]= Register(master, name, length)
                                           
        
class GUI():
    def __init__(self, r, cpu, startaddress, memory):
        # Initialize the GUI window and other variables
        self.r = r
        self.r.title('GUI OO pyCPU')
        self.cpu = cpu
        self.r.wm_geometry('1200x600+50+50')
        self.okfunc = cpu.start
        self.memory = memory
        self.memory.check()
        self.startaddress = startaddress
        # Create the GUI widgets and display them
        self.widgets()
        # Initialize CPU display variables
        cpu.setdisplay(self.text)
        cpu.setcommandout(self.comtext)
        cpu.setinfoout(self.infotext)
        # Display start message
        self.start_message()

    def widgets(self):
        # Create the GUI widgets and display them
        self.regf = tk.Frame(self.r)
        regs = self.cpu.regnames
        regslen = self.cpu.reglens
        # Display the CPU registers
        list(map(lambda x : RegisterDisplayer(self.regf, *x),\
            zip(regs, regslen)))
        self.regf.pack()
        # Display the text widget for displaying CPU cycle information
        self.tf = tk.Frame(self.r)
        self.ptf = tk.Frame(self.tf)
        tk.Label(self.ptf,text='Κύκλοι εντολής').pack()
        self.text = tk.Text(self.ptf, font='Consolas 10', width=80, height=19)
        self.scroll = tk.Scrollbar(self.ptf, command=self.text.yview)
        self.scroll.pack(side='right', fill='y')
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.pack(side='left', padx=10, pady=5)
        self.ptf.pack(side='left')
        # Display the text widget for displaying memory contents
        self.mtf = tk.Frame(self.tf)
        tk.Label(self.mtf, text='Περιεχόμενα μνήμης').pack()
        self.memtext = tk.Text(self.mtf, font='Consolas 10', width=20, height=19)
        self.scrollmem = tk.Scrollbar(self.mtf, command=self.memtext.yview)
        self.scrollmem.pack(side='right', fill='both')
        self.memtext.configure(yscrollcommand=self.scrollmem.set)
        self.memtext.pack(side='left', fill='both', padx=10, pady=5)
        self.mtf.pack(side='left')
        # Display the text widget for displaying the CPU commands
        self.comtf = tk.Frame(self.tf)
        tk.Label(self.comtf, text='Εντολές').pack()
        self.comtext = tk.Text(self.comtf, font='Consolas 10', width=20, height=19)
        self.comscroll = tk.Scrollbar(self.comtf, command=self.comtext.yview)
        self.comscroll.pack(side='right', fill='both')
        self.comtext.configure(yscrollcommand=self.comscroll.set)
        self.comtext.pack(side='left', fill='both', padx=10, pady=5)
        self.comtf.pack(side='left')
        self.tf.pack()
        # Display the text widget for displaying CPU information
        self.infof = tk.Frame(self.r)
        self.infotext = tk.Text(self.infof, font='Consolas 10', width=100,  height=4)
        # Create a scrollbar for the info text widget
        self.infscroll = tk.Scrollbar(self.infof, command=self.infotext.yview)
        self.infscroll.pack(side='right', fill='both')
        # Configure the info text widget to use the scrollbar
        self.infotext.configure(yscrollcommand=self.infscroll.set)
        self.infotext.pack(side='left', fill='both', padx=10, pady=10)
        self.infof.pack()
        # Create a frame for buttons to control program execution
        self.butf = tk.Frame(self.r)
        # Create a button to execute the entire program at once
        button = tk.Button(self.butf, text='EXEC PROGRAM')
        button.bind('<Button-1>', self.execall)
        button.pack(side='left')
        # Create a button to execute the next instruction
        button2 = tk.Button(self.butf, text='NEXT INSTRUCTION')
        button2.bind('<Button-1>', self.nextinstruction)
        button2.pack(side='left')
        # Create a button to execute the next cycle
        button3 = tk.Button(self.butf, text='NEXT CYCLE')
        button3.bind('<Button-1>', self.nextcycle)
        button3.pack(side='left')
        # Create a button to reset the program
        button4 = tk.Button(self.butf, text='RESET')
        button4.bind('<Button-1>', self.reset)
        button4.pack(side='left')
        self.butf.pack()

def start_message(self):
    # Inserts the initial instructions into the infotext widget
    self.infotext.insert('end','EXEC PROGRAM: εκτέλεση προγράμματος\n')
    self.infotext.insert('end','NEXT INSTRUCTION: εκτέλεση επόμενης εντολής\n')
    self.infotext.insert('end','NEXT CYCLE: εκτέλεση επόμενου βήματος εκτέλεσης\n')
    self.infotext.insert('end','RESET: αρχικοποίηση CPU και επαναφόρτωση μνήμης\n')

@updateviews
def nextinstruction(self, event):
    # Binds the "next instruction" button to the nextinstruction method of the CPU class, and updates the view
    self.cpu.nextinstruction(event)

@updateviews
def nextcycle(self, event):
    # Binds the "next cycle" button to the nextcycle method of the CPU class, and updates the view
    self.cpu.nextcycle(event)

@updateviews
def execall(self, event):
    # Binds the "exec all" button to the execall method of the CPU class, and updates the view
    self.cpu.execall(self.startaddress, event)

def initvalues(self):
    # Initializes the register values to 0
    for i in RegisterDisplayer.registers.keys():
        bits = RegisterDisplayer.registers[i].bitlength
        value = format(0, '0'+str(int(bits/4))+'X') 
        RegisterDisplayer.registers[i].data.set(value)

def setvalues(self, vals = {}):
    # Sets the register values to random values
    for i in RegisterDisplayer.registers.keys():
        bits = RegisterDisplayer.registers[i].bitlength
        value = format(random.randint(0,2**bits-1), '0'+str(int(bits/4))+'X') 
        RegisterDisplayer.registers[i].data.set(value)

def readvalues(self):
    # Reads the register values from the CPU and displays them
    for i in RegisterDisplayer.registers.keys():
        bits = RegisterDisplayer.registers[i].bitlength
        try:
            value = format(int(self.cpu.regdict[i]), '0'+str(int(bits/4))+'X')
        except:
            value = self.cpu.regdict[i] 
        RegisterDisplayer.registers[i].data.set(value)

def reset(self, event):
    # Resets the CPU and memory, and updates the view
    self.text.delete('1.0', 'end')
    self.comtext.delete('1.0', 'end')
    self.infotext.insert('end', 'CPU reset, memory reloaded\n')
    self.infotext.see('end')
    self.cpu.reset()
    self.initvalues()
    self.printmemory()

def printmemory(self):
    # Prints the memory contents
    self.memtext.delete('1.0', 'end')
    for i in range(len(self.memory.M)):
        v = self.memory.M[i]
        self.memtext.insert('end',\
            format(i,'04d')+': '+format(v,'04X') + ' ('+str(v)+')\n')
    

def main(*args):
    # Initializes the GUI and runs the main event loop
    root = tk.Tk()
    a = GUI(root, args[0], args[1], args[2])
    root.mainloop()


if __name__ == '__main__':
    print('requires arguments and/or to be imported')

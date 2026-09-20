import tkinter
import pickle as p
import tkinter.messagebox
import sys

# Arrangement of buttons
Value_buttons=[("!","mod","RCL","Hyp","Inv"),
               ("nPr","←","SAVE","→","nCr"),
               ("Rec()","sin","cos","tan","Pol()"),
               ("RAD","csc","sec","cot","10^x"),
               ("log","√","e","n√","ln"),
               ("(",")","π","^","ENG"),
               ("7","8","9","DEL","AC"),
               ("4","5","6","x","/"),
               ("1","2","3","+","-"),
               ("0",".","=","Ans","EXP")]

# Basic buttons present even in normal calculators
right_buttons=  ["AC","/","x","-","+","DEL","EXP","Ans"]

# . and = included for symmetry
digit_buttons=     ["0","1","2","3","4","5","6","7","8","9",".","=",]

function_buttons=  ["!","mod","RCL","Hyp","Inv", "nPr","←","SAVE","→","nCr", "Rec()","sin","cos","tan","Pol()", "RAD","csc","sec","cot","10^x", "log","√","e","n√","ln", "(",")","π","^","ENG",]

# Buttons that work even if the character limit is exceeded
non_enforced_buttons= ["AC", "DEL", "←", "→", "="]

# Buttons that can change their function
spcl_buttons = ["RAD", "sin", "cos", "tan", "csc", "sec", "cot"]

light_blue = "#ADD8E6"
light_grey = "#D3D3D3"
pink = "#FFC0CB"

row_count = len(Value_buttons)
column_count = len(Value_buttons[0])

# Characters to the left of the cursor and their corresponding values
leftStr = ["0"]
leftVal = [0]

# Characters to the left of the cursor and their corresponding values
rightStr = []
rightVal = []

# The most important character
leftChar = "0"

# Used to store expressions and their values when SAVE is clicked
save = []
saveVal = []

"""
Characters are classified according to values
digit values   : 0
. value        : 1
+ - x / values : 2
, value        : 3

the value of a function is (x+1)*10 + funcCounts[x], where x is the corresponding index of the function in funcCounts
This means that the code will break if you include more than 10 of the same function

I have not placed any restrictions when it comes to characters on the right side as the input goes from left to right
"""

# Counts of certain functions
# Used to distinguish functions when multiple are used in a single expression
#               0   1    2    3    4    5    6    7   8   9   10   11    12   13   14   15    16    17   18
# Index order: (), sin, cos, tan, csc, sec, cot, EXP, !, mod, Rec, Pol, 10^x, log, ln, sqrt, nRoot, nPr, nCr
funcCounts = [0 for i in range(19)]

# Used to store the answer when Ans is clicked
Ans = None

# Save the state of certain toggles
RADMode = True
InvMode = False
HypMode = False

tab=tkinter.Tk()

frame= tkinter.Frame(tab)

# | is used to indicate the cursor position
label= tkinter.Label(frame, text= "0|", font= ("arial",23), background= "black", foreground= "white", anchor= "e", width= column_count,height= 2)

# Abstraction/Macro
def createSpclButton(value):
    return tkinter.Button(frame, text= value, font= ("arial",20), width= column_count-1, height= 1, foreground= "black", background= light_grey)

# This has to be done as we need a place to store the special buttons as they can be modified later
RADButton = createSpclButton("RAD")

sinButton = createSpclButton("sin")
cosButton = createSpclButton("cos")
tanButton = createSpclButton("tan")
cscButton = createSpclButton("csc")
secButton = createSpclButton("sec")
cotButton = createSpclButton("cot")

""" Data must strictly follow this order. This means there always 12 objects in the file
leftChar
leftStr
leftVal
rightStr
rightVal
funcCounts
RADMode
HypMode
InvMode
Ans
save
saveVal
"""

fhandle = open("storage.dat", "wb+")

# Users must pack/unpack file objects when storing/retrieving
def readFromFile():
    fhandle.seek(0)
    out = []
    try:
        while True:
            out.append(p.load(fhandle))
    except EOFError:
        return out
    except p.UnpicklingError as err:
        tkinter.messagebox.showerror("ERROR: Reading from file", f"The program was unable to read the file storage.dat and will terminate.\nError message: {err}")
        sys.exit(-2)

def writeToFile(l):
    # Allow passing placeholder values and incomplete lists for brevity's sake
    # You might notice that we are using None as a placeholder, but Ans can actually assume a None value. We deal with issue by ignoring it
    if len(l) != 12:
        previous = readFromFile()
        for i in range(12):
            if i < len(l):
                if l[i] == None:
                    l[i] = previous[i]
            else:
                l.append(previous[i])

    fhandle.seek(0)
    fhandle.truncate(0)
    try:
        for element in l:
            p.dump(element, fhandle)
    except p.PicklingError as err:
            tkinter.messagebox.showerror("ERROR: Writing from file", f"The program was unable to write to the file storage.dat and will terminate.\nError message: {err}")
            sys.exit(-1)


# Initial values
writeToFile(["0", ["0"], [0], [], [], [0 for i in range(19)], True, False, False, None, [], []])
import tkinter

# Arrangement of buttons
Value_buttons=[("!","abs","RCL","Hyp","Inv"),
               ("nPr","←","SAVE","→","nCr"),
               ("Rec()","sin","cos","tan","Pol()"),
               ("RAD","csc","sec","cot","10^x"),
               ("log","√","e","n√","ln"),
               ("(",")","π","^","ENG"),
               ("7","8","9","DEL","AC"),
               ("4","5","6","x","/"),
               ("1","2","3","+","-"),
               ("0",".","=","Ans","EXP")]

# Basic buttons present even in normal calculators except maybe EXP, I don't know why that is there instead of ^, but my teammates insisted that this placement was correct
right_buttons=  ["AC","/","x","-","+","DEL","EXP","Ans"]

# . and = included for symmetry
digit_buttons=     ["0","1","2","3","4","5","6","7","8","9",".","=",]

function_buttons=  ["!","abs","RCL","Hyp","Inv", "nPr","←","SAVE","→","nCr", "Rec()","sin","cos","tan","Pol()", "RAD","csc","sec","cot","10^x", "log","√","e","n√","ln", "(",")","π","^","ENG",]

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
# Index order: (), sin, cos, tan, csc, sec, cot, EXP, !, abs, Rec, Pol, 10^x, log, ln, sqrt, nRoot, nPr, nCr
funcCounts = [0 for i in range(19)]                                         # type: ignore # type: ignore

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
import tkinter

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

right_buttons=  ["AC","/","x","-","+","DEL","EXP","Ans"]
digit_buttons=     ["0","1","2","3","4","5","6","7","8","9",".","=",]
function_buttons=  ["!","abs","RCL","Hyp","Inv", "nPr","←","SAVE","→","nCr", "Rec()","sin","cos","tan","Pol()", "RAD","csc","sec","cot","10^x", "log","√","e","n√","ln", "(",")","π","^","ENG",]
non_enforced_buttons= ["AC", "DEL", "←", "→", "="]
spcl_buttons = ["RAD", "sin", "cos", "tan", "csc", "sec", "cot"]

Light_blue="#ADD8E6"
Light_grey="#D3D3D3"
Pink="#FFC0CB"
row_count= len(Value_buttons)
column_count= len(Value_buttons[0])

leftStr = ["0"]
leftVal = [0]
rightStr = []
rightVal = []
leftChar = "0"
rightChar = None
save = []
saveVal = []

"""
digit value: 0
. : 1
+ - x /: 2
, : 3
the value of a function is (x+1)*10 + funcCounts[x], where x is the corresponding index of the function in funcCounts
This means that the code will break if you include more than 10 of the same function
"""
# I have not placed any restrictions when it comes to characters on the right side as the input goes from left to right

#               0   1    2    3    4    5    6    7   8   9   10   11    12   13   14   15    16    17   18
# Index order: (), sin, cos, tan, csc, sec, cot, EXP, !, abs, Rec, Pol, 10^x, log, ln, sqrt, nRoot, nPr, nCr
funcCounts = [0 for i in range(19)] # type: ignore # type: ignore

a = None
RADMode = True
InvMode = False
HypMode = False

tab=tkinter.Tk()

frame= tkinter.Frame(tab)

label= tkinter.Label(frame, text="0|", font=("arial",20), background="black",
                     foreground="white", anchor="e", width= column_count,height= 2)

def createSpclButton(value):
    return tkinter.Button(frame, text=value, font=("arial",20),
                width=column_count-1, height=1,
                foreground="black", background=Light_grey)

RADButton = createSpclButton("RAD")

sinButton = createSpclButton("sin")
cosButton = createSpclButton("cos")
tanButton = createSpclButton("tan")
cscButton = createSpclButton("csc")
secButton = createSpclButton("sec")
cotButton = createSpclButton("cot")
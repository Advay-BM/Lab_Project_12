import tkinter
from mathFunctions import *

Value_buttons=[("!","abs","RCL","Hyp","Inv"),   #all the functions present in the calculator
               ("nPr","←","M+","→","nCr"),
               ("Rec()","Sin","Cos","Tan","Pol()"),
               ("DEG","Csc","Sec","Cot","10^x"),
               ("log","√","e","n√","ln"),
               ("(",")","π","^","ENG"),
               ("7","8","9","DEL","AC"),
               ("4","5","6","x","÷"),
               ("1","2","3","+","-"),
               ("0",".","=","Ans","EXP")]

right_buttons=  ["AC","÷","x","-","+","DEL","EXP","Ans"]
digit_buttons=     ["0","1","2","3","4","5","6","7","8","9",".","=",]
function_buttons=  ["!","abs","RCL","Hyp","Inv", "nPr","←","M+","→","nCr", "Rec()","Sin","Cos","Tan","Pol()", "DEG","Csc","Sec","Cot","10^x", "log","√","e","n√","ln", "(",")","π","^","ENG",]
Light_blue="#ADD8E6"
Light_grey="#D3D3D3"

row_count= len(Value_buttons)
column_count= len(Value_buttons[0])

tab=tkinter.Tk()
tab.title("SCIENTIFIC CALCULATOR")

frame= tkinter.Frame(tab)
label= tkinter.Label(frame, text="0", font=("arial",20), background="black",
                     foreground="white", anchor="e", width= column_count,height= 2)
label.grid(row=0,column=0, columnspan=column_count, sticky="we")
for row in range(row_count):
    for column in range(column_count):
        value=Value_buttons[row][column]
        buttons=tkinter.Button(frame, text=value, font=("arial",20),
                               width=column_count-1, height=1,
                               command=lambda value=value: buttons_pressed(value))
        if value in right_buttons:
            buttons.config(foreground="black", background=Light_blue)
        elif value in digit_buttons:
            buttons.config(foreground="black", background="pink")
        elif value in function_buttons:
            buttons.config(foreground="black", background=Light_grey)
        else:
            buttons.config(foreground="black", background=Light_grey)
        buttons.grid(row=row+1, column=column)

        
frame.pack()
A = "0"
B = None
operator = None

leftStr = ["0"]
leftVal = [0]
rightStr = []
rightVal = []
leftChar = "0"
rightChar = None
# (), sin, cos, tan, sec, cot, csc, EXP
funcCounts = [0 for i in range(8)]

"""
digit value: 0
decimal value: 1
+ - x /: 2
"""
# I have not placed any restrictions when it comes to characters on the right side as the input goes from left to right

def insertParantheses(val):
    global leftChar, leftStr, leftVal, rightChar, rightStr, rightVal
    leftStr.append("(")
    leftVal.append(val)
    leftChar = "("
    rightStr.insert(0,")")
    rightVal.insert(0,val)
    rightChar = ")"

def buttons_pressed(value):
    global leftChar, leftStr, leftVal, rightChar, rightStr, rightVal, funcCounts
    if (value in right_buttons):
        match (value):
            case "AC":
                # Reset everything
                leftStr = ["0"]
                leftVal = [0]
                rightStr = []
                rightVal = []
                leftChar = "0"
                rightChar = None
            case "DEL":
                ...
            case "EXP":
                if (leftVal[-1] != 0 and leftVal[-1] != 1) or (len(leftStr) == 1 and leftChar == "0"):
                    val = 80
                    val += funcCounts[7]
                    if leftChar == "0":
                        leftStr.pop()
                        leftVal.pop()
                    leftStr += list("exp")
                    leftVal.extend([val for i in range(3)])
                    insertParantheses(val)
            case "Ans":
                ...
            case "+":
                # Should only be allowed if character to the left is not a decimal or another operator
                if leftVal[-1] != 2 and leftVal[-1] != 1:
                    leftChar = "+"
                    leftVal.append(2)
                    leftStr.append("+")
            case "-":
                # Same restriction as +
                if leftVal[-1] != 2 and leftVal[-1] != 1:
                    leftChar = "-"
                    leftVal.append(2)
                    leftStr.append("-")
            case "x":
                # Same restriction as + but additionally, x cannot prefix a number
                if leftVal[-1] != 2 and leftVal[-1] != 1 and leftChar != "(":
                    leftChar = "x"
                    leftVal.append(2)
                    leftStr.append("x")
            case "÷":
                # Same restriction as x
                if leftVal[-1] != 2 and leftVal[-1] != 1 and leftChar != "(":
                    leftChar = "/"
                    leftVal.append(2)
                    leftStr.append("/")
    
    elif (value in digit_buttons):
        if value in "0123456789":
            if len(leftStr) == 1 and leftChar == "0":
                leftStr[-1] = value
            else:
                leftStr.append(value)
                leftVal.append(0)
            leftChar = value
        elif value == ".":
            canPlace = True
            # Go backwards through leftStr
            for i in range(-1, -len(leftVal)-1, -1):
                if leftVal[i] == 1:
                    # If we encounter another decimal point, do not allow to place
                    canPlace = False
                    break
                if leftVal[i] != 0:
                    # Stop checking if we reach the end of the number
                    break

            if leftVal[-1] == 0 and canPlace:
                leftChar = "."
                leftVal.append(1)
                leftStr.append(".")
        else:
            # Display result
            displayString = ""
            for i in range(len(leftStr)):
                if leftStr[i] == "x" and leftStr[i-1] != "e":
                    displayString += "*"
                else:
                    displayString += leftStr[i]
            for i in range(len(rightStr)):
                if rightStr[i] == "x":
                    displayString += "*"
                else:
                    displayString += rightStr[i]
            print(displayString)
            result = eval(displayString)
            label["text"] = str(result)

            # Reset input label to hold result
            leftStr = []
            leftVal = []
            rightStr = []
            rightVal = []
            rightChar = None
            for i in str(result):
                leftStr.append(i)
                if i == "-":
                    leftVal.append(2)
                elif i == ".":
                    leftVal.append(1)
                else:
                    leftVal.append(0)
            leftChar = leftStr[-1]
            funcCounts = [0 for i in range(7)]
            return None
    elif (value in function_buttons):
        match (value):
            case "←":
                if (leftStr != []):
                    storeStr = leftStr.pop()
                    storeVal = leftVal.pop()
                    rightStr.insert(0, storeStr)
                    rightVal.insert(0, storeVal)
                    rightChar = rightStr[0]
                    if (leftStr == []):
                        leftChar = None
                    else:
                        leftChar = leftStr[0]

            case "→":
                if (rightStr != []):
                    storeStr = rightStr.pop(0)
                    storeVal = rightVal.pop(0)
                    leftStr.append(storeStr)
                    leftVal.append(storeVal)
                    leftChar = leftStr[-1]
                    if (rightStr == []):
                        rightChar = None
                    else:
                        rightChar = rightStr[0]
            
            case "(":
                if (leftVal[-1] != 0 and leftVal[-1] != 1) or (len(leftStr) == 1 and leftChar == "0"):
                    val = 10
                    val += funcCounts[0]
                    if leftChar == "0":
                        leftStr.pop()
                        leftVal.pop()
                    insertParantheses(val)

            case "Sin":
                if (leftVal[-1] != 0 and leftVal[-1] != 1) or (len(leftStr) == 1 and leftChar == "0"):
                    val = 20
                    val += funcCounts[1]
                    if leftChar == "0":
                        leftStr.pop()
                        leftVal.pop()
                    leftStr += list("sin")
                    leftVal.extend([val for i in range(3)])
                    insertParantheses(val)

            case "Cos":
                if (leftVal[-1] != 0 and leftVal[-1] != 1) or (len(leftStr) == 1 and leftChar == "0"):
                    val = 30
                    val += funcCounts[2]
                    if leftChar == "0":
                        leftStr.pop()
                        leftVal.pop()
                    leftStr += list("cos")
                    leftVal.extend([val for i in range(3)])
                    insertParantheses(val)
                    

            case "Tan":
                if (leftVal[-1] != 0 and leftVal[-1] != 1) or (len(leftStr) == 1 and leftChar == "0"):
                    val = 40
                    val += funcCounts[3]
                    if leftChar == "0":
                        leftStr.pop()
                        leftVal.pop()
                    leftStr += list("tan")
                    leftVal.extend([val for i in range(3)])
                    insertParantheses(val)
            
            case "Csc":
                if (leftVal[-1] != 0 and leftVal[-1] != 1) or (len(leftStr) == 1 and leftChar == "0"):
                    val = 50
                    val += funcCounts[4]
                    if leftChar == "0":
                        leftStr.pop()
                        leftVal.pop()
                    leftStr += list("csc")
                    leftVal.extend([val for i in range(3)])
                    insertParantheses(val)
            
            case "Sec":
                if (leftVal[-1] != 0 and leftVal[-1] != 1) or (len(leftStr) == 1 and leftChar == "0"):
                    val = 60
                    val += funcCounts[5]
                    if leftChar == "0":
                        leftStr.pop()
                        leftVal.pop()
                    leftStr += list("sec")
                    leftVal.extend([val for i in range(3)])
                    insertParantheses(val)
            
            case "Cot":
                if (leftVal[-1] != 0 and leftVal[-1] != 1) or (len(leftStr) == 1 and leftChar == "0"):
                    val = 70
                    val += funcCounts[6]
                    if leftChar == "0":
                        leftStr.pop()
                        leftVal.pop()
                    leftStr += list("cot")
                    leftVal.extend([val for i in range(3)])
                    insertParantheses(val)



    displayString = ""
    for i in leftStr:
        displayString += i
    for i in rightStr:
        displayString += i
    
    label["text"] = displayString


tab.mainloop()


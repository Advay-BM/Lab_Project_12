import tkinter
from tkinter import Radiobutton, messagebox
from mathFunctions import *

# To do:
# RCL, M+, Hyp, Inv, RAD, DEL

Value_buttons=[("!","abs","RCL","Hyp","Inv"),   #all the functions present in the calculator
               ("nPr","←","M+","→","nCr"),
               ("Rec()","Sin","Cos","Tan","Pol()"),
               ("RAD","Csc","Sec","Cot","10^x"),
               ("log","√","e","n√","ln"),
               ("(",")","π","^","ENG"),
               ("7","8","9","DEL","AC"),
               ("4","5","6","x","÷"),
               ("1","2","3","+","-"),
               ("0",".","=","Ans","EXP")]

right_buttons=  ["AC","÷","x","-","+","DEL","EXP","Ans"]
digit_buttons=     ["0","1","2","3","4","5","6","7","8","9",".","=",]
function_buttons=  ["!","abs","RCL","Hyp","Inv", "nPr","←","M+","→","nCr", "Rec()","Sin","Cos","Tan","Pol()", "RAD","Csc","Sec","Cot","10^x", "log","√","e","n√","ln", "(",")","π","^","ENG",]
non_enforced_buttons= ["AC", "DEL", "←", "→"]
spcl_buttons = ["RAD", "Hyp", "Inv"]
Light_blue="#ADD8E6"
Light_grey="#D3D3D3"
Pink="#FFC0CB"
row_count= len(Value_buttons)
column_count= len(Value_buttons[0])

tab=tkinter.Tk()
tab.title("SCIENTIFIC CALCULATOR")

frame= tkinter.Frame(tab)
label= tkinter.Label(frame, text="0|", font=("arial",20), background="black",
                     foreground="white", anchor="e", width= column_count,height= 2)
label.grid(row=0,column=0, columnspan=column_count, sticky="we")


RADLambda = lambda v = "RAD": buttons_pressed(v)
DEGLambda = lambda v = "DEG": buttons_pressed(v)
RADButton = tkinter.Button(frame, text="RAD", font=("arial",20),
                               width=column_count-1, height=1,
                               command= RADLambda, foreground="black", background=Light_grey)
RADButton.grid(row= 4, column= 0)

HypButton = tkinter.Button(frame, text="Hyp", font=("arial",20),
                               width=column_count-1, height=1,
                               command=lambda value="Hyp": buttons_pressed(value), foreground="black", background=Light_grey)
HypButton.grid(row= 1, column= 3)

InvButton = tkinter.Button(frame, text="Inv", font=("arial",20),
                               width=column_count-1, height=1,
                               command=lambda value="Inv": buttons_pressed(value), foreground="black", background=Light_grey)
InvButton.grid(row= 1, column= 4)


for row in range(row_count):
    for column in range(column_count):
        value=Value_buttons[row][column]
        if value not in spcl_buttons:
            buttons=tkinter.Button(frame, text=value, font=("arial",20),
                                width=column_count-1, height=1,
                                command=lambda value=value: buttons_pressed(value))
            if value in right_buttons:
                buttons.config(foreground="black", background=Light_blue)
            elif value in digit_buttons:
                buttons.config(foreground="black", background=Pink)
            elif value in function_buttons:
                buttons.config(foreground="black", background=Light_grey)
            else:
                buttons.config(foreground="black", background=Light_grey)
            buttons.grid(row=row+1, column=column)
            

        
frame.pack()

leftStr = ["0"]
leftVal = [0]
rightStr = []
rightVal = []
leftChar = "0"
rightChar = None
#               0   1    2    3    4    5    6    7   8   9   10   11    12   13   14   15    16    17   18
# Index order: (), sin, cos, tan, sec, cot, csc, EXP, !, abs, Rec, Pol, 10^x, log, ln, sqrt, nRoot, nPr, nCr
funcCounts = [0 for i in range(19)] # type: ignore # type: ignore
a = None
RADMode = True

"""
digit value: 0
. : 1
+ - x /: 2
, : 3
the value of a function is (x+1)*10 + funcCounts[x], where x is the corresponding index of the functions in funcCounts
This means that the code will break if you include more than 10 of the same function
"""
# I have not placed any restrictions when it comes to characters on the right side as the input goes from left to right

def insertParantheses(val): # type: ignore
    global leftChar, leftStr, leftVal, rightChar, rightStr, rightVal
    leftStr.append("(")
    leftVal.append(val) # type: ignore
    leftChar = "("
    rightStr.insert(0,")") # type: ignore
    rightVal.insert(0,val) # type: ignore
    rightChar = ")"

def canPlaceStdFunc():
    global leftVal, leftStr, leftChar
    return (leftVal[-1] != 0 and leftVal[-1] != 1) or (len(leftStr) == 1 and leftChar == "0")

def initStdFunc(ind):
    global funcCounts, leftChar, leftStr, leftVal
    val = (ind+1)* 10 + funcCounts[ind]
    if leftChar == "0":
        leftStr.pop()
        leftVal.pop()
    funcCounts[ind] += 1
    return val

def buttons_pressed(value): # type: ignore
    global leftChar, leftStr, leftVal, rightChar, rightStr, rightVal, funcCounts, a, RADButton, RADMode, RADLambda, DEGLambda
    
    if len(label["text"]) >= 25 and value not in non_enforced_buttons:         # Character limit
        return None

    if (value in right_buttons):
        match (value): # type: ignore
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
                if canPlaceStdFunc():
                    val = initStdFunc(7)
                    leftStr += list("exp")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)
            case "Ans":
                if a == None:
                    messagebox.showerror("ERROR: Cannot input answer", "Either an answer was not evaluated or the previous answer was invalid.\nPlease evaluate an expression using '=' before using 'Ans'")
                    return None
                if len(leftStr) == 1 and leftChar == "0":
                    leftStr[-1] = "a"
                else:
                    leftStr.append("a")
                    leftVal.append(0)
                leftChar = "a"
            case "+":
                # Should only be allowed if character to the left is not a decimal or another operator
                if leftVal[-1] != 2 and leftVal[-1] != 1:
                    leftChar = "+"
                    leftVal.append(2)
                    leftStr.append("+")
            case "-":
                # Same restriction as +
                if leftVal[-1] != 2 and leftVal[-1] != 1:
                    if len(leftStr) == 1 and leftChar == "0":
                        leftStr.pop()
                        leftVal.pop()
                    leftChar = "-"
                    leftStr.append("-")
                    leftVal.append(2)
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
                leftStr.append(value) # type: ignore
                leftVal.append(0)
            leftChar = value # type: ignore
        elif value == ".":
            canPlace = True
            # Go backwards through leftStr
            for i in range(-1, -len(leftVal)-1, -1):
                if leftVal[i] == 1 or leftVal[i] == 3:
                    # If we encounter another decimal point or a comma, do not allow to place
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
            # Move everything to a single array
            array = leftStr + rightStr
            arrayVals = leftVal + rightVal

            for i in range(array.count("!")):
                index = array.index("!")
                array.pop(index)
                paranthesesVal = arrayVals[index-1]
                paranthesesIndex = arrayVals.index(paranthesesVal)
                array[paranthesesIndex:paranthesesIndex] = list("factorial")

            for i in range(array.count("P")):
                index = array.index("P")
                array[index] = "p"
                paranthesesVal = arrayVals[index-1]
                paranthesesIndexn = arrayVals.index(paranthesesVal)
                paranthesesIndexr = index + 1
                n = array[paranthesesIndexn:index]

                array.insert(index+1, "r")
                arrayVals.insert(index+1, paranthesesVal)
                array[paranthesesIndexr+2:paranthesesIndexr+2] = n + [","]
                arrayVals[paranthesesIndexr+2:paranthesesIndexr+2] = list([paranthesesVal for i in range(len(n))]) + [3]
                array[paranthesesIndexn: index] = "n"
                arrayVals[paranthesesIndexn: index] = [paranthesesVal]

            for i in range(array.count("C")):
                index = array.index("C")
                array[index] = "c"
                paranthesesVal = arrayVals[index-1]
                paranthesesIndexn = arrayVals.index(paranthesesVal)
                paranthesesIndexr = index + 1
                n = array[paranthesesIndexn:index]

                array.insert(index+1, "r")
                arrayVals.insert(index+1, paranthesesVal)
                array[paranthesesIndexr+2:paranthesesIndexr+2] = n + [","]
                arrayVals[paranthesesIndexr+2:paranthesesIndexr+2] = list([paranthesesVal for i in range(len(n))]) + [3]
                array[paranthesesIndexn: index] = "n"
                arrayVals[paranthesesIndexn: index] = [paranthesesVal]

            for i in range(len(array)):
                match array[i]:
                    case "x":
                        if array[i-1] != "e" or array[i+1] != "p":
                            displayString += "*"
                        else:
                            displayString += "x"
                    case "^":
                        displayString += "**"
                    case "π":
                        displayString += "pi"
                    case "√":
                        displayString += "sqrt"
                    case _:
                        displayString += array[i]
            try:
                result = eval(displayString)
            except SyntaxError as err:
                messagebox.showerror("ERROR: Cannot compute", f"The calculator was unable to compute the given expression.\nPlease change it and try again.\nError Message: {err}") # type: ignore
            except ZeroDivisionError as err:
                messagebox.showerror("ERROR: Division by zero",f"Calculation could not be completed as there was an instance of division by zero.\nError Message: {err}")
            except OverflowError as err:
                messagebox.showerror("Error: Invalid input to inverse functions",f"The input to an inverse function was not valid, i.e, it is outside the orginal functions range.\nError Message: {err}")
            except Exception as err:
                messagebox.showerror("ERROR", f"Something went wrong...\nError Message: {err}") # type: ignore
            else:
                if type(result) == tuple:
                    result = f"{result[0]:.6f}, {result[1]:.6f}"
                    label["text"] = result
                elif type(result) == float:
                    a = result
                    label["text"] = f"{result:.6f}".rstrip("0")
                    if label["text"][-1] == ".":
                        label["text"] += "0"
                else:
                    a = result
                    label["text"] = str(result)

                if label["text"] == "inf":
                    a = None
                    messagebox.showwarning("WARNING: Infinity", "The calculation resulted in infinity\nPlease do not save the result or attempt further calculation to avoid errors\nPress the AC button to continue using the calculator")
                
                # Reset input label to hold result
                leftStr = []
                leftVal = []
                rightStr = []
                rightVal = []
                rightChar = None
                funcCounts = [0 for i in range(19)] # type: ignore
                for i in str(result):
                    leftStr.append(i) # type: ignore
                    match (i):
                        case "-":
                            leftVal.append(2) # type: ignore
                        case ".":
                            leftVal.append(1) # type: ignore
                        case ",":
                            leftVal.append(3)
                        case _:
                            leftVal.append(0) # type: ignore
                leftChar = leftStr[-1] # type: ignore
                label["text"] += "|"
                return None
            
    elif (value in function_buttons):
        match (value): # type: ignore
            case "←":
                if (leftStr != []):
                    storeStr = leftStr.pop()
                    storeVal = leftVal.pop()
                    rightStr.insert(0, storeStr) # type: ignore
                    rightVal.insert(0, storeVal) # type: ignore
                    rightChar = rightStr[0] # type: ignore
                    if (leftStr == []):
                        leftChar = None
                    else:
                        leftChar = leftStr[0]

            case "→":
                if (rightStr != []):
                    storeStr = rightStr.pop(0) # type: ignore
                    storeVal = rightVal.pop(0) # type: ignore
                    leftStr.append(storeStr) # type: ignore
                    leftVal.append(storeVal) # type: ignore
                    leftChar = leftStr[-1]
                    if (rightStr == []):
                        rightChar = None
                    else:
                        rightChar = rightStr[0] # type: ignore
            
            case "(":
                if canPlaceStdFunc():
                    val = initStdFunc(0)
                    insertParantheses(val)

            case "Sin":
                if canPlaceStdFunc():
                    val = initStdFunc(1)
                    leftStr += list("sin")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)

            case "Cos":
                if canPlaceStdFunc():
                    val = initStdFunc(2)
                    leftStr += list("cos")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)
                    

            case "Tan":
                if canPlaceStdFunc():
                    val = initStdFunc(3)
                    leftStr += list("tan")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)
            
            case "Csc":
                if canPlaceStdFunc():
                    val = initStdFunc(4)
                    leftStr += list("csc")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)
            
            case "Sec":
                if canPlaceStdFunc():
                    val = initStdFunc(5)
                    leftStr += list("sec")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)
            
            case "Cot":
                if canPlaceStdFunc():
                    val = initStdFunc(6)
                    leftStr += list("cot")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)
            
            case "!":
                if canPlaceStdFunc():
                    val = initStdFunc(8)
                    rightStr.insert(0, "!") # type: ignore
                    rightVal.insert(0, val) # type: ignore
                    insertParantheses(val)

            case "abs":
                if canPlaceStdFunc():
                    val = initStdFunc(9)
                    leftStr += list("abs")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)
            
            case "Rec()":
                if (len(leftStr) == 1 and leftChar == "0"):
                    val = initStdFunc(10)
                    leftStr += list("Rec")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)
                    rightStr.insert(0, ",") # type: ignore
                    rightVal.insert(0,3) # type: ignore
                    rightChar = ","

            case "Pol()":
                if (len(leftStr) == 1 and leftChar == "0"):
                    val = initStdFunc(11)
                    leftStr += list("Pol")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)
                    rightStr.insert(0, ",") # type: ignore
                    rightVal.insert(0,3) # type: ignore
                    rightChar = ","

            case "10^x":
                 if canPlaceStdFunc():
                    val = initStdFunc(12)
                    leftStr += list("10^")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)
            
            case "^":
                if leftVal[-1] != 2 and leftVal[-1] != 1 and leftChar != "(":
                    leftChar = "^"
                    leftVal.append(2)
                    leftStr.append("^")

            case "e":
                if len(leftStr) == 1 and leftChar == "0":
                    leftStr[-1] = value
                else:
                    leftStr.append(value)
                    leftVal.append(0)
                leftChar = value
            
            case "π":
                if len(leftStr) == 1 and leftChar == "0":
                    leftStr[-1] = value
                else:
                    leftStr.append(value)
                    leftVal.append(0)
                leftChar = value
            
            case "log":
                if canPlaceStdFunc():
                    val = initStdFunc(13)
                    leftStr += list("log")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)
            
            case "ln":
                if canPlaceStdFunc():
                    val = initStdFunc(14)
                    leftStr += list("ln")
                    leftVal.extend([val for i in range(2)]) # type: ignore
                    insertParantheses(val)
            
            case "√":
                if canPlaceStdFunc():
                    val = initStdFunc(15)
                    leftStr.append("√")
                    leftVal.append(val) # type: ignore
                    insertParantheses(val)

            case "n√":
                if canPlaceStdFunc():
                    val = initStdFunc(16)
                    leftStr += list("nRoot")
                    leftVal.extend([val for i in range(5)]) # type: ignore
                    insertParantheses(val)
                    rightStr.insert(0, ",") # type: ignore
                    rightVal.insert(0,3) # type: ignore
                    rightChar = ","
            
            case "nPr":
                if canPlaceStdFunc():
                    val = initStdFunc(17)
                    print(val)
                    insertParantheses(val)
                    rightStr.insert(1,"P")
                    rightVal.insert(1, val) # type: ignore
                    rightStr.insert(2,"(")
                    rightVal.insert(2, val) # type: ignore
                    rightStr.insert(3,")")
                    rightVal.insert(3, val) # type: ignore
            
            case "nCr":
                if canPlaceStdFunc():
                    val = initStdFunc(18)
                    insertParantheses(val)
                    rightStr.insert(1,"C")
                    rightVal.insert(1, val) # type: ignore
                    rightStr.insert(2,"(")
                    rightVal.insert(2, val) # type: ignore
                    rightStr.insert(3,")")
                    rightVal.insert(3, val) # type: ignore
            
            case "ENG":
                array = leftStr + rightStr
                arrayVals = leftVal+rightVal
                for i in range(len(array)):
                    if arrayVals[i] != 0 and arrayVals[i] != 1 and arrayVals[i] != 2:
                        return None
                
                inp = float("".join(array))
                magnitude = 0
                while abs(inp) < 1:
                    inp *= 10
                    magnitude -= 1
                while abs(inp) >= 10:
                    inp /= 10
                    magnitude += 1
                label["text"] = f"{inp}x10^({magnitude})"
                leftStr = []
                leftVal = []
                rightStr = []
                rightVal = []
                rightChar = None
                funcCounts = [0 for i in range(19)] # type: ignore
                for i in label["text"]:
                    leftStr.append(i) # type: ignore
                    match (i):
                        case "-" | "x" | "^":
                            leftVal.append(2) # type: ignore
                        case ".":
                            leftVal.append(1) # type: ignore
                        case "(" | ")":
                            leftVal.append(10)
                            funcCounts[0] += 1
                        case _:
                            leftVal.append(0) # type: ignore
                leftChar = leftStr[-1] # type: ignore
                label["text"] += "|"
                return None
            
            case "RAD":
                RADMode = False
                RADButton.config(text= "DEG", command= DEGLambda)
                function_buttons[15] = "DEG"
            
            case "DEG":
                RADMode = True
                RADButton.config(text= "RAD", command= RADLambda)
                function_buttons[15] = "RAD"


    displayString = ""
    for i in leftStr:
        displayString += i
    displayString += "|"
    for i in rightStr: # type: ignore
        displayString += i # type: ignore
    
    label["text"] = displayString

tab.mainloop()
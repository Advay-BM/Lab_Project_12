from tkinter import messagebox
from mathFunctions import *
from definitions import *

tab.title("SCIENTIFIC CALCULATOR")

label.grid(row= 0,column= 0, columnspan= column_count, sticky= "we")

# Inititialize special buttons
# I could not find a way to abstract this to make it look nice
RADButton.config(command= lambda v = "RAD": buttons_pressed(v))
RADButton.grid(row= 4, column= 0)

sinButton.config(command= lambda v = "sin": buttons_pressed(v))
sinButton.grid(row= 3, column= 1)
cosButton.config(command= lambda v = "cos": buttons_pressed(v))
cosButton.grid(row= 3, column= 2)
tanButton.config(command= lambda v = "tan": buttons_pressed(v))
tanButton.grid(row= 3, column= 3)
cscButton.config(command= lambda v = "csc": buttons_pressed(v))
cscButton.grid(row= 4, column= 3)
secButton.config(command= lambda v = "sec": buttons_pressed(v))
secButton.grid(row= 4, column= 1)
cotButton.config(command= lambda v = "cot": buttons_pressed(v))
cotButton.grid(row= 4, column= 2)

# Place the rest of the buttons in their spots and give them their color
for row in range(row_count):
    for column in range(column_count):

        # Use the name of the buttons when figuring out which one was pressed
        value = Value_buttons[row][column]

        # Special buttons were already initialized
        if value not in spcl_buttons:

            buttons=tkinter.Button(frame, text=value, font=("arial",20), width= column_count-1, height= 1, command= lambda value= value: buttons_pressed(value))
            
            if value in right_buttons:
                buttons.config(foreground="black", background=light_blue)
            elif value in digit_buttons:
                buttons.config(foreground="black", background=pink)
            elif value in function_buttons:
                buttons.config(foreground="black", background=light_grey)
            else:
                buttons.config(foreground="black", background=light_grey)

            buttons.grid(row=row+1, column=column)
            
frame.pack()

# Abstraction/Macro
def insertParantheses(val):                                                 # type: ignore
    global leftChar, leftStr, leftVal, rightStr, rightVal
    leftStr.append("(")
    leftVal.append(val)                                                     # type: ignore
    leftChar = "("
    rightStr.insert(0,")")                                                  # type: ignore
    rightVal.insert(0,val)                                                  # type: ignore

# Abstraction/Macro
def canPlaceStdFunc():
    global leftVal, leftStr, leftChar
    return (leftVal[-1] != 0 and leftVal[-1] != 1) or (len(leftStr) == 1 and leftChar == "0")

# Abstraction/Macro
def initStdFunc(ind):
    global funcCounts, leftChar, leftStr, leftVal
    val = (ind+1)* 10 + funcCounts[ind]
    if leftChar == "0":
        leftStr.pop()
        leftVal.pop()
    funcCounts[ind] += 1
    return val

# Abstraction/Macro
def changeTrigButtonText(prefix= "", suffix= ""):
    global sinButton, cosButton, tanButton, secButton, cotButton, cscButton
    sinButton.config(text= f"{prefix}sin{suffix}")
    cosButton.config(text= f"{prefix}cos{suffix}")
    tanButton.config(text= f"{prefix}tan{suffix}")
    cscButton.config(text= f"{prefix}csc{suffix}")
    secButton.config(text= f"{prefix}sec{suffix}")
    cotButton.config(text= f"{prefix}cot{suffix}")

# The place where stuff actually happens
def buttons_pressed(value):                                                 # type: ignore
    global leftChar, leftStr, leftVal, rightStr, rightVal, funcCounts, Ans, RADButton, RADMode, sinButton, cosButton, tanButton, secButton, cotButton, cscButton, HypMode, InvMode, save, saveVal
    
    if len(label["text"]) >= 25 and value not in non_enforced_buttons:         # Character limit
        return None

    if (value in right_buttons):
        match (value):                                                      # type: ignore
            case "AC":
                # Reset everything
                leftStr = ["0"]
                leftVal = [0]
                rightStr = []
                rightVal = []
                leftChar = "0"

            case "DEL":
                # Don't do anything if there is nothing left to delete
                if leftStr == []:
                    return None

                # Delete the entire function if we are deleting a function
                # Delete a single character otherwise
                if (leftVal[-1] > 9):
                    val = leftVal[-1]

                    i = 0
                    while val in leftVal:
                        if (leftVal[i] == val):
                            leftVal.pop(i)
                            leftStr.pop(i)
                            i -= 1
                        i += 1

                    i = 0
                    while val in rightVal:
                        if (rightVal[i] == val):
                            rightVal.pop(i)
                            rightStr.pop(i)
                            i -= 1
                        i += 1
                else:
                    leftStr.pop()
                    leftVal.pop()
                
                if (leftStr == []):
                    # We cannot have an empty display
                    if (rightStr == []):
                        leftChar = "0"
                        leftStr = ["0"]
                        leftVal = [0]
                    else:
                        leftChar = None
                else:
                    leftChar = leftStr[-1]

            case "EXP":
                if canPlaceStdFunc():
                    val = initStdFunc(7)
                    leftStr += list("exp")
                    leftVal.extend([val for i in range(3)]) # type: ignore
                    insertParantheses(val)

            case "Ans":
                if Ans == None:
                    messagebox.showerror("ERROR: Cannot input answer", "Either an answer was not evaluated or the previous answer was invalid.\nPlease evaluate an expression using '=' before using 'Ans'")
                    return None
                
                if len(leftStr) == 1 and leftChar == "0":
                    leftStr[-1] = "Ans"
                else:
                    leftStr.append("Ans")
                    leftVal.append(0)

                leftChar = "Ans"

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

            case "/":
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
                leftStr.append(value)                                       # type: ignore
                leftVal.append(0)
            leftChar = value                                                # type: ignore

        elif value == ".":
            # Go backwards through leftStr
            for i in range(-1, -len(leftVal)-1, -1):
                if leftVal[i] == 1 or leftVal[i] == 3:
                    # If we encounter another decimal point or a comma, do not allow to place
                    return None
                
                if leftVal[i] != 0:
                    # Stop checking if we reach the end of the number
                    break

            if leftVal[-1] == 0:
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
                facVal = arrayVals[index]
                array[index] = ")"
                for i in range(index,-1,-1):
                    if arrayVals[i] == 2:
                        array.insert(i+1,"factorial(")
                        arrayVals.insert(i+1,facVal)
                        break
                    if i == 0:
                        array.insert(0,"factorial(")
                        arrayVals.insert(0,facVal)
                        break

            # I am NOT documenting the logic for these, or not now atleast...
            for i in range(array.count("P")):
                index = array.index("P")
                if array[index+1] == "o":
                    break
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

            if not (RADMode):
                # Reverse everything, becuase the first occurrence of a value is guaranteed to be the closing parantheses
                arrayVals = arrayVals[::-1]
                array = array[::-1]

                for i in range(0,10):
                    # Sneakily insert rad = False, so that the math function can handle the conversion
                    # Have to do 6 times for all 6 trig functions, could not find a good way to abstract
                    if (arrayVals.count(20+i)) > 0:
                        index = arrayVals.index(20+i)
                        array.insert(index + 1, ", rad = False")
                        arrayVals.insert(index + 1, 20 + i)

                    if (arrayVals.count(30+i)) > 0:
                        index = arrayVals.index(30+i)
                        array.insert(index + 1, ", rad = False")
                        arrayVals.insert(index + 1, 30 + i)

                    if (arrayVals.count(40+i)) > 0:
                        index = arrayVals.index(40+i)
                        array.insert(index + 1, ", rad = False")
                        arrayVals.insert(index + 1, 40 + i)

                    if (arrayVals.count(50+i)) > 0:
                        index = arrayVals.index(50+i)
                        array.insert(index + 1, ", rad = False")
                        arrayVals.insert(index + 1, 50 + i)

                    if (arrayVals.count(60+i)) > 0:
                        index = arrayVals.index(60+i)
                        array.insert(index + 1, ", rad = False")
                        arrayVals.insert(index + 1, 60 + i)

                    if (arrayVals.count(70+i)) > 0:
                        index = arrayVals.index(70+i)
                        array.insert(index + 1, ", rad = False")
                        arrayVals.insert(index + 1, 70 + i)
                    
                    if (arrayVals.count(110+i)) > 0:
                        index = arrayVals.index(110+i)
                        array.insert(index + 1, ", rad = False")
                        arrayVals.insert(index + 1, 110 + i)

                    if (arrayVals.count(120+i)) > 0:
                        index = arrayVals.index(120+i)
                        array.insert(index + 1, ", rad = False")
                        arrayVals.insert(index + 1, 120 + i)
                # Return evrything to normal
                array = array[::-1]
                arrayVals = arrayVals[::-1]

            for i in range(len(array)):
                # Perform certain conversions for eval
                match array[i]:
                    case "x":
                        # Be careful because exp has a x in it
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
                # Eval does most of the heavy lifting here, although probably might be easily possible without it?
                result = eval(displayString)

            # Handle errors
            except SyntaxError as err:
                messagebox.showerror("ERROR: Cannot compute", f"The calculator was unable to compute the given expression.\nPlease change it and try again.\nError Message: {err}") # type: ignore
            except ZeroDivisionError as err:
                messagebox.showerror("ERROR: Division by zero",f"Calculation could not be completed as there was an instance of division by zero.\nError Message: {err}")
            except OverflowError as err:
                messagebox.showerror("Error: Invalid input",f"The input to a function was not valid, i.e, it is outside the function's domain.")
            except Exception as err:
                messagebox.showerror("ERROR", f"Something went wrong...\nError Message: {err}") # type: ignore
            
            else:

                if type(result) == tuple:
                    # Used when a coordinate conversion was performed
                    result = f"{result[0]:.6f}, {result[1]:.6f}"
                    label["text"] = result

                elif type(result) == float:
                    # Truncate the result to 6 decimal places
                    # Prevent -0.0
                    if f"{result:.6f}" == "-0.000000":
                        result = 0
                    Ans = result
                    label["text"] = f"{result:.6f}".rstrip("0")
                    if label["text"][-1] == ".":
                        label["text"] += "0"
                else:
                    Ans = result
                    label["text"] = str(result)

                # Handle the case of infinity result
                if label["text"] == "inf" or label["text"] == "-inf":
                    Ans = None
                    messagebox.showwarning("WARNING: Infinity", "The calculation resulted in infinity\nPlease do not save the result or attempt further calculation to avoid errors\nPress the AC button to continue using the calculator")
                
                # Reset these to hold result
                leftStr = []
                leftVal = []
                rightStr = []
                rightVal = []
                funcCounts = [0 for i in range(19)]                         # type: ignore
                for i in str(result):
                    leftStr.append(i)                                       # type: ignore
                    match (i):
                        case "-":
                            leftVal.append(2)                               # type: ignore
                        case ".":
                            leftVal.append(1)                               # type: ignore
                        case ",":
                            leftVal.append(3)
                        case _:
                            leftVal.append(0)                               # type: ignore
                leftChar = leftStr[-1]                                      # type: ignore
                label["text"] += "|"
                return None
            
    elif (value in function_buttons):
        match (value):                                                      # type: ignore
            case "←":
                # Only perform the action if we are not at the leftmost end
                if (leftStr != []):
                    # Move the last character in the left to the right
                    storeStr = leftStr.pop()
                    storeVal = leftVal.pop()
                    rightStr.insert(0, storeStr)                            # type: ignore
                    rightVal.insert(0, storeVal)                            # type: ignore
                    if (leftStr == []):
                        leftChar = None
                    else:
                        leftChar = leftStr[0]

            case "→":
                # Only perform the action if we are not at the rightmost end
                if (rightStr != []):
                    # Move the last character in the right to the left
                    storeStr = rightStr.pop(0)                              # type: ignore
                    storeVal = rightVal.pop(0)                              # type: ignore
                    leftStr.append(storeStr)                                # type: ignore
                    leftVal.append(storeVal)                                # type: ignore
                    leftChar = leftStr[-1]
            
            case "(":
                if canPlaceStdFunc():
                    val = initStdFunc(0)
                    insertParantheses(val)

            case "sin":
                if canPlaceStdFunc():
                    val = initStdFunc(1)
                    if (InvMode and not(HypMode)):
                        leftStr += list("asin")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and not(InvMode)):
                        leftStr += list("sinh")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and InvMode):
                        leftStr += list("asinh")
                        leftVal.extend([val for i in range(5)])             # type: ignore
                    else:
                        leftStr += list("sin")
                        leftVal.extend([val for i in range(3)])             # type: ignore
                    insertParantheses(val)

            case "cos":
                if canPlaceStdFunc():
                    val = initStdFunc(2)
                    if (InvMode and not(HypMode)):
                        leftStr += list("acos")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and not(InvMode)):
                        leftStr += list("cosh")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and InvMode):
                        leftStr += list("acosh")
                        leftVal.extend([val for i in range(5)])             # type: ignore
                    else:
                        leftStr += list("cos")
                        leftVal.extend([val for i in range(3)])             # type: ignore
                    insertParantheses(val)
                    

            case "tan":
                if canPlaceStdFunc():
                    val = initStdFunc(3)
                    if (InvMode and not(HypMode)):
                        leftStr += list("atan")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and not(InvMode)):
                        leftStr += list("tanh")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and InvMode):
                        leftStr += list("atanh")
                        leftVal.extend([val for i in range(5)])             # type: ignore
                    else:
                        leftStr += list("tan")
                        leftVal.extend([val for i in range(3)])             # type: ignore
                    insertParantheses(val)
            
            case "csc":
                if canPlaceStdFunc():
                    val = initStdFunc(4)
                    if (InvMode and not(HypMode)):
                        leftStr += list("acsc")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and not(InvMode)):
                        leftStr += list("csch")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and InvMode):
                        leftStr += list("acsch")
                        leftVal.extend([val for i in range(5)])             # type: ignore
                    else:
                        leftStr += list("csc")
                        leftVal.extend([val for i in range(3)])             # type: ignore
                    insertParantheses(val)
            
            case "sec":
                if canPlaceStdFunc():
                    val = initStdFunc(5)
                    if (InvMode and not(HypMode)):
                        leftStr += list("asec")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and not(InvMode)):
                        leftStr += list("sech")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and InvMode):
                        leftStr += list("asech")
                        leftVal.extend([val for i in range(5)])             # type: ignore
                    else:
                        leftStr += list("sec")
                        leftVal.extend([val for i in range(3)])             # type: ignore
                    insertParantheses(val)
            
            case "cot":
                if canPlaceStdFunc():
                    val = initStdFunc(6)
                    if (InvMode and not(HypMode)):
                        leftStr += list("acot")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and not(InvMode)):
                        leftStr += list("coth")
                        leftVal.extend([val for i in range(4)])             # type: ignore
                    elif (HypMode and InvMode):
                        leftStr += list("acoth")
                        leftVal.extend([val for i in range(5)])             # type: ignore
                    else:
                        leftStr += list("cot")
                        leftVal.extend([val for i in range(3)])             # type: ignore
                    insertParantheses(val)
            
            case "!":
                if leftVal[-1] == 0 or leftChar == ")":
                    val = 90 + funcCounts[8]
                    funcCounts[8] += 1
                    leftStr.append("!")                                     # type: ignore
                    leftVal.append(val)                                     # type: ignore

            case "abs":
                if canPlaceStdFunc():
                    val = initStdFunc(9)
                    leftStr += list("abs")
                    leftVal.extend([val for i in range(3)])                 # type: ignore
                    insertParantheses(val)
            
            case "Rec()":
                # Only allow conversion when display is clear
                if (len(leftStr) == 1 and leftChar == "0"):
                    val = initStdFunc(10)
                    leftStr += list("Rec")
                    leftVal.extend([val for i in range(3)])                 # type: ignore
                    insertParantheses(val)
                    rightStr.insert(0, ",")                                 # type: ignore
                    rightVal.insert(0,3)                                    # type: ignore

            case "Pol()":
                # Only allow conversion when display is clear
                if (len(leftStr) == 1 and leftChar == "0"):
                    val = initStdFunc(11)
                    leftStr += list("Pol")
                    leftVal.extend([val for i in range(3)])                 # type: ignore
                    insertParantheses(val)
                    rightStr.insert(0, ",")                                 # type: ignore
                    rightVal.insert(0,3)                                    # type: ignore

            case "10^x":
                 if canPlaceStdFunc():
                    val = initStdFunc(12)
                    leftStr += list("10^")
                    leftVal.extend([val for i in range(3)])                 # type: ignore
                    insertParantheses(val)
            
            case "^":
                if leftVal[-1] != 2 and leftVal[-1] != 1 and leftChar != "(":
                    leftChar = "^"
                    leftVal.append(2)
                    leftStr.append("^")

            case "e":
                if len(leftStr) == 1 and leftChar == "0":
                    leftStr[-1] = value
                    leftChar = value
                else:
                    if leftVal[-1] != 0:
                        leftStr.append(value)
                        leftVal.append(0)
                        leftChar = value
            
            case "π":
                if len(leftStr) == 1 and leftChar == "0":
                    leftStr[-1] = value
                    leftChar = value
                else:
                    if leftVal[-1] != 0:
                        leftStr.append(value)
                        leftVal.append(0)
                        leftChar = value
            
            case "log":
                if canPlaceStdFunc():
                    val = initStdFunc(13)
                    leftStr += list("log")
                    leftVal.extend([val for i in range(3)])                 # type: ignore
                    insertParantheses(val)
            
            case "ln":
                if canPlaceStdFunc():
                    val = initStdFunc(14)
                    leftStr += list("ln")
                    leftVal.extend([val for i in range(2)])                 # type: ignore
                    insertParantheses(val)
            
            case "√":
                if canPlaceStdFunc():
                    val = initStdFunc(15)
                    leftStr.append("√")
                    leftVal.append(val)                                     # type: ignore
                    insertParantheses(val)

            case "n√":
                if canPlaceStdFunc():
                    val = initStdFunc(16)
                    leftStr += list("nRoot")
                    leftVal.extend([val for i in range(5)])                 # type: ignore
                    insertParantheses(val)
                    # first argument is n, second is the actual value
                    rightStr.insert(0, ",")                                 # type: ignore
                    rightVal.insert(0,3)                                    # type: ignore
            
            case "nPr":
                if canPlaceStdFunc():
                    val = initStdFunc(17)
                    print(val)
                    insertParantheses(val)
                    rightStr.insert(1,"P")
                    rightVal.insert(1, val)                                 # type: ignore
                    rightStr.insert(2,"(")
                    rightVal.insert(2, val)                                 # type: ignore
                    rightStr.insert(3,")")
                    rightVal.insert(3, val)                                 # type: ignore
            
            case "nCr":
                if canPlaceStdFunc():
                    val = initStdFunc(18)
                    insertParantheses(val)
                    rightStr.insert(1,"C")
                    rightVal.insert(1, val)                                 # type: ignore
                    rightStr.insert(2,"(")
                    rightVal.insert(2, val)                                 # type: ignore
                    rightStr.insert(3,")")
                    rightVal.insert(3, val)                                 # type: ignore
            
            case "ENG":
                # Convert answer to standard form
                if (len(leftStr) == 1 and leftChar == "0"):
                    return None
                # Merge left and right
                array = leftStr + rightStr
                arrayVals = leftVal+rightVal

                # Only convert if there is just a number in the display
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

                # Display and set the variables accordingly
                label["text"] = f"{inp}x10^({magnitude})"

                leftStr = []
                leftVal = []
                rightStr = []
                rightVal = []
                funcCounts = [0 for i in range(19)]                         # type: ignore

                for i in label["text"]:
                    leftStr.append(i)                                       # type: ignore
                    match (i):
                        case "-" | "x" | "^":
                            leftVal.append(2)                               # type: ignore
                        case ".":
                            leftVal.append(1)                               # type: ignore
                        case "(" | ")":
                            leftVal.append(10)
                            funcCounts[0] += 1
                        case _:
                            leftVal.append(0)                               # type: ignore
                leftChar = leftStr[-1]                                      # type: ignore
                label["text"] += "|"
                return None
            
            case "RAD":
                if (RADMode):
                    RADMode = False
                    RADButton.config(text= "DEG")
                else:
                    RADMode = True
                    RADButton.config(text= "RAD")
                return None
            
            case "Hyp":
                HypMode = False if HypMode else True
                
            case "Inv":
                InvMode = False if InvMode else True
            
            case "SAVE":
                save = leftStr + rightStr
                saveVal = leftVal + rightVal
                return None
            
            case "RCL":
                if (save == []):
                    messagebox.showerror("ERROR: No save to recall", "Please save something before attempting to recall.")
                    return None
                
                if (len(leftStr) == 1 and leftChar == "0"):
                    leftStr.pop()
                    leftVal.pop()

                leftStr += save
                leftVal += saveVal
                leftChar = leftStr[-1]

            case ")":
                # Because of the way DEL works, should NEVER need to be called but just in case...
                blacklistVals = []
                found = False

                # Logic for finding the correct value of the parantheses
                for i in range(-1, -len(leftStr)-1, -1):
                    if (leftStr[i] == ")"):
                        blacklistVals.append(leftVal[i])
                    if (leftStr[i] == "(" and leftVal[i] not in blacklistVals and leftVal[i] not in rightVal):
                        found = True
                        leftStr.append(")")
                        leftVal.append(leftVal[i])
                        leftChar = ")"
                if not found:
                    return None

    if (InvMode and not(HypMode)):
        changeTrigButtonText(prefix= "a")
    elif (HypMode and not(InvMode)):
        changeTrigButtonText(suffix= "h")
    elif (HypMode and InvMode):
        changeTrigButtonText(prefix= "a", suffix= "h")
    else:
        changeTrigButtonText()

    displayString = ""
    for i in leftStr:
        displayString += i
    displayString += "|"
    for i in rightStr:                                                      # type: ignore
        displayString += i                                                  # type: ignore
    
    label["text"] = displayString

tab.mainloop()
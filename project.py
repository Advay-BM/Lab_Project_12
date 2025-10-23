import tkinter
import mathFunctions as m

Value_buttons=[("!","mod","RCL","Hyp","Inv"),   #all the functions present in the calculator
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
function_buttons=  ["!","mod","RCL","Hyp","Inv", "nPr","←","M+","→","nCr", "Rec()","Sin","Cos","Tan","Pol()", "DEG","Csc","Sec","Cot","10^x", "log","√","e","n√","ln", "(",")","π","^","ENG",]
Light_blue="#ADD8E6"
Light_grey="#D3D3D3"

row_count= len(Value_buttons)
column_count= len(Value_buttons[0])

tab=tkinter.Tk()
tab.title("SCIENTIFIC CALCULATOR")

frame= tkinter.Frame(tab)
label= tkinter.Label(frame, text="0", font=("arial",30), background="black",
                     foreground="white", anchor="e", width= column_count)
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

"""
digit value: 0
decimal value: 1
+ - x /: 2
"""
# I have not placed any restrictions when it comes to characters on the right side as the input goes from left to right

def buttons_pressed(value):
    global leftChar, leftStr, leftVal, rightChar, rightStr, rightVal
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
                ...
            case "Ans":
                ...
            case "+":
                # Should only be allowed if character to te left is not a decimal or another operator
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
                # Should only be allowed if character to left is a digit
                if leftVal[-1] == 0:
                    leftChar = "x"
                    leftVal.append(2)
                    leftStr.append("x")
            case "÷":
                # Same restriction as x
                if leftVal[-1] == 0:
                    leftChar = "/"
                    leftVal.append(2)
                    leftStr.append("/")
    
    elif (value in digit_buttons):
        if value in "0123456789":
            if leftChar == "0":
                leftStr[-1] = value
            else:
                leftStr.append(value)
                leftVal.append(0)
            leftChar = value
        elif value == ".":
            canPlace = True
            for i in range(-1, -len(leftVal)-1, -1):
                if leftVal[i] == 1:
                    canPlace = False
                    break
                if leftVal[i] != 0:
                    break

            if leftVal[-1] == 0 and canPlace:
                leftChar = "."
                leftVal.append(1)
                leftStr.append(".")
        else:
            # Display result
            displayString = ""
            for i in range(len(leftStr)):
                if leftStr[i] == "x":
                    displayString += "*"
                elif leftStr[i] == "÷":
                    displayString += "/"
                else:
                    displayString += leftStr[i]
            for i in rightStr:
                if rightStr[i] == "x":
                    displayString += "*"
                elif rightStr[i] == "÷":
                    displayString += "/"
                else:
                    displayString += rightStr[i]
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
            return None
    elif (value in function_buttons):
        ...

    displayString = ""
    for i in leftStr:
        displayString += i
    for i in rightStr:
        displayString += i
    
    label["text"] = displayString


tab.mainloop()


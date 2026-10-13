from definitions import *
from buttons import *

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
def changeTrigButtonText(prefix= "", suffix= ""):
    global sinButton, cosButton, tanButton, secButton, cotButton, cscButton
    sinButton.config(text= f"{prefix}sin{suffix}")
    cosButton.config(text= f"{prefix}cos{suffix}")
    tanButton.config(text= f"{prefix}tan{suffix}")
    cscButton.config(text= f"{prefix}csc{suffix}")
    secButton.config(text= f"{prefix}sec{suffix}")
    cotButton.config(text= f"{prefix}cot{suffix}")

""" THE PLAN
2. Load the data, and pass into button functions as a list
3. Button functions may unpack the list and use the data in the form of local variables, and must return updated data as a list
4. Rewrite the updated data back into the file
"""


# The place where stuff actually happens
def buttons_pressed(value):
    global RADButton

    objList = readFromFile()

    if len(label["text"]) >= 50 and value not in non_enforced_buttons:         # Character limit
        return None

    if (value in right_buttons):
        match (value):
            case "AC":
                # Reset everything
                objList[:5] = ["0", ["0"], [0], [], []]

            case "DEL":
                objList = DEL_bttn(objList)

            case "EXP":
                objList = EXP_bttn(objList)

            case "Ans":
                objList = Ans_bttn(objList)

            case "+":
                objList = plus_bttn(objList)

            case "-":
                objList = sub_bttn(objList)

            case "x":
                objList = mult_bttn(objList)

            case "/":
                objList = div_bttn(objList)

    elif (value in digit_buttons):
        if value in "0123456789":
            objList = digit_bttn(objList, value)

        elif value == ".":
            objList = period_bttn(objList)

        else:
            objList = equal_bttn(objList, label)

    elif (value in function_buttons):
        match (value):
            case "←":
                objList = larrow_bttn(objList)

            case "→":
                objList = rarrow_bttn(objList)

            case "(":
                objList = lparen_bttn(objList)

            case "sin":
                objList = sin_bttn(objList)

            case "cos":
                objList = cos_bttn(objList)

            case "tan":
                objList = tan_bttn(objList)

            case "csc":
                objList = csc_bttn(objList)

            case "sec":
                objList = sec_bttn(objList)

            case "cot":
                objList = cot_bttn(objList)

            case "!":
                objList = factorial_bttn(objList)

            case "mod":
                objList = mod_bttn(objList)

            case "Rec()":
                objList = Rec_bttn(objList)

            case "Pol()":
                objList = Pol_bttn(objList)

            case "10^x":
                objList = power10_bttn(objList)

            case "^":
                objList = power_bttn(objList)

            case "e":
                objList = e_bttn(objList, value)

            case "π":
                objList = pi_bttn(objList, value)

            case "log":
                objList = log_bttn(objList)

            case "ln":
                objList = ln_bttn(objList)

            case "√":
                objList = sqrt_bttn(objList)

            case "n√":
                objList = nsqrt_bttn(objList)

            case "nPr":
                objList = npr_bttn(objList)

            case "nCr":
                objList = ncr_bttn(objList)

            case "ENG":
                objList = eng_bttn(objList, label)

            case "RAD":
                RADMode = objList[6]
                if (RADMode):
                    RADMode = False
                    RADButton.config(text= "DEG")
                else:
                    RADMode = True
                    RADButton.config(text= "RAD")

            case "Hyp":
                objList[7] = False if objList[7] else True

            case "Inv":
                objList[8] = False if objList[8] else True

            case "SAVE":
                objList = save_bttn(objList)

            case "RCL":
                objList = recall_bttn(objList)

            case ")":
                objList = rparen_bttn(objList)

    if objList == None:
        return

    leftStr = objList[1]
    rightStr = objList[3]
    HypMode = objList[7]
    InvMode = objList[8]

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
    for i in rightStr:
        displayString += i

    label["text"] = displayString
    if (len(label["text"]) > 10):
        label.config(font= ["arial", int(27*2.718281828459045235**((-len(label["text"])+10)*0.0274653072167027))]) # Magic constant is approx (ln 3)/(50-10)
    else:
        label.config(font= ["arial", 23])

    writeToFile(objList)


tab.mainloop()
fhandle.close()
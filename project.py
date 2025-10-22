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

def buttons_pressed(value):
    if (value in right_buttons):
        ...
    elif (value in digit_buttons):
        ...
    elif (value in function_buttons):
        ...

tab.mainloop()


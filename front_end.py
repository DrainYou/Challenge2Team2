"""This code is for the UI of the ENGS101P Challenge 2 Project for Team 2
Non-standard libraries used are Pyserial and MatPlotLib"""

from tkinter import *
from tkinter import ttk
from decimal import *
from serial import *

root = Tk()

#Stores the current values of the variables for the Label
displayed_temp = StringVar()
displayed_ph = StringVar()
displayed_stir = StringVar()

#Stores the value of the setpoints
displayed_temp_setpoint = StringVar()
displayed_ph_setpoint = StringVar()
displayed_stir_setpoint = StringVar()

#Three launchpads have been
heat_launchpad = Serial('COM3', timeout=0, writeTimeout=0)
ph_launchpad = Serial(timeout=0, writeTimeout=0)
stir_launchpad = Serial(timeout=0, writeTimeout=0)

def rolling_temperature():
    heat_output = str(heat_launchpad.readline())

    formatted_heat = heat_output
    formatted_heat = formatted_heat.rstrip("\\r\\n'")
    formatted_heat = formatted_heat.strip("b'")
    displayed_temp.set(formatted_heat + '\u2103')
    ttk.Label(root, textvariable=displayed_temp).grid(row=0, column=4)

    root.after(100, rolling_temperature)

def rolling_ph():
    ph_output = str(ph_launchpad.readline())

    formatted_ph = ph_output
    formatted_ph = formatted_ph.rstrip("\\r\\n'")
    formatted_ph = formatted_ph.strip("b'")
    displayed_ph.set(formatted_ph)
    ttk.Label(root, textvariable=displayed_ph).grid(row=1, column=4)

    root.after(100, rolling_ph)

def rolling_stir():
    stir_output = str(stir_launchpad.readline())

    formatted_stir = stir_output
    formatted_stir = formatted_stir.rstrip("\\r\\n'")
    formatted_stir = formatted_stir.strip("b'")
    displayed_stir.set(formatted_stir + "RPM")
    ttk.Label(root, textvariable=displayed_stir).grid(row=2, column=4)

    root.after(100, rolling_stir)

def update_temppoint():
    if temp_verification(var_values[0].get()) == True:
        temp_set = var_values[0].get()
        displayed_temp_setpoint.set("Current temperature setpoint: " + temp_set + "\u2103")
        ser.write(chr(int(temp_set)).encode())
    else:
        displayed_temp_setpoint.set("Please enter a value between 25 and 35 (inclusive).")
    ttk.Label(root, textvariable = displayed_temp_setpoint).grid(row = 3, column = 0) 
    var_values[0].delete(0, 100)
    

def update_phpoint():
    if ph_verification(var_values[1].get()) == True:
        ph_set = var_values[1].get()
        displayed_ph_setpoint.set("Current pH setpoint: " + ph_set)
        ser.write(chr(int(ph_set)).encode())
    else:
        displayed_ph_setpoint.set("Please enter a value between 3 and 7 (inclusive).")
    ttk.Label(root, textvariable = displayed_ph).grid(row = 4, column = 0) 
    var_values[1].delete(0, 100)


def update_stirpoint():
    if stir_verification(var_values[2].get()) == True:
        stir_set = var_values[2].get()
        displayed_stir.set("Current stirring setpoint: " + stir_set + " RPM")
        ser.write(chr(int(stir_set) // 20).encode()) # Have to divide to send over serial, multiplied by 20 for Launchpad
    else:
        displayed_stir.set("Please enter a value between 500 and 1500 (inclusive).")
    ttk.Label(root, textvariable = displayed_stir).grid(row = 5, column = 0) 
    var_values[2].delete(0, 100)
    

controllables = ['Temperature', 'pH', 'Stirring']
var_values = ['new_temp', 'new_ph', 'new_stir']
command_names = [update_temppoint, update_phpoint, update_stirpoint]
units = ['(\u2103)', '', '(RPM)']

def temp_verification(entered):
    if entered.isdigit():
        if Decimal(entered) >= 25 and Decimal(entered) <= 35:
            return True
        else:
            return False
    else:
        return False

def ph_verification(entered):
    if entered.isdigit():
        if Decimal(entered) >= 3 and Decimal(entered) <= 7:
            return True
        else:
            return False
    else:
        return False

def stir_verification(entered):
    if entered.isdigit():
        if Decimal(entered) >= 500 and Decimal(entered) <= 1500:
            return True
        else:
            return False
    else:
        return False


for i in range (0, 3):
    var_values[i] = ttk.Entry(root, width = 20)
    var_values[i].grid(row=i, column=1)
    enter = ttk.Button(root, command= command_names[i] , text="Enter")
    enter.grid(row=i, column=2)
    ttk.Label(root, text="Update " + controllables[i] + " Setpoint " + units[i]).grid(row=i, column=0)
    ttk.Label(root, text="Current " + controllables[i] + ": ").grid(row=i, column=3)

rolling_temperature()
rolling_ph()
rolling_stir()
root.mainloop()
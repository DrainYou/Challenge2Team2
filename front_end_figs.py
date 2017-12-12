"""This code is for the UI of the ENGS101P Challenge 2 Project for Team 2
External libraries used are Pyserial and MatPlotLib"""
from tkinter import *
from tkinter import ttk
from decimal import *
from serial import *
import matplotlib.pyplot as plt

plt.ion()
root = Tk()

#Stores the current values of the variables for the Label
displayed_temp = StringVar()
displayed_ph = StringVar()
displayed_stir = StringVar()

#Stores the value of the setpoints
displayed_temp_setpoint = StringVar()
displayed_ph_setpoint = StringVar()
displayed_stir_setpoint = StringVar()

#heat_launchpad = Serial('COM3', timeout=0, writeTimeout=0)
#ph_launchpad = Serial('COM7', timeout=0, writeTimeout=0)
stir_launchpad = Serial('COM6', timeout=0, writeTimeout=0)

temp_y_vals = []
temp_x_vals = []
temp_count = 0

ph_y_vals = []
ph_x_vals = []
ph_count = 0

stir_y_vals = []
stir_x_vals = []
stir_count = 0

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def rolling_temperature():
    global temp_count
    heat_output = str(heat_launchpad.readline())

    formatted_heat = heat_output
    formatted_heat = formatted_heat.rstrip("\\r\\n'")
    formatted_heat = formatted_heat.strip("b'")
    temp_count = temp_count + 1
    if formatted_heat.isdigit():
        temp_y_vals.append(float(formatted_heat))
        temp_x_vals.append(temp_count * 0.1)
    
    plt.ylim(20,40)

    plt.plot(temp_x_vals, temp_y_vals,'b')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Temperature (\u2103)')
    plt.title('Temperature Monitoring')
    plt.show()


    displayed_temp.set(formatted_heat + '\u2103')
    ttk.Label(root, textvariable=displayed_temp).grid(row=0, column=4)

    
    root.after(100, rolling_temperature)

def rolling_ph():
    global ph_count
    ph_output = str(ph_launchpad.readline())

    formatted_ph = ph_output
    formatted_ph = formatted_ph.rstrip("\\r\\n'")
    formatted_ph = formatted_ph.strip("b'")
    ph_count = ph_count + 1
    if is_number(formatted_ph) == True:
        ph_y_vals.append(float(formatted_ph))
        ph_x_vals.append(ph_count * 0.1)
    
    if len(ph_x_vals) > 50:
        ph_x_vals.pop(0)
        ph_y_vals.pop(0)
    plt.ylim(1,14)

    plt.plot(ph_x_vals,ph_y_vals,'b')
    plt.xlabel('Time (seconds)')
    plt.ylabel('pH')
    plt.title('pH Monitoring')
    plt.show()

    displayed_ph.set(formatted_ph)
    ttk.Label(root, textvariable=displayed_ph).grid(row=1, column=4)

    root.after(100, rolling_ph)

def rolling_stir():
    global stir_count
    stir_output = str(stir_launchpad.readline())

    formatted_stir = stir_output
    formatted_stir = formatted_stir.rstrip("\\r\\n'")
    formatted_stir = formatted_stir.strip("b'")
    stir_count = stir_count + 1
    if formatted_stir.isdigit():
        stir_y_vals.append(float(formatted_stir))
        stir_x_vals.append(stir_count * 0.1)
        
    if len(stir_x_vals) > 50:
        stir_x_vals.pop(0)
        stir_y_vals.pop(0)
    plt.ylim(400,1600)

    plt.plot(stir_x_vals,stir_y_vals,'b')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Motor speed (RPM)')
    plt.title('Stirring Monitoring')
    plt.show()


    displayed_stir.set(formatted_stir + "RPM")
    ttk.Label(root, textvariable=displayed_stir).grid(row=2, column=4)


    root.after(100, rolling_stir)

def update_temppoint():
    temp_set = var_values[0].get()
    displayed_temp_setpoint.set("Current temperature setpoint: " + temp_set + "\u2103")
    heat_launchpad.write(chr(int(temp_set)).encode())
    ttk.Label(root, textvariable = displayed_temp_setpoint).grid(row = 3, column = 0) 
    var_values[0].delete(0, 100)
    rolling_temperature()

def update_phpoint():
    ph_set = var_values[1].get()
    displayed_ph_setpoint.set("Current pH setpoint: " + ph_set)
    ph_launchpad.write(chr(int(ph_set)).encode())
    ttk.Label(root, textvariable = displayed_ph_setpoint).grid(row = 4, column = 0) 
    var_values[1].delete(0, 100)
    rolling_ph()


def update_stirpoint():
    stir_set = var_values[2].get()
    displayed_stir.set("Current stirring setpoint: " + stir_set + " RPM")
    stir_launchpad.write(chr(int(stir_set) // 20).encode()) # Have to divide to send over serial, multiplied by 20 for Launchpad
    ttk.Label(root, textvariable = displayed_stir_setpoint).grid(row = 5, column = 0) 
    var_values[2].delete(0, 100)
    rolling_stir()
    

controllables = ['Temperature', 'pH', 'Stirring']
var_values = ['new_temp', 'new_ph', 'new_stir']
command_names = [update_temppoint, update_phpoint, update_stirpoint]
units = ['(\u2103)', '', '(RPM)']




"""def temp_verification(entered):
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
        return False"""


for i in range (0, 3):
    var_values[i] = ttk.Entry(root, width = 20)
    var_values[i].grid(row=i, column=1)
    enter = ttk.Button(root, command= command_names[i] , text="Enter")
    enter.grid(row=i, column=2)
    ttk.Label(root, text="Update " + controllables[i] + " Setpoint " + units[i]).grid(row=i, column=0)
    ttk.Label(root, text="Current " + controllables[i] + ": ").grid(row=i, column=3)





root.mainloop()
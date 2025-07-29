import tkinter as tk
from tkinter import ttk, messagebox

unit_data = {
    "Length": {
        "Millimeters": 0.001,
        "Centimeters": 0.01,
        "Meters": 1.0,
        "Kilometers": 1000.0,
        "Inches": 0.0254,
        "Feet": 0.3048,
        "Yards": 0.9144,
        "Miles": 1609.34
    },
    "Time": {
        "Seconds": 1.0,
        "Minutes": 60.0,
        "Hours": 3600.0,
        "Days": 86400.0,
        "Weeks": 604800.0
    },
    "Temperature": {
        "Celsius": "C",
        "Fahrenheit": "F",
        "Kelvin": "K"
    }
}

def update_units(*_):
    category = combo_type.get()
    units = list(unit_data[category].keys())
    combo_from["values"], combo_to["values"] = units, units
    combo_from.set(units[0])
    combo_to.set(units[1])

def swap_units():
    from_unit = combo_from.get()
    to_unit = combo_to.get()
    combo_from.set(to_unit)
    combo_to.set(from_unit)

def convert():
    try:
        value = float(entry_value.get())
        precision = int(spin_precision.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return

    category = combo_type.get()
    from_u = combo_from.get()
    to_u = combo_to.get()

    if category == "Temperature":
        c = f = k = value
        if from_u == "Celsius":
            f, k = (value * 9/5) + 32, value + 273.15
        elif from_u == "Fahrenheit":
            c = (value - 32) * 5/9
            k = c + 273.15
        elif from_u == "Kelvin":
            c = value - 273.15
            f = (c * 9/5) + 32
        result = {"Celsius": c, "Fahrenheit": f, "Kelvin": k}[to_u]
    else:
        base = value * unit_data[category][from_u]
        result = base / unit_data[category][to_u]

    entry_result.config(state="normal")
    entry_result.delete(0, tk.END)
    entry_result.insert(0, f"{result:.{precision}f}")
    entry_result.config(state="readonly")

root = tk.Tk()
root.title("Styled Unit Converter")
root.geometry("460x400")
root.configure(bg="#f2f2f2")
root.resizable(False, False)

font_title = ("Arial", 11)
font_body = ("Arial", 10)

frame_input = tk.LabelFrame(root, text="Input", bg="#f2f2f2", font=font_body)
frame_input.pack(fill="x", padx=15, pady=10)

tk.Label(frame_input, text="Enter Value:", font=font_title, bg="#f2f2f2").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_value = tk.Entry(frame_input, font=font_title, width=18)
entry_value.grid(row=0, column=1, pady=5)

tk.Label(frame_input, text="Decimal Places:", font=font_title, bg="#f2f2f2").grid(row=1, column=0, padx=10, sticky="w")
spin_precision = tk.Spinbox(frame_input, from_=0, to=10, width=5)
spin_precision.grid(row=1, column=1, sticky="w", pady=5)
spin_precision.delete(0, tk.END)
spin_precision.insert(0, "4")

frame_units = tk.LabelFrame(root, text="Units", bg="#f2f2f2", font=font_body)
frame_units.pack(fill="x", padx=15, pady=5)

tk.Label(frame_units, text="Category:", font=font_title, bg="#f2f2f2").grid(row=0, column=0, padx=10, pady=5, sticky="w")
combo_type = ttk.Combobox(frame_units, values=list(unit_data.keys()), state="readonly", width=16)
combo_type.grid(row=0, column=1, padx=10)
combo_type.set("Length")
combo_type.bind("<<ComboboxSelected>>", update_units)

tk.Label(frame_units, text="From:", font=font_title, bg="#f2f2f2").grid(row=1, column=0, padx=10, pady=5, sticky="w")
combo_from = ttk.Combobox(frame_units, state="readonly", width=16)
combo_from.grid(row=1, column=1, padx=10)

tk.Label(frame_units, text="To:", font=font_title, bg="#f2f2f2").grid(row=2, column=0, padx=10, pady=5, sticky="w")
combo_to = ttk.Combobox(frame_units, state="readonly", width=16)
combo_to.grid(row=2, column=1, padx=10)

ttk.Button(frame_units, text="Swap Units", command=swap_units).grid(row=3, column=0, columnspan=2, pady=8)

ttk.Button(root, text="Convert", command=convert).pack(pady=10)

entry_result = tk.Entry(root, font=font_title, width=28, state="readonly", justify="center")
entry_result.pack(pady=5)

update_units()
root.mainloop()

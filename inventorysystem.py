import tkinter as tk
from tkinter import messagebox
import pyodbc
from PIL import Image, ImageTk

# =========================
# CONEXIÓN SQL SERVER
# =========================

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-HDVCOI5\\SQLEXPRESS;"
    "DATABASE=InventoryDB;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# =========================
# VENTANA
# =========================

window = tk.Tk()
window.title("Sistema de Inventario")
window.geometry("1100x650")

# =========================
# FONDO DINÁMICO
# =========================

original_image = Image.open("inventario.jpg")

bg_label = tk.Label(window)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def resize_bg(event):
    w, h = event.width, event.height
    img = original_image.resize((w, h))
    photo = ImageTk.PhotoImage(img)

    bg_label.config(image=photo)
    bg_label.image = photo

window.bind("<Configure>", resize_bg)

# =========================
# FUNCIONES CRUD
# =========================

def update_list():
    listbox.delete(0, tk.END)

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    for r in rows:
        listbox.insert(tk.END, f"{r[1]} | Stock: {r[2]} | Precio: {r[3]}")

def add_product():
    name = entry_name.get()
    quantity = entry_quantity.get()
    price = entry_price.get()

    if name == "" or quantity == "" or price == "":
        messagebox.showwarning("Error", "Completa todos los campos")
        return

    cursor.execute(
        "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
        (name, quantity, price)
    )

    conn.commit()
    update_list()
    clear_fields()

def delete_product():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Error", "Selecciona un producto")
        return

    text = listbox.get(selected)
    name = text.split(" | ")[0]

    cursor.execute("DELETE FROM products WHERE name=?", (name,))
    conn.commit()

    update_list()

def update_product():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Error", "Selecciona un producto")
        return

    text = listbox.get(selected)
    name = text.split(" | ")[0]

    quantity = entry_quantity.get()
    price = entry_price.get()

    cursor.execute("""
        UPDATE products
        SET quantity=?, price=?
        WHERE name=?
    """, (quantity, price, name))

    conn.commit()
    update_list()
    clear_fields()

def select_item(event):
    selected = listbox.curselection()

    if not selected:
        return

    text = listbox.get(selected)
    parts = text.split(" | ")

    name = parts[0]
    quantity = parts[1].replace("Stock: ", "")
    price = parts[2]

    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)

    entry_name.insert(0, name)
    entry_quantity.insert(0, quantity)
    entry_price.insert(0, price)

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)

# =========================
# INTERFAZ
# =========================

frame = tk.Frame(window, bg="white")
frame.place(x=50, y=50)

tk.Label(frame, text="Producto").grid(row=0, column=0)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Cantidad").grid(row=1, column=0)
entry_quantity = tk.Entry(frame)
entry_quantity.grid(row=1, column=1)

tk.Label(frame, text="Precio").grid(row=2, column=0)
entry_price = tk.Entry(frame)
entry_price.grid(row=2, column=1)

tk.Button(frame, text="Agregar", command=add_product, bg="green", fg="white").grid(row=3, column=0)
tk.Button(frame, text="Actualizar", command=update_product, bg="blue", fg="white").grid(row=3, column=1)
tk.Button(frame, text="Eliminar", command=delete_product, bg="red", fg="white").grid(row=3, column=2)

listbox = tk.Listbox(window, width=70, height=20)
listbox.place(x=50, y=220)

listbox.bind("<<ListboxSelect>>", select_item)

# =========================
# INICIO
# =========================

update_list()

window.update()
class FakeEvent:
    pass

def init_bg():
    event = FakeEvent()
    event.width = window.winfo_width()
    event.height = window.winfo_height()
    resize_bg(event)

window.after(100, init_bg)

window.mainloop()
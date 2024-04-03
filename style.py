from tkinter import ttk


def run():
    style = ttk.Style()
    style.theme_use("clam")
    style.theme_use("default")

    style.configure("Treeview",
                    background="#2a2d2e",
                    foreground="white",
                    rowheight=30,
                    fieldbackground="#343638",
                    bordercolor="#ff0000",
                    borderwidth=8,
                    font=("Arial", 10),
                    relief="ridge",
                    )
    style.map('Treeview', background=[('selected', '#22559b')])

    style.configure("Treeview.Heading",
                    background="#565b5e",
                    foreground="white",
                    relief="ridge",
                    bordercolor="#ff0000",
                    font=("Arial", 12, "bold"),
                    )
    style.map("Treeview.Heading",
              background=[('active', '#3484F0')])

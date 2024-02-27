from customtkinter import *

class loginPage(CTk):
    def __init__(self):
        super().__init__()
        self.title("LoginPage")
        

    def start(self):
        self.mainloop()

if __name__ == '__main__':
    app = loginPage()
    app.start()
import requests
from PIL import Image, ImageTk
from customtkinter import *

import Personalization as per
import app
from forgot_password import forgot_password


class gg(CTk):
    def __init__(self):
        super().__init__()
        self.show_im = ImageTk.PhotoImage(
            Image.open("image\\show.png").resize((20, 20))
        )
        self.hide_im = ImageTk.PhotoImage(
            Image.open("image\\hide.png").resize((20, 20))
        )

        self.im = ImageTk.PhotoImage(
            Image.open("image\\im2.jpg").resize((560, 800))
        )
        self.Lim = CTkLabel(self, image=self.im)
        self.Lim.grid(row=0, column=0, padx=(0, 20))

        self.tabview = CTkTabview(self)
        self.tabview.grid(row=0, column=1, padx=(0, 10))
        # ======================================================login tab=================================================
        self.loginTab = self.tabview.add("login")

        self.user_input = per.Entry_Placeholder(
            self.loginTab,
            placeholder="Username",
            width=170,
        )
        self.user_input.pack(padx=25, pady=30)

        self.passFrame = CTkFrame(self.loginTab)
        self.pass_input = per.Entry_Placeholder_password(
            self.passFrame,
            placeholder="Password",
            show_image="image/show.png",
            hide_image="image/hide.png",
        )
        self.passFrame.pack(padx=25, pady=30)

        self.forget_button = CTkButton(
            self.loginTab, text="Forget your Password?", command=lambda: forgot_password(self)
        )
        self.forget_button.pack()
        self.LoginB = CTkButton(self.loginTab, text="Login", command=self.login)
        self.LoginB.pack(padx=20, pady=25)

        self.login_status = CTkLabel(self.loginTab, text="")
        self.login_status.pack()

        # ============================================================signup tab=================================================
        self.signupTab = self.tabview.add("signup")
        self.signup_user_input = per.Entry_Placeholder(
            self.signupTab,
            placeholder="Username",
            width=170,
        )
        self.signup_user_input.pack(padx=15, pady=20)

        self.signup_email_input = per.Entry_Placeholder(
            self.signupTab,
            placeholder="Email",
            width=170,
        )
        self.signup_email_input.pack(padx=15, pady=20)

        self.signup_passFrame1 = CTkFrame(self.signupTab)
        self.signup_pass_input1 = per.Entry_Placeholder_password(
            self.signup_passFrame1,
            placeholder="Password",
            show_image="image/show.png",
            hide_image="image/hide.png",
        )
        self.signup_passFrame1.pack(padx=15, pady=20)

        self.signup_passFrame2 = CTkFrame(self.signupTab)
        self.signup_pass_input2 = per.Entry_Placeholder_password(
            self.signup_passFrame2,
            placeholder="Repeat password",
            show_image="image/show.png",
            hide_image="image/hide.png",
        )
        self.signup_passFrame2.pack(padx=15, pady=20)

        self.SignupB = CTkButton(self.signupTab, text="Sign up", command=self.signup)
        self.SignupB.pack(padx=10, pady=15)

        self.signup_status = CTkLabel(self.signupTab, text="")
        self.signup_status.pack()

    def start(self):
        self.resizable(0, 0)
        self.mainloop()

    def login(self):
        send_data = {
            "username": self.user_input.get().strip(),
            "password": self.pass_input.get().strip(),
        }
        respone = requests.post(url="http://127.0.0.1:80/login", json=send_data)
        if respone.status_code != 200:
            self.login_status.configure(text=respone.json().get("message"))
        else:
            self.login_status.configure(text=respone.json().get("message"))

            self.withdraw()
            self.t = CTkToplevel(self)
            self.t.protocol("WM_DELETE_WINDOW", self.close_all)
            self.aa = app.graghic(api_key="12089a0890294cc08148c89840b5b95a", root=self.t)

    def close_all(self):
        self.t.destroy()
        self.destroy()

    def signup(self):
        send_data = {
            "username": self.signup_user_input.get().strip(),
            "email": self.signup_email_input.get().strip(),
            "password1": self.signup_pass_input1.get().strip(),
            "password2": self.signup_pass_input2.get().strip(),
        }
        respone = requests.post(url="http://127.0.0.1:80/signup", json=send_data)
        if respone.status_code != 200:
            self.signup_status.configure(text=respone.json().get("message"))
        elif respone.status_code == 200:
            self.signup_status.configure(text=respone.json().get("message"))


if __name__ == "__main__":
    appli = gg()
    appli.start()

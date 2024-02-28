import requests
from customtkinter import *

import Personalization as per


class forgot_password(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.email_entry = per.Entry_Placeholder(self, placeholder="Email", width=170)
        self.email_entry.pack(padx=10, pady=15)

        self.email_button = CTkButton(self, text="get verification code", width=170, command=self.get_verification_code)
        self.email_button.pack(padx=10, pady=15)

        self.verification_entry = per.Entry_Placeholder(self, placeholder="Verification code", width=170)
        self.verification_entry.pack(padx=10, pady=15)

        self.f1 = CTkFrame(self)
        self.password1_entry = per.Entry_Placeholder_password(
            self.f1,
            placeholder="Password",
            show_image="image/show.png",
            hide_image="image/hide.png",
            width=170,
        )
        self.f1.pack(padx=10, pady=15)

        self.f2 = CTkFrame(self)
        self.password2_entry = per.Entry_Placeholder_password(
            self.f2,
            placeholder="Repet password",
            show_image="image/show.png",
            hide_image="image/hide.png",
            width=170,
        )
        self.f2.pack(padx=10, pady=15)

        self.change_button = CTkButton(self, text="change password", command=self.change_password)
        self.change_button.pack()
        self.status = CTkLabel(self, text="")
        self.status.pack(padx=10, pady=5)

    def get_verification_code(self):
        respone = requests.get(url="http://127.0.0.1:5000/get_verify_code",
                               params={"email": f"{self.email_entry.get().strip()}"})
        if respone.status_code != 200:
            self.status.configure(text=respone.json().get("message"))
        else:
            self.status.configure(text=respone.json().get("message"))

    def change_password(self):
        send_data = {
            "email": self.email_entry.get().strip(),
            "verification_code": self.verification_entry.get().strip(),
            "password1": self.password1_entry.get().strip(),
            "password2": self.password2_entry.get().strip(),
        }
        respone = requests.post(url="http://127.0.0.1:5000/reset_password", json=send_data)
        if respone.status_code != 200:
            self.status.configure(text=respone.json().get("message"))
        else:
            self.status.configure(text=respone.json().get("message"))


if __name__ == '__main__':
    root = CTk()
    root.geometry("400x400+500+500")
    app = forgot_password(root)
    root.mainloop()

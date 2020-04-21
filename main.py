from tkinter import *


def model():
    root.destroy()
    import model_generator


def miner():
    root.destroy()
    import tweet_miner


root = Tk()
root.title("Epidemic analysis")
root.geometry("800x900")

lbl = Label(root, text="Epidemic analysis", font=("Arial Bold", 25), bg="#415a5f", fg="white",
            padx=200,
            pady=20)
lbl.pack()
miner_btn = Button(root, text="Mine tweets", command=miner, padx=15, pady=15,
                   bg="#ce6664", fg="white")
miner_btn.place(y=500, x=150)
model_btn = Button(root, text="Generate model", command=model, padx=15, pady=15,
                   bg="#ce6664", fg="white")
model_btn.place(y=500, x=450)
root.mainloop()

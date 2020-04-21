import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from tkinter import *
from threading import Thread
from tkinter.ttk import Progressbar
import datetime
import json
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

all_tweets = []
tweets = 0
maximum_number_of_tweets = 10000
consumer_key = 'ThYmCUXgFynqRgm9PYrX6nll4'
consumer_secret = 'tKwO888THWydOIVFkne4iGBxdLQqIFW5Yq5DKvmVk0qWgqWFF6'
access_token = '1234794554232123397-UxNNnKIdAhO6sgkryZk2FJidCfbtt5'
access_secret = 'LnaM9QqP3rd4dytwg34SG6xtsjZXYAKteWwzw6gcC9bKP'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


class Statistics:
    def __init__(self):
        # Declare the format that all dates are shown in
        self.date_formats = "%a %b %d %H:%M:%S +%f %Y"
        self.tweet_frequencies = {}

    def graph_data(self, filename):
        # Open tweets json file
        with open(filename) as data_file:
            # Load object in json file
            data = json.load(data_file)
            # Loop through tweets in object
            for i in range(len(data) - 1):
                # Parse each tweet as a separate json object
                parsed_line = json.loads(data[i])
                # If created_at key exists
                if 'created_at' in parsed_line.keys():
                    date = parsed_line['created_at']
                    # Parse the created_at field into a datetime object
                    date_time_obj = datetime.datetime.strptime(date, self.date_formats)
                    # Create key that will be used as data reference
                    time_key = str(date_time_obj.hour) + ":" + str(date_time_obj.minute)
                    # If counter already exists increment counter by 1
                    if time_key in self.tweet_frequencies:
                        self.tweet_frequencies[time_key] += 1
                    # If counter does not exist, start at 1
                    else:
                        self.tweet_frequencies[time_key] = 1

        # Arrange times in order
        pos = np.arange(len(self.tweet_frequencies))
        # Give histogram aspect to the bar diagram
        width = 1.0

        fig = Figure(figsize=(5, 4), dpi=100)
        fig_graph = fig.add_subplot(1, 1, 1)
        fig_graph.bar(self.tweet_frequencies.keys(), self.tweet_frequencies.values(), width, color='b')
        # Set x axis
        fig_graph.set_xticks(pos + (width / 2))
        # Set x axis labels as times that were recorded
        fig_graph.set_xticklabels(self.tweet_frequencies.keys())

        fig_graph.set_ylabel('Tweets')
        fig_graph.set_xlabel('Time (minutes)')
        fig_graph.set_title("#" + str(hashtag_entry.get()) + " tweet frequency")
        # Create bar chart

        bar = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        bar.draw()
        bar.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


hashtag = ""


def monitor():
    progress_lbl.place(x=125, y=200)
    progress.place(x=100, y=250)
    twitter_stream = Stream(auth, MyListener(int(max_entry.get())))
    twitter_stream.filter(track=["#" + str(hashtag_entry.get())])
    graph_btn.place(y=500, x=350)


def graph():
    try:
        with open('tweets.json', 'r') as fp:
            old_data = json.load(fp)
            all_tweets.append(old_data)
    except IOError:
        err_lbl = Label(window, text="\n Data doesn't already exist, so creating new tweets.json file! \n")
        err_lbl.place(y=450, x=300)
    with open('tweets.json', 'w') as fp:
        fp.write(json.dumps(all_tweets))
        new_graph = Statistics()
        new_graph.graph_data("tweets.json")


class MyListener(StreamListener):
    def __init__(self, maximum):
        super().__init__()
        self.tweets = 0
        self.max = maximum
        canvas.pack_forget()
        generate_btn.destroy()

    def on_data(self, data):
        if self.tweets < self.max:
            try:
                all_tweets.append(data)
                progress['value'] = self.tweets / self.max * 100
                progress_lbl.config(text="Progress: " + str(round(self.tweets / self.max * 100)) + "%")
                window.update_idletasks()
                self.tweets += 1
                return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
            return True
        else:
            return False

    def on_error(self, status):
        print(status)
        return True


window = Tk()
window.title("Tweet miner")
window.geometry("800x900")

lbl = Label(window, text="Tweet miner", font=("Arial Bold", 25), bg="#415a5f", fg="white",
            padx=200,
            pady=20)
lbl.pack()

canvas = Canvas(width=675, height=300, bg='#369693')
canvas.pack()

lbl_one = Label(canvas, text="Hash tag to monitor", bg="#369693", fg="white")
lbl_one.place(y=75, x=100)

hashtag_entry = Entry(canvas, bg="white", fg="#369693")
hashtag_entry.place(y=75, x=350)
hashtag_entry.insert(0, 'CoronaVirus')

lbl_two = Label(canvas, text="Maximum number of tweets", bg="#369693", fg="white")
lbl_two.place(y=175, x=100)

max_entry = Entry(canvas, bg="white", fg="#369693")
max_entry.place(y=175, x=350)
max_entry.insert(0, '1500')

generate_btn = Button(window, text="Start monitoring", command=lambda: Thread(target=monitor).start(), padx=15, pady=15,
                      bg="#ce6664", fg="white")
generate_btn.place(y=500, x=350)
progress = Progressbar(window, orient=HORIZONTAL,
                       length=600, mode='determinate')
progress_lbl = Label(window, text="Progress: 0%")
graph_btn = Button(window, text="Graph result", command=graph, padx=15, pady=15, bg="#ce6664", fg="white")

window.mainloop()

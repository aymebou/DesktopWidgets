"""
This File creates a widget on your desktop (on the bottom) with curves for Ethereum and Bitcoin last buy for the last 5 minutes or so.
The variables in the beginning define the number of values stored and the time frame

To avoid using to much internet in the beginning, it initializes with a flat curves and starts recovering data.

"""
total_time = 300
#number of points to store (ajust if you wish to use less RAM) and length of the X axis
time_interval = 1 #in seconds


import json
import requests
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from matplotlib import style
# URL: https://api.kraken.com/0/public/Ticker

def krak(ticker):
    uri = "https://api.kraken.com/0/public/Ticker"
    blah = uri + "?pair=" + ticker
    r = requests.get(blah)
    json_data = r.text
    fj = json.loads(json_data)
    fuu = fj["result"][ticker]["c"]

    for price in fuu:
        btc = fuu[0]
        size = fuu[1]
    return btc


x = [i*time_interval for i in range(total_time)]
initial = krak("XXBTZEUR")
XBT = [initial for i in range(total_time)]
initial = krak("XETHZEUR")
ETH = [initial for i in range(total_time)]


def get_back_values(L,cur):
    try :
        L.append(krak(cur))
        L.pop(0)
    except :
        print("Error in data  maybe internet is down ?")


def update_graph(dt):
    get_back_values(XBT,"XXBTZEUR")
    get_back_values(ETH,"XETHZEUR")
    ax1.clear()
    ax2.clear()
    ax2.set_xlabel('Time (seconds)')
    ax2.yaxis.label.set_color('black')
    ax1.set_ylabel('XBT prices', color='g')
    ax2.set_ylabel('ETH prices', color='r')
    ax1.plot(x, XBT, 'g')
    ax2.plot(x, ETH, 'r')

app = tk.Tk()
app.wm_title("Cryptocurrencies")
app.wm_attributes('-type',"desktop")
app.geometry("+250+780")
app.wm_attributes("-alpha", 0.35)

style.use("dark_background")
fig = Figure(figsize=(8, 3), dpi=112)
fig.patch.set_facecolor('None')
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax2.set_xlabel('Time (seconds)')
ax1.set_ylabel('XBT prices', color='g')
ax2.set_ylabel('ETH prices', color='r')
fig.tight_layout()

graph = FigureCanvasTkAgg(fig, master=app)
canvas = graph.get_tk_widget()
canvas.grid(row=0, column=0)

ani = animation.FuncAnimation(fig, update_graph, interval=int(time_interval*1000))
app.mainloop()

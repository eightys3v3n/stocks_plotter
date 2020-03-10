import random
from collections import defaultdict
from pathlib import Path
from queue import Queue
import plotly.graph_objects as go


def plot_wise(data):
    """Takes in {act: {date: balance}} and converts it to (act, [dates], [balances], color)."""
    lines = []
    colors = ('aqua','blue','brown','cyan','darkblue','darkgreen','darkorange','darkred','gold','green','grey','hotpink','lime','orange','pink','purple','red','silver','tan','yellow')
    used = [None, ] # used colors

    # Check the validity of the input data.
    dates = set()

    for act, act_dates in data.items():
        for date, bal in act_dates.items():
            dates.add(date)
    
    for act, act_dates in data.items():
        if set(act_dates) != dates:
            with open("error.log", "w") as f:
                f.write("{}\n".format(dates))
                f.write("{}: {}\n".format(act, act_dates))
            raise Exception("Account: '{}' doesn't have the same dates as other given accounts.".format(act))

    for act, act_dates in data.items():
        # pick a random color for this account
        c = None
        if act != "total":
            while c in used: c = random.choice(colors)
        else:
            c = "black"
        used.append(c)

        # append the data as a line
        lines.append([act, list(act_dates.keys()), list(act_dates.values()), c])

    return lines


def plot(data):
    figure = go.Figure()

    lines = plot_wise(data)

    for act, dates, bals, color in lines:
        figure.add_trace(go.Scatter(x=dates, y=bals,
                                    mode='lines',
                                    name=act,
                                    line=dict(color=color, width=2)))

    figure.update_layout(title="Net Worth Over Time",
                         xaxis_title="Date",
                         yaxis_title="CAD $")
    figure.show()
    return figure


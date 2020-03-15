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

    figure.update_layout(title="Various information over time",
                         xaxis_title="Date",
                         yaxis_title="Various scales")
    figure.show()
    return figure


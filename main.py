import csv, random
from collections import defaultdict
from pathlib import Path
from queue import Queue
from datetime import datetime
from bokeh.plotting import output_file, figure, show
from bokeh.models import DatetimeTickFormatter


class Transaction:
    def __init__(self, row=None):
        if row is not None:
            self.from_row(row)
        else:
            self.act = None
            self.date = None
            self.desc = None
            self.amt = None
            self.bal_af = None

    def from_row(self, row):
        self.act = row[0]
        self.date = datetime.strptime(row[1], "%d-%b-%Y").date()
        self.desc = row[2]

        if row[4] != '':
            self.amt = float(row[4])
        else:
            self.amt = None

        if row[6] != '':
            self.bal_af = float(row[6])
        else:
            self.bal_af = None
        return self

    def __repr__(self):
        return {'act' : self.act,
                'date': self.date, 
                'desc': self.desc,
                'amt' : self.amt,
                'bal_af': self.bal_af,
                }.__str__()

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash("{}:{}:{}:{}:{}".format(self.act, self.date, self.desc, self.amt, self.bal_af))

    def __eq__(self, o):
        if self.__hash__() == o.__hash__(): return True
        return False


def list_files(root, recursive=True):
    files = []
    to_search = Queue()
    to_search.put(root)

    while not to_search.empty():
        path = to_search.get()
        for p in path.iterdir():
            if p.is_file() and not p.is_symlink():
                files.append(p)
            elif recursive and p.is_dir():
                to_search.put(p)
    return files
    

def parse_csv_row(row):
    row = [c.strip() for c in row]
    return tuple(row)


def read_csv(path):
    reader = csv.reader(open(path, 'r'))
    data = []
    for row in reader:
        row = parse_csv_row(row)
        data.append(row)
    return data


def read_trans(path):
    csv = read_csv(path)
    trans = []
    for r in csv:
        trans.append(Transaction(r))
    return trans


def read_statements(path):
    files = list_files(path)
    print("Reading {} files".format(len(files)))

    trans = []
    for f in files:
        trans.extend(read_trans(f))
    print("Read {} rows".format(len(trans)))


    trans = list(set(trans))
    print("Only {} unique rows".format(len(trans)))

    return trans


def seperate_act(trans):
    acts = {}
    for t in trans:
        if t.act in acts:
            acts[t.act].append(t)
        else:
            acts[t.act] = [t,]
    return acts


def process_statements(path):
    trans = read_statements(path)
    trans = seperate_act(trans)
    return trans


def daily_last_bal(trans):
    dates = set()
    bals = []
    for t in trans:
        dates.add(t.date)
    dates = list(dates)
    dates.sort()

    for d in dates:
        d_trans = list(filter(lambda x:x.date == d, trans))
        bals.append(d_trans[-1].bal_af)
    return dates, bals


def create_total_act(data):
    totals = defaultdict(lambda:0)

    for act, trans in data.items():
        dates, bals = daily_last_bal(trans)
        for d, b in zip(dates, bals):
            totals[d] += b
    
    totals = list(zip(totals.keys(), totals.values()))
    totals.sort()
    dates = [d for d, _ in totals]
    bals = [b for _, b in totals]

    return dates, bals


def plot_data(data, acts):
    lines = []
    colors = ('aqua','blue','brown','cyan','darkblue','darkgreen','darkorange','darkred','gold','green','grey','hotpink','ivory','lime','orange','pink','purple','red','silver','tan','yellow')
    used = [None, ] # used colors

    for act, trans in data.items():
        if acts is not None and act.split('-')[-1] not in acts:
            continue

        # get dates and their balances
        dates, bals = daily_last_bal(trans)
        
        # get color
        c = None
        while c in used: c = random.choice(colors)
        used.append(c)
        
        # append line data
        lines.append([act, dates, bals, c])

    # add a total line
    if acts is None or 'total' in acts:
        dates, bals = create_total_act(data)
        lines.append(['total', dates, bals, 'black'])

    return lines


def fill_balances(plot_data):
    # [ [act, [dates], [bals]] ]
    dates = set()
    for act, dates, bals in plot_data:
        for d in dates:
            dates.add(d)




def plot(data, acts):
    output_file("plot.html", mode="inline")
    p = figure(title="Balance vs Date/time",
               x_axis_label="Date/time",
               y_axis_label="$ Balance",
               x_axis_type="datetime",
               sizing_mode="stretch_both")

    lines = plot_data(data, acts)
    lines = fill_balances(lines)
    if acts is not None:
        print(list(a for a, _, _, _ in lines))
        assert len(lines) == len(acts)

    for act, dates, trans, color in lines:
        p.line(dates, trans, line_color=color, legend_label=act, line_width=4)

    return p


def main():
    global data
    data = process_statements(Path("statements"))
    show(plot(data, None))


if __name__ == '__main__':
    main()

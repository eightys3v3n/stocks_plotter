from collections import defaultdict
from transaction import Transaction


def act_wise(trans):
    """
    Seperates a list of transactions into a dictionary of acounts and their transactions.

    why: This allows us to easily fill in missing transactions without mixing up which account they are for.
         It also allows us to easily plot only a single account balance.

    input: [Transaction]
    output: {Transaction.act: [Transaction]}
    """
    #Ensure the input array is the expected structure.
    assert isinstance(trans, list)
    assert all(isinstance(t, Transaction) for t in trans)
    
    acts = {}

    for t in trans:
        if t.act in acts:
            acts[t.act].append(t)
        else:
            acts[t.act] = [t,]

    return acts


def date_wise(acts):
    """
    Seperates transactions already sorted by act, also by date.

    why: This allows us to easily figure out which balance is the previous one. This is required
         so we can graph the balance over time without it jumping down to zero if there isn't a
         transaction that day.

    input: {Transaction.act: [Transaction]}
    output: {Transaction.act: {datetime.date: [Transaction]}}
    """
    new_acts = {}

    for act, trans in acts.items():
        new_acts[act] = defaultdict(lambda:[])

        for t in trans:
            new_acts[act][t.date].append(t)

    # turn everything into a regular dict instead of a defaultdict.
    new_acts = {k: dict(v) for k, v in new_acts.items()}

    return new_acts




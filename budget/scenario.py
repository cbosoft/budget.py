class Scenario:

    def __init__(self, items=None):
        if not items:
            items = list()
        self.items = items

def _next_level_combo(last, scenarios):
    rv = list()
    for s in scenarios:
        for l in last:
            if s in l or s == l:
                continue

            if isinstance(l, list):
                n = list(sorted([*l,s]))
            else:
                n = list(sorted([l, s]))

            if n not in rv:
                rv.append(n)
    return rv


def all_possible_combinations_of(scenarios):
    combinations = [list(scenarios)]
    for i in range(len(scenarios)-1):
        combinations.append(_next_level_combo(combinations[-1], scenarios))
    rv = list()
    for comb in combinations:
        rv.extend(comb)
    return rv

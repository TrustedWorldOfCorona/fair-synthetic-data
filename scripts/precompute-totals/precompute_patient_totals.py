import sys

def precompute(csv, threshold=0.95):
    """Precompute the totals for each binary state."""

    with open(csv) as file:
        # skip header line
        next(file)

        totals = {
            "000": 0,
            "001": 0,
            "010": 0,
            "011": 0,
            "100": 0,
            "101": 0,
            "110": 0,
            "111": 0
        }

        for line in file:
            (n, s, m, p) = line.rstrip().split(",")

            state = s + m + ("0" if float(p) < threshold else "1")

            totals[state] += 1

        return totals


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing csv data argument")

    totals = precompute(sys.argv[1])

    for state in totals.items():
        print(state)

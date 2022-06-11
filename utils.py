import qxelarator
from openql.openql import Program
from functools import reduce
from collections import defaultdict
import matplotlib.pyplot as plt


def simulate(*, program: Program, measured: list = None, shots: int) -> dict:
    qx = qxelarator.QX()
    qx.set(f"output/{program.name}.qasm")

    qubits = range(program.qubit_count) if measured is None else measured

    counts = defaultdict(int)
    for _ in range(shots):
        qx.execute()
        result = [int(qx.get_measurement_outcome(qubit)) for qubit in qubits]
        result = reduce(lambda x, y: x + str(y), result, "")
        counts[result] += 1

    return dict(counts)


def plot_histogram(counts: dict, **kwargs):
    total = sum(counts.values())

    plt.bar(
        list(counts.keys()),
        list(map(lambda x: x / total, counts.values())),
        **kwargs,
    )

    plt.title("Counts")
    plt.ylabel("Probability")

    plt.grid(axis="y")
    plt.show()

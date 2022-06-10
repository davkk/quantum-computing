from openql import openql as ql
import qxelarator
from functools import reduce
import os
import matplotlib.pyplot as plt


nqubits = 3


def dice_compile():
    c = ql.Compiler("custom_compiler", "./compiler-config.json")

    platform = ql.Platform("myPlatform", "none")

    p = ql.Program("dice", platform, nqubits)
    k = ql.Kernel("aKernel", platform, nqubits)

    for q in range(nqubits):
        k.gate("h", [q])

    for q in range(nqubits):
        k.gate("measure", [q])

    p.add_kernel(k)
    c.compile(p)


dice_compile()


def plot_histogram(dice_faces):
    plt.hist(dice_faces, bins=8, color="#0504aa", alpha=0.7, rwidth=0.85)
    plt.grid(axis="y", alpha=0.75)
    plt.xlabel("Dice Face", fontsize=15)
    plt.ylabel("Frequency", fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylabel("Frequency", fontsize=15)
    plt.title("Histogram", fontsize=15)
    plt.savefig("hist.png")


def dice_execute_multishot():
    print("executing 8-face dice program on qxelarator")
    qx = qxelarator.QX()
    qx.set("./dice.qasm")
    dice_faces = []
    ntests = 100
    for _ in range(ntests):
        qx.execute()
        res = [int(qx.get_measurement_outcome(q)) for q in range(nqubits)]
        dice_face = reduce(lambda x, y: 2 * x + y, res, 0) + 1
        dice_faces.append(dice_face)

    plot_histogram(dice_faces)


dice_execute_multishot()

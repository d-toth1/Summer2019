import matplotlib.pyplot as plt

def twin_plot(x1, y1, x2, y2):

    fig, ax1 = plt.subplots()
    label1 = input("Label 1: ")
    label2 = input("Label 2: ")
    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel(str(label1), color=color)
    ax1.plot(x1, y1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel(str(label2), color=color)
    ax2.plot(x2, y2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.show()

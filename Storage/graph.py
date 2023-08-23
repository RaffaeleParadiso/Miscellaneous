import matplotlib.pyplot as plt
import numpy as np

def plot_graph(x, y, title, x_label, y_label):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(0, 150000)
    plt.show()  

data = np.loadtxt("Data_disk_usage.txt")
print(data.shape)
plot_graph(range(0, len(data)), data, "Disk usage over time", "minutes", "Mb_used")
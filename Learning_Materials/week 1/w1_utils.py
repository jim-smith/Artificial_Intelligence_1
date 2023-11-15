import math

import matplotlib.pyplot as plt
import numpy as np
import sklearn.datasets as datasets

# values ( mean_red, mean_green, mean_blue,width, height, weight)
typical_banana = (100, 88.2, 20.8, 130, 28, 125)
typical_apple = (55.3, 71.4, 0, 80, 80, 340)
typical_orange = (100, 64.7, 0, 76, 76, 357)

labels = []
colours = []


# make ten examples of each type with a bit of random noise added
def make_fake_fruit():
    np.set_printoptions(precision=2)
    feature_values, label_ids = datasets.make_blobs(
        n_samples=[10, 10, 10],
        centers=[typical_banana, typical_apple, typical_orange],
        cluster_std=5.0,
        n_features=6,
    )

    for row in label_ids:
        if row == 0:
            labels.append("banana")
            colours.append("yellow")
        elif row == 1:
            labels.append("apple")
            colours.append("green")
        else:
            labels.append("orange")
            colours.append("orange")

    np.savetxt("data/fruit_values.csv", feature_values, delimiter=",")
    np.savetxt("data/fruit_label_ids.csv", label_ids, delimiter=",")
    np.savetxt("data/fruit_labels.csv", labels, delimiter=",", fmt="%s")
    return feature_values, labels


def make3dscatters(feature_values, labels):
    # print(feature_values.shape, len(labels))

    fig = plt.figure(tight_layout=True, figsize=(10, 5))
    ax1 = fig.add_subplot(121, projection="3d")
    ax2 = fig.add_subplot(122, projection="3d")

    ax1.scatter(
        feature_values[:, :1],
        feature_values[:, 1:2],
        feature_values[:, 2:3],
        c=colours,
        marker="o",
        s=100,
        label=labels,
    )
    ax1.set_xlabel("Red")
    ax1.set_ylabel("Green")
    ax1.set_zlabel("Blue", rotation=270, labelpad=0)
    # ax1.w_xaxis.set_pane_color(panecolor)
    # ax1.w_yaxis.set_pane_color(panecolor)
    # ax1.w_zaxis.set_pane_color(panecolor)

    ax2.scatter(
        feature_values[:, 3:4],
        feature_values[:, 4:5],
        feature_values[:, 5:6],
        c=colours,
        marker="o",
        s=100,
        label=labels,
    )
    ax2.set_xlabel("Width")
    ax2.set_ylabel("Height")
    ax2.set_zlabel("Weight", rotation=270, labelpad=0)
    # ax2.w_xaxis.set_pane_color(panecolor)
    # ax2.w_yaxis.set_pane_color(panecolor)
    # ax2.w_zaxis.set_pane_color(panecolor)
    plt.subplots_adjust(left=0.0, right=1.0, top=0.9, bottom=0.1)

    return fig


def get_distances(cities):
    # how many rows are there in the list of city coordinates?
    num_cities = len(cities)
    # initialise 3d table with zeros
    distances = np.zeros((num_cities, num_cities))
    # then fill it up
    for row in range(num_cities):
        for col in range(num_cities):
            if row != col:
                xdist = cities[row][0] - cities[col][0]
                ydist = cities[row][1] - cities[col][1]
                distances[row][col] = math.sqrt(xdist * xdist + ydist * ydist)
    return distances


def plot_cities(cities, model):
    # model is just the table of inter-city distances
    # how many rows are there ?
    num_cities = model.shape[0]

    fig, ax = plt.subplots(figsize=(5, 5))
    for i in range(num_cities):
        ax.plot(cities[i][0], cities[i][1], "Xb")
    modelstrings = np.array(["%.2f" % x for x in model.reshape(model.size)])
    modelstrings = modelstrings.reshape(model.shape)
    ax.table(cellText=modelstrings, loc="right", bbox=[1.1, 0, 1, 1])
    plt.show()


def show_tour(cities, tour, start=0):
    num_cities = len(cities)
    plt.plot(cities[start][0], cities[start][1], "or", markersize=12)
    plt.plot(
        [cities[tour[i % num_cities]][0] for i in range(num_cities + 1)],
        [cities[tour[i % num_cities]][1] for i in range(num_cities + 1)],
        "Xb-",
    )
    plt.show()

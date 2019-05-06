#stdlib includes
import argparse
import matplotlib.pyplot as plt

# external includes
import numpy as np

#internal includes
import svm

def rotation_matrix(deg):
    c, s = np.cos(deg), np.sin(deg)
    return np.array([[c, -s], [s, c]])

def stretch_matrix(a, b):
    return np.array([[a, 0], [0, b]])

def gen_rands(center, num, var):
    rotate = rotation_matrix(np.radians(45))
    rotate += rotation_matrix(np.radians(np.random.uniform(-4, 4)))

    stretch = stretch_matrix(1.5, var)

    cov = rotate @ stretch @ np.linalg.inv(rotate)
    return center + np.random.multivariate_normal(center, cov, num)

colors = ['black', 'grey', 'brown', 'm', 'c', 'g', 'y']

def plot_svm_line(a, b, sep, off, color, weight, ax):

    x_min = np.min([a[:, 0], b[:, 0]])
    x_max = np.max([a[:, 0], b[:, 0]])
    bottom = (-sep[0]*x_min + off) / sep[1]
    top = (-sep[0]*x_max + off) / sep[1]

    ax.plot([x_min, x_max], [bottom, top], color=color, label=str(weight))

def plot_svm(a, b, results, weights):

    fig, ax = plt.subplots()
    ax.scatter(a[:, 0],a[:, 1], color='blue')
    ax.scatter(b[:, 0],b[:, 1], color='red')
    for (sep, off), color, weight in zip(results, colors, weights):
        plot_svm_line(a, b, sep, off, color, weight, ax)

    plt.title("SVM plane separating red and blue clusters")
    plt.show()

def run_example(seed, num, weight, var):

    np.random.seed(seed)

    a_center = [-.4, .4]
    b_center = [.4, -.4]

    a_train = gen_rands(a_center, num, var)
    b_train = gen_rands(b_center, num, var)
    a_test = gen_rands(a_center, num, var)
    b_test = gen_rands(b_center, num, var)

    weights = [weight]

    results = [svm.train_linear_svm(a_train, b_train, weight)
               for weight in weights]

    plot_svm(a_train, b_train, results, [])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate example plots for report',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--seed", help="RNG seed to ensure replicability", type=int,
                         default=0xDEAD111F)
    parser.add_argument("--weight", type=float, help="Bias of svm towards one side",
                        default=0.5)
    parser.add_argument("--num", type=int, help="Number of points in each cluster",
                        default=200)
    parser.add_argument("--var", type=float, help="Variance of each cluster",
                        default=0.4)

    args = parser.parse_args()

    if args.weight < 0 or args.weight > 1:
        parser.error("Weight is {}, must be between zero and one".format(args.weight))

    run_example(args.seed, args.num, args.weight, args.var)

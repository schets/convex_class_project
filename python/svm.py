import numpy as np
import cvxpy as cvx
from cvxpy import *

# As it turns out, a linear svm does extremely well on the provided test and training sets
# as such, I don't implement a solver on the dual to use a kernel trick since that would
# be impractical for use, since it's more complex and greatly reduces interpretability.
#
# Instead, I investigate how to bias the svm so that it will be more likely to err one way
# or another on test data - one might be much more interested in correctly classifying
# not-spam emails that correctly classifying spam, for example.
#
# I introduce an simple extension that's expanded on more in the report. The short story
# is that I bias the support vectors to be smaller in the undesired direction, so that
# real-world values on the edge will be more likely to fall into the other category:
#
#  *  *  * (desired side)
#
#  +
#  - - - - - - - - - (seperating hyperplane)
#  +  +  + (undesired side)
def train_linear_svm(ham, spam, weight):

    signs = np.concatenate([
        np.ones(len(ham)),
        -1 * np.ones(len(spam))
    ])
    weights = np.concatenate([
        weight * np.ones(len(ham)),
        (1 - weight) * np.ones(len(spam))
    ])

    vecs = np.concatenate([ham, spam])

    beta = Variable(len(ham[0]))
    off = Variable()
    slack = Variable(len(ham) + len(spam))

    proj_point = diag(signs) * (vecs * beta + off)
    close_penalty = cvx.sum(diag(weights) * cvx.pos(1 - proj_point))

    prob = Problem(Minimize(norm(beta) + close_penalty),
            [proj_point >= 1 - slack,
             slack >= 0])

    prob.solve(verbose=True)

    return beta.value, off.value

def score_svm(emails, desired, weight, off):
    val = emails @ weight + off
    print(val, desired)
    desired_pos = desired > 0
    score_pos = val > 0

    same = np.equal(desired_pos, score_pos)

    return float(np.sum(same)) / len(same)

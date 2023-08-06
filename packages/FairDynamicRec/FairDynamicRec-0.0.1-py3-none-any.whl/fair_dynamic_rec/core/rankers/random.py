from collections import defaultdict
from math import log
# from online_logistic_regression import OnlineLogisticRegression
from scipy.special import expit
from scipy.optimize import minimize
import numpy as np
from .abstract_ranker import AbstractRanker

# A simple baseline that randomly recommends n_recos playlists to each user.
class RandomPolicy(AbstractRanker):
    def __init__(self, config, dataObj, parameters=None):
        super(RandomPolicy, self).__init__(config, dataObj)

    def get_ranking(self, batch_users):
        n_users = len(batch_users)
        rankings = np.zeros((n_users, self.config.list_size), dtype=np.int64)
        r = np.arange(self.dataObj.n_items)
        for i in range(n_users):
            np.random.shuffle(r)
            rankings[i] = r[:self.config.list_size]
        return rankings

    def update(self, batch_users, rankings, clicks):
        return
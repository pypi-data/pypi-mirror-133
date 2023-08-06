import numpy as np

"""
The base class of all rankers. 
"""
class AbstractRanker():
    def __init__(self, config, dataObj):
        self.config= config
        self.dataObj = dataObj
        self.rankers = config.get_ranker_params()



    @staticmethod
    def get_features_for_optimal_ranker(config, dataObj):
        if config.full_feature:
            return np.concatenate((dataObj.feature_data['test_user_latent_features'], dataObj.feature_data['test_user_topical_features']), axis=1), np.concatenate((dataObj.feature_data['test_item_latent_features'], dataObj.feature_data['test_item_topical_features']), axis=1)
        elif config.optimal_ranker == 'naive_relevance' or config.optimal_ranker == 'sigmoid_relevance':
            return dataObj.feature_data['test_user_latent_features'], dataObj.feature_data['test_item_latent_features']
        elif config.optimal_ranker == 'topical_coverage':
            return dataObj.feature_data['test_user_topical_features'], dataObj.feature_data['test_item_topical_features']

    @staticmethod
    def ranking_coverage(s):
        """
        Return the coverage of an list s for topics. Eq 2 of Nips-11
        :param s: ranked list s in (0, 1), n by d numpy ndarray
        :return:
        """
        s = np.asarray(s) if type(s) is list else s
        return 1 - np.prod(1 - s, axis=0)

    @staticmethod
    def conditional_coverage(x, coverage):
        """
        Return the coverage of an item given the current ranking
        Based on Eq. 2 and Eq. 3 of NIPS11
        :param x: coverage of this item
        :param coverage: topic covergate of previous items
        :return: conditional coverage of x given ranking
        """
        x = np.asarray(x)
        coverage = np.asarray(coverage)
        return 1 - np.multiply(1 - x, 1 - coverage) - coverage





# class AbstractRanker(object):
#
#
#     name = 'abstract'
#
#     def __init__(self, d, sigma=.1, alpha=0.5, seed=42, name=None, n_items=100, mitigation=None):
#         """
#
#         :param d: number of topics
#         :param sigma: learning rate (0, 1)
#         :param alpha: exploration parameter in [0, 1]
#         :param seed: random seed
#         """
#         if name:
#             self.name = name
#         self.d = d
#         self.sigma = sigma
#         self.alpha = alpha
#         self.t = 1
#         self.seed = seed
#         self.prng = np.random.RandomState(seed=seed)
#         # parameters
#         self.ill_matrix_counter = 0
#         self.theta = np.ones(self.d)  # d-dimensional
#         self.b = np.zeros(self.d)  # d
#         self.M = np.eye(self.d)  # d by d
#         self.MInv = np.eye(self.d)  # for fast matrix inverse computation, d by d
#         # for ill inverse
#         self.b_tmp = np.zeros(self.d)
#         self.MInv_tmp = np.zeros((self.d, self.d))
#
#         # for the delta of topic
#         self.delta_t = None
#
#         # MM
#         self.n_recommended = np.zeros(n_items)
#         self.mitigation = mitigation
#
#     @staticmethod
#     def ranking_coverage(s):
#         """
#         Return the coverage of a list s for topics. Eq 2 of Nips-11
#         :param s: ranked list s in (0, 1), n by d numpy ndarray
#         :return:
#         """
#         s = np.asarray(s) if type(s) is list else s
#         return 1 - np.prod(1 - s, axis=0)
#
#     @staticmethod
#     def conditional_coverage(x, coverage):
#         """
#         Return the coverage of an item given the current ranking
#         Based on Eq. 2 and Eq. 3 of NIPS11
#         :param x: coverage of this item
#         :param coverage: topic covergate of previous items
#         :return: conditional coverage of x given ranking
#         """
#         x = np.asarray(x)
#         coverage = np.asarray(coverage)
#         return 1 - np.multiply(1 - x, 1 - coverage) - coverage
#
#     def score(self, delta):
#         """
#         return score for an item
#         """
#         return np.dot(delta, self.theta)
#
#     def ucb(self, delta):
#         """
#         return the upper confident bound of each item. This is for debugging.
#         :param delta:
#         :return:
#         """
#         score = self.score(delta)
#         cb = self.alpha * np.sqrt(np.multiply(np.dot(delta, self.MInv), delta).sum(axis=1))
#         return score + cb
#
#     def get_ranking(self, x, k):
#         """
#         given the features of all items, return the ranking
#         :param x: features
#         :param k: number of positions
#         :return:
#         """
#         raise NotImplementedError
#
#     def __collect_feedback(self, y):
#         """
#         Called by update. Collect feedback. Different types of implements are required for different assumptions.
#         :param y:
#         :return:
#         """
#         raise NotImplementedError
#
#     def __compute_parameters(self, delta, y):
#         """
#         Called by update.
#         :param delta:
#         :param y:
#         :return: None
#         """
#         raise NotImplementedError
#
#     def update(self, y, delta, recommended_items):
#         raise NotImplementedError
#
#     def save(self, filename):
#         with open(filename, 'wb') as f:
#             pk.dump(self, f)
#
#     @staticmethod
#     def load(filename):
#         with open(filename, 'rb') as f:
#             ranker = pk.load(f)
#         return ranker

import numpy as np
import os
from pathlib import Path
import json
from fair_dynamic_rec.core.util.utils import get_legend_labels
from fair_dynamic_rec.core.util.utils import get_param_config_name

class MetricCmd:
    def __init__(self, config, dataObj, rankers):
        self.optimal_reward_filename = 'optimal-reward'
        self.ranker_reward_filename = 'ranker-reward'
        self.rankers = rankers
        config.get_metrics()
        self.load_rewards(config)

    def compute(self, config, dataObj, viz):
        for metric in config.metrics:
            if metric == 'n-step-regret':
                viz.draw(metric, self.n_step_regret(), {'x': 'rounds', 'y': metric, 'legend': get_legend_labels(self.rankers)})
            if metric == 'cumulative-alpha-ia':
                viz.draw(metric, self.cumulative_alpha_ia(config, dataObj), {'x': 'rounds', 'y': metric, 'legend': get_legend_labels(self.rankers)})

    def n_step_regret(self):
        regret = {}
        for key, value in self.rewards.items():
            regret[key] = {'x':range(len(value['optimal'])), 'y': np.cumsum(np.array(value['optimal']) - np.array(value['ranker']))}
        return regret

    def cumulative_alpha_ia(self, config, dataObj):
        ia = self.compute_ia_per_round(config, dataObj)
        cumulative_ia = {}
        for key, value in ia.items():
            tmp = np.zeros(value.shape[0])
            for i in range(value.shape[0]):
                tmp[i] = np.count_nonzero(np.sum(value[:i+1, :], axis=0) >= 1) / dataObj.n_items
            cumulative_ia[key] = {'x': range(len(tmp)), 'y': tmp}
        return cumulative_ia


    def compute_ia_per_round(self, config, dataObj):
        ia = {}
        subdirs, dir_name = self.get_result_subdir(config)
        ranker_index = 0
        for subdir in subdirs:
            ia[dir_name[ranker_index]] = np.zeros((config.rounds, dataObj.n_items))
            for i in range(config.rounds):
                with open(str(subdir / str(i)), 'r') as f:
                    ranking = self.load_ranking_as_matrix(dataObj, json.load(f))
                    ia[dir_name[ranker_index]][i, :] = np.sum(ranking, axis=0)
            ranker_index += 1
        return ia

    def load_rewards(self, config):
        self.rewards = {}
        subdirs, dir_name = self.get_result_subdir(config)
        i = 0
        for subdir in subdirs:
            with open(str(subdir / self.optimal_reward_filename), 'r') as f:
                optimal_reward = json.load(f)
            with open(str(subdir / self.ranker_reward_filename), 'r') as f:
                ranker_reward = json.load(f)
            self.rewards[dir_name[i]] = {'optimal': optimal_reward['reward'], 'ranker': ranker_reward['reward']}
            i += 1

    def get_result_subdir(self, config):
        subdirs, dir_name = [], []
        result_dir = config._target / Path('results')

        for i in range(len(self.rankers)):
            param_name = get_param_config_name(self.rankers[i]["config"])
            subdirs.append(result_dir / param_name)
            dir_name.append(param_name)

        # dirs = os.listdir(result_dir)
        # for dir in dirs:
        #     if os.path.isdir(result_dir / dir):
        #         subdirs.append(result_dir / dir)
        #         dir_name.append(dir)

        return subdirs, dir_name

    def load_ranking_as_matrix(self, dataObj, json_ranking):
        ranking = np.zeros((dataObj.n_users, dataObj.n_items))
        for key, value in json_ranking.items():
            ranking[dataObj.userid_mapped_data[key]][self.convert_itemids_to_internal_ids(dataObj, value['r'])] += 1
        return ranking

    def convert_itemids_to_internal_ids(self, dataObj, items):
        internal_list = []
        for item in items:
            internal_list.append(dataObj.itemid_mapped_data[item])
        return internal_list
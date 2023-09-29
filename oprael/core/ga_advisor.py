# License: MIT

import abc
import random
import numpy as np

from oprael import logger
from oprael.utils.util_funcs import check_random_state, deprecate_kwarg
from oprael.utils.history import Observation, History
from oprael.utils.constants import MAXINT, SUCCESS
from oprael.utils.config_space import get_one_exchange_neighbourhood

class GA_Advisor(object, metaclass=abc.ABCMeta):
    """
    Genetic Algorithm Advisor
    """

    @deprecate_kwarg('num_objs', 'num_objectives', 'a future version')
    def __init__(
            self,
            config_space,
            num_objectives=1,
            num_constraints=0,
            population_size=30,
            subset_size=20,
            epsilon=0.2,
            strategy='worst',  # 'worst', 'oldest'
            optimization_strategy='ga',
            batch_size=1,
            output_dir='logs',
            task_id='OPRAEL',
            random_state=None,
            logger_kwargs: dict = None,
    ):

        self.num_objectives = num_objectives
        self.num_constraints = num_constraints
        assert self.num_objectives == 1 and self.num_constraints == 0
        self.output_dir = output_dir
        self.task_id = task_id
        self.rng = check_random_state(random_state)
        self.config_space = config_space
        self.config_space_seed = self.rng.randint(MAXINT)
        self.config_space.seed(self.config_space_seed)

        _logger_kwargs = {'name': task_id, 'logdir': output_dir}
        _logger_kwargs.update(logger_kwargs or {})
        logger.init(**_logger_kwargs)

        # Init parallel settings
        self.batch_size = batch_size
        self.init_num = batch_size  # for compatibility in pSMBO
        self.running_configs = list()

        # Basic components in Advisor.
        self.optimization_strategy = optimization_strategy

        # Init the basic ingredients
        self.all_configs = set()
        self.age = 0
        self.population = list()
        self.population_size = population_size
        self.subset_size = subset_size
        assert 0 < self.subset_size <= self.population_size
        self.epsilon = epsilon
        self.strategy = strategy
        assert self.strategy in ['worst', 'oldest']

        # init history
        self.history = History(
            task_id=task_id, num_objectives=num_objectives, num_constraints=num_constraints, config_space=config_space,
            ref_point=None, meta_info=None,  # todo: add meta info
        )

    def get_suggestion(self, history=None):
        """
        Generate a configuration (suggestion) for this query.
        Returns
        -------
        A configuration.
        """
        if history is None:
            history = self.history

        if len(self.population) < self.population_size:
            # Initialize population
            next_config = self.sample_random_config(excluded_configs=self.all_configs)
        else:
            pm = 0.05
            population = self.population
            population.sort(key=lambda x: x['perf'])
            if self.rng.random() < self.epsilon:
                subset = random.sample(self.population, self.subset_size)
                subset.sort(key=lambda x: x['perf'])    # minimize
                parent_1 = subset[0]['config']
            else :
                parent_1 = population[0]['config']
            if self.rng.random() < self.epsilon:
                parent_2 = random.sample(self.population, 1)[0]['config']
                while parent_1 == parent_2 :
                    parent_2 = random.sample(self.population, 1)[0]['config']
            else :
                subset = random.sample(self.population, self.subset_size)
                subset.sort(key=lambda x: x['perf'])    # minimize
                parent_2 = subset[0]['config']
                while parent_1 == parent_2 :
                    parent_2 = subset[random.randint(1, 19)]['config']
            '''
            # IOR
            # Divide a set of configurations into three sections：0 - cross_phase_1，cross_point，cross_phase_2 - 5
            cross_point = random.randint(0, 5)
            cross_phase_1 = cross_point-1
            cross_phase_2 = cross_point + 1
            offspring = self.sample_random_config()   # Instantiate an object
            phase1 = random.randint(0, 1)
            phase2 = random.randint(0, 1)
            phase3 = random.randint(0, 1)
            name = ['Romio_CB_Read', 'Romio_CB_Write', 'Romio_DS_Read', 'Romio_DS_Write', 'Strip_Count', 'Strip_Size']
            if phase1 == 0 :
                i = 0
                while i <= cross_phase_1:
                    offspring[name[i]] = parent_1[name[i]]
                    i = i+1
            else :
                i = 0
                while i <= cross_phase_1:
                    offspring[name[i]] = parent_2[name[i]]
                    i = i+1
            if phase2 == 0:
                offspring[name[cross_point]] = parent_1[name[cross_point]]
            else :
                offspring[name[cross_point]] = parent_2[name[cross_point]]
            if phase3 == 0:
                i = cross_phase_2
                while i <= 5:
                    offspring[name[i]] = parent_1[name[i]]
                    i = i+1
            else :
                i = cross_phase_2
                while i <= 5:
                    offspring[name[i]] = parent_2[name[i]]
                    i = i+1
            # mutation
            if random.random() < pm :
                mpoint = random.randint(0, 5)
                if mpoint == 4 :
                    ran = random.randint(1, 32)
                    while offspring[name[mpoint]] == ran :
                        ran = random.randint(1, 32)
                elif mpoint == 5:
                    ran = random.randint(1, 512)
                    while offspring[name[mpoint]] == ran :
                        ran = random.randint(1, 512)
                else:
                    ran = random.randint(0, 2)
                    while offspring[name[mpoint]] == ran :
                        ran = random.randint(0, 2)
                offspring[name[mpoint]] = ran
            '''
            # S3D-IO and BT-IO
            # Divide a set of configurations into three sections：0 - cross_phase_1，cross_point，cross_phase_2 - 7
            cross_point = random.randint(0, 7)
            cross_phase_1 = cross_point - 1
            cross_phase_2 = cross_point + 1
            offspring = self.sample_random_config()  # Instantiate an object
            phase1 = random.randint(0, 1)
            phase2 = random.randint(0, 1)
            phase3 = random.randint(0, 1)
            name = ['Romio_CB_Read', 'Romio_CB_Write', 'Romio_DS_Read', 'Romio_DS_Write', 'Strip_Count', 'Strip_Size', 'Cb_nodes' ,'Cb_config']
            if phase1 == 0:
                i = 0
                while i <= cross_phase_1:
                    offspring[name[i]] = parent_1[name[i]]
                    i = i + 1
            else:
                i = 0
                while i <= cross_phase_1:
                    offspring[name[i]] = parent_2[name[i]]
                    i = i + 1
            if phase2 == 0:
                offspring[name[cross_point]] = parent_1[name[cross_point]]
            else:
                offspring[name[cross_point]] = parent_2[name[cross_point]]
            if phase3 == 0:
                i = cross_phase_2
                while i <= 7:
                    offspring[name[i]] = parent_1[name[i]]
                    i = i + 1
            else:
                i = cross_phase_2
                while i <= 7:
                    offspring[name[i]] = parent_2[name[i]]
                    i = i + 1
            # mutation
            if random.random() < pm:
                mpoint = random.randint(0, 7)
                if mpoint == 4:
                    ran = random.randint(1, 32)
                    while offspring[name[mpoint]] == ran:
                        ran = random.randint(1, 32)
                elif mpoint == 5:
                    ran = random.randint(1, 512)
                    while offspring[name[mpoint]] == ran:
                        ran = random.randint(1, 512)
                elif mpoint == 6:
                    ran = random.randint(1, 64)
                    while offspring[name[mpoint]] == ran:
                        ran = random.randint(1, 64)
                elif mpoint == 7:
                    ran = random.randint(1, 8)
                    while offspring[name[mpoint]] == ran:
                        ran = random.randint(1, 8)
                else:
                    ran = random.randint(0, 2)
                    while offspring[name[mpoint]] == ran:
                        ran = random.randint(0, 2)
                offspring[name[mpoint]] = ran
        

            next_config = offspring
            if next_config in self.all_configs:
                next_config = self.sample_random_config(excluded_configs=self.all_configs)
        self.all_configs.add(next_config)
        self.running_configs.append(next_config)
        return next_config

    def get_suggestions(self, batch_size=None, history=None):
        if batch_size is None:
            batch_size = self.batch_size

        configs = list()
        for i in range(batch_size):
            config = self.get_suggestion(history)
            configs.append(config)
        return configs

    def update_observation(self, observation: Observation):
        """
        Update the current observations.
        Parameters
        ----------
        observation

        Returns
        -------

        """

        config = observation.config
        perf = observation.objectives[0]
        trial_state = observation.trial_state


        #assert config in self.running_configs
        #self.running_configs.remove(config)
        if config in self.running_configs:
            self.running_configs.remove(config)

        # update population
        if trial_state == SUCCESS and perf < np.inf:
            self.population.append(dict(config=config, age=self.age, perf=perf))
            self.age += 1

        # Eliminate samples
        if len(self.population) > self.population_size:
            if self.strategy == 'oldest':
                self.population.sort(key=lambda x: x['age'])
                self.population.pop(0)
            elif self.strategy == 'worst':
                self.population.sort(key=lambda x: x['perf'])
                self.population.pop(-1)
            else:
                raise ValueError('Unknown strategy: %s' % self.strategy)

        return self.history.update_observation(observation)

    def sample_random_config(self, excluded_configs=None):
        if excluded_configs is None:
            excluded_configs = set()

        sample_cnt = 0
        max_sample_cnt = 1000
        while True:
            config = self.config_space.sample_configuration()
            sample_cnt += 1
            if config not in excluded_configs:
                break
            if sample_cnt >= max_sample_cnt:
                logger.warning('Cannot sample non duplicate configuration after %d iterations.' % max_sample_cnt)
                break
        return config

    def get_history(self):
        return self.history

# License: MIT

import time
import math
from typing import List
from tqdm import tqdm
import numpy as np
from oprael import logger
from oprael.optimizer.base import BOBase
from oprael.utils.constants import SUCCESS, FAILED, TIMEOUT
from oprael.utils.limit import time_limit, TimeoutException
from oprael.utils.util_funcs import parse_result, deprecate_kwarg
from oprael.utils.history import Observation, History
import asyncio
import pandas as pd

from oprael.utils.trainModel import train_XGB, get_darshanFeature, log_scale_feature, getColumns
from concurrent.futures import ThreadPoolExecutor


class Ensemble(BOBase):
    @deprecate_kwarg('num_objs', 'num_objectives', 'a future version')
    def __init__(
            self,
            objective_function: callable,
            config_space,
            num_objectives=1,
            num_constraints=0,
            sample_strategy: str = 'bo',
            max_runs=200,
            runtime_limit=None,
            time_limit_per_trial=180,
            advisor_type='default',
            surrogate_type='auto',
            acq_type='auto',
            acq_optimizer_type='auto',
            initial_runs=3,
            init_strategy='random_explore_first',
            initial_configurations=None,
            ref_point=None,
            transfer_learning_history: List[History] = None,
            logging_dir='logs',
            task_id='OPRAEL',
            visualization='none',
            auto_open_html=False,
            random_state=None,
            logger_kwargs: dict = None,
            advisor_kwargs: dict = None,
            train_csv: str = None,
            access: str = "w",
            darshan_path: str = None,
            common_feature: dict = None,
            custom_advisor_list: list = None,

    ):

        if task_id is None:
            raise ValueError('Task id is not SPECIFIED. Please input task id first.')

        self.num_objectives = num_objectives
        self.num_constraints = num_constraints
        self.FAILED_PERF = [np.inf] * num_objectives
        super().__init__(objective_function, config_space, task_id=task_id, output_dir=logging_dir,
                         random_state=random_state, initial_runs=initial_runs, max_runs=max_runs,
                         runtime_limit=runtime_limit, sample_strategy=sample_strategy,
                         time_limit_per_trial=time_limit_per_trial, transfer_learning_history=transfer_learning_history,
                         logger_kwargs=logger_kwargs)

        self.common_feature = common_feature
        self.advisor_type = advisor_type
        self.Mbytes = 1024 * 1024
        advisor_kwargs = advisor_kwargs or {}
        _logger_kwargs = {'force_init': False}  # do not init logger in advisor
        self.custom_advisor_list = custom_advisor_list
        self.start = time.time()

        if access == "r":
            self.model = train_XGB(train_csv, "read")
            self.input_columns = getColumns("read")
        elif access == "w":
            start = time.perf_counter()
            self.model = train_XGB(train_csv, "write")
            end = time.perf_counter()
            elapsed = end - start
            self.input_columns = getColumns("write")
        self.darshan_feature = get_darshanFeature(darshan_path)
        if advisor_type == 'default':
            from oprael.core.tpe_advisor import TPE_Advisor
            from oprael.core.ga_advisor import GA_Advisor
            self.config_advisor_list = []
            self.pool = ThreadPoolExecutor(max_workers=2)
            ga = GA_Advisor(config_space,
                            num_objectives=num_objectives,
                            num_constraints=num_constraints,
                            optimization_strategy=sample_strategy,
                            batch_size=1,
                            task_id=task_id,
                            output_dir=logging_dir,
                            random_state=random_state,
                            logger_kwargs=_logger_kwargs,
                            **advisor_kwargs)

            tpe = TPE_Advisor(config_space, task_id=task_id, random_state=random_state,
                              logger_kwargs=_logger_kwargs, **advisor_kwargs)
            self.config_advisor_list.append(tpe)
            self.config_advisor_list.append(ga)
        elif advisor_type == 'custom':  # Customizable additions and deletions
            self.pool = ThreadPoolExecutor(max_workers=len(self.custom_advisor_list))
            self.config_advisor_list = []

            for _ in self.custom_advisor_list:
                if _ == "bo":
                    from oprael.core.bo_advisor import Advisor
                    self.config_advisor_list.append(Advisor(config_space,
                                                            num_objectives=num_objectives,
                                                            num_constraints=num_constraints,
                                                            initial_trials=initial_runs,
                                                            init_strategy=init_strategy,
                                                            initial_configurations=initial_configurations,
                                                            optimization_strategy=sample_strategy,
                                                            surrogate_type=surrogate_type,
                                                            acq_type=acq_type,
                                                            acq_optimizer_type=acq_optimizer_type,
                                                            ref_point=ref_point,
                                                            transfer_learning_history=transfer_learning_history,
                                                            task_id=task_id,
                                                            output_dir=logging_dir,
                                                            random_state=random_state,
                                                            logger_kwargs=_logger_kwargs,
                                                            **advisor_kwargs))

                elif _ == "tpe":
                    from oprael.core.tpe_advisor import TPE_Advisor
                    self.config_advisor_list.append(TPE_Advisor(config_space, task_id=task_id, random_state=random_state,
                                                                logger_kwargs=_logger_kwargs, **advisor_kwargs))

                elif _ == "ga":
                    from oprael.core.ga_advisor import GA_Advisor
                    self.config_advisor_list.append(GA_Advisor(config_space,
                                                               num_objectives=num_objectives,
                                                               num_constraints=num_constraints,
                                                               optimization_strategy=sample_strategy,
                                                               batch_size=1,
                                                               task_id=task_id,
                                                               output_dir=logging_dir,
                                                               random_state=random_state,
                                                               logger_kwargs=_logger_kwargs,
                                                               **advisor_kwargs))
        else:
            raise ValueError('Invalid advisor type!')

    def run(self) -> History:
        for _ in tqdm(range(self.iteration_id, self.max_iterations)):
            if self.budget_left < 0:
                logger.info('Time %f elapsed!' % self.runtime_limit)
                break
            start_time = time.time()
            self.iterate(budget_left=self.budget_left)
            runtime = time.time() - start_time
            self.budget_left -= runtime
        return self.get_history()

    def parallel_get_suggestion(self, advisor):
        config = advisor.get_suggestion()

        config_feature = config.get_dictionary()

        cb_common_feature = {**config_feature, **self.common_feature}

        if "Strip_Size" in cb_common_feature:
            cb_common_feature["Strip_Size"] = cb_common_feature["Strip_Size"] * self.Mbytes

        predict_feature = pd.concat([log_scale_feature(pd.DataFrame([cb_common_feature])), self.darshan_feature],
                                    axis=1)
        f_names = self.model.get_booster().feature_names
        df = predict_feature[self.input_columns]
        df = df[f_names]
        performance = self.model.predict(df)
        return [config,performance]


    def score(self):
        tasks = []
        for adv_ in self.config_advisor_list:
            tasks.append(self.pool.submit(self.parallel_get_suggestion,adv_))

        results = []

        for task_ in tasks:
            t_result = task_.result()
            results.append(t_result)

        # Take maximum
        max_score = 0
        max_id = 0

        for i in range(len(results)):
            performance = results[i][1]
            if performance > max_score:  # or max_score * 1.2: consider a 20% error
                max_score = performance
                max_id = i

        return results[max_id][0]

    def iterate(self, budget_left=None) -> Observation:
        # get configuration suggestion from advisor

        time_s = time.time()
        config = self.score()
        time_e = time.time()
        elapsed = time_e-time_s


        trial_state = SUCCESS
        _budget_left = int(1e10) if budget_left is None else budget_left
        _time_limit_per_trial = math.ceil(min(self.time_limit_per_trial, _budget_left))

        cost_time = time.time() - self.start
        logger.info("cost_time:%f"%(cost_time))
        start_time = time.time()
        try:
            # evaluate configuration on objective_function within time_limit_per_trial
            args, kwargs = (config,), dict()
            timeout_status, _result = time_limit(self.objective_function,
                                                 _time_limit_per_trial,
                                                 args=args, kwargs=kwargs)

            if timeout_status:
                raise TimeoutException(
                    'Timeout: time limit for this evaluation is %.1fs' % _time_limit_per_trial)
            else:
                # parse result
                objectives, constraints, extra_info = parse_result(_result)
        except Exception as e:
            # parse result of failed trial
            if isinstance(e, TimeoutException):
                logger.warning(str(e))
                trial_state = TIMEOUT
            else:  # todo: log exception if objective function raises error
                logger.warning(f'Exception when calling objective function: {e}\nconfig: {config}')
                trial_state = FAILED
            objectives = self.FAILED_PERF
            constraints = None
            extra_info = None

        elapsed_time = time.time() - start_time
        # update observation to advisor
        observation = Observation(
            config=config, objectives=objectives, constraints=constraints,
            trial_state=trial_state, elapsed_time=elapsed_time, extra_info=extra_info,
        )
        if _time_limit_per_trial != self.time_limit_per_trial and trial_state == TIMEOUT:
            # Timeout in the last iteration.
            pass
        else:
            for adv_ in self.config_advisor_list:
                adv_.update_observation(observation)

        self.iteration_id += 1
        # Logging
        if self.num_constraints > 0:
            logger.info('Iter %d, objectives: %s. constraints: %s.'
                        % (self.iteration_id, objectives, constraints))
        else:
            logger.info('Iter %d, objectives: %s.' % (self.iteration_id, objectives))

        return observation

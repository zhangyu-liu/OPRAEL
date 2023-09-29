# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from .utils import color_logger as logger

from .utils import space
from .utils import space as sp

from .utils.history import Observation, History

from .optimizer.generic_smbo import SMBO as Optimizer
from .optimizer.parallel_smbo import pSMBO as ParallelOptimizer
from .optimizer.message_queue_smbo import mqSMBO as DistributedOptimizer
from .core.message_queue.worker import Worker as DistributedWorker
from .optimizer.nsga_optimizer import NSGAOptimizer

from .optimizer.OPRAEL import Ensemble as OPRAELOptimizer

from .utils.start_smbo import create_smbo as create_optimizer

from .core.bo_advisor import Advisor
from .core.async_batch_advisor import AsyncBatchAdvisor
from .core.sync_batch_advisor import SyncBatchAdvisor
from .core.tpe_advisor import TPE_Advisor
from .core.ga_advisor import GA_Advisor

from .utils.tuning import get_config_space, get_objective_function

from .utils.test_install import run_test


__version__ = version = "0.8.0"


__all__ = [
    "__version__", "version",
    "logger",
    "sp", "space",
    "Observation", "History",
    "Optimizer", "ParallelOptimizer", "DistributedOptimizer", "DistributedWorker", "OPRAELOptimizer",
    "NSGAOptimizer",
    "create_optimizer",
    "Advisor",
    "AsyncBatchAdvisor", "SyncBatchAdvisor",
    "TPE_Advisor", "GA_Advisor", "Advisor",
    "get_config_space", "get_objective_function",
    "run_test",
]

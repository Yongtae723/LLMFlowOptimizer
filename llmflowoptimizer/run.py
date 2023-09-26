import logging
from typing import Any, Dict, List, Optional, Tuple

import hydra
import rootutils
from omegaconf import DictConfig
from pprint import pprint
from llmflowoptimizer.models.components.base import BaseChainModel, BaseEvaluationModel
from llmflowoptimizer.utils.utils import print_config_tree

log = logging.getLogger(__name__)


rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)


@hydra.main(version_base="1.3", config_path="../configs", config_name="run.yaml")
def main(cfg: DictConfig) -> Optional[float]:
    """
    This is the main entry point of the tune script.
    """
    log.info(f"Instantiating model <{cfg.model._target_}>")
    model: BaseChainModel = hydra.utils.instantiate(cfg.model)

    if cfg.extras.print_config:
        print_config_tree(cfg)

    if cfg.extras.evaluation:
        evaluator: BaseEvaluationModel = hydra.utils.instantiate(cfg.evaluation)
        log.info(f"Evaluating <{cfg.model._target_}>")
        metric_value = evaluator.evaluate(model)
        log.info(f"Score is  {metric_value}")
        return metric_value



if __name__ == "__main__":
    main()

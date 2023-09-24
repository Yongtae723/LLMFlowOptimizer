from typing import Any, Dict, List, Optional, Tuple

import hydra
from omegaconf import DictConfig
import rootutils

from llmflowtuner.models.components.base import BaseChainModel, BaseEvaluationModel

import logging
log = logging.getLogger(__name__)


rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)


@hydra.main(version_base="1.3", config_path="../configs", config_name="tune.yaml")
def main(cfg: DictConfig) -> Optional[float]:
    """
    This is the main entry point of the tune script.
    """

    log.info(f"Instantiating model <{cfg.model._target_}>")
    model:BaseChainModel  = hydra.utils.instantiate(cfg.model)
    evaluator:BaseEvaluationModel  = hydra.utils.instantiate(cfg.evaluation)

    log.info(f"Evaluating <{cfg.model._target_}>")
    metric_value = evaluator.evaluate(model)
    
    return metric_value

if __name__ == "__main__":
    main()
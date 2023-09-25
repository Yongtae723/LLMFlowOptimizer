import logging
from typing import Any, Dict, List, Optional, Tuple

import hydra
import rootutils
from omegaconf import DictConfig
from pprint import pprint
from llmflowoptimizer.models.components.base import BaseChainModel, BaseEvaluationModel

log = logging.getLogger(__name__)


rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)


@hydra.main(version_base="1.3", config_path="../configs", config_name="tune.yaml")
def main(cfg: DictConfig) -> Optional[float]:
    """
    This is the main entry point of the tune script.
    """
    pprint(cfg)
    log.info(f"Instantiating model <{cfg.model._target_}>")
    model: BaseChainModel = hydra.utils.instantiate(cfg.model)

    if not cfg.skip_eval:
        evaluator: BaseEvaluationModel = hydra.utils.instantiate(cfg.evaluation)
        log.info(f"Evaluating <{cfg.model._target_}>")
        metric_value = evaluator.evaluate(model)

        return metric_value


if __name__ == "__main__":
    main()

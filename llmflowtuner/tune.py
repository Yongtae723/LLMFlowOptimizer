from typing import Any, Dict, List, Optional, Tuple

import hydra
from omegaconf import DictConfig
import rootutils


rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)


@hydra.main(version_base="1.3", config_path="../configs", config_name="tune.yaml")
def main(cfg: DictConfig) -> Optional[float]:
    """
    This is the main entry point of the tune script.
    """
    print(cfg.model)
    model:Any  = hydra.utils.instantiate(cfg.model)
    print(model("いい感じの質問"))

if __name__ == "__main__":
    main()
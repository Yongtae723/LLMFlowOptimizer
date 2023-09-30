import os

import pytest
import rootutils
from hydra import compose, initialize
from omegaconf import DictConfig, open_dict

os.environ["OPENAI_API_KEY"] = "sk-xxx"


@pytest.fixture(scope="package")
def cfg_run() -> DictConfig:
    """A pytest fixture for providing a configuration.

    :return: A DictConfig object containing a default Hydra configuration.
    """
    with initialize(version_base="1.3", config_path="../configs"):
        cfg = compose(config_name="run.yaml", return_hydra_config=True, overrides=[])
        with open_dict(cfg):
            cfg.paths.root = str(rootutils.find_root(indicator=".project-root"))
    return cfg

"""This file prepares config fixtures for other tests."""

from pathlib import Path

import pytest
import rootutils
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra
from omegaconf import DictConfig, open_dict


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

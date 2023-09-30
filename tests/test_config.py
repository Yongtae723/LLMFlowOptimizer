import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig


def test_config(cfg_run: DictConfig) -> None:
    """Tests whether the config is valid and can be instantiated.

    :param cfg_run: A DictConfig containing a valid training configuration.
    """
    assert cfg_run
    assert cfg_run.model
    assert cfg_run.evaluation

    HydraConfig().set_config(cfg_run)

    hydra.utils.instantiate(cfg_run.model)
    hydra.utils.instantiate(cfg_run.evaluation)

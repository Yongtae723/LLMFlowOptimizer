from omegaconf import DictConfig
from optuna.trial import Trial


def configure(cfg: DictConfig, trial: Trial) -> None:
    """You can use `cfg` and `trial` to define the search space."""
    chunk_size = trial.params["model.text_splitter.chunk_size"]
    min_chunk_overlap = max(0, chunk_size - 900)
    max_chunk_overlap = max(0, chunk_size - 400)
    trial.suggest_int("model.text_splitter.chunk_overlap", min_chunk_overlap, max_chunk_overlap)

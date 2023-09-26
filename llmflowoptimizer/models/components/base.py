from abc import ABC, abstractmethod
from typing import Any


class BaseChainModel(ABC):
    """Define the flow of the model to be adjusted.

    ```python
    def __init__(self):
    # Define the flow. component defined here can be optimized by hyperparameter search.

    def __call__(self, input):
    # Define when this model is called.
    ```
    """

    def __init__(self, **kwargs) -> None:
        ...

    def __call__(self, input: str) -> Any:
        """You can define when this class is called."""
        ...


class BaseEvaluationModel(ABC):
    """Define the evaluation system. llmflowoptimizer optimizes the hyperparameters of the model
    based on the output of this evaluation system.

    ```python
    def __init__(self):
    # component defined here can specified as a hyperparameter.

    def __call__(self, input):
    # evaluate AI model.
    ```
    """

    def __init__(self, **kwargs) -> None:
        ...

    def evaluate(self, model: BaseChainModel, **kwargs) -> Any:
        """# evaluate AI model.

        Optimizer maximize/minimize the output of this function.
        """
        ...

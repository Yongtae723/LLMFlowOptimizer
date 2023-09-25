import json

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_recall,
    context_relevancy,
    faithfulness,
)
from ragas.metrics.critique import harmfulness

from llmflowoptimizer.models.components.base import BaseChainModel, BaseEvaluationModel


class Evaluation(BaseEvaluationModel):
    """
    Define the evaluation system.
    llmflowoptimizer optimizes the hyperparameters of the model based on the output of this evaluation system.

    ```python
    def __init__(self):
    # component defined here can specified as a hyperparameter.

    def __call__(self, input):
    # evaluate AI model.
    Optimizer maximize/minimize the output of this function.
    ```
    """

    def __init__(
        self,
        eval_data_path: str,
        target_metric: str = "ragas_score",
    ):
        with open(eval_data_path) as f:
            self.eval_data = json.load(f)
        self.target_metric = target_metric

    def evaluate(
        self,
        model: BaseChainModel,
    ):
        # execute model
        result_dict = {
            "question": [],
            "answer": [],
            "ground_truths": [],
            "contexts": [],
        }
        for data in self.eval_data:
            answer = model(data["question"])
            result_dict["question"].append(data["question"])
            result_dict["answer"].append(answer["answer"])
            result_dict["ground_truths"].append([data["ground_truth"]])
            contexts = [
                source_document.page_content
                for source_document in answer["source_documents"]
            ]
            result_dict["contexts"].append(contexts)
        results = Dataset.from_dict(result_dict)

        # evaluate model
        result = evaluate(
            dataset=results,
            metrics=[
                context_relevancy,
                faithfulness,
                answer_relevancy,
                context_recall,
                harmfulness,
            ],
        )
        return result[self.target_metric]

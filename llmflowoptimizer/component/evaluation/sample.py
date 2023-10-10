import json
from typing import Any

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy


class Evaluation:
    """Define the evaluation system.

    llmflowoptimizer optimizes the hyperparameters of the model
    Return value of `__call__` is used as score and component will be optimized to maximize/minimize the score.
    """

    def __init__(
        self,
        eval_dataset_path: str,
    ):
        with open(eval_dataset_path) as f:
            self.eval_data = json.load(f)

    def evaluate(
        self,
        model: Any,  # this model should be defined in llmflowoptimizer/component/model/sample_qa.py
    ):
        # simple evaluation using ragas
        evaluation_dataset = {
            "question": [],
            "answer": [],
            "contexts": [],
            "ground_truths": [],
        }
        for data in self.eval_data:
            output = model(data["question"])
            evaluation_dataset["question"].append(data["question"])
            evaluation_dataset["answer"].append(output["result"])
            evaluation_dataset["contexts"].append(
                [document.page_content for document in output["source_documents"]]
            )
            evaluation_dataset["ground_truths"].append([data["ground_truth"]])
        evaluation_dataset = Dataset.from_dict(evaluation_dataset)

        result = evaluate(evaluation_dataset, metrics=[answer_relevancy])

        return result["answer_relevancy"]

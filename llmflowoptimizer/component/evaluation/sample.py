import datetime
from typing import Any, Optional

from langchain.smith import RunEvalConfig, run_on_dataset
from langsmith import Client
from ragas.langchain.evalchain import RagasEvaluatorChain
from ragas.metrics import (
    answer_relevancy,
    context_recall,
    context_relevancy,
    faithfulness,
)
from scipy import stats

from llmflowoptimizer.component.base.base import BaseChainModel, BaseEvaluationModel


class Evaluation(BaseEvaluationModel):
    """Define the evaluation system. llmflowoptimizer optimizes the hyperparameters of the model
    based on the output of this evaluation system.

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
        dataset_name: str,
        project_name: Optional[str] = None,
        **kwargs: Any,
    ):
        self.client = Client()
        self.dataset_name = dataset_name
        self.project_name = project_name
        self.additional_setting = kwargs

        # create evaluation chains
        faithfulness_chain = RagasEvaluatorChain(metric=faithfulness)
        answer_rel_chain = RagasEvaluatorChain(metric=answer_relevancy)
        context_rel_chain = RagasEvaluatorChain(metric=context_relevancy)
        context_recall_chain = RagasEvaluatorChain(metric=context_recall)
        self.evaluation_config = RunEvalConfig(
            evaluators=["qa"],
            custom_evaluators=[
                faithfulness_chain,
                answer_rel_chain,
                context_rel_chain,
                context_recall_chain,
            ],
            prediction_key="result",
        )

    def evaluate(
        self,
        model: BaseChainModel,
    ):
        """Return of this method is used for hyperparameter optimization."""
        project_name = self.project_name + datetime.datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
        result = run_on_dataset(
            client=self.client,
            dataset_name=self.dataset_name,
            llm_or_chain_factory=model,
            evaluation=self.evaluation_config,
            project_name=project_name,
            input_mapper=lambda x: x,
            **self.additional_setting,
        )
        result = self.calculate_score_from_langsmith(result)
        return result["final_score"]

    def calculate_score_from_langsmith(self, result):
        """In this sample, we calculate mean score of correctness and ragas_score.

        ragas_score is calculated by harmonic mean of faithfulness, answer_relevancy,
        context_relevancy, context_recall.
        https://github.com/explodinggradients/ragas
        """
        correctness = 0
        ragas_score = 0

        for _, val in result["results"].items():
            scores_for_ragas_score = []
            for feedback in val["feedback"]:
                if feedback.key == "correctness":
                    correctness += feedback.score
                else:
                    scores_for_ragas_score.append(feedback.score)

            ragas_score += stats.hmean(scores_for_ragas_score)
        correctness = correctness / len(result["results"].keys())
        ragas_score = ragas_score / len(result["results"].keys())
        final_score = sum([correctness, ragas_score]) / len([correctness, ragas_score])
        return {"final_score": final_score, "ragas_score": ragas_score}

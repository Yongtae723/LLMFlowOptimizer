from typing import Any

from langchain.document_loaders import TextLoader
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.schema.embeddings import Embeddings
from langchain.schema.language_model import BaseLanguageModel
from langchain.text_splitter import TextSplitter


class SampleQA:
    """
    Define the flow of the model to be adjusted.


    ```python
    def __init__(self):
    # Define the flow. component defined here can be optimized by hyperparameter search.

    def __call__(self, input):
    # Define when this model is called.
    ```
    """

    def __init__(
        self,
        data_path: str,
        embedding: Embeddings,
        text_splitter: TextSplitter,
        llm_for_answer: BaseLanguageModel,
    ) -> None:
        """
        Input the elements necessary for LLM flow
        The arguments here can be searched for hyperparameters in the future.

        the arguments are defined by `configs/model/sample.yaml`
        """
        text_loader = TextLoader(data_path)
        self.index = VectorstoreIndexCreator(
            embedding=embedding, text_splitter=text_splitter
        ).from_loaders([text_loader])

        self.llm_for_answer = llm_for_answer

    def __call__(self, input: str) -> Any:
        return self.index.query_with_sources(
            input, llm=self.llm_for_answer, return_source_documents=True
        )

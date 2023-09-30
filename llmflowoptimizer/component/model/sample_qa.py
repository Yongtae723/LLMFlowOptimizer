from langchain.chains import RetrievalQA
from langchain.chains.base import Chain
from langchain.document_loaders import TextLoader
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.schema.embeddings import Embeddings
from langchain.schema.language_model import BaseLanguageModel
from langchain.text_splitter import TextSplitter

from llmflowoptimizer.component.base.base import BaseChainModel


class SampleQA(BaseChainModel):
    """Define the flow of the model to be adjusted."""

    def __init__(
        self,
        data_path: str,
        embedding: Embeddings,
        text_splitter: TextSplitter,
        llm: BaseLanguageModel,
    ) -> None:
        """Input the elements necessary for LLM flow The arguments here will be used as a
        hyperparameters and optimized.

        the arguments are defined by `configs/model/sample.yaml`
        """
        self.embedding = embedding
        self.text_splitter = text_splitter
        text_loader = TextLoader(data_path)
        self.index = VectorstoreIndexCreator(
            embedding=embedding, text_splitter=text_splitter
        ).from_loaders([text_loader])

        self.chain = RetrievalQA.from_chain_type(
            llm,
            retriever=self.index.vectorstore.as_retriever(),
            return_source_documents=True,
        )

    def get_chain(self) -> Chain:
        """Get langchain chain."""
        return self.chain
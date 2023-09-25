# LLMFlowOptimizer (WIP)

## 📌  Introduction
In recent years, various LLMs, embedding models, and LLM flows utilizing them have been proposed, making it difficult to manually verify which flow or component is optimal.

This repository aims to treat LLMs and Embeddings as a single hyperparameter, with the goal of automatically searching for the optimal hyperparameter of the LLM flow.

This repository is strongly inspired by [lightning-hydra-template](https://github.com/ashleve/lightning-hydra-template)

![concept_image](documents/concept.png)
**This is the concept image of this repository (image from [Flowise](https://github.com/FlowiseAI/Flowise)). Component of LangChain like a LLM or Embedding can be treated as hyperparameter. You can find optimal component from various candidate.**

## 🔧  Main Technologies

- [LangChain](https://github.com/langchain-ai/langchain) : LangChain is a framework for developing applications powered by large language models. It can be divided conceptually into components (like llm component, embedding component), which are well-abstracted and easy to switch. This is the reason we can treat each component as hyperparameter.

- [Hydra](https://github.com/facebookresearch/hydra) : Hydra is an open-source Python framework that simplifies the development of research and other complex applications. It has the ability to dynamically create a hierarchical configuration system, which is its key feature


- [Optuna](https://github.com/optuna/optuna) : Optuna is an open-source Python library for hyperparameter optimization. It offers a define-by-run API that allows users to construct search spaces, a mixture of efficient searching, and pruning algorithm to enhance the cost-effectiveness of optimization. Optuna also provides a web dashboard for visualization and evaluation of studies in real-time. 

- [ragas](https://github.com/explodinggradients/ragas) : Ragas is an evaluation framework for Retrieval Augmented Generation (RAG) pipelines that provides tools based on the latest research for evaluating LLM-generated text to give insights about the RAG pipeline.

# How to use
please clone this repository and install requirements.
```bash
git clone git@github.com:Yongtae723/LLMFlowOptimizer.git
cd llmflowoptimizer
```

## setup
We use poetry for package management. you can install poetry and python packages by following command.
```bash
pip install poetry
poetry install
```

## define model architect and config.
1. Define model architect on [llmflowoptimizer/model](llmflowoptimizer/model) like [sample_qa.py](llmflowoptimizer/model/sample_qa.py)
    The arguments in this `__init__()` can be used as hyperparameter and will be optimized.

2. Define model config on [configs/model](configs/model).

3. then you can check your model and config by following command.
```bash
poetry run python llmflowoptimizer/tune.py skip_eval=true
```

## define evaluation system
1. Define evaluation system on [llmflowoptimizer/model/evaluation.py](llmflowoptimizer/model/evaluation.py).
    The arguments in this `__init__()` can be used as hyperparameter. config
        Optuna will optimize component of LLM flow by maximizing or minimizing the return value of this evaluation system.
2. then you can check your evaluation system by following command.
```bash
poetry run python llmflowoptimizer/tune.py
```

## override

when you want to change component without any changing code, hydra offers override option since we can treat component as a hyperparameter.

### override single parameter
when you want to change single parameter, you have to use `.` between parameter name.
```bash
poetry run python llmflowoptimizer/tune.py model.llm_for_answer.model_name="gpt-4"
```
By doing this, you change `model_name` parameter of `llm_for_answer` to gpt-4.

### override group parameter
when you want to change parameter group, you have to use `/` between parameter name and value.
```bash
poetry run python llmflowoptimizer/tune.py model/llm_for_answer=OpenAI
```

By doing this, LLM flow use [`OpenAI.yaml`](configs/model/llm_for_answer/OpenAI.yaml) model instead of [`ChatOpenAI.yaml`](configs/model/llm_for_answer/ChatOpenAI.yaml) model.

### Experiment config
you can also save experimental config on [configs/experiment](configs/experiment).

after you save config [configs/experiment](configs/experiment)., you can override like below.
```bash
poetry run python llmflowoptimizer/tune.py experiment=example
```




## Hyperparameter search
WIP


# TODO
- [ ] Hyperparameter search by optuna
- [ ] manage experiment config (langsmith? WandB?)
- [ ] add test function
- [ ] update readme
- [ ] model can be build from GUI langchain builder
    - [ ] langflow
    - [ ] Flowise
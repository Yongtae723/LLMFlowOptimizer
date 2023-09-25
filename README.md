# override

when you want to change huperparameter, hydra offers override option.

### override single parameter
when you want to change single parameter, you have to use `.` between parameter name.
```bash
python llmflowoptimizer/tune.py model.llm_for_answer.model_name="gpt-4"
```
By doing this, you change `model_name` parameter of `llm_for_answer` to gpt-4.

### override group parameter
when you want to change parameter group, you have to use `/` between parameter name and value.
```bash
python llmflowoptimizer/tune.py model/llm_for_answer=OpenAI
```

By doing this, you use [`OpenAI.yaml`](configs/model/llm_for_answer/OpenAI.yaml) model instead of [`ChatOpenAI.yaml`](configs/model/llm_for_answer/ChatOpenAI.yaml) model.

### Experiment config
you can also save experimental config on [configs/experiment](configs/experiment).

after you save config [configs/experiment](configs/experiment)., you can override like below.
```bash
python llmflowoptimizer/tune.py experiment=example
```
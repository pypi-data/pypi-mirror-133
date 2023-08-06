# ExplainaBoard SDK
Reconstruct ExplainaBoard into OOP Version





```
python setup.py install
```

```python
from explainaboard import TaskType, get_loader, get_processor

path_data = "./explainaboard/tests/artifacts/test-summ.tsv"
loader = get_loader(TaskType.summarization, data = path_data)
data = loader.load()
processor = get_processor(TaskType.summarization, data = data)
analysis = processor.process()
analysis.write_to_directory("./")
```

### Existing Support [More](https://github.com/ExpressAI/ExplainaBoard/blob/main/docs/existing_supports.md)
* `TaskType.text_classification`
  * `FileType.tsv`
* `TaskType.named_entity_recognition`
  * `FileType.conll`
* `TaskType.summarization`
  * `FileType.tsv`
* `TaskType.extractive_qa`
  * `FileType.json` (same format with squad)




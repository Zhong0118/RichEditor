---
frameworks:
- Pytorch
license: Apache License 2.0
tasks:
- sentence-embedding
---

```python
from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

pipeline_se = pipeline(Tasks.sentence_embedding,
                       model='thomas/text2vec-base-chinese', model_revision='v1.0.0')

inputs = {
        "source_sentence": [
            "不可以，早晨喝牛奶不科学",
            "吃了海鲜后是不能再喝牛奶的，因为牛奶中含得有维生素C，如果海鲜喝牛奶一起服用会对人体造成一定的伤害",
            "吃海鲜是不能同时喝牛奶吃水果，这个至少间隔6小时以上才可以。",
            "吃海鲜是不可以吃柠檬的因为其中的维生素C会和海鲜中的矿物质形成砷"
        ]
}
result = pipeline_se(input=inputs)
print (result)
```

#### Clone with HTTP
```bash
 git clone https://www.modelscope.cn/thomas/text2vec-base-chinese.git
```
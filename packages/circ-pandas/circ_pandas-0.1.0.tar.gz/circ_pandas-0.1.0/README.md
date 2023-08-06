# circ-pandas

`circ-pandas` extends pandas data for circular data.

### Mean direction

```python
>> import pandas as pd
>> from circpandas import circseries

>> s = pd.Series([170, -160])
>> s.circ.mean(radian=False)
-175.0
```

### Circular variance

```python
>> import pandas as pd
>> from circpandas import circseries

>> s = pd.Series([45, -45])
>> s.circ.var(radian=False)
0.2928932188134524 # 1 - (1 / sqrt(2))
```

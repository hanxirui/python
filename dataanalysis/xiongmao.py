import pandas as pd
import seaborn as sns

df = pd.DataFrame({ 'A' : 1.,
                    'B' : pd.Timestamp('20130102'),
                    'C' : pd.Series(1, index=list(range(4)), dtype='float32'),
                    'D' : pd.Series([1, 2, 1, 2], dtype='int32'),
                    'E' : pd.Categorical(["test", "train", "test", "train"]),
                    'F' : 'foo' })
print(df.B)
print(df.groupby('E').sum().D)


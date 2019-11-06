```python
from useful_scit.imps import *
```


```python
path = '/Users/diego/Downloads/error/flxout_d02_20171224_080000.nc'
```


```python

```


```python
%load_ext autoreload
%autoreload 2
```


```python
import useful_scit.util.list_manipulation as lm
```


```python
l1,n1 = [1,2,3,4],100
```


```python
lm.partition(l1,n1)
```




    []




```python
lm.partition(l1,n1,up2=True)
```




    [[1, 2, 3, 4]]




```python

```

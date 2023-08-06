# MCHostResolver

Эта библиотека создана чтобы упростить получение айпи майнкрафт сервера.

Использование:
```python
from MCHostResolver import IPFinder

hostname = 'hypixel.net'
resolved = IPFinder.resolve(hostname)
print(resolved)
```
Так же можно использовать resolve но уже только получая вывод в виде айпи.
```python
from MCHostResolver import IPFinder

hostname = 'hypixel.net'
resolved = IPFinder.resonlyip(hostname)
print(resolved)
```

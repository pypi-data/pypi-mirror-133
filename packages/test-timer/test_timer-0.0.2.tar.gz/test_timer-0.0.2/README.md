## Benchmark your code while unit testing them

### Usecases
1. Problem solving. To quickly check different implementations and compare versions to find which one performs better.
2. Quick algorithm mockup. Again, to quickly check different approaches and implementations and compare versions to find which one performs better.

### What it does not provide insights about
1. Overall performance score of your application.
2. Algorithmic complexity.


```Python
import time
import test_timer


def function_a():
    ...


def function_b():
    time.sleep(1)


class TestSrc(test_timer.BenchTestCase):
    def test_function_a(self):
        function_a()

    def test_function_b(self):
        function_b()

if __name__ == "__main__":
    test_timer.main()
```

```Bash
test_function_a (__main__.TestSrc): 0:00:00.000052
.
test_function_b (__main__.TestSrc): 0:00:01.001192
.
----------------------------------------------------------------------
Ran 2 tests in 1.002s

OK
```

### How to install:
```Bash
pip install test_timer
```

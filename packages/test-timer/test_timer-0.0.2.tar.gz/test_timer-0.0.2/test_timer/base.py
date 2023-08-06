import time
import unittest
from datetime import timedelta
from unittest import TestProgram, loader, TextTestResult


class BenchTestCase(unittest.TestCase):
    ...


class TimeLoggingTestResult(TextTestResult):

    def startTest(self, test):
        self._started_at = time.time()
        super().startTest(test)

    def addSuccess(self, test):
        elapsed = time.time() - self._started_at
        name = self.getDescription(test)
        self.stream.write("\n{}: {}\n".format(name, timedelta(seconds=elapsed)))
        super().addSuccess(test)


class BenchTestTextTestRunner(unittest.TextTestRunner):
    resultclass = TimeLoggingTestResult


class BenchTest(TestProgram):
    testRunner = BenchTestTextTestRunner

    def __init__(self, module='__main__', defaultTest=None, argv=None,
                 testLoader=loader.defaultTestLoader,
                 exit=True, verbosity=1, failfast=None, catchbreak=None,
                 buffer=None, warnings=None, tb_locals=False):
        super().__init__(module='__main__', defaultTest=None, argv=None,
                         testLoader=testLoader, testRunner=self.testRunner,
                         exit=True, verbosity=1, failfast=None, catchbreak=None,
                         buffer=None, warnings=None, tb_locals=False)

main = BenchTest

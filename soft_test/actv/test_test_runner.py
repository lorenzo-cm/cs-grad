from test_loader import TestLoader
from test_runner import TestRunner
from test_test_loader import TestLoaderTest

loader = TestLoader()
suite = loader.make_suite(TestLoaderTest)

runner = TestRunner()
runner.run(suite)
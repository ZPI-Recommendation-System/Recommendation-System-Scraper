import pytest

from src.constants import TOKENS_CPU_COL_NAME


class MergeAllegroCPUTests:

    @pytest.fixture(scope='function')
    def laptops_data(self):
        data = {TOKENS_CPU_COL_NAME: ["['AMD 3020e']", "['AMD A4-9125']"]}
    def test_create_laptop_token_column(self):
        assert False

    def test_create_laptops_tokens(self):
        assert False

    def test_create_benchmark_tokens(self):
        assert False

    def test_test_tokens(self):
        assert False

    def test_print_assigns(self):
        assert False

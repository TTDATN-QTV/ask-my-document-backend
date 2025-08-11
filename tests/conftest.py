import sys
import os
import pytest

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.utils.build_mock_index import build_mock_index

@pytest.fixture(scope="session")
def build_mock_faiss_index():
    """
    Build a mock FAISS index before running tests that depend on it.
    """
    build_mock_index()
    yield

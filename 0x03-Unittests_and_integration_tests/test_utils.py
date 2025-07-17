
"""Test module for utils.access_nested_map, utils.get_json, and utils.memoize functions."""

import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict
from unittest.mock import patch, Mock

class TestAccessNestedMap(unittest.TestCase):
    """Test class for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """Test that access_nested_map returns the expected nested value.

        Args:
            nested_map (Mapping): The nested dictionary to access.
            path (Sequence): The path of keys to navigate.
            expected (Any): The expected value at the path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence, expected_msg: str) -> None:
        """Test that access_nested_map raises a KeyError with the expected message for invalid paths.

        Args:
            nested_map (Mapping): The nested dictionary to access.
            path (Sequence): The path of keys that should raise an exception.
            expected_msg (str): The expected substring of the KeyError message.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_msg)

class TestGetJson(unittest.TestCase):
    """Test class for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict) -> None:
        """Test that get_json returns the mocked payload and calls requests.get once.

        Args:
            test_url (str): The URL to mock for the HTTP request.
            test_payload (Dict): The expected JSON payload to return.
        """
        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(**{'json.return_value': test_payload})
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """Test class for the memoize decorator."""

    def test_memoize(self) -> None:
        """Test that memoize caches the result and calls the method only once.

        The test defines a class with a_method and a_property decorated with memoize.
        It mocks a_method to return 42 and verifies a_property returns 42 twice,
        while a_method is called only once.
        """
        class TestClass:
            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42
            test_instance = TestClass()
            result1 = test_instance.a_property
            result2 = test_instance.a_property
            mock_method.assert_called_once()
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
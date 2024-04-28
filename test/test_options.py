from dataclasses import dataclass
from typing import Any

import pytest
from glue_utils import BaseOptions


@dataclass(frozen=True)
class Options(BaseOptions):
    connection_name: str
    source_database: str
    source_schema: str
    source_table: str
    target_database: str
    target_schema: str
    target_table: str


class TestOptions:
    def test_from_resolved_options(self):
        resolved_options = {
            "JOB_NAME": "test-job",
            "CONNECTION_NAME": "test-connection",
            "SOURCE_DATABASE": "test-source-database",
            "SOURCE_SCHEMA": "test-source-schema",
            "SOURCE_TABLE": "test-source-table",
            "TARGET_DATABASE": "test-target-database",
            "TARGET_SCHEMA": "test-target-schema",
            "TARGET_TABLE": "test-target-table",
        }

        options = Options.from_resolved_options(resolved_options)

        assert options.job_name == "test-job"
        assert options.connection_name == "test-connection"
        assert options.source_database == "test-source-database"
        assert options.source_schema == "test-source-schema"
        assert options.source_table == "test-source-table"
        assert options.target_database == "test-target-database"
        assert options.target_schema == "test-target-schema"
        assert options.target_table == "test-target-table"


@dataclass(frozen=True)
class OptionsWithDifferentTypes(BaseOptions):
    string_option: str
    integer_option: int
    float_option: float
    boolean_option: bool
    dictionary_option: dict[str, Any]
    list_option: list[Any]


class TestOptionsWithDifferentTypes:
    def test_from_resolved_options(self):
        resolved_options = {
            "JOB_NAME": "test-job",
            "STRING_OPTION": "test-string",
            "INTEGER_OPTION": "1",
            "FLOAT_OPTION": "1.0",
            "BOOLEAN_OPTION": "false",
            "DICTIONARY_OPTION": '{"key": "value"}',
            "LIST_OPTION": '["item"]',
        }

        options = OptionsWithDifferentTypes.from_resolved_options(resolved_options)

        assert options.job_name == "test-job"
        assert options.string_option == "test-string"
        assert options.integer_option == 1
        assert options.float_option == 1.0
        assert options.boolean_option is False
        assert options.dictionary_option == {"key": "value"}
        assert options.list_option == ["item"]


@dataclass(frozen=True)
class OptionsWithBooleanVariants(BaseOptions):
    boolean_option: bool


class TestOptionsWithBooleanVariants:
    @pytest.mark.parametrize(
        "given, expected",
        [
            ("0", False),
            ("1", True),
            ("false", False),
            ("true", True),
            ("null", False),
            ("{}", False),
            ("[]", False),
        ],
    )
    def test_from_resolved_options(self, given: str, expected: bool):  # noqa: FBT001
        resolved_options = {
            "JOB_NAME": "test-job",
            "BOOLEAN_OPTION": given,
        }

        options = OptionsWithBooleanVariants.from_resolved_options(resolved_options)

        assert options.job_name == "test-job"
        assert options.boolean_option is expected


@dataclass(frozen=True)
class OptionsWithJSONTypes(BaseOptions):
    dictionary_option: dict[str, Any]
    list_option: list[Any]


class TestOptionsWithJSONTypes:
    def test_from_resolved_options(self):
        resolved_options = {
            "JOB_NAME": "test-job",
            "DICTIONARY_OPTION": '{"key": "value"}',
            "LIST_OPTION": '["item"]',
        }

        options = OptionsWithJSONTypes.from_resolved_options(resolved_options)

        assert options.job_name == "test-job"
        assert options.dictionary_option == {"key": "value"}
        assert options.list_option == ["item"]

    @pytest.mark.parametrize(
        "incorrect_option, value",
        [("list_option", '{"key": "value"}'), ("dictionary_option", '["item"]')],
    )
    def test_with_incorrect_types(self, incorrect_option: str, value: str):
        resolved_options = {
            "JOB_NAME": "test-job",
            "LIST_OPTION": value,
            "DICTIONARY_OPTION": value,
        }

        with pytest.raises(TypeError, match=incorrect_option):
            OptionsWithJSONTypes.from_resolved_options(resolved_options)

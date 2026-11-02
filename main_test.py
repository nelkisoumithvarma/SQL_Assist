
import json

import pytest
from pydantic import ValidationError

from main import (
    SQLAnalysis,
    validate_sql,
    save_analysis,
)


# 1. Test valid SQL input
def test_valid_sql():
    sql = "SELECT * FROM Customers"

    result = validate_sql(sql)

    assert result == sql


# 2. Test empty SQL input
def test_empty_sql():
    with pytest.raises(ValueError):
        validate_sql("")


# 3. Test SQL exceeding maximum length
def test_long_sql():
    sql = "A" * 10001

    with pytest.raises(ValueError):
        validate_sql(sql)


# 4. Test Pydantic structured output
def test_pydantic_model():
    result = SQLAnalysis(
        query_type="SELECT",
        tables=["Customers"],
        columns=["CustomerID"],
        joins=[],
        complexity="Beginner",
        filters=[],
        aggregations=[],
        group_by=[],
        order_by=[],
        subqueries=[],
        business_purpose="Retrieve customer information.",
        explanation="Retrieves customer IDs.",
        optimization_tips=[]
    )

    assert result.query_type == "SELECT"
    assert result.tables == ["Customers"]
    assert result.joins == []
    assert result.business_purpose == "Retrieve customer information."


# 5. Test saving JSON output
def test_save_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = SQLAnalysis(
        query_type="SELECT",
        tables=["Customers"],
        columns=["CustomerID"],
        joins=[],
        complexity="Beginner",
        filters=[],
        aggregations=[],
        group_by=[],
        order_by=[],
        subqueries=[],
        business_purpose="Retrieve customer information.",
        explanation="Retrieves customer IDs.",
        optimization_tips=[]
    )

    output_file = save_analysis(result)

    assert output_file.exists()

    saved_data = json.loads(
        output_file.read_text(encoding="utf-8")
    )

    assert saved_data["query_type"] == "SELECT"
    assert saved_data["tables"] == ["Customers"]
    assert saved_data["business_purpose"] == "Retrieve customer information."


# 6. Test rejection of unexpected fields
def test_extra_fields_rejected():
    with pytest.raises(ValidationError):
        SQLAnalysis(
            query_type="SELECT",
            tables=["Customers"],
            columns=["CustomerID"],
            joins=[],
            complexity="Beginner",
            filters=[],
            aggregations=[],
            group_by=[],
            order_by=[],
            subqueries=[],
            business_purpose="Retrieve customer information.",
            explanation="Retrieves customer IDs.",
            optimization_tips=[],
            unexpected_field="Not allowed"
        )

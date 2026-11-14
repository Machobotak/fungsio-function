
import pytest

from library import (
    search_data,
    filter_data,
    sort_data,
    group_data,
    calculate_stats
)


# ==========================================
# SAMPLE DATA
# ==========================================

@pytest.fixture
def sample_data():
    return [
        {"name": "Laptop", "category": "Electronics", "price": 8000000},
        {"name": "Mouse", "category": "Electronics", "price": 150000},
        {"name": "Book", "category": "Education", "price": 50000},
        {"name": "Keyboard", "category": "Electronics", "price": 300000}
    ]


# ==========================================
# TEST SEARCH DATA
# ==========================================

def test_search_data(sample_data):
    result = search_data(
        sample_data,
        "laptop",
        ["name"]
    )

    assert len(result) == 1
    assert result[0]["name"] == "Laptop"


def test_search_case_insensitive(sample_data):
    result = search_data(
        sample_data,
        "ELECTRONICS",
        ["category"]
    )

    assert len(result) == 3


def test_search_no_result(sample_data):
    result = search_data(
        sample_data,
        "Phone",
        ["name"]
    )

    assert result == []


def test_search_invalid_keyword(sample_data):
    with pytest.raises(ValueError):
        search_data(sample_data, " ", ["name"])


def test_search_invalid_fields(sample_data):
    with pytest.raises(ValueError):
        search_data(sample_data, "Laptop", [])


# ==========================================
# TEST FILTER DATA
# ==========================================

def test_filter_data(sample_data):
    result = filter_data(
        sample_data,
        "category",
        "Electronics"
    )

    assert len(result) == 3


def test_filter_no_result(sample_data):
    result = filter_data(
        sample_data,
        "category",
        "Furniture"
    )

    assert result == []


def test_filter_missing_field(sample_data):
    result = filter_data(
        sample_data,
        "brand",
        "Apple"
    )

    assert result == []


# ==========================================
# TEST SORT DATA
# ==========================================

def test_sort_ascending(sample_data):
    result = sort_data(
        sample_data,
        "price"
    )

    assert result[0]["price"] == 50000
    assert result[-1]["price"] == 8000000


def test_sort_descending(sample_data):
    result = sort_data(
        sample_data,
        "price",
        reverse=True
    )

    assert result[0]["price"] == 8000000


def test_sort_missing_field(sample_data):
    with pytest.raises(ValueError):
        sort_data(sample_data, "brand")


def test_sort_inconsistent_type():
    data = [
        {"value": 100},
        {"value": "200"}
    ]

    with pytest.raises(TypeError):
        sort_data(data, "value")


def test_sort_invalid_reverse(sample_data):
    with pytest.raises(TypeError):
        sort_data(sample_data, "price", reverse="yes")


# ==========================================
# TEST GROUP DATA
# ==========================================

def test_group_data(sample_data):
    result = group_data(
        sample_data,
        "category"
    )

    assert len(result["Electronics"]) == 3
    assert len(result["Education"]) == 1


def test_group_missing_field(sample_data):
    with pytest.raises(ValueError):
        group_data(sample_data, "brand")


def test_group_unhashable_key():
    data = [
        {"category": ["Electronics"]}
    ]

    with pytest.raises(TypeError):
        group_data(data, "category")


# ==========================================
# TEST CALCULATE STATS
# ==========================================

def test_calculate_stats(sample_data):
    result = calculate_stats(
        sample_data,
        "price"
    )

    assert result["count"] == 4
    assert result["total"] == 8500000
    assert result["average"] == 2125000
    assert result["minimum"] == 50000
    assert result["maximum"] == 8000000


def test_calculate_stats_empty():
    result = calculate_stats([], "price")

    assert result["count"] == 0
    assert result["total"] == 0
    assert result["average"] == 0
    assert result["minimum"] is None
    assert result["maximum"] is None


def test_calculate_stats_ignore_invalid_values():
    data = [
        {"price": 100},
        {"price": None},
        {"price": "unknown"},
        {"price": 200}
    ]

    result = calculate_stats(data, "price")

    assert result["count"] == 2
    assert result["total"] == 300
    assert result["average"] == 150


def test_calculate_stats_ignore_boolean():
    data = [
        {"price": 100},
        {"price": True},
        {"price": False}
    ]

    result = calculate_stats(data, "price")

    assert result["count"] == 1
    assert result["total"] == 100


def test_calculate_stats_reject_infinity():
    data = [
        {"price": 100},
        {"price": float("inf")}
    ]

    with pytest.raises(ValueError):
        calculate_stats(data, "price")


# ==========================================
# TEST IMMUTABILITY
# ==========================================

def test_original_data_unchanged(sample_data):
    original = [item.copy() for item in sample_data]

    search_data(sample_data, "Laptop", ["name"])
    filter_data(sample_data, "category", "Electronics")
    sort_data(sample_data, "price")
    group_data(sample_data, "category")
    calculate_stats(sample_data, "price")

    assert sample_data == original

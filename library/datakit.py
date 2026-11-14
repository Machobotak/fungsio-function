
"""
DataKit - Reusable Data Processing Library

A collection of reusable functions for processing
list-based dictionary data.

Functions:
    search_data()
    filter_data()
    sort_data()
    group_data()
    calculate_stats()
"""

import math


# ==================================================
# INTERNAL VALIDATION
# ==================================================

def _validate_data(data):
    """Memvalidasi struktur data utama."""

    if not isinstance(data, list):
        raise TypeError("data harus berupa list.")

    if not all(isinstance(item, dict) for item in data):
        raise TypeError(
            "Setiap elemen data harus berupa dictionary."
        )


def _validate_field(field):
    """Memvalidasi nama field."""

    if not isinstance(field, str):
        raise TypeError("field harus berupa string.")

    if not field.strip():
        raise ValueError("field tidak boleh kosong.")


def _validate_fields(fields):
    """Memvalidasi kumpulan field."""

    if not isinstance(fields, (list, tuple)):
        raise TypeError("fields harus berupa list atau tuple.")

    if not fields:
        raise ValueError("fields tidak boleh kosong.")

    for field in fields:
        _validate_field(field)


# ==================================================
# 1. SEARCH DATA
# ==================================================

def search_data(data, keyword, fields):
    """
    Mencari data berdasarkan keyword pada field tertentu.

    Parameters:
        data (list): Kumpulan dictionary.
        keyword (str): Kata kunci pencarian.
        fields (list/tuple): Field yang diperiksa.

    Returns:
        list: Data yang cocok dengan keyword.

    Notes:
        - Pencarian tidak membedakan huruf besar/kecil.
        - Field yang tidak ditemukan akan dilewati.
        - Data asli tidak dimodifikasi.
    """

    _validate_data(data)
    _validate_fields(fields)

    if not isinstance(keyword, str):
        raise TypeError("keyword harus berupa string.")

    if not keyword.strip():
        raise ValueError("keyword tidak boleh kosong.")

    keyword = keyword.casefold()

    return [
        item for item in data
        if any(
            keyword in str(item[field]).casefold()
            for field in fields
            if field in item and item[field] is not None
        )
    ]


# ==================================================
# 2. FILTER DATA
# ==================================================

def filter_data(data, field, value):
    """
    Menyaring data berdasarkan kesamaan nilai field.

    Parameters:
        data (list): Kumpulan dictionary.
        field (str): Atribut yang diperiksa.
        value: Nilai yang dicari.

    Returns:
        list: Data yang memenuhi kondisi.

    Notes:
        - Menggunakan perbandingan equality (==).
        - Data tanpa field tersebut akan dilewati.
        - Data asli tidak dimodifikasi.
    """

    _validate_data(data)
    _validate_field(field)

    return [
        item for item in data
        if field in item and item[field] == value
    ]


# ==================================================
# 3. SORT DATA
# ==================================================

def sort_data(data, field, reverse=False):
    """
    Mengurutkan data berdasarkan field tertentu.

    Parameters:
        data (list): Kumpulan dictionary.
        field (str): Atribut pengurutan.
        reverse (bool): True untuk descending.

    Returns:
        list: Data yang sudah diurutkan.

    Raises:
        ValueError: Jika field tidak tersedia pada data.
        TypeError: Jika nilai tidak dapat dibandingkan.
    """

    _validate_data(data)
    _validate_field(field)

    if not isinstance(reverse, bool):
        raise TypeError("reverse harus berupa boolean.")

    if not data:
        return []

    if any(field not in item for item in data):
        raise ValueError(
            f"Field '{field}' harus tersedia pada semua data."
        )

    values = [item[field] for item in data]

    if any(value is None for value in values):
        raise ValueError(
            f"Field '{field}' tidak boleh mengandung None."
        )

    try:
        return sorted(
            data,
            key=lambda item: item[field],
            reverse=reverse
        )
    except TypeError as error:
        raise TypeError(
            f"Nilai pada field '{field}' tidak dapat "
            "diurutkan karena tipe datanya tidak konsisten."
        ) from error


# ==================================================
# 4. GROUP DATA
# ==================================================

def group_data(data, field):
    """
    Mengelompokkan data berdasarkan nilai field.

    Parameters:
        data (list): Kumpulan dictionary.
        field (str): Atribut pengelompokan.

    Returns:
        dict: Dictionary berisi kelompok data.

    Raises:
        ValueError: Jika field tidak tersedia.
        TypeError: Jika nilai field tidak dapat dijadikan key.
    """

    _validate_data(data)
    _validate_field(field)

    if any(field not in item for item in data):
        raise ValueError(
            f"Field '{field}' harus tersedia pada semua data."
        )

    groups = {}

    for item in data:
        key = item[field]

        try:
            hash(key)
        except TypeError as error:
            raise TypeError(
                f"Nilai pada field '{field}' harus hashable "
                "agar dapat digunakan sebagai group key."
            ) from error

        groups.setdefault(key, []).append(item)

    return groups


# ==================================================
# 5. CALCULATE STATS
# ==================================================

def calculate_stats(data, field):
    """
    Menghitung statistik dari field numerik.

    Parameters:
        data (list): Kumpulan dictionary.
        field (str): Field yang dihitung.

    Returns:
        dict: Count, total, average, minimum, maximum.

    Notes:
        - None dan nilai non-numerik akan dilewati.
        - Boolean tidak dianggap sebagai angka.
        - NaN dan infinity tidak diterima.
        - Jika tidak ada angka valid, statistik bernilai
          count=0, total=0, average=0, min/max=None.
    """

    _validate_data(data)
    _validate_field(field)

    values = [
        item[field]
        for item in data
        if field in item
        and isinstance(item[field], (int, float))
        and not isinstance(item[field], bool)
    ]

    if any(
        not math.isfinite(value)
        for value in values
    ):
        raise ValueError(
            f"Field '{field}' tidak boleh mengandung "
            "NaN atau infinity."
        )

    if not values:
        return {
            "count": 0,
            "total": 0,
            "average": 0,
            "minimum": None,
            "maximum": None
        }

    total = sum(values)

    return {
        "count": len(values),
        "total": total,
        "average": total / len(values),
        "minimum": min(values),
        "maximum": max(values)
    }

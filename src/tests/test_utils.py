import os

import pytest

from src.cmdb_exchange.utils import concatenate_path, get_file_by_name_pattern


def test_concatenate_path(tmpdir):
    expected = tmpdir.join('test_filename')
    actual = concatenate_path(tmpdir, 'test_filename')
    assert expected == actual


def test_concatenate_path_incorrect_dir():
    with pytest.raises(OSError) as error:
        concatenate_path('testdir', 'test_filename')
    exception_msg = error.value.args[0]
    assert exception_msg == "Given path testdir is not a directory"


def test_get_file_by_name_pattern(tmpdir):
    os.mknod(f'{tmpdir}/cmdb-sample-download.csv')
    actual = get_file_by_name_pattern(tmpdir, 'cmdb*.csv')
    expected = tmpdir.join('cmdb-sample-download.csv')
    assert actual == expected


def test_get_file_by_name_pattern_invalid_filename(tmpdir):
    with pytest.raises(OSError) as error:
        get_file_by_name_pattern(tmpdir, 'cmdb*.csv')
    exception_msg = error.value.args[0]
    assert exception_msg == "File not found"


def test_get_file_by_name_pattern_few_files(tmpdir):
    os.mknod(f'{tmpdir}/cmdb-sample-download.csv')
    os.mknod(f'{tmpdir}/cmdb-sample-download2.csv')
    with pytest.raises(OSError) as error:
        get_file_by_name_pattern(tmpdir, 'cmdb*.csv')
    exception_msg = error.value.args[0]
    assert exception_msg == "More than one file was found"

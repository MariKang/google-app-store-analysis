import pytest
from collect_appdata import get_app_info


# Define sets of test cases.

get_app_info_col_cases = [
    # Check a case with appropriate column name.
    ({'title', 'genre'}, {'title': 'Netflix', 'genre': 'Entertainment'}),
    # Test when the input column set is empty and check that the result is
    # an empty dictionary.
    ({}, {}),
    # Test when the name of the column in the column set is not the column
    # name of the information of application.
    ({'tt'}, {})
]

get_app_info_country_lang_cases = [
    # Check a basic case with country as US and language as English.
    ('en', 'us', {'title': 'Netflix', 'genre': 'Entertainment'}),
    # Test when the country and language is other than US and English
    # and see if it still works.
    ('de', 'de', {'genre': 'Unterhaltung', 'title': 'Netflix'}),
    # Test the case when the country code and language code is empty and
    # see if it returns English information.
    ('', '', {'title': 'Netflix', 'genre': 'Entertainment'})
]

get_app_info_id_cases = [
    # Test a case of ID that starts with 'com'.
    ('com.netflix.mediaclient', {'title': 'Netflix', 'genre': 'Entertainment'}),
    # Test a case of ID that doesn't start with 'com' to see if it works
    # for any IDs.
    ('no.mobitroll.kahoot.android', {'genre': 'Education', 'title':
     'Kahoot! Play & Create Quizzes'})
]

# Define standard testing functions to check functions' outputs given certain
# inputs defined above.


@pytest.mark.parametrize('column,result', get_app_info_col_cases)
def test_column(column, result):
    assert get_app_info('com.netflix.mediaclient', 'en', 'us', column) == result


@pytest.mark.parametrize('lang,country,result', get_app_info_country_lang_cases)
def test_lang_country(lang, country, result):
    assert get_app_info('com.netflix.mediaclient', lang, country,
                        {'title', 'genre'}) == result


@pytest.mark.parametrize('ids,result', get_app_info_id_cases)
def test_ids(ids, result):
    assert get_app_info(ids, 'en', 'us', {'title', 'genre'}) == result

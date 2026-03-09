def test_import_csv():
    from pathlib import Path
    from exam_seating.platzabfrage import _import_csv
    test_file = Path(__file__).parent / 'moodle_data.csv'
    df = _import_csv(str(test_file))
    assert not df.empty, "CSV file is empty"
    assert 'Vollständiger Name' in df.columns, "CSV file does not contain 'Vollständiger Name' column"
    assert 'Matrikelnummer' in df.columns, "CSV file does not contain 'Matrikelnummer' column"

def test_sorting():
    from exam_seating.platzabfrage import _sort_per_name
    import pandas as pd
    
    # Create a test DataFrame with German names
    data_german = {
        'Vollständiger Name': ['Osterzeit', 'Österreich', 'Österlich'],
        'Matrikelnummer': [123, 456, 789]
    }
    data_english = {
        'Vollständiger Name': ['Smith', 'Johnson', 'Williams'],
        'Matrikelnummer': [123, 456, 789]
    }

    data_german = pd.DataFrame(data_german)
    data_english = pd.DataFrame(data_english)

    # Sort the DataFrame using the _sort_per_name function
    _sort_per_name(data_german, german_locale=True)
    _sort_per_name(data_english)

    # Check if the sorting is correct according to German rules
    expected_order = ['Österlich', 'Österreich', 'Osterzeit']
    assert list(data_german['Vollständiger Name']) == expected_order, "Sorting did not follow German rules"

    # Check if the sorting is correct according to English rules
    expected_order = ['Johnson', 'Smith', 'Williams']
    assert list(data_english['Vollständiger Name']) == expected_order, "Sorting did not follow English rules"
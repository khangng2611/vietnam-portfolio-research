"""Boundary checks for provider parsing and the explicitly assumed three-day sensitivity."""
import unittest

import pandas as pd

from run_dragon_benchmark import normalize_history, reconstruct_three_sessions


class DragonBenchmarkTests(unittest.TestCase):
    def test_blank_source_row_is_not_filled(self):
        payload = {'returnValue': {'fundDates': ['2020-02-18', '2020-02-19', '2020-02-20'],
                                  'fundBenchmarkData': [
                                      {'navDate': '2020-02-18', 'navPrice': 100, 'navCurrency': 'VND'},
                                      {'navDate': '2020-02-19'},
                                      {'navDate': '2020-02-20', 'navPrice': 110, 'navCurrency': 'VND'}]}}
        result = normalize_history(payload)
        self.assertEqual(result.index_level.tolist(), [100, 110])
        self.assertNotIn(pd.Timestamp('2020-02-19'), result.index_date.tolist())

    def test_wrong_currency_and_duplicate_dates_fail(self):
        row = {'navDate': '2020-02-18', 'navPrice': 100, 'navCurrency': 'USD'}
        payload = {'returnValue': {'fundDates': ['2020-02-18'], 'fundBenchmarkData': [row]}}
        with self.assertRaisesRegex(ValueError, 'VND'):
            normalize_history(payload)
        row['navCurrency'] = 'VND'
        payload['returnValue']['fundDates'] *= 2
        payload['returnValue']['fundBenchmarkData'] *= 2
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            normalize_history(payload)

    def test_sensitivity_changes_only_three_interior_levels(self):
        dates = pd.to_datetime(['2025-04-29', '2025-05-05', '2025-05-06', '2025-05-07', '2025-05-08'])
        levels = pd.DataFrame({'index_date': dates, 'index_level': [100., 100., 100., 100., 110.]})
        prices = pd.DataFrame({'index_date': dates, 'index_level': [50., 51., 52., 53., 55.]})
        repaired, audit = reconstruct_three_sessions(levels, prices)
        self.assertEqual(repaired.index_level.tolist(), [100, 102, 104, 106, 110])
        self.assertEqual(len(audit), 3)
        changed_right = levels.copy()
        changed_right.loc[4, 'index_level'] = 111
        with self.assertRaisesRegex(ValueError, 'right-end'):
            reconstruct_three_sessions(changed_right, prices)
        changed_gap = levels.copy()
        changed_gap.loc[1, 'index_level'] = 101
        with self.assertRaisesRegex(ValueError, 'flat'):
            reconstruct_three_sessions(changed_gap, prices)


if __name__ == '__main__':
    unittest.main()

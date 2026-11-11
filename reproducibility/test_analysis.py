"""Hand-computable checks for phase drawdowns and linked wealth attribution."""
import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from reproduce import drawdown_episodes, attribution


class AnalysisTests(unittest.TestCase):
    def test_recovery_and_unrecovered_tail(self):
        dates = pd.bdate_range('2020-01-01', periods=6)
        events = drawdown_episodes(pd.Series([1, 1.1, .99, 1.05, 1.1, .88], index=dates))
        self.assertEqual(len(events), 2)
        self.assertAlmostEqual(events.iloc[0].depth, -.1)
        self.assertEqual(events.iloc[0].underwater_sessions, 2)
        self.assertEqual(events.iloc[0].recovery_date, dates[4])
        self.assertEqual(events.iloc[1].peak_date, dates[4])
        self.assertAlmostEqual(events.iloc[1].depth, -.2)
        self.assertTrue(pd.isna(events.iloc[1].recovery_date))
        self.assertEqual(events.iloc[1].status, 'unrecovered_right_censored')

    def test_anchor_is_in_running_peak(self):
        nav = pd.Series([1, .9, .8], index=pd.bdate_range('2020-01-01', periods=3))
        event = drawdown_episodes(nav).iloc[0]
        self.assertAlmostEqual(event.depth, -.2)
        self.assertEqual(event.peak_to_trough_sessions, 2)
        self.assertEqual(event.underwater_sessions, 2)

    def test_linked_wealth_is_additive(self):
        dates = pd.bdate_range('2020-01-01', periods=2)
        contributions = pd.DataFrame({'equities': [.1, 0], 'GOLD': [0, -.1], 'VFF': [0, 0]}, index=dates)
        linked, error = attribution(contributions, pd.Series([.1, -.1], index=dates))
        np.testing.assert_allclose(linked.sum(), [.1, -.11, 0])
        self.assertAlmostEqual(linked.to_numpy().sum(), -.01)
        self.assertEqual(error, 0)
        with self.assertRaises(ValueError):
            attribution(contributions, pd.Series([.1, .1], index=dates))

    def test_monotone_nav_has_no_episodes(self):
        nav = pd.Series([1, 1, 1.1], index=pd.bdate_range('2020-01-01', periods=3))
        self.assertTrue(drawdown_episodes(nav).empty)

class BenchmarkTests(unittest.TestCase):
    def test_missing_index_session_cannot_bridge(self):
        from benchmark import align_levels
        dates = pd.bdate_range('2020-01-01', periods=5)
        levels = pd.DataFrame({'index_date': dates[[0, 1, 3, 4]], 'index_level': [100, 110, 120, 132]})
        returns, _ = align_levels(levels, dates)
        self.assertTrue(pd.isna(returns.iloc[2]))
        self.assertTrue(pd.isna(returns.iloc[3]))
        self.assertAlmostEqual(returns.iloc[4], .1)

    def test_index_extra_session_is_not_one_portfolio_interval(self):
        from benchmark import align_levels
        dates = pd.bdate_range('2020-01-01', periods=5)
        levels = pd.DataFrame({'index_date': dates, 'index_level': np.arange(100, 105)})
        returns, _ = align_levels(levels, dates.delete(2))
        self.assertTrue(pd.isna(returns.loc[dates[3]]))


if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-

import unittest
import archive
from datetime import date


class Tests(unittest.TestCase):
    def test_parse_dates(self):
        year = date.today().year
        syear = str(year)

        expected = date(year, 1, 30)

        testcases = [
            syear + "-01-30",
            "30/01/" + syear,
            "30/01"
        ]

        for testcase in testcases:
            result = archive.get_date_from_string(testcase, allow_no_year=True)
            self.assertEqual(expected, result)

    def test_parse_difficult_dates(self):
        testcase = "hjghkjd 13012016 fshdfhkds"
        expected = date(2016, 1, 13)
        result = archive.get_date_from_string(testcase)
        self.assertEqual(expected, result)

        testcase = "19/04/2013 12 15"
        expected = date(2013, 4, 19)
        result = archive.get_date_from_string(testcase)
        self.assertEqual(expected, result)

        testcase = "Legge 30/11/1991 11.413-0.1.1. 30-3~1<192ﬁ0.izR.11-11-105 11.000  N _,"
        expected = date(1991, 11, 30)
        result = archive.get_date_from_string(testcase)
        self.assertEqual(expected, result)

        testcase = "ä Kvitteringnr. 254499 --1 01.07.2017 10320"
        expected = date(2017, 7, 1)
        result = archive.get_date_from_string(testcase)
        self.assertEqual(expected, result)

    def test_parse_non_date(self):
        # this ended getting parsed as $year-04-23 !!
        testcase = "ART. NR 30011832 22304"
        result = archive.get_date_from_string(testcase)
        self.assertEqual(None, result)

        # has been parsed as 2016-09-20...
        testcase = "N15310: 1424020092016 11:17 (Jrdre nr: 231555"
        result = archive.get_date_from_string(testcase)
        self.assertEqual(None, result)

    def test_parse_path_as_date(self):
        testcase = "/home/jostein/DocumentArchive/2012/01/28/hp photosmart 5510 5515 all in one printer ink/result.txt"
        expected = date(2012, 1, 28)
        result = archive.get_date_from_string(testcase)
        self.assertEqual(expected, result)

    def test_filter_past_dates(self):
        today = date(2016, 8, 1)
        tomorrow = date(2016, 8, 2)
        past_month = date(2016, 7, 15)
        past_past_month = date(2016, 6, 15)

        def is_past_month(date):
            results = archive.past_month([date], today=today)
            return len(results) == 1

        self.assertEqual(False, is_past_month(tomorrow))
        self.assertEqual(True,  is_past_month(past_month))
        self.assertEqual(False, is_past_month(past_past_month))

    def test_past_month_returns_list(self):
        today = date(2016, 8, 1)
        dates = [date(2016, 7, 15)]
        result = archive.past_month(dates, today=today)
        self.assertTrue(isinstance(result, list))


if __name__ == "__main__":
    unittest.main()

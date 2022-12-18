import unittest

import sciencemorningradio.arvix_reader.query as query

class TestURLBuilder(unittest.TestCase):
    def test_search_all_electron(self):
        expected = 'http://export.arxiv.org/api/query?search_query=all:electron'
        self.assertEqual(query.url_builder(search={'all':'electron'}),expected)
    def test_search_all_proton(self):
        expected = 'http://export.arxiv.org/api/query?search_query=all:proton'
        self.assertEqual(query.url_builder(search={'all':'electron'}),expected)
    def test_search_all_electron_with_max_number(self):
        expected = 'http://export.arxiv.org/api/query?search_query=all:electron&max_results=7'
        self.assertEqual(query.url_builder(search={'all':'electron'},max_results=7),expected)

    def test_search_all_electron_with_starting_offset(self):
        expected = 'http://export.arxiv.org/api/query?search_query=all:electron&start=3'
        self.assertEqual(query.url_builder(search={'all':'electron'},start=3),expected)


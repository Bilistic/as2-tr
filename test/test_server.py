from server.Server import DataAnalysis
import pytest

"""
tests sentiment analysis on server.
"""
def test_sentiment():
    obj = {'length': 80, 'method': 'reddit',
           'text': 'I m A Democrat And The Left s Russia Gaslighting Scares Me More Than Trump Does'}
    ans = DataAnalysis().analyze_sentiment(obj)
    assert float(ans['sentiment']) == 0.25


"""
tests cleaning text on server.
"""
def test_twitter():
    sentence = "[Dirty-] sentence that (/needs/) {cleaning}"
    ans = DataAnalysis().clean(sentence)
    assert ans == "Dirty sentence that needs cleaning"
    

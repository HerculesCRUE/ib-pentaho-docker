import unittest

import pandas as pd
from fairviz import get_level

'''
------------------------------TEST1------------------------------
FINDABLE -> ningÃºn esencial -> 0
ACCESSIBLE -> tiene todos los importantes y Ãºtiles, pero ningÃºn esencial -> 0
INTEROPERABLE -> tiene  menos del 50 % de los importantes y todos los Ãºtiles -> 1
REUSABLE -> tiene todos los esenciales y todos los Ãºtiles, pero menos de la mitad de los importantes -> 1

------------------------------TEST2------------------------------
FINDABLE -> todos los esenciales -> 5
ACCESSIBLE -> tiene todos los esenciales, mÃ¡s de la mitad de los importantes y ningÃºn Ãºtil -> 2
INTEROPERABLE -> tiene  todos los importantes y ningÃºn Ãºtil -> 3
REUSABLE -> tiene todos los esenciales, todos los importantes y ningÃºn Ãºtil -> 3

------------------------------TEST3------------------------------
FINDABLE -> ningÃºn esencial -> 0
ACCESSIBLE -> tiene todos los esenciales, todos los importantes y ningÃºn Ãºtil -> 3
INTEROPERABLE -> tiene todos los importantes y mÃ¡s de la mitad de Ãºtiles -> 4
REUSABLE -> tiene todos los esenciales, todos los importantes y todos los Ãºtiles -> 5

------------------------------TEST4------------------------------
FINDABLE -> todos los esenciales -> 5
ACCESSIBLE -> tiene todos los esenciales, todos los importantes y todos los Ãºtiles -> 5
INTEROPERABLE -> tiene todos los importantes y todos los Ãºtiles -> 5
REUSABLE -> tiene todos los esenciales, todos los importantes y todos los Ãºtiles -> 5

'''

class Test(unittest.TestCase):
    def test1(self):
        df = pd.read_csv('./test/test1.csv')
        self.assertEqual(get_level(df,'FINDABLE'),0)
        self.assertEqual(get_level(df,'ACCESSIBLE'),0)
        self.assertEqual(get_level(df, 'INTEROPERABLE'), 1)
        self.assertEqual(get_level(df, 'REUSABLE'), 1)

    def test2(self):
        df = pd.read_csv('./test/test2.csv')
        self.assertEqual(get_level(df,'FINDABLE'),5)
        self.assertEqual(get_level(df,'ACCESSIBLE'),2)
        self.assertEqual(get_level(df, 'INTEROPERABLE'), 3)
        self.assertEqual(get_level(df, 'REUSABLE'), 3)

    def test3(self):
        df = pd.read_csv('./test/test3.csv')
        self.assertEqual(get_level(df,'FINDABLE'),0)
        self.assertEqual(get_level(df,'ACCESSIBLE'),3)
        self.assertEqual(get_level(df, 'INTEROPERABLE'), 4)
        self.assertEqual(get_level(df, 'REUSABLE'), 5)

    def test4(self):
        df = pd.read_csv('./test/test4.csv')
        self.assertEqual(get_level(df,'FINDABLE'),5)
        self.assertEqual(get_level(df,'ACCESSIBLE'),5)
        self.assertEqual(get_level(df, 'INTEROPERABLE'), 5)
        self.assertEqual(get_level(df, 'REUSABLE'), 5)

if __name__ == "__main__":
        unittest.main()

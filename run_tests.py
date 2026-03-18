import sys
import unittest
import os
sys.path.insert(0, os.path.abspath('.'))

if __name__ == '__main__':
    with open('out.txt', 'w', encoding='utf-8') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        suite = unittest.TestLoader().discover('tests')
        runner.run(suite)

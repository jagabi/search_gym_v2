"""Offline suite against working code or committed baseline, without changing files."""
import argparse
from pathlib import Path
import subprocess
import sys
import types
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'tests'))
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--baseline',action='store_true')
args=p.parse_args()
if args.baseline:
    source=subprocess.run(['git','show','HEAD:searchgym/rawtree.py'],cwd=ROOT,
                          capture_output=True,check=True,encoding='utf-8').stdout
    import searchgym
    module=types.ModuleType('searchgym.rawtree')
    module.__file__=str(ROOT/'searchgym/rawtree.py')
    module.__package__='searchgym'
    sys.modules['searchgym.rawtree']=module
    searchgym.rawtree=module
    exec(compile(source,module.__file__,'exec'),module.__dict__)
suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_rawtree*.py')
result=unittest.TextTestRunner(verbosity=1).run(suite)
sys.exit(not result.wasSuccessful())

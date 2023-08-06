# Usage:
# python -c "from nembis.test.main import *; unittest.main()"
#

import unittest

from nembis.test.unit.test_version import *
from nembis.test.ed.ed import *


if __name__ == "__main__":
    unittest.main(verbosity=1)



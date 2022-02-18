#!/usr/bin/env python3

from pixely.operator import Operator
from pixely.applications.strange import DoctorStrangeCostume


c = DoctorStrangeCostume()
o = Operator(c)
o.run()

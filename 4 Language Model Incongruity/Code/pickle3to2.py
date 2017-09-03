#!/usr/bin/env python3

import pickle
import sys
with open(sys.argv[1], "rb") as f:
    w = pickle.load(f)

pickle.dump(w, open(sys.argv[1]+'.ver2',"wb"), protocol=2)

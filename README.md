# TamperCheck


This is **NOT PRODUCTION READY**. Do not use this in production.


## What?

- Digitally signing documents is the way to go!
- But it requires that you have secure connectivity of some sort at some point
  since you need the other person's public key at the very least to verify that
  they indeed wrote what you have received
- Can we instead have documents that verify that they have not been tampered with?
- What if we relax the requirement of source verification and we don't care about MitM attacks?

## Use

Here's an example using `tampercheck.py` to freeze and make it's own code tamperproof.

```bash
~.tc 17:50 🌀 python3 tampercheck.py -f tampercheck.py
Generating signature
# tampercheck:3f8f7
~.tc 17:50 🌀 python3 tampercheck.py  tampercheck.py
File has :3f8f7
Md5sum is:3f8f7d057b27b1b5a4bef6379c55df80
~.tc 17:50 🌀 md5sum tampercheck.py 
3f8f7d057b27b1b5a4bef6379c55df80  tampercheck.py
~.tc 17:51 🌀 head tampercheck.py 
# tampercheck:3f8f7
import random
import string
import hashlib
import argparse
from itertools import repeat
from multiprocessing import Pool, cpu_count

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Code file")
~.tc 17:51 🌀 
```

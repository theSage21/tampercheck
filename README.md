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

```bash
python tampercheck.py mytext.txt
python tampercheck.py --freeze mytext.txt  # will take some time
```

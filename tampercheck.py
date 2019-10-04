import random
import string
import hashlib
import argparse
from itertools import repeat
from multiprocessing import Pool, cpu_count

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Code file")
parser.add_argument(
    "-f",
    "--freeze",
    help="Edit the file's header to contain a signature",
    default=False,
    action="store_true",
)
parser.add_argument(
    "--header", help="Header Prefix", default="# tampercheck:", type=str
)
parser.add_argument(
    "-s", "--size", help="How many chars in hexdigest?", default=5, type=int
)
args = parser.parse_args()


def generate(code):
    while True:
        sig = "".join(random.choice(string.hexdigits) for _ in repeat(None, args.size))
        data = (f"{args.header}{sig}" + "\n").encode() + code
        predicted = hashlib.md5(data).hexdigest()
        if predicted.startswith(sig):
            return sig, data.decode()


with open(args.file, "r") as fl:
    code = fl.readlines()
data = "".join(code).encode()
if not code[0].startswith(args.header) and not args.freeze:
    raise Exception(f"File does not contain header '{args.header}'")
if not args.freeze:
    sig = code[0][code[0].index(args.header) + len(args.header) :].strip()
    print(f"File has :{sig}")
    hsh = hashlib.md5(data).hexdigest()
    print(f"Md5sum is:{hsh}")
    if not hsh.startswith(sig):
        raise Exception("Headers mismatch")
else:
    print("Generating signature")
    code = "".join(code[1:]) if code[0].startswith(args.header) else "".join(code)
    with Pool() as pool:
        work = pool.imap_unordered(
            generate, [code.encode() for index in range(cpu_count())]
        )
        for sig, string in work:
            with open(args.file, "w") as fl:
                fl.write(string)
            break
    print(f"{args.header}{sig}")

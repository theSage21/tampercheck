import random
import hashlib
import argparse
from itertools import repeat
import string
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
args = parser.parse_args()
found = False


def generate(code):
    global found, pbar
    while not found:
        # 32 comes from length of hex digest
        sig = "".join(random.choice(string.hexdigits) for _ in repeat(None, 32))
        data = f"""{args.header}{sig}
{code}""".encode()
        predicted = hashlib.md5(data).hexdigest()
        if predicted == sig:
            found = True
            return sig, data.decode()


with open(args.file, "r") as fl:
    code = fl.readlines()
data = "".join(code).encode()
if not code[0].startswith(args.header) and not args.freeze:
    raise Exception(f"File does not contain header '{args.header}'")
if not args.freeze:
    sig = code[0][code[0].index(args.header) + len(args.header) :]
    if hashlib.md5(data).hexdigest() != sig:
        raise Exception("Headers mismatch")
else:
    print("Generating signature")
    code = "".join(code[1:]) if code[0].startswith(args.header) else "".join(code)
    with Pool() as pool:
        work = pool.imap_unordered(generate, [code for _ in range(cpu_count())])
        for sig, string in work:
            with open(args.file, "w") as fl:
                fl.write(string)
    print(f"{args.header}{sig}")
    print("Done!")

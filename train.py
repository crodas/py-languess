import languess
import os
from glob import glob

def main():
    for file in glob("samples/*.sam"):
        name = os.path.basename(file).split(".")
        languess.train(file, "knowledge/%s.lm" % name[0], name[1] == "utf8")

if __name__ == "__main__":
    main()

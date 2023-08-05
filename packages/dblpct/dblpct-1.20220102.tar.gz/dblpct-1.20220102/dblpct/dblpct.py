import sys


def main():
    if len(sys.argv) == 1:
        exit(1)
    else:
        target = sys.argv[1]
        ret = ""
        for x in target:
            if x == "%":
                ret += "%%"
            else:
                ret += x

    print(ret)
    exit(0)


if __name__ == "__main__":
    main()

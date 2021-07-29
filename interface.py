from calc_parser import calculate


def main():
    while True:
        txt = input(">>")
        print(calculate(txt))

if __name__ == "__main__":
    main()
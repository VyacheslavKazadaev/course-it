def main():
    t1 = 1
    print(f"{t1 = } - int")
    t2 = 1.5
    print(f"{t2 = } - float")
    t3 = True
    print(f"{t3 = } - bool")
    t4 = "строка"
    print(f"{t4 = } - str")

    if isinstance(t1, int):
        print("t1 is integer")
    elif isinstance(t1, str):
        print("t1 is string")    


if __name__ == "__main__":
    main()
# end main
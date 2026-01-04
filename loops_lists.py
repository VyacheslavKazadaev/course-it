def main():
    # Циклы
    # Цикл for
    for i in range(5):
        print(f"Итерация {i}")

    # Цикл while
    count = 0
    while count < 3:
        print(f"Счетчик: {count}")
        count += 1        

    # Списки (Lists)
    numbers = [1, 2, 3, 4, 5]
    names = ["Анна", "Борис", "Виктор"]
    print(f"{numbers = }")

    # Доступ к элементам
    first_number = numbers[0]  # 1
    last_name = names[-1]       # "Виктор"
    print(f"{first_number = } {last_name = }")

    # Основные методы списков
    numbers.append(6)           # добавить в конец
    numbers.insert(0, 0)        # вставить в начало
    numbers.pop()               # удалить последний элемент
    print(f"{numbers = }")

if __name__ == "__main__":
    main()    
# end main
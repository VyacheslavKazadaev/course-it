# Словари (Dictionaries)
person = {
    'name': 'Анна',
    'age': 25,
    'city': 'Москва'
}

# Доступ к значениям
name = person['name']  # 'Анна'
age = person.get('age')  # 25

# Добавление/изменение элементов
person['email'] = 'anna@example.com'
person['age'] = 26

# Итерация по словарю
for key, value in person.items():
    print(f"{key}: {value}")

# Строковые методы
text = "привет мир"
print(text.upper())      # "ПРИВЕТ МИР"
print(text.capitalize()) # "Привет мир"
print(text.split())      # ["привет", "мир"]
print(len(text))         # 11

# Форматирование строк
name = "Мария"
age = 30
print(f"Меня зовут {name}, мне {age} лет")
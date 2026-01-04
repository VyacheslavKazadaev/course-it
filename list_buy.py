# shopping_list.py
def shopping_list_manager():
    """
    Менеджер списка покупок с возможностью добавления,
    удаления и просмотра товаров
    """
    shopping_list = []
    
    print("=== Менеджер списка покупок ===")
    print("Команды:")
    print("1. Добавить товар")
    print("2. Удалить товар")
    print("3. Показать список")
    print("4. Показать количество товаров")
    print("5. Очистить список")
    print("0. Выход")
    
    while True:
        try:
            command = input("\nВведите команду (0-5): ")
            
            if command == '0':
                print("До свидания!")
                break
                
            elif command == '1':
                item = input("Введите название товара: ").strip()
                if item:
                    shopping_list.append(item)
                    print(f"✅ Товар '{item}' добавлен в список")
                else:
                    print("❌ Название товара не может быть пустым")
                
            elif command == '2':
                if not shopping_list:
                    print("❌ Список пуст")
                    continue
                
                print("\nТекущий список:")
                for i, item in enumerate(shopping_list, 1):
                    print(f"{i}. {item}")
                
                try:
                    index = int(input("Введите номер товара для удаления: ")) - 1
                    if 0 <= index < len(shopping_list):
                        removed_item = shopping_list.pop(index)
                        print(f"✅ Товар '{removed_item}' удален из списка")
                    else:
                        print("❌ Неверный номер товара")
                except ValueError:
                    print("❌ Введите корректный номер")
                
            elif command == '3':
                if shopping_list:
                    print("\n📋 Список покупок:")
                    for i, item in enumerate(shopping_list, 1):
                        print(f"{i}. {item}")
                else:
                    print("❌ Список пуст")
                
            elif command == '4':
                print(f"\nКоличество товаров в списке: {len(shopping_list)}")
                
            elif command == '5':
                shopping_list.clear()
                print("✅ Список очищен")
                
            else:
                print("❌ Неверная команда. Попробуйте еще раз")
        
        except KeyboardInterrupt:
            print("\n\nПрограмма завершена")
            break
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")

# Запуск менеджера
if __name__ == "__main__":
    shopping_list_manager()
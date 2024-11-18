import json


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Flowers:
    def __init__(self):
        self.flower_data = {
            "Роза": 100,
            "Лилия": 80,
            "Тюльпан": 50,
            "Гербера": 40,
            "Фиалки": 110
        }

    def get_flowers(self):
        return self.flower_data

    def calculate_price(self, selected_flowers):
        price = 0
        for flower, count in selected_flowers.items():
            price += self.flower_data[flower] * count
        return price


class Users:
    def __init__(self):
        self.users_data = self.load_users()

    def load_users(self):
        try:
            with open("users.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open("users.json", "w") as f:
            json.dump(self.users_data, f)

    @staticmethod
    def register_user(shop):
        username = input("Введите имя пользователя: ")
        while True:
            password = input("Введите пароль: ")
            confirm_password = input("Повторите пароль: ")
            if password == confirm_password:
                break
            else:
                print("Пароли не совпадают. Попробуйте снова.")

        if username in shop.users.users_data:
            print("Пользователь с таким именем уже существует.")
            return None
        else:
            user = User(username, password)
            shop.users.users_data[username] = user.__dict__
            shop.users.save_users()
            print("Регистрация прошла успешно!")
            return username

    @staticmethod
    def login_user(shop):
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")

        if username in shop.users.users_data:
            if shop.users.users_data[username]["password"] == password:
                print("Вход выполнен успешно!")
                return username
            else:
                print("Неверный пароль.")
        else:
            print("Пользователь не найден.")
        return None


class FlowerShop:
    def __init__(self):
        self.flowers = Flowers()
        self.users = Users()

    def apply_discount(self, price, is_registered):
        if is_registered:
            return price * 0.95
        else:
            return price

    def buy_flowers(self, current_user):
        selected_flowers = {}
        while True:
            print("Выберите цветы:")
            for flower, price in self.flowers.get_flowers().items():
                print(f"- {flower} ({price} руб.)")
            print("Введите 'Готово', чтобы завершить выбор.")

            flower_name = input("Введите название цветка: ")
            if flower_name == "Готово":
                break
            elif flower_name in self.flowers.get_flowers():
                while True:
                    try:
                        count = int(input(f"Сколько {flower_name} добавить? "))
                        if count > 0:
                            selected_flowers[flower_name] = count
                            break
                        else:
                            print("Количество должно быть больше 0.")
                    except ValueError:
                        print("Введите целое число.")
            else:
                print("Неправильное название цветка. Попробуйте снова.")

        while True:
            print("Хотите ли убрать какие-нибудь цветы из букета? (да/нет)")
            remove_choice = input("Введите ваш выбор: ").lower()
            if remove_choice in ("да", "нет"):
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
        if remove_choice == "да":
            while True:
                print("Выберите цветок, который хотите убрать (или 'Готово', чтобы завершить):")
                for flower in selected_flowers:
                    print(f"- {flower}")
                print("Введите 'Готово', чтобы завершить выбор.")
                remove_flower = input("Введите название цветка: ")
                if remove_flower == "Готово":
                    break
                elif remove_flower in selected_flowers:
                    del selected_flowers[remove_flower]
                    print(f"{remove_flower} был удален из вашего букета.")
                else:
                    print("Неправильное название цветка. Попробуйте снова.")
        price = self.flowers.calculate_price(selected_flowers)
        discount_price = self.apply_discount(price, current_user in self.users.users_data)
        print(f"Стоимость цветов: {price} руб.")
        if discount_price < price:
            print(f"Скидка для зарегистрированных пользователей: {discount_price} руб.")


def main():
    shop = FlowerShop()

    while True:
        action = input("Введите 'р' для регистрации, 'в' для входа или 'выйти' для выхода: ").lower()
        if action == 'р':
            Users.register_user(shop)
        elif action == 'в':
            username = Users.login_user(shop)
            if username:
                shop.buy_flowers(username)
        elif action == 'выйти':
            print("Спасибо за использование магазина!")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
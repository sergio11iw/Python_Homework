class Shop:
    Products = {'Молоко': 50, 'Колбаса': 120, 'Яица': 100}
    Discount = ['Молоко', 'Яица']
    def __init__(self):
        self.count = 0
        self.all_sum = 0
    def buy(self, product):
        if product in self.Products:
            self.all_sum += self.Products[product]
            self.count += 1
            self._check_discount(product)
            print('Купил продукт')
        else:
            print('Продукта нет')
    def add_product(self, product, price):
        self.Products[product] = price
        print('Обновили базу')
    def get_info(self):
        print(f'Всего купили на {self.all_sum}р')
        print(f'Всего чеков {self.count}')
    def _check_discount(self, product):
        if product in self.Discount:
            self.all_sum -= 5
    def delete_product(self, product):
        if product in self.Products:
            del self.Products[product]
            print('Удалил продукт')
            print('Обновили базу')
        else:
            print('Нет продукта в базе')


shop = Shop()
shop.buy('Молоко')
shop.buy('Яица')
shop.buy('Хрен')
shop.add_product('Хрен', 60)
shop.buy('Хрен')
shop.get_info()
shop.delete_product('Хрен')
shop.buy('Хрен')
shop.delete_product('Хрен')
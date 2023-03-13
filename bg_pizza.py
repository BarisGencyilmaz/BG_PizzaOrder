import csv
import datetime
import pandas as pd 
from getpass import getpass
import os.path

# 1 : Pizza üst sınıfının oluşturulması
class Pizza:
    def get_description(self): 
        return self.__class__.__name__
        

    def get_cost(self): 
        return self.__class__.cost

# 2 : Pizza üst sınıfından alt sınıfı olarak pizza türlerine ait sınıflar oluşturulması
class Klasik(Pizza):
    
    cost = 80.0
    def __init__(self):
        self.description = "Klasik pizza: Pizza sosu, mozzarella peyniri, dilimlenmiş sosis, taze mantar, siyah zeytin, taze dilimlenmiş yeşil ve kırmızı biber!"
        print(self.description +"\n")

class Margarita(Pizza):
    
    cost = 65.0
    def __init__(self):
        self.description = "Margarita pizza: Pizza sosu, mozzarella peyniri, taze dilimlenmiş kırmızı ve yeşil biber, taze doğranmış mantar, küp kesilmiş taze domates, mısır, zeytin, beyaz küp peynir ve kekik!"
        print(self.description +"\n")

class TurkPizza(Pizza):
    
    cost = 70.0
    def __init__(self):
        self.description = "TürkPizza: Pizza sosu, mozarella, pepperoni, kekik!"
        print(self.description +"\n")

class SadePizza(Pizza):
    
    cost = 45.0
    def __init__(self):
        self.description = "Sade pizza: Pizza sosu, mozzarella peyniri, sucuk!"
        print(self.description + "\n" )

# 3 : Ekstra ürünler için "decorator" üst sınıfının oluşturulması
class Extras(Pizza):
    
    def __init__(self, added):
        self.component = added

    def get_cost(self):
        return self.component.get_cost() + \
          Pizza.get_cost(self)

    def get_description(self):
        return self.component.get_description() + \
          ' ;' + Pizza.get_description(self)

# 4 : Ekstra ürünlerin kendi özellik ve değerlerini içeren "decorator" alt sınıfın oluşturulması 
class Zeytin(Extras):
    
    cost = 2.0
    def __init__(self, added):
        Extras.__init__(self, added)


class Mantar(Extras):
    
    cost = 3.0
    def __init__(self, added):
        Extras.__init__(self, added)


class Peynir(Extras):
    
    cost = 4.0
    def __init__(self, added):
        Extras.__init__(self, added)


class Et(Extras):
    
    cost = 10.0
    def __init__(self, added):
        Extras.__init__(self, added)


class Sogan(Extras):
    
    cost = 5.0
    def __init__(self, added):
        Extras.__init__(self, added)


class Misir(Extras):
    
    cost = 5.0
    def __init__(self, added):
        Extras.__init__(self, added)

# 5 : Seçim işlemlerinin yapılacağı ekran için main() fonksiyonunun oluşturulması

def main():
    
    with open("Menu.txt", encoding = "utf-8") as pizzaMenu:
        for i in pizzaMenu:
            print(i, end="")

    menuClass = {1: Klasik, 
                  2: Margarita, 
                  3: TurkPizza, 
                  4: SadePizza, 
                  11: Zeytin, 
                  12: Mantar, 
                  13: Peynir, 
                  14: Et, 
                  15: Sogan, 
                  16: Misir}

    selection = input("Seçtiğiniz pizzanın numarasını girip Enter'a basın: ")
    while selection not in ["1", "2", "3", "4"]:
        selection = input("Bu 4 lezzetli pizzadan birini seçtiğinizden emin olun ve tekrar girin: ")

    pizzaOrder = menuClass[int(selection)]()

    while selection != "*":
        selection = input("İsteğe bağlı ekstra ürün için numarasını girin veya siparişi tamamlamak için '*' girip Enter'a basın : ")
        if selection in ['11', '12', '13', '14', '15', '16']:
            pizzaOrder = menuClass[int(selection)](pizzaOrder)
    print("\n -------------------------------------------- \n")
    print(pizzaOrder.get_description() +
          " ; " + "\n" + " TL(₺) : " + str(pizzaOrder.get_cost()) + "\n")
    

    print("________  Sipariş Bilgileri  ________\n")
    orderer = input("Müşteri Adı Soyadı: ")
    ID = input("Kimlik No: ")
    creditCard = input("Kredi Kartı Numarası: ")
#şifre bilgisini ekranda görünmeyecek şekilde alıyorum
    Password = getpass("Şifre: ")
    orderTime = datetime.datetime.now()


#Müşteri bilgilerini dataframe oluşturarak almayı tercih ettim, colab'de çok daha güzel göründü.

    orderInfo = [{'Müşteri Ad Soyad': orderer,
                    'Kimlik No' : ID,
                    'Kredi Kartı No' : creditCard,
                    'Seçilen Pizza' : pizzaOrder.get_description(),
                    'Sipariş zamanı' : orderTime,
                    'Şifre' : Password}]
    
#Burada sipariş notunu ekrana yazdırıken "müşteri ismi, pizza seçimi, sipariş tutarı ve işlem saati" yer alıyor, diğer bilgiler database'e gidiyor.
    
    print(f"----- Talebiniz alındı. İşlem bilgileri: ----- \n İsminiz: {orderer} \n Seçiminiz: {pizzaOrder.get_description()} \n Sipariş Tutarı: {pizzaOrder.get_cost()} \n Talep zamanı: {orderTime}")

    df1 = pd.DataFrame(orderInfo)

#Bu kısımda daha önce oluşturulmuş bir veritabanı dosyası olup olmadığını kontrol ediyor ve duruma göre dosyayı oluşturuyor ya da güncelliyoruz.

    database_check = os.path.exists("Orders_Database.csv")
    if database_check == False:
        with open('Orders_Database.csv', 'a') as file:
            df1.to_csv(file, index=False, header=True)
    else:
        with open('Orders_Database.csv', 'a') as file:
            df1.to_csv(file, index=False, header=False)
    
    
    
main()    
    











import random
import sqlite3


class CardAnatomy:
    keys = {}
    def __init__(self):
        self.cardnum = None
        self.code = None
        self.gen = None
        self.button = None
        self.logcard = None
        self.logbalance = None
        self.logpassword = None
        self.cardluhn = None
        self.conn = None
        self.c = None
        self.income = None
        self.cardpasschecker = None
        self.sendamount = None
        self.sendto = None

    def db_2_intialize(self):
        self.conn = sqlite3.connect('card.s3db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number text, pin text, balance INTEGER DEFAULT 0)")


    def menu(self):
        print('1. Create an account\n2. Log into account\n0. Exit')
        self.button = int(input())
        if self.button == 1:
            self.code_genetaration()
            self.menu()
        elif self.button == 0:
            print('Bye!')
        elif self.button == 2:
            print('Enter your card number:')
            self.logcard = input()
            print('Enter your PIN:')
            self.logpassword = input()
            self.c.execute("SELECT number, pin from card where number = ?", (self.logcard,))
            self.cardpasschecker = self.c.fetchone()
            ''''if self.logcard not in self.c.execute('SELECT number FROM card').fetchone():
                print('Such a card does not exist.')'''''
            # self.cardpasschecker, self.passchecker = self.c.fetchone()[0], self.c.fetchone()[1]
            if self.cardpasschecker is not None:
                if self.cardpasschecker[0] == self.logcard and self.cardpasschecker[1] == self.logpassword:
                    print('You have successfully logged in!')
                    self.login()
                else:
                    print('Wrong card number or PIN!')
                    self.menu()
            else:
                print('Wrong card number or PIN!')
                self.menu()
        else:
            self.menu()

    def code_genetaration(self):
        random.seed()
        gen = random.randint(1000000000, 9999999999)
        self.cardnum = '400000' + str(gen)
        self.cardluhn = [int(x) * 2 if i % 2 else int(x) for i, x in enumerate(self.cardnum[:-1], 1)]
        self.cardluhn = [(x - 9) if x > 9 else x for x in self.cardluhn]
        if (sum(self.cardluhn) + int(self.cardnum[-1])) % 10 == 0:
            self.code = random.randint(1000, 9999)
            self.keys.update({int(self.cardnum): str(self.code)})
            self.c.execute("INSERT INTO card (number, pin) VALUES(?,?)", (str(self.cardnum), self.code))
            self.conn.commit()
            print("Your card has been created.\nYour card number:\n{}\nYour card PIN:\n{}".format(self.cardnum, self.code))
        else:
            self.code_genetaration()

    def login(self):
                print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
                self.logbalance = int(input())
                if self.logbalance == 1:
                    self.c.execute("SELECT balance from card where number = ?", (self.logcard,))
                    print('Balance:', self.c.fetchone()[0])
                    self.login()
                elif self.logbalance == 2:
                    self.add_income()
                    self.login()
                elif self.logbalance == 3:
                    self.transfer()
                elif self.logbalance == 4:
                    self.c.execute("DELETE FROM card WHERE number = ?", (self.logcard,))
                    self.conn.commit()
                    print('The account has been closed!')
                    self.menu()
                elif self.logbalance == 5:
                    self.menu()
                elif self.logbalance == 0:
                    print('Bye!')
                else:
                    self.login()

    def add_income(self):
        try:
            self.income = int(input('Enter income:'))
            self.c.execute('UPDATE card SET balance = balance + ? where number = ?', (self.income, self.logcard))
            self.conn.commit()
            print('Income was added!')
        except ValueError:
            self.add_income()

    def transfer(self):
        try:
            print('Transfer')
            self.sendto = input('Enter card number:')
            self.cardluhn = [int(x) * 2 if i % 2 else int(x) for i, x in enumerate(self.sendto[:-1], 1)]
            self.cardluhn = [(x - 9) if x > 9 else x for x in self.cardluhn]
            if (sum(self.cardluhn) + int(self.sendto[-1])) % 10 == 0:
                self.c.execute("SELECT * from card where number = ?", (self.sendto,))
                self.sendtoquery = self.c.fetchone()
                if self.sendtoquery is not None:
                    if self.sendto != self.logcard:
                        self.sendamount = int(input('Enter how much money you want to transfer:'))
                        self.c.execute("SELECT number, balance from card where number = ?", (self.logcard,))
                        self.senderbalance = self.c.fetchone()
                        if self.senderbalance[1] >= self.sendamount:
                            self.c.execute('UPDATE card SET balance = balance + ? where number = ?', (self.sendamount, self.sendtoquery[1]))
                            self.c.execute('UPDATE card SET balance = balance - ? where number = ?', (self.sendamount, self.senderbalance[0]))
                            self.conn.commit()
                            print('Success!')
                            self.login()
                        else:
                            print('Not enough money!')
                            self.login()
                    else:
                        print("You can't transfer money to the same account!")
                        self.login()
                else:
                    print('Such a card does not exist.')
                    self.login()
            else:
                print('Probably you made a mistake in the card number. Please try again!')
                self.login()
        except ValueError:
            self.login()


a = CardAnatomy()
a.db_2_intialize()
a.menu()
# c.execute("SELECT * from card")
# print(c.fetchall())

import random
class EventCard:
    def __init__(self, title, descricao, evento1=None, evento2=None, evento3=None, evento4=None, evento5=None, evento6=None) -> None:
        self.title = title
        self.descricao = descricao
        self.evento1 = evento1
        self.evento2 = evento2
        self.evento3 = evento3
        self.evento4 = evento4
        self.evento5 = evento5
        self.evento6 = evento6
    def dado(self):
        result = random.randint(1, 6)
        print(f"O resultado do dado é {result}")
        if result == 6:
            return print('As forças monarquistas evitaram que o evento acontecesse')
        if result  == 1 or result == 2:            
            print(f"{self.nome} deu tão certo que você ainda deve retirar uma força monarquista de um local à sua escolha")
            a = input('Você deseja retirar forças da região:' )
            a.tira_rep(1)
            return 


        if result == 3 or result == 4 or result == 5:
            print(f"O evento acontece e as forças republicanas ganham mais potência")


class Regiao:
    def __init__(self, nome, espacos) -> None:
        self.nome = nome
        self.espacos = espacos    
        self.total = []
        for i in range(1, self.espacos+1):
            self.total.append(0)
    @property
    def nome(self):
        return self.nome
    def add_mon(self, a):
        if a == 0:
            print('Não é possível adicionar zero forças')
            return
        if a > len(self.total): #eliminar chances de ser maior ou menor que o total de espaços
            print('Não há tantos espaços vazios')
            return
        check = False
        if self.total.count('m') == len(self.total):
            print('Todas as forças já são da monarquia') #checar se todas as forças já são da monarquia         
        if self.total.count(0) >= a: #checar se tem mais espaços vazios que mudanças
            check = True
        if check: #fazer as mudanças
            loop = a
            while loop > 0:
                self.total.pop(0)
                self.total.append('m')
                loop-=1
            return            
        if not check: #caso sejam mais mudanças que espaços vazios
            for i in range(len(self.total)): #primeiro preenche os vazios disponíveis
                if self.total[i] == 0:
                    self.total[i] = 'm'
                    a-=1            
            for i in range(len(self.total)): #depois começa a inverter as forças
                if self.total[i] == 'r':
                    self.total[i] = 'm'
                    a-=1
                    if a == 0:
                        return
    def add_rep(self, a):
        if a == 0:
            print('Não é possível adicionar zero forças')
            return
        if a > len(self.total): #eliminar chances de ser maior ou menor que o total de espaços
            print('Não há tantos espaços')
            return
        check = False
        if self.total.count('r') == len(self.total):
            print('Todas as forças já são da república') #checar se todas as forças já são da república
        if self.total.count(0) >= a: #checar se tem mais espaços vazios que mudanças
            check = True
        if check: #fazer as mudanças
            loop = a
            while loop > 0:
                self.total.pop(0)
                self.total.append('r')
                loop-=1
            return            
        if not check: #caso sejam mais mudanças que espaços vazios
            for i in range(len(self.total)): #primeiro preenche os vazios disponíveis
                if self.total[i] == 0:
                    self.total[i] = 'r'
                    a-=1            
            for i in range(len(self.total)): #depois começa a inverter as forças
                if self.total[i] == 'm':
                    self.total[i] = 'r'
                    a-=1
                    if a == 0:
                        return
    def tira_mon(self, a):
        if a == 0:
            print('Não é possível retirar zero forças')
            return
        if a > len(self.total): #eliminar chances de ser maior que o total de espaços ou zero
            print('Não há tantos espaços')
            return
        if 'm' not in self.total:
            print('Não há forças monarquistas nessa região')
            return
        for i in range(len(self.total)): #primeiro preenche os vazios disponíveis
            if self.total[i] == 'm':
                self.total[i] = 0
                a-=1
                if a == 0:
                    return 
    
    def tira_rep(self, a):
        if a == 0:
            print('Não é possível retirar zero forças')
            return
        if a > len(self.total): #eliminar chances de ser maior que o total de espaços ou zero
            print('Não há tantos espaços')
            return
        if 'r' not in self.total:
            print('Não há forças republicanas nessa região')
            return
        for i in range(len(self.total)): #primeiro preenche os vazios disponíveis
            if self.total[i] == 'r':
                self.total[i] = 0
                a-=1
                if a == 0:
                    return
     
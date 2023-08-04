import random
import pygame
import os
import sys
class EventCard:
    def __init__(self, title, descricao, desc_efeito, id, evento1=None, evento2=None, evento3=None, evento4=None, evento5=None, evento6=None) -> None:
        self.title = title
        self.descricao = descricao
        self.id = id
        self.desc_efeito = desc_efeito
        self.evento1 = evento1
        self.evento2 = evento2
        self.evento3 = evento3
        self.evento4 = evento4
        self.evento5 = evento5
        self.evento6 = evento6
            
    def efeito(self, a=None, b=None, c=None, d=None, e=None, f=None):
        a = self.evento1
        b = self.evento2
        c = self.evento3
        d = self.evento4
        e = self.evento5
        f = self.evento6
        return a, b, c, d, e, f
    
    def dado(self):
        result = random.randint(1, 6)
        print(f"O resultado do dado é {result}")
        if result == 6:
            return print('As forças monarquistas evitaram que o evento acontecesse')
        if result  == 1 or result == 2:
            print(self.desc_efeito)            
            print(f"{self.title} deu tão certo que você ainda deve retirar uma força monarquista de um local à sua escolha")            
            return
        if result == 3 or result == 4 or result == 5:
            print(f"O evento acontece e as forças republicanas ganham mais potência")
            print(self.desc_efeito)

    def ativar_efeito(self):
        if self.evento1 != None:
            regiao = self.evento1[0]
            if self.evento1[1] == 'tira':
                comando = self.evento1[2]
                regiao.tira_mon(comando)
            if self.evento1[1] == 'add':
                comando2 = self.evento1[2]
                regiao.add_rep(comando2)
        elif self.evento2 != None:
            regiao = self.evento2[0]
            if self.evento2[1] == 'tira':
                regiao.tira_mon(self.evento2[2])
            if self.evento2[1] == 'add':
                regiao.add_rep(self.evento2[2])
        elif self.evento3 != None:
            regiao = self.evento3[0]
            if self.evento3[1] == 'tira':
                regiao.tira_mon(self.evento3[2])
            if self.evento3[1] == 'add':
                regiao.add_rep(self.evento3[2])
        elif self.evento4 != None:
            regiao = self.evento4[0]
            if self.evento4[1] == 'tira':
                regiao.tira_mon(self.evento4[2])
            if self.evento4[1] == 'add':
                regiao.add_rep(self.evento4[2])        
        elif self.evento5 != None:
            regiao = self.evento5[0]
            if self.evento5[1] == 'tira':
                regiao.tira_mon(self.evento5[2])
            if self.evento5[1] == 'add':
                regiao.add_rep(self.evento5[2])
        elif self.evento6 != None:
            regiao = self.evento6[0]
            if self.evento6[1] == 'tira':
                regiao.tira_mon(self.evento6[2])
            if self.evento6[1] == 'add':
                regiao.add_rep(self.evento6[2])

class Placar:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
    def update(self):
        e = self.a
        f = self.b
        g = self.c
        h = self.d
        result1 = f"Rio de Janeiro:\nForças monarquistas: {e.count('m')}\nForças republicanas: {e.count('r')}"
        r1 = '\033[0m'+'Rio de Janeiro'+'\033[0m'
        result2 = f"Nordeste:\nForças monarquistas: {f.count('m')}\nForças republicanas: {f.count('r')}"
        r2 = '\033[0m'+'Nordeste'+'\033[0m'
        result3 = f"Sudeste:\nForças monarquistas: {g.count('m')}\nForças republicanas: {g.count('r')}"
        r3 = '\033[0m'+'Sudeste'+'\033[0m'
        result4 = f"Norte:\nForças monarquistas: {h.count('m')}\nForças republicanas: {h.count('r')}"
        r4 = '\033[0m'+'Norte'+'\033[0m'
        resultado = f"{result1}\n{result2}\n{result3}\n{result4}"
        
   
        return resultado
               
class Regiao:
    def __init__(self, nome, espacos) -> None:
        self.nome = nome
        self.espacos = espacos    
        self.total = []
        for i in range(1, self.espacos+1):
            self.total.append(0)
    
    
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

def verificar_fim(a, b, c, d):    
    if a.count('r')>a.count('m'):
        if b.count('r')>b.count('m'):
            if c.count('r')>c.count('m'):
                if d.count('r')>d.count('m'):                    
                    print('')
                    print('Em seu jardim no palácio em Petrópolis você recebe uma carta. Ela conta que o Marechal Deodoro da Fonseca, \num de seus homens de confiança, entrou no quartel à cavalo e obrigou Visconde de Ouro Preto, seu ministro, \na se demitir. Você não acredita muito que isso vá muito longe, e prepara sua viagem para o \nRio de Janeiro para apaziguar a situação. Após dois dias, ao chegar no paço imperial, você \nrecebe a notícia: a câmara municipal tinha proclamado a república e você tem vinte e quatro horas para deixar o Brasil com sua família.')
                    print('')
                    input('Escreva perdi para sair: ')
                    sys.exit()

class Button:
    def __init__(self, image, pos, text_input, font, hovering_color) -> None:
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, (0,0,0))     
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position, new_image):
        self.new_image = new_image
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image = self.new_image

class GoButton:
    def __init__(self, image, pos) -> None:
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]        
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)        

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

class dice_result:
    def __init__(self, result):
        self.result = result

    def dice_event(self, screen, fundo_texto_title, fonte_texto, texto_desc):
        self.screen = screen
        self.texto_desc = texto_desc
        pos_fundo_texto_x = 100
        pos_fundo_texto_y = 230        
        self.screen.blit(fundo_texto_title, (100, 180))
        if self.result == 6:
            texto_eficacia = 'Os monarquistas evitaram que o evento ocorresse'
            texto_linha = fonte_texto.render(texto_eficacia, True, (0, 0, 0))
            pos_texto_x = pos_fundo_texto_x + 90
            self.screen.blit(texto_linha, (pos_texto_x, 225))

        if self.result  == 1 or self.result == 2:
            texto_eficacia = 'Os republicanos obtiveram um enorme sucesso'
            texto_eficacia2 = 'retire duas forças monarquistas'
            texto_linha = fonte_texto.render(texto_eficacia, True, (0, 0, 0))
            texto_linha2 = fonte_texto.render(texto_eficacia2, True, (0, 0, 0))
            pos_texto_x = pos_fundo_texto_x + 100
            self.screen.blit(texto_linha, (pos_texto_x, 210))
            self.screen.blit(texto_linha2, (pos_texto_x+50, 240))

        if self.result == 3 or self.result == 4 or self.result == 5:
            texto_eficacia = 'Os republicanos tiveram sucesso'
            texto_eficacia2 = 'retire uma força monarquista'
            texto_linha = fonte_texto.render(texto_eficacia, True, (0, 0, 0))
            texto_linha2 = fonte_texto.render(texto_eficacia2, True, (0, 0, 0))
            pos_texto_x = pos_fundo_texto_x + 150
            self.screen.blit(texto_linha, (pos_texto_x, 210))
            self.screen.blit(texto_linha2, (pos_texto_x+20, 240))

    def king_event(self):
        pass
        # if self.result == 6:
        #     TELA = screen            
        #     pos_fundo_texto_x = 100
        #     pos_fundo_texto_y = 230
        #     TELA.blit(fundo_texto_desc, (pos_fundo_texto_x, pos_fundo_texto_y))
        # if self.result  == 1 or self.result == 2:
        #     TELA = screen            
        #     pos_fundo_texto_x = 100
        #     pos_fundo_texto_y = 230
        #     TELA.blit(fundo_texto_desc, (pos_fundo_texto_x, pos_fundo_texto_y))
        # if self.result == 3 or self.result == 4 or self.result == 5:
        #     TELA = screen            
        #     pos_fundo_texto_x = 100
        #     pos_fundo_texto_y = 230
        #     TELA.blit(fundo_texto_desc, (pos_fundo_texto_x, pos_fundo_texto_y))
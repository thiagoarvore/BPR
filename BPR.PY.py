import pygame, sys, os
import random
from pygame.locals import *
from classe import *
pygame.init()
largura, altura = 1200, 800
FONTE_TEXTOS = pygame.font.SysFont('microsoftsansserif', 20)
FONTE_PONTOS = pygame.font.SysFont('arial', 12, True)
TELA = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Batalha Pela República')

IMAGEM_BACKGROUND = pygame.transform.scale2x((pygame.image.load(os.path.join('images', 'pergaminho.jpg'))))
IMAGEM_TEXTO = (pygame.image.load(os.path.join('images', 'fundo_texto.png')))
IMAGEM_BOTAO_PROX = (pygame.image.load(os.path.join('images', 'botao_prox.png')))
IMAGEM_PLACAR = (pygame.image.load(os.path.join('images', 'placar.png')))
sprite_sheet = pygame.image.load(os.path.join('images', 'dices.png')).convert_alpha()

norte = Regiao('Norte', 5)
sudes = Regiao('Sudeste', 7)
norde = Regiao('Nordeste', 5)
rio = Regiao('Rio de Janeiro', 4) 
lista_regioes = [norte, sudes, norde, rio]
placar = Placar(rio.total, norde.total, sudes.total, norte.total)

class Dado(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dices = []
        self.sortear = False

        for i in range(6):
            img = sprite_sheet.subsurface((i*100,0), (100,100))
            img = pygame.transform.scale(img, (100/2, 100/2))
            self.imagens_dices.append(img)
        self.index_lista = 0
        self.image = self.imagens_dices[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.x = 590
        self.rect.y = 500
        self.x_pos = 590
        self.y_pos = 500        

    def update(self):
        if self.sorteado != None:
            self.index_lista = random.randint(0, 5)
            if self.index_lista > 5:
                self.index_lista = 0
            self.index_lista += 0.5
            self.image = self.imagens_dices[int(self.index_lista)]
        

    def sorteado(self):
        result = int(self.index_lista) + 1
        texto_result = f"O resultado é {result}"
        texto_linha = FONTE_TEXTOS.render(texto_result, True, (0, 0, 0))
        self.image = self.imagens_dices[int(self.index_lista)]
        fundo_texto_result = pygame.transform.scale(IMAGEM_TEXTO, (600+200, 230-100))
        pos_fundo_texto_x = largura // 2-390
        pos_texto_x = pos_fundo_texto_x + 300
        TELA.blit(fundo_texto_result, (pos_fundo_texto_x, 650))
        TELA.blit(texto_linha, (pos_texto_x+35, 700))
        return result
            

    def checkForInput(self, position):        
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

        
#mecanicas
def turno():    
    sortear_carta(cartas_restantes)
    placar.update()    
    verificar_fim(norte.total, sudes.total, rio.total, norde.total)

def sortear_carta(a):
    carta_sorteada = random.choice(a)    
    print('')
    print(f"O evento é: {carta_sorteada.title}")
    print('')
    print(carta_sorteada.descricao)   
    print('')
    print(input('Aperte Enter para jogar um dado'))
    result = random.randint(1, 6)
    print('')
    print(f"O resultado do dado é {result}")
    print('')
    if result == 6:            
        print('As forças monarquistas evitaram que o evento acontecesse')
        del cartas_restantes[cartas_restantes.index(carta_sorteada)]
        return
    if result  == 1 or result == 2:
        print(carta_sorteada.desc_efeito)
        print('')           
        print(f"Além disso, {carta_sorteada.title} deu tão certo que você ainda deve retirar uma força monarquista de um local à sua escolha")
        tirar_forca()
        carta_sorteada.ativar_efeito()
        del cartas_restantes[cartas_restantes.index(carta_sorteada)]                
        return
    if result == 3 or result == 4 or result == 5:        
        print(carta_sorteada.desc_efeito)
        carta_sorteada.ativar_efeito()
        del cartas_restantes[cartas_restantes.index(carta_sorteada)]

def escolher_regiao(regioes):
    while True:
        print("Escolha uma região:")
        for i, regiao in enumerate(regioes, start=1):
            print(f"{i}. {regiao.nome}")

        try:
            escolha = int(input("Digite o número da região que perderá uma força: "))
            if 1 <= escolha <= len(regioes):
                return regioes[escolha - 1]
            else:
                print('Opção Inválida. Digite um número da lista.')
        except (ValueError, IndexError):
            print('Opção Inválida. Digite um número da lista.')

#e tirar uma força da região
def tirar_forca():    
    regiao_escolhida = escolher_regiao(lista_regioes)
    if 'm' in regiao_escolhida.total:
        regiao_escolhida.tira_mon(1)
    else:
        print('Não há forças monarquistas nessa região')
        tirar_forca() 

#criação das cartas de eventos
carta1 = EventCard('Lei Áurea', 'Enfim a escravidão foi proibida no Brasil', '(mas isso não significou uma grande melhoria na vida dos negros)\nSubstitua duas forças monarquistas do nordeste por forças republicanas\nSubstitua duas forças monarquistas do sudeste por forças republicanas', 1, 
                   [norde, 'tira', 2], [norde, 'add', 2], [sudes, 'tira', 2], [sudes, 'add', 2])
carta2 = EventCard('Boom da Borracha', 'O norte do país é inundado de trabalhadores para extrair o látex', 'Substitua duas forças monarquistas no norte por forças republicanas', 2, 
                   [norte, 'tira', 2], [norte, 'add', 2])
carta3 = EventCard('Maçonaria', 'As relações de D. Pedro II com a maçonaria não são vistas com bons olhos pela Igreja Católica', 'Retire 1 força monarquista de cada região', 3, 
                   [norte, 'tira', 1], [norde, 'tira', 1], [sudes, 'tira', 1], [rio, 'tira', 1])
carta4 = EventCard('Guerra do Paraguai', 'O exército brasileiro volta vitorioso do massacre ocorrido no Paraguai, mas com ideias republicanas cada vez mais presentes', 'Substitua três forças monarquistas do sudeste por forças republicanas\nSubstitua uma força monarquista no norte por uma força republicana\nRetire uma força monarquista do Rio de Janeiro', 4, 
                   [norte, 'tira', 1], [norte, 'add', 1], [sudes, 'tira', 3], [sudes, 'add', 3], [rio, 'tira', 1])
carta5 = EventCard('Partido Republicano', 'Foi fundado o partido republicano', 'Substitua uma força monarquista no Rio de Janeiro por uma Republicana\nSubstitua uma força monarquista no sudeste por uma republicana ', 5, 
                   [norde, 'tira', 1], [rio, 'add', 1], [sudes, 'add', 1], [sudes, 'tira', 1], [rio, 'tira', 1])
carta6 = EventCard('Charges em jornais', 'Jornalistas, intelectuais e artistas estão criticando o império e o imperador nos periódicos brasileiros', 'Substitua uma força monarquista no Rio de Janeiro por uma republicana\nSubstitua uma força monarquista no nordeste por uma republicana\nRetire uma força monarquista no sudeste', 6, 
                   [norde, 'tira', 1], [rio, 'add', 1], [norde, 'add', 1], [sudes, 'tira', 1], [rio, 'tira', 1])
carta7 = EventCard('Demissão de ministros', 'Marechal Deodoro da Fonseca, aliado do imperador, obriga o ministro Visconde de Ouro Preto a se demitir', 'Substitua duas forças monarquistas no Rio de Janeiro por republicanas\nSubstitua duas forças monarquistas no sudeste por republicanas\nRetire uma força monarquista do nordeste\nRetire uma força monarquista do norte', 7, 
                   [norde, 'tira', 1], [rio, 'add', 2], [sudes, 'add', 2], [sudes, 'tira', 2], [rio, 'tira', 2], [norte, 'tira', 1])
#criação da lista de cartas
lista_cartas = []
lista_cartas.append(carta1)
lista_cartas.append(carta2)
lista_cartas.append(carta3)
lista_cartas.append(carta4)
lista_cartas.append(carta5)
lista_cartas.append(carta6)
lista_cartas.append(carta7)
cartas_restantes = lista_cartas.copy()

def comecar_jogo1():
    result = 'A BATALHA PELA REPÚBLICA\nO ano é 1889. O Brasil passa por momentos conturbados e as\nideias republicanas ameaçam seu poder.\nVocê, o imperador brasileiro D. Pedro II, teme que o pior aconteça.\nEm BATALHA PELA REPÚBLICA seu objetivo\né evitar que a república seja proclamada.\nSerá que você vai conseguir manter sua dinastia?!'
    return result

def intro():    
    while True:
        TELA.blit(IMAGEM_BACKGROUND, (0, 0))
        novo_fundo_texto = pygame.transform.scale(IMAGEM_TEXTO, (600+200, 230+200))
        pos_texto_x = largura // 2-400
        TELA.blit(novo_fundo_texto, (pos_texto_x, 200))         
        text1 = comecar_jogo1()
        linhas_info = text1.split('\n')
        pos_y = 300  # Posição vertical para começar a renderizar as linhas
        for linha in linhas_info:
            texto_linha = FONTE_TEXTOS.render(linha, True, (0, 0, 0))
            pos_x = largura // 2 - texto_linha.get_width() // 2# Centraliza horizontalmente
            TELA.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 5  # Espaçamento entre as linhas

        
        INTRO_MOUSE_POS = pygame.mouse.get_pos()
        continue_button = GoButton(IMAGEM_BOTAO_PROX, pos=(900, 600))
        continue_button.update(TELA)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.checkForInput(INTRO_MOUSE_POS):
                    intro2()
        pygame.display.update()

def comecar_jogo2():
    result = 'O país está dividido em três grandes regiões de influência:\nNorte, Nordeste e Sudeste.\nO Rio de Janeiro, a capital do país, é uma zona de influência à parte.\n\nCaso as forças republicanas consigam a maioria das quatro regiões\nsua posição de chefe de Estado ficará em grande perigo.'    
    return result

def intro2():
    while True:
        TELA.blit(IMAGEM_BACKGROUND, (0, 0))
        novo_fundo_texto = pygame.transform.scale(IMAGEM_TEXTO, (600+200, 230+200))
        pos_texto_x = largura // 2-400
        TELA.blit(novo_fundo_texto, (pos_texto_x, 200))         
        text1 = comecar_jogo2()
        linhas_info = text1.split('\n')
        pos_y = 320  # Posição vertical para começar a renderizar as linhas
        for linha in linhas_info:
            texto_linha = FONTE_TEXTOS.render(linha, True, (0, 0, 0))
            pos_x = largura // 2 - texto_linha.get_width() // 2# Centraliza horizontalmente
            TELA.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 5  # Espaçamento entre as linhas

        
        INTRO_MOUSE_POS = pygame.mouse.get_pos()
        continue_button = GoButton(IMAGEM_BOTAO_PROX, pos=(900, 600))
        continue_button.update(TELA)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.checkForInput(INTRO_MOUSE_POS):
                    intro3()
        pygame.display.update()

def comecar_jogo3():
    result = 'Se mesmo após todos os acontecimentos você tiver\na maioria do Rio de Janeiro, mas as outras três regiões forem\nde maioria republicana, sua posição ainda estará insustentável\nMas como a monarquia é um sistema em que a população confia,\nem caso de empate você está grantido como\na grande influência da região'    
    return result

def intro3():
    while True:
        TELA.blit(IMAGEM_BACKGROUND, (0, 0))
        novo_fundo_texto = pygame.transform.scale(IMAGEM_TEXTO, (600+200, 230+200))
        pos_texto_x = largura // 2-400
        TELA.blit(novo_fundo_texto, (pos_texto_x, 200))         
        text1 = comecar_jogo3()
        linhas_info = text1.split('\n')
        pos_y = 320  # Posição vertical para começar a renderizar as linhas
        for linha in linhas_info:
            texto_linha = FONTE_TEXTOS.render(linha, True, (0, 0, 0))
            pos_x = largura // 2 - texto_linha.get_width() // 2# Centraliza horizontalmente
            TELA.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 5  # Espaçamento entre as linhas

        
        INTRO_MOUSE_POS = pygame.mouse.get_pos()
        continue_button = GoButton(IMAGEM_BOTAO_PROX, pos=(900, 600))
        continue_button.update(TELA)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.checkForInput(INTRO_MOUSE_POS):
                    intro4()
        pygame.display.update()

def comecar_jogo4():
    result = 'A cada evento, você vai jogar um dado,\ndependendo do resultado,\no evento pode tornar sua vida MUITO mais difícil.\n'
    return result

def intro4():
    while True:
        TELA.blit(IMAGEM_BACKGROUND, (0, 0))
        TELA.blit(IMAGEM_PLACAR, (890, 90))#lugar ótimo já
        novo_fundo_texto = pygame.transform.scale(IMAGEM_TEXTO, (600, 230))
        TELA.blit(novo_fundo_texto, (100, 100))         
        text1 = 'O cenário político começa favorável à você:'
        texto_linha = FONTE_TEXTOS.render(text1, True, (0, 0, 0))            
        TELA.blit(texto_linha, (200, 200))
        info_pontos = placar.update()    
        linhas_info = info_pontos.split('\n')
        pos_y = 115  # Posição vertical para começar a renderizar as linhas
        for linha in linhas_info:
            texto_linha = FONTE_PONTOS.render(linha, True, (0, 0, 0))
            pos_x = largura // 2 - texto_linha.get_width() // 2 +390 # Centraliza horizontalmente
            TELA.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 5  # Espaçamento entre as linhas
        novo_fundo_texto2 = pygame.transform.scale(IMAGEM_TEXTO, (800, 350))
        TELA.blit(novo_fundo_texto2, (100, 400))
        text1 = comecar_jogo4()
        linhas_info = text1.split('\n')
        pos_y = 530  # Posição vertical para começar a renderizar as linhas
        for linha in linhas_info:
            texto_linha = FONTE_TEXTOS.render(linha, True, (0, 0, 0))
            pos_x = largura // 2 - texto_linha.get_width() // 2# Centraliza horizontalmente
            TELA.blit(texto_linha, (pos_x-100, pos_y))
            pos_y += texto_linha.get_height() + 5  # Espaçamento entre as linhas
        

        
        INTRO_MOUSE_POS = pygame.mouse.get_pos()
        continue_button = GoButton(IMAGEM_BOTAO_PROX, pos=(900, 700))
        continue_button.update(TELA)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.checkForInput(INTRO_MOUSE_POS):
                    pass
        pygame.display.update()
todas_as_sprites = pygame.sprite.Group()
dado = Dado()
todas_as_sprites.add(dado)

def turno1():
    sorteado = False    
    while True:
        TELA.blit(IMAGEM_BACKGROUND, (0, 0))
        TELA.blit(IMAGEM_PLACAR, (890, 90))#lugar ótimo já
        info_pontos = placar.update()    
        linhas_info = info_pontos.split('\n')
        pos_y = 115
        for linha in linhas_info:
            texto_linha = FONTE_PONTOS.render(linha, True, (0, 0, 0))
            pos_x = largura // 2 - texto_linha.get_width() // 2 +390 # Centraliza horizontalmente
            TELA.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 5  # Espaçamento entre as linhas
        GAME_MOUSE_POS = pygame.mouse.get_pos()
        norte_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(430, 468), text_input='Norte',
                            font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
        norde_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(800, 468), text_input='Nordeste',
                            font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
        rio_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(430, 590), text_input='Norte',
                            font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
        sudes_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(800, 590), text_input='Norte',
                            font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
        norte_buton.update(TELA)
        norde_buton.update(TELA)
        rio_buton.update(TELA)
        sudes_buton.update(TELA)

        for button in [norde_buton, norte_buton, rio_buton, sudes_buton]:
            button.changeColor(GAME_MOUSE_POS, pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            button.update(TELA)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if norte_buton.checkForInput(GAME_MOUSE_POS):
                    intro()
                if norde_buton.checkForInput(GAME_MOUSE_POS):
                    intro()
                if sudes_buton.checkForInput(GAME_MOUSE_POS):
                    intro()
                if rio_buton.checkForInput(GAME_MOUSE_POS):
                    intro()
                if dado.checkForInput(GAME_MOUSE_POS):
                    sorteado = True
            
        if sorteado == False:            
            todas_as_sprites.draw(TELA)
            todas_as_sprites.update()
        if sorteado == True:
            dado.sorteado()
        pygame.display.update()

        

turno1()
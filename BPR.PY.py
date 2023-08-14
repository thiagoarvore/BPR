import pygame, sys, os
import random
from pygame.locals import *
from classe import *

pygame.init()
pygame.display.set_caption('Batalha Pela República')

largura, altura = 1200, 800
FONTE_TEXTOS = pygame.font.SysFont('microsoftsansserif', 20)
FONTE_TEXTOS_TIROU6 = pygame.font.SysFont('microsoftsansserif', 40)
FONTE_PONTOS = pygame.font.SysFont('arial', 15, True)
FONTE_FINAL = pygame.font.SysFont('microsoftsansserif', 28)
TELA = pygame.display.set_mode((largura, altura))

IMAGEM_BACKGROUND = pygame.transform.scale2x((pygame.image.load(os.path.join('images', 'pergaminho.jpg'))))
IMAGEM_TEXTO = (pygame.image.load(os.path.join('images', 'fundo_texto.png')))
IMAGEM_BG_TITULO_EVENTO = pygame.transform.scale(IMAGEM_TEXTO, (600, 230-100))
IMAGEM_BG_DESC_EVENTO = pygame.transform.scale(IMAGEM_TEXTO, (600, 230-50))
IMAGEM_BOTAO_PROX = (pygame.image.load(os.path.join('images', 'botao_prox.png')))
IMAGEM_PLACAR = (pygame.image.load(os.path.join('images', 'placar.png')))
IMAGEM_PLACAR = pygame.transform.scale(IMAGEM_PLACAR, (200+80, 272+80))
sprite_sheet = pygame.image.load(os.path.join('images', 'dices.png')).convert_alpha()

norte = Regiao('Norte', 5)
sudes = Regiao('Sudeste', 7)
norde = Regiao('Nordeste', 5)
rio = Regiao('Rio de Janeiro', 4) 
lista_regioes = [norte, sudes, norde, rio]
#setup de forças monarquistas
rio.add_mon(3, TELA)
norte.add_mon(2, TELA)
norde.add_mon(4, TELA)
sudes.add_mon(4, TELA)

#setup de forças republicanas
rio.add_rep(1, TELA)
norte.add_rep(1, TELA)
sudes.add_rep(2, TELA)
placar = Placar(rio.total, norde.total, sudes.total, norte.total)

#criação de botoes
norte_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(420, 480), text_input='Norte',
                    font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
norde_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(790, 480), text_input='Nordeste',
                    font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
rio_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(420, 600), text_input='Rio de Janeiro',
                    font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
sudes_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(790, 600), text_input='Sudeste',
                    font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
buton_list = [norte_buton, norde_buton, rio_buton, sudes_buton]

class Dado(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dices = []
        self.sortear = False

        for i in range(6):
            img = sprite_sheet.subsurface((i*100,0), (100,100))
            img = pygame.transform.scale(img, (100/2+5, 100/2+5))
            self.imagens_dices.append(img)
        self.index_lista = 0
        self.image = self.imagens_dices[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.x = 950
        self.rect.y = 570
        self.x_pos = 950
        self.y_pos = 570        

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
        TELA.blit(fundo_texto_result, (pos_fundo_texto_x, 670))
        TELA.blit(texto_linha, (pos_texto_x+35, 720))
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

def tela_final():    
    while True:
        TELA.fill((0,0,0))                
        TELA.blit(IMAGEM_BACKGROUND, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        fundo_texto_final = pygame.transform.scale2x(IMAGEM_TEXTO)
        fundo_texto_final = pygame.transform.scale(IMAGEM_TEXTO, (1150, 630))
        fundo_texto_final_rect = fundo_texto_final.get_rect()
        pos_fundo_texto_finalx = largura // 2 - fundo_texto_final_rect.width // 2
        pos_fundo_texto_finaly = 50
        TELA.blit(fundo_texto_final, (pos_fundo_texto_finalx, pos_fundo_texto_finaly))
        texto_final = 'Em seu jardim no palácio em Petrópolis você recebe uma carta.\nEla conta que o Marechal Deodoro da Fonseca,\num de seus homens de confiança, entrou no quartel à cavalo\ne obrigou Visconde de Ouro Preto, seu ministro, a se demitir.\nVocê não acredita muito que isso vá muito longe,\ne prepara sua viagem para o Rio de Janeiro para apaziguar a situação.\nApós dois dias, ao chegar no paço imperial, você \nrecebe a notícia: a câmara municipal tinha proclamado a república\ne você tem vinte e quatro horas para deixar o Brasil com sua família.'        
        pos_y = pos_fundo_texto_finaly + 140
        for linha in texto_final.split('\n'):
            texto_linha = FONTE_FINAL.render(linha, True, (0, 0, 0))        
            pos_x = largura // 2 - texto_linha.get_width() //2
            TELA.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 2
        pygame.display.update()


def mostrar_placar():
    TELA.blit(IMAGEM_PLACAR, (820, 50))#lugar ótimo já
    info_pontos = placar.update()    
    linhas_info = info_pontos.split('\n')
    pos_y_placar = 100
    for linha_placar in linhas_info:
        texto_linha = FONTE_PONTOS.render(linha_placar, True, (0, 0, 0))
        pos_x_placar = largura // 2 - texto_linha.get_width() // 2 +365 # Centraliza horizontalmente
        TELA.blit(texto_linha, (pos_x_placar, pos_y_placar))
        pos_y_placar += texto_linha.get_height() + 5  # Espaçamento entre as linhas

def sortear_carta(a):
    carta_sorteada = random.choice(a)
    del cartas_restantes[cartas_restantes.index(carta_sorteada)]    
    return carta_sorteada
    
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

def escolher_regiao(regiao: Regiao):
    regiao.tira_mon(1, TELA)
    mostrar_placar()    
    return

#e tirar uma força da região
def tirar_forca():    
    regiao_escolhida = escolher_regiao(lista_regioes)
    if 'm' in regiao_escolhida.total:
        regiao_escolhida.tira_mon(1)
    else: #fazer uma mensagem aparecer e desaparecer
        print('Não há forças monarquistas nessa região')
        tirar_forca() 

#criação das cartas de eventos
carta1 = EventCard('Lei Áurea', '\nEnfim a escravidão foi proibida no Brasil\n(mas isso não significou uma imediata\nmelhoria na vida dos negros','Substitua duas forças monarquistas do nordeste por forças republicanas\nSubstitua duas forças monarquistas do sudeste por forças republicanas', 1, 
                   [norde, 'tira', 2], [norde, 'add', 2], [sudes, 'tira', 2], [sudes, 'add', 2])
carta2 = EventCard('Boom da Borracha', 'O norte do país é inundado de\ntrabalhadores para extrair o látex', 'Substitua duas forças monarquistas no norte por forças republicanas', 2, 
                   [norte, 'tira', 2], [norte, 'add', 2])
carta3 = EventCard('Maçonaria', ' \nAs relações de D. Pedro II com a maçonaria\nnão são vistas com bons olhos pela Igreja Católica', 'Retire 1 força monarquista de cada região', 3, 
                   [norte, 'tira', 1], [norde, 'tira', 1], [sudes, 'tira', 1], [rio, 'tira', 1])
carta4 = EventCard('Guerra do Paraguai', 'O exército brasileiro volta vitorioso\ndo massacre ocorrido no Paraguai,\nmas com ideias republicanas cada vez mais presentes', 'Substitua três forças monarquistas do sudeste por forças republicanas\nSubstitua uma força monarquista no norte por uma força republicana\nRetire uma força monarquista do Rio de Janeiro', 4, 
                   [norte, 'tira', 1], [norte, 'add', 1], [sudes, 'tira', 3], [sudes, 'add', 3], [rio, 'tira', 1])
carta5 = EventCard('Partido Republicano', ' \nFoi fundado o partido republicano', 'Substitua uma força monarquista no Rio de Janeiro por uma Republicana\nSubstitua uma força monarquista no sudeste por uma republicana ', 5, 
                   [norde, 'tira', 1], [rio, 'add', 1], [sudes, 'add', 1], [sudes, 'tira', 1], [rio, 'tira', 1])
carta6 = EventCard('Charges em jornais', ' \nJornalistas, intelectuais e artistas estão criticando\no império e o imperador nos periódicos brasileiros', 'Substitua uma força monarquista no Rio de Janeiro por uma republicana\nSubstitua uma força monarquista no nordeste por uma republicana\nRetire uma força monarquista no sudeste', 6, 
                   [norde, 'tira', 1], [rio, 'add', 1], [norde, 'add', 1], [sudes, 'tira', 1], [rio, 'tira', 1])
carta7 = EventCard('Demissão de ministros', '\nMarechal Deodoro da Fonseca, aliado do imperador,\nobriga o ministro Visconde de Ouro Preto a se demitir', 'Substitua duas forças monarquistas no Rio de Janeiro por republicanas\nSubstitua duas forças monarquistas no sudeste por republicanas\nRetire uma força monarquista do nordeste\nRetire uma força monarquista do norte', 7, 
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

def intro(a=None):
    if a == None:
        while True:
            TELA.blit(IMAGEM_BACKGROUND, (0, 0))
            novo_fundo_texto = pygame.transform.scale(IMAGEM_TEXTO, (600+200, 230+200))
            pos_texto_x = largura // 2-400
            TELA.blit(novo_fundo_texto, (pos_texto_x, 200))        
            text1 = 'A BATALHA PELA REPÚBLICA\nO ano é 1889. O Brasil passa por momentos conturbados e as\nideias republicanas ameaçam seu poder.\nVocê, o imperador brasileiro D. Pedro II, teme que o pior aconteça.\nEm BATALHA PELA REPÚBLICA seu objetivo\né evitar que a república seja proclamada.\nSerá que você vai conseguir manter sua dinastia?!'
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
                        intro(1)
            pygame.display.update()
    if a == 1:
        while True:
            TELA.blit(IMAGEM_BACKGROUND, (0, 0))
            novo_fundo_texto = pygame.transform.scale(IMAGEM_TEXTO, (600+200, 230+200))
            pos_texto_x = largura // 2-400
            TELA.blit(novo_fundo_texto, (pos_texto_x, 200))         
            text1 = 'O país está dividido em três grandes regiões de influência:\nNorte, Nordeste e Sudeste.\nO Rio de Janeiro, a capital do país, é uma zona de influência à parte.\n\nCaso as forças republicanas consigam a maioria das quatro regiões\nsua posição de chefe de Estado ficará em grande perigo.'
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
                        intro(2)
            pygame.display.update()
    if a == 2:
        while True:
            TELA.blit(IMAGEM_BACKGROUND, (0, 0))
            novo_fundo_texto = pygame.transform.scale(IMAGEM_TEXTO, (600+200, 230+200))
            pos_texto_x = largura // 2-400
            TELA.blit(novo_fundo_texto, (pos_texto_x, 200))         
            text1 = 'Se mesmo após todos os acontecimentos você tiver\na maioria do Rio de Janeiro, mas as outras três regiões forem\nde maioria republicana, sua posição ainda estará insustentável\nMas como a monarquia é um sistema em que a população confia,\nem caso de empate você está grantido como\na grande influência da região'
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
                        intro(3)
            pygame.display.update()
    if a == 3:
        while True:
            TELA.blit(IMAGEM_BACKGROUND, (0, 0))            
            novo_fundo_texto = pygame.transform.scale(IMAGEM_TEXTO, (600, 230))
            TELA.blit(novo_fundo_texto, (100, 100))         
            text1 = 'O cenário político começa favorável à você:'
            texto_linha = FONTE_TEXTOS.render(text1, True, (0, 0, 0))            
            TELA.blit(texto_linha, (200, 200))
            mostrar_placar()
            novo_fundo_texto2 = pygame.transform.scale(IMAGEM_TEXTO, (800, 350))
            TELA.blit(novo_fundo_texto2, (100, 400))
            text1 = 'A cada evento, você vai jogar um dado,\ndependendo do resultado,\no evento pode tornar sua vida MUITO mais difícil.\n'
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
                        turno1()
            pygame.display.update() 

todas_as_sprites = pygame.sprite.Group()
dado = Dado()
todas_as_sprites.add(dado)

def turno1():
    sorteado = False
    cartadavez = sortear_carta(cartas_restantes) 
    while True:        
        TELA.blit(IMAGEM_BACKGROUND, (0, 0))        
        #título da carta sorteada
        fundo_texto_title = pygame.transform.scale(IMAGEM_TEXTO, (600, 230-100))
        texto_title = f"{cartadavez.title}"
        texto_linha = FONTE_TEXTOS.render(texto_title, True, (0, 0, 0))        
        pos_fundo_texto_x = 100
        pos_texto_x = pos_fundo_texto_x + 200
        TELA.blit(fundo_texto_title, (pos_fundo_texto_x, 50))
        TELA.blit(texto_linha, (pos_texto_x, 100))
        #descrição da carta sorteada
        fundo_texto_desc = pygame.transform.scale(IMAGEM_TEXTO, (600, 230))
        fundo_texto_desc_rect = fundo_texto_desc.get_rect()
        pos_fundo_texto_x = 100
        pos_fundo_texto_y = 180
        TELA.blit(fundo_texto_desc, (pos_fundo_texto_x, pos_fundo_texto_y))
        texto_desc = f"{cartadavez.descricao}"        
        pos_y = pos_fundo_texto_y + 50
        for linha in texto_desc.split('\n'):
            texto_linha = FONTE_TEXTOS.render(linha, True, (0, 0, 0))        
            pos_x = fundo_texto_desc_rect.centerx +100 - texto_linha.get_width() //2
            TELA.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 2
        #descrição do efeito
        fundo_texto_efeito = pygame.transform.scale(IMAGEM_TEXTO, (600+400, 230+100))
        TELA.blit(fundo_texto_efeito, (pos_fundo_texto_x, 450))
        texto_efeito = f"{cartadavez.desc_efeito}"
        fundo_texto_efeito_rect = fundo_texto_efeito.get_rect()        
        pos_y = 550
        for linha in texto_efeito.split('\n'):
            texto_linha = FONTE_TEXTOS.render(linha, True, (0, 0, 0))        
            pos_x = fundo_texto_efeito_rect.centerx +100 - texto_linha.get_width() //2
            TELA.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 2     
        #placar
        mostrar_placar()
        #botões    
        GAME_MOUSE_POS = pygame.mouse.get_pos() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:                
                if dado.checkForInput(GAME_MOUSE_POS):
                    sorteado = True 
        text_dado = "Jogue um dado para testar sua sorte"
        text_dado_renderizado = FONTE_TEXTOS.render(text_dado, True, (0, 0, 0))
        x_text_dado = largura //2 - text_dado_renderizado.get_width() // 2
        y_text_dado = 700
        TELA.blit(text_dado_renderizado, (x_text_dado, y_text_dado-40))      
        if sorteado == False:            
            todas_as_sprites.draw(TELA)
            todas_as_sprites.update()
        if sorteado == True:
            if verificar_fim(norte.total, sudes.total, rio.total, norde.total):
                tela_final()
            else:
                dado.sorteado()                
                dado_rolado = dice_result(dado.sorteado())   
                efeito_func1(cartadavez, dado_rolado.result)
            
        pygame.display.update()

#efeito da carta funcionar (ou não) e escolher a região para perder força:
def efeito_func1(carta: EventCard, resultado_dado: dice_result):
    x = resultado_dado
    cartadavez = carta
    number = resultado_dado    
    if x == 6:
        TELA.fill((0,0,0))
        TELA.blit(IMAGEM_BACKGROUND, (0, 0))                
        while True:
            INTRO_MOUSE_POS = pygame.mouse.get_pos()            
            fundo_texto_desc = pygame.transform.scale(IMAGEM_TEXTO, (600+300, 230+250))
            fundo_texto_desc_rect = fundo_texto_desc.get_rect()
            pos_fundo_texto_x = 100
            pos_fundo_texto_y = 180
            TELA.blit(fundo_texto_desc, (pos_fundo_texto_x, pos_fundo_texto_y))
            texto_desc = "As forças monarquistas evitaram\nque o evento ocorresse"        
            pos_y = pos_fundo_texto_y + 200
            for linha in texto_desc.split('\n'):
                texto_linha = FONTE_TEXTOS_TIROU6.render(linha, True, (0, 0, 0))        
                pos_x = fundo_texto_desc_rect.centerx +100 - texto_linha.get_width() //2
                TELA.blit(texto_linha, (pos_x, pos_y))
                pos_y += texto_linha.get_height() + 2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if continue_button.checkForInput(INTRO_MOUSE_POS):
                            turno2()
            continue_button = GoButton(IMAGEM_BOTAO_PROX, pos=(900, 600))
            continue_button.update(TELA)
            pygame.display.update()
        
    if x == 3 or x == 4 or x == 5: 
        aplicado = False
        regiao_escolhida = False        
        while True:
            norte_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(420, 480), text_input='Norte',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            norde_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(790, 480), text_input='Nordeste',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            rio_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(420, 600), text_input='Rio de Janeiro',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            sudes_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(790, 600), text_input='Sudeste',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            GAME_MOUSE_POS = pygame.mouse.get_pos()            
            TELA.fill((0,0,0))
            TELA.blit(IMAGEM_BACKGROUND, (0, 0))
            if aplicado == False:
                cartadavez.ativar_efeito(TELA)
                aplicado = True            
            mostrar_placar()
            dado_evento = dice_result(number)
            dado_evento.dice_event(TELA, IMAGEM_BG_TITULO_EVENTO, FONTE_TEXTOS)
            if regiao_escolhida == True:
                if verificar_fim(norte.total, sudes.total, rio.total, norde.total):
                    tela_final()
                else:
                    turno2() #prox turno                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if norte_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(norte)
                        regiao_escolhida = True                        
                        #turno2                            
                    if norde_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(norde)
                        regiao_escolhida = True
                    if sudes_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(sudes)
                        regiao_escolhida = True
                    if rio_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(rio)
                        regiao_escolhida = True                    
            for button in [norde_buton, norte_buton, rio_buton, sudes_buton]:
                button.changeColor(GAME_MOUSE_POS, pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
                button.update(TELA)                
            pygame.display.update()
    if x == 1 or x == 2: 
        loop = 2
        aplicado = False        
        while True:
            norte_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(420, 480), text_input='Norte',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            norde_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(790, 480), text_input='Nordeste',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            rio_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(420, 600), text_input='Rio de Janeiro',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            sudes_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(790, 600), text_input='Sudeste',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))        
            GAME_MOUSE_POS = pygame.mouse.get_pos()            
            TELA.fill((0,0,0))
            TELA.blit(IMAGEM_BACKGROUND, (0, 0))
            if aplicado == False:
                cartadavez.ativar_efeito(TELA)
                aplicado = True
                       
            for button in [norde_buton, norte_buton, rio_buton, sudes_buton]:
                button.changeColor(GAME_MOUSE_POS, pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
                button.update(TELA)
            mostrar_placar()
            dado_evento =   dice_result(number)
            dado_evento.dice_event(TELA, IMAGEM_BG_TITULO_EVENTO, FONTE_TEXTOS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if norte_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(norte)
                        loop -= 1                            
                    if norde_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(norde)
                        loop -= 1
                    if sudes_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(sudes)
                        loop -= 1
                    if rio_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(rio)
                        loop -= 1
            if verificar_fim(norte.total, sudes.total, rio.total, norde.total):
                tela_final()
            if loop == 0:
                turno2()
            pygame.display.update()

def turno2():
    sorteado = False
    cartadavez = sortear_carta(cartas_restantes) 
    while True:        
        TELA.blit(IMAGEM_BACKGROUND, (0, 0))        
        #título da carta sorteada
        fundo_texto_title = pygame.transform.scale(IMAGEM_TEXTO, (600, 230-100))
        texto_title = f"{cartadavez.title}"
        texto_linha = FONTE_TEXTOS.render(texto_title, True, (0, 0, 0))        
        pos_fundo_texto_x = 100
        pos_texto_x = pos_fundo_texto_x + 200
        TELA.blit(fundo_texto_title, (pos_fundo_texto_x, 50))
        TELA.blit(texto_linha, (pos_texto_x, 100))
        #descrição da carta sorteada
        fundo_texto_desc = pygame.transform.scale(IMAGEM_TEXTO, (600, 230))
        fundo_texto_desc_rect = fundo_texto_desc.get_rect()
        pos_fundo_texto_x = 100
        pos_fundo_texto_y = 180
        TELA.blit(fundo_texto_desc, (pos_fundo_texto_x, pos_fundo_texto_y))
        texto_desc = f"{cartadavez.descricao}"        
        pos_y = pos_fundo_texto_y + 50
        for linha in texto_desc.split('\n'):
            texto_linha = FONTE_TEXTOS.render(linha, True, (0, 0, 0))        
            pos_x = fundo_texto_desc_rect.centerx +100 - texto_linha.get_width() //2
            TELA.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 2
        #descrição do efeito
        fundo_texto_efeito = pygame.transform.scale(IMAGEM_TEXTO, (600+400, 230+100))
        TELA.blit(fundo_texto_efeito, (pos_fundo_texto_x, 450))
        texto_efeito = f"{cartadavez.desc_efeito}"
        fundo_texto_efeito_rect = fundo_texto_efeito.get_rect()        
        pos_y = 550
        for linha in texto_efeito.split('\n'):
            texto_linha = FONTE_TEXTOS.render(linha, True, (0, 0, 0))        
            pos_x = fundo_texto_efeito_rect.centerx +100 - texto_linha.get_width() //2
            TELA.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 2     
        #placar
        mostrar_placar()
        #botões    
        GAME_MOUSE_POS = pygame.mouse.get_pos() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:                
                if dado.checkForInput(GAME_MOUSE_POS):
                    sorteado = True 
        text_dado = "Jogue um dado para testar sua sorte"
        text_dado_renderizado = FONTE_TEXTOS.render(text_dado, True, (0, 0, 0))
        x_text_dado = largura //2 - text_dado_renderizado.get_width() // 2
        y_text_dado = 700
        TELA.blit(text_dado_renderizado, (x_text_dado, y_text_dado-40))      
        if sorteado == False:            
            todas_as_sprites.draw(TELA)
            todas_as_sprites.update()
        if sorteado == True:
            if verificar_fim(norte.total, sudes.total, rio.total, norde.total):
                tela_final()
            else:
                dado.sorteado()                
                dado_rolado = dice_result(dado.sorteado())   
                efeito_func2(cartadavez, dado_rolado.result)
            
        pygame.display.update()

def efeito_func2(carta: EventCard, resultado_dado: dice_result):
    print('###################################################################/nturno2############################################################################################')
    x = resultado_dado
    cartadavez = carta
    number = resultado_dado
    
    if x == 6:
        #tela de nada acontece
        intro()
    if x == 3 or x == 4 or x == 5: 
        aplicado = False
        regiao_escolhida = False        
        while True:
            norte_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(420, 480), text_input='Norte',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            norde_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(790, 480), text_input='Nordeste',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            rio_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(420, 600), text_input='Rio de Janeiro',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            sudes_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(790, 600), text_input='Sudeste',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            GAME_MOUSE_POS = pygame.mouse.get_pos()            
            TELA.fill((0,0,0))
            TELA.blit(IMAGEM_BACKGROUND, (0, 0))
            if aplicado == False:
                cartadavez.ativar_efeito(TELA)
                aplicado = True            
            mostrar_placar()
            dado_evento = dice_result(number)
            dado_evento.dice_event(TELA, IMAGEM_BG_TITULO_EVENTO, FONTE_TEXTOS)
            if regiao_escolhida == True:
                if verificar_fim(norte.total, sudes.total, rio.total, norde.total):
                    tela_final()
                else:
                    pass
                    # turno_rei1() #prox turno
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if norte_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(norte)
                        regiao_escolhida = True                        
                        #turno2                            
                    if norde_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(norde)
                        regiao_escolhida = True
                    if sudes_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(sudes)
                        regiao_escolhida = True
                    if rio_buton.checkForInput(GAME_MOUSE_POS):
                        escolher_regiao(rio)
                        regiao_escolhida = True                    
            for button in [norde_buton, norte_buton, rio_buton, sudes_buton]:
                button.changeColor(GAME_MOUSE_POS, pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
                button.update(TELA)                
            pygame.display.update()
    if x == 1 or x == 2: 
        loop = 2
        aplicado = False        
        while True:
            norte_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(420, 480), text_input='Norte',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            norde_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(790, 480), text_input='Nordeste',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            rio_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(420, 600), text_input='Rio de Janeiro',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
            sudes_buton = Button(pygame.image.load(os.path.join('images', 'botao_regiao.png')), pos=(790, 600), text_input='Sudeste',
                                font=FONTE_TEXTOS, hovering_color=pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))        
            GAME_MOUSE_POS = pygame.mouse.get_pos()            
            TELA.fill((0,0,0))
            TELA.blit(IMAGEM_BACKGROUND, (0, 0))
            if aplicado == False:
                cartadavez.ativar_efeito(TELA)
                aplicado = True
            else:            
                for button in [norde_buton, norte_buton, rio_buton, sudes_buton]:
                    button.changeColor(GAME_MOUSE_POS, pygame.image.load(os.path.join('images', 'botao_regiao_clicado.png')))
                    button.update(TELA)
                mostrar_placar()
                dado_evento =   dice_result(number)
                dado_evento.dice_event(TELA, IMAGEM_BG_TITULO_EVENTO, FONTE_TEXTOS)
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if norte_buton.checkForInput(GAME_MOUSE_POS):
                            escolher_regiao(norte)
                            loop -= 1                            
                        if norde_buton.checkForInput(GAME_MOUSE_POS):
                            escolher_regiao(norde)
                            loop -= 1
                        if sudes_buton.checkForInput(GAME_MOUSE_POS):
                            escolher_regiao(sudes)
                            loop -= 1
                        if rio_buton.checkForInput(GAME_MOUSE_POS):
                            escolher_regiao(rio)
                            loop -= 1
            if verificar_fim(norte.total, sudes.total, rio.total, norde.total):
                    tela_final()
            if loop == 0:
                pass #turnorei1()
            pygame.display.update()

def turnorei1():
    sorteado = False
    while True:        
        TELA.blit(IMAGEM_BACKGROUND, (0, 0))
        fundo_texto_title = pygame.transform.scale(IMAGEM_TEXTO, (600, 230-100))
        pos_fundo_texto_x = 100
        pos_texto_x = pos_fundo_texto_x + 200
        TELA.blit(fundo_texto_title, (pos_fundo_texto_x, 50))        
        texto_title = "Mas é claro que as forças monarquistas\nnão iam ficar de mãos amarradas!"
        fundo_texto_title_rect = fundo_texto_title.get_rect() 
        pos_y = 85
        for linha in texto_title.split('\n'):
            texto_linha = FONTE_TEXTOS.render(linha, True, (0, 0, 0))        
            pos_x = fundo_texto_title_rect.centerx +100 - texto_linha.get_width() //2
            TELA.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 2
        mostrar_placar()
        #botões    
        GAME_MOUSE_POS = pygame.mouse.get_pos() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:                
                if dado.checkForInput(GAME_MOUSE_POS):
                    sorteado = True 
        text_dado = "Jogue um dado para testar sua sorte"
        text_dado_renderizado = FONTE_TEXTOS.render(text_dado, True, (0, 0, 0))
        x_text_dado = largura //2 - text_dado_renderizado.get_width() // 2
        y_text_dado = 700
        TELA.blit(text_dado_renderizado, (x_text_dado, y_text_dado-40))
        if sorteado == False:            
            todas_as_sprites.draw(TELA)
            todas_as_sprites.update()
        if sorteado == True:            
            dado.sorteado()                
            dado_rolado = dice_result(dado.sorteado())   
            escolha_rei1(dado_rolado.result)
             #ir para a escolha
        pygame.display.update()
def escolha_rei1(result_dado):
    dado_rei = result_dado
    if dado_rei == 1 or dado_rei == 2:
        pass #adiciona 1
    if dado_rei in range(3,6):
        pass #adiciona 2
    if dado_rei == 6:
        pass #adidiona 3
    return

turnorei1()
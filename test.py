import pygame
from pygame.locals import *
import os
import sys
from classe import *
from sys import exit
from classe import Regiao, EventCard, Placar
import random

pygame.init()
pygame.display.set_caption('Batalha Pela República')

class ImgBotao:
    def __init__(self, image, regiao):
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.regiao = regiao
     

largura = 1200
altura = 800
#buscar imgs
IMAGEM_BACKGROUND = pygame.transform.scale2x((pygame.image.load(os.path.join('images', 'pergaminho.jpg'))))
IMAGEM_BOTAO_REGIAO1 = (pygame.image.load(os.path.join('images', 'botao_regiao.png')))
IMAGEM_BOTAO_REGIAO2 = (pygame.image.load(os.path.join('images', 'botao_regiao.png')))
IMAGEM_BOTAO_REGIAO3 = (pygame.image.load(os.path.join('images', 'botao_regiao.png')))
IMAGEM_BOTAO_REGIAO4 = (pygame.image.load(os.path.join('images', 'botao_regiao.png')))
IMAGEM_PLACAR = (pygame.image.load(os.path.join('images', 'placar.png')))
IMAGEM_TEXTO = (pygame.image.load(os.path.join('images', 'fundo_texto.png')))
IMAGEM_BOTAO_PROX = (pygame.image.load(os.path.join('images', 'botao_prox.png')))
IMAGEM_BOTAO_PROX = pygame.transform.scale(IMAGEM_BOTAO_PROX, (32*3, 32*3))
FONTE_PONTOS = pygame.font.SysFont('arial', 12, True)
FONTE_TEXTOS = pygame.font.SysFont('microsoftsansserif', 20)
#variaveis universais
tela = pygame.display.set_mode((largura, altura))

#centralizar o background:
bg_centralizado = IMAGEM_BACKGROUND.get_rect()
bg_centralizado.center = (largura/2, altura/2)
tela.blit(IMAGEM_BACKGROUND, (bg_centralizado))
tela.blit(IMAGEM_BOTAO_REGIAO1, (600, 600))
tela.blit(IMAGEM_TEXTO, (330, 10))
tela.blit(IMAGEM_PLACAR, (990, 10))#lugar ótimo já


clock = pygame.time.Clock()
pontos_renderizados = False
intro = True
intro1 = True
intro2 = False
intro3 = False
intro4 = False

#criação de espaços em cada região
norte = Regiao('Norte', 5)
sudes = Regiao('Sudeste', 7)
norde = Regiao('Nordeste', 5)
rio = Regiao('Rio de Janeiro', 4) 
lista_regioes = [norte, sudes, norde, rio]

#criação dos botões
# botao_rio = Botao(IMAGEM_BOTAO_REGIAO1, rio)
# botao_norde = Botao(IMAGEM_BOTAO_REGIAO1, norde)
# botao_norte = Botao(IMAGEM_BOTAO_REGIAO1, norte)
# botao_sudes = Botao(IMAGEM_BOTAO_REGIAO1, sudes)


# botao_rio_tira_mon = Botao(fundo_botao, 'Rio de Janeiro', rio)

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

def tirar_forca():    
    regiao_escolhida = escolher_regiao(lista_regioes)
    if 'm' in regiao_escolhida.total:
        regiao_escolhida.tira_mon(1)
    else:
        print('Não há forças monarquistas nessa região')
        tirar_forca()   

#escolher a região 


#e tirar uma força da região
def tirar_forca():    
    regiao_escolhida = escolher_regiao(lista_regioes)
    if 'm' in regiao_escolhida.total:
        regiao_escolhida.tira_mon(1)
    else:
        print('Não há forças monarquistas nessa região')
        tirar_forca()        
    

def turno_rei():
    print('Mas é claro que você não vai esperar sentado! Seus aliados estarão por todo o país, confabulando para seu poder não diminuir')
    print('A cada dois eventos você jogará outro dado, e com o resultado, poderá aumentar suas forças e diminuir as forças republicanas')
    print(input('Tecle enter para jogar um dado'))
    print('')
    result = random.randint(1, 6)
    print(f"O resultado do dado é {result}")
    print('')
    if result == 1 or result == 2:
        count = 1
        print('Você pode adicionar uma força monarquista a uma região de sua escolha.\nCaso não haja espaços livres, você pode retirar uma força republicana.')
    if result == 3 or result == 4 or result == 5:
        count = 2
        print('Você pode adicionar duas forças monarquistas em regiões de sua escolha.\nCaso não haja espaços livres, você pode retirar forças republicanas.')
    if result == 6:
        count = 3
        print('Você pode adicionar três forças monarquistas em regiões de sua escolha.\nCaso não haja espaços livres, você pode retirar forças republicanas.')
    return count
def ativar_turno_rei():
    a =  turno_rei()   
    while a > 0:
        regiao_escolhida = escolher_regiao(lista_regioes)        
        if 0 not in regiao_escolhida.total and 'r' not in regiao_escolhida.total:
            print('Essa região já está dominada pelos monarquistas')
        elif 0 in regiao_escolhida.total:
            regiao_escolhida.add_mon(1)
            print(f"Você adicionou uma força monarquista no {regiao_escolhida.nome}")
            a-=1        
        else: 
            regiao_escolhida.tira_rep(1)
            print(f"Você retirou uma força republicana do {regiao_escolhida.nome}")
            a-=1
        placar.update()
    if a == 0:
        return

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


    

#criação de espaços em cada região
norte = Regiao('Norte', 5)
sudes = Regiao('Sudeste', 7)
norde = Regiao('Nordeste', 5)
rio = Regiao('Rio de Janeiro', 4) 
lista_regioes = [norte, sudes, norde, rio]

#setup de forças monarquistas
rio.add_mon(3)
norte.add_mon(2)
norde.add_mon(4)
sudes.add_mon(4)

#setup de forças republicanas
rio.add_rep(1)
norte.add_rep(1)
sudes.add_rep(2)

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
placar = Placar(rio.total, norde.total, sudes.total, norte.total)
pontos = placar.update()
# Começo do jogo no prompt
# def comecar_jogo():
    # print('')
    # print('A BATALHA PELA REPÚBLICA')
    # print('')
    # print('O ano é 1889. O Brasil passa por momentos conturbados e as ideias republicanas ameaçam seu poder.\nVocê, o imperador brasileiro D. Pedro II teme que o pior aconteça.')
    # print('Em BATALHA PELA REPÚBLICA seu objetivo é evitar que a república seja proclamada.')
    # print('')
    # print('Mas essa não será uma tarefa fácil.\nPara manter a monarquia intacta, você deve garantir que as forças\nmonarquistas nos confins do país mantenham-se leais à coroa.')
    # print('Tudo isso enquanto as forças republicanas avançam evento após evento.')
    # print('')
    # print('Será que você vai conseguir manter sua dinastia?!')
    # print('')
    # print(input('Tecle ENTER para começar'))
    # print('O país está dividido em três grandes regiões de influência: Norte, Nordeste e Sudeste.\nO Rio de Janeiro, a capital do país, é uma zona de influência à parte.')
    # print('')
    # print('Caso as forças republicanas consigam a maioria das quatro regiões, sua posição de chefe de Estado ficará em grande perigo.')
    # print('Se mesmo após todos os acontecimentos você tiver a maioria do Rio de Janeiro, mas as outras três regiões forem de maioria republicana,\nsua posição ainda estará insustentável')
    # print("")
    # print('Mas como a monarquia é um sistema em que a população minimamente confia, em caso de empate você está grantido como a grande influência da região')
    # print('')
    # print(input('Tecle ENTER para continuar'))
    # print('O cenário político começa favorável à você:')
    # placar.update()
    # print('')    
    # print('A cada evento, você vai jogar um dado, dependendo do resultado, o evento pode tornar sua vida muito mais difícil')
    # print('')
    # a = input('Se entendeu as regras e quer começar, digite "entendi": ')
    # if a == 'entendi':
    #     return
    # else: comecar_jogo()
def comecar_jogo1():
    result = 'A BATALHA PELA REPÚBLICA\nO ano é 1889. O Brasil passa por momentos conturbados e as\nideias republicanas ameaçam seu poder.\nVocê, o imperador brasileiro D. Pedro II, teme que o pior aconteça.\nEm BATALHA PELA REPÚBLICA seu objetivo\né evitar que a república seja proclamada.\nSerá que você vai conseguir manter sua dinastia?!'
    return result
def comecar_jogo2():
    result = 'O país está dividido em três grandes regiões de influência:\nNorte, Nordeste e Sudeste. O Rio de Janeiro, a capital do país, é uma zona de influência à parte.\nCaso as forças republicanas consigam a maioria das quatro regiões, sua posição de chefe de Estado ficará em grande perigo.\nSe mesmo após todos os acontecimentos você tiver a maioria do Rio de Janeiro,\nmas as outras três regiões forem de maioria republicana,\nsua posição ainda estará insustentável\nMas como a monarquia é um sistema em que a população minimamente confia,\nem caso de empate você está grantido como a grande influência da região'    
    return result

def turno():    
    sortear_carta(cartas_restantes)
    placar.update()    
    verificar_fim(norte.total, sudes.total, rio.total, norde.total)


clock.tick(20)


if intro1 == True:
    for event in pygame.event.get():   
        if event.type == pygame.MOUSEBUTTONDOWN:
            text1 = comecar_jogo1()
            texto_na_tela = FONTE_PONTOS.render(text1, True, (0,0,0))
                
            linhas_info = text1.split('\n')
            pos_y = 55  # Posição vertical para começar a renderizar as linhas
            for linha in linhas_info:
                texto_linha = FONTE_PONTOS.render(linha, True, (0, 0, 0))
                pos_x = largura // 2 - texto_linha.get_width() // 2 +35# Centraliza horizontalmente
                tela.blit(texto_linha, (pos_x, pos_y))
                pos_y += texto_linha.get_height() + 5  # Espaçamento entre as linhas
            intro1 = False
            intro2 = True
            pygame.display.flip()
if intro2:       
    if event.type == pygame.MOUSEBUTTONDOWN:
        text2 = comecar_jogo2()
        texto_na_tela2 = FONTE_PONTOS.render(text2, True, (0,0,0))
        pos_y = 110  # Posição vertical para começar a renderizar as linhas            
        pos_x = largura // 2 - texto_na_tela2.get_width() // 2 + 35# Centraliza horizontalmente
        tela.blit(texto_na_tela2, (pos_x, pos_y))
        intro2 = False
        

intro = False
pygame.display.flip()
if intro == False:
                            #isso tudo pro Placar aparecer um abaixo do outro.
    pontos_na_tela = FONTE_PONTOS.render(pontos, True, (0,0,0))
    
    if not pontos_renderizados:
        info_pontos = placar.update()    
        linhas_info = info_pontos.split('\n')
        pos_y = 35  # Posição vertical para começar a renderizar as linhas
        for linha in linhas_info:
            texto_linha = FONTE_PONTOS.render(linha, True, (0, 0, 0))
            pos_x = largura // 2 - texto_linha.get_width() // 2 +490 # Centraliza horizontalmente
            tela.blit(texto_linha, (pos_x, pos_y))
            pos_y += texto_linha.get_height() + 5  # Espaçamento entre as linhas
        pontos_renderizados = True
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    # Atualiza a tela
    pygame.display.update()
# comecar_jogo()
# turn = 1
# print('')
# print(f"Turno {turn}")
# print('')
# turno()
# turn += 1
# print('')
# print(f"Turno {turn}")
# print('')
# turno()
# ativar_turno_rei()
# turn += 1
# print('')
# print(f"Turno {turn}")
# print('')
# turno()
# turn += 1
# print('')
# print(f"Turno {turn}")
# print('')
# turno()
# ativar_turno_rei()
# turn += 1
# print('')
# print(f"Turno {turn}")
# print('')
# turno()
# turn += 1
# print('')
# print(f"Turno {turn}")
# print('')
# turno()
# ativar_turno_rei()
# turn += 1
# print('')
# print(f"Turno {turn}")
# print('')
# turno()

# print('')
# print('Se você chegou até aqui e conseguiu, por sorte ou talento político,\nevitar que a república fosse proclamada, PARABÉNS!\nSeus descendentes continuarão sua linhagem real enquanto o povo brasileiro\nse mantén sobre o domínio cruel de uma família nobre.')
# print('')
# placar.update()
# print('')
# input('Escreva ganhei para sair: ')


# texto_pontos = FONTE_PONTOS.render(f"Pontuação: {placar.update()}", 1, (255, 255, 255))


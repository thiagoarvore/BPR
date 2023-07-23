from classe import Regiao, EventCard, Placar
import random
import sys
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
                        
    return False
#escolher a região 
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
# Começo do jogo
def comecar_jogo():
    print('')
    print('A BATALHA PELA REPÚBLICA')
    print('')
    print('O ano é 1889. O Brasil passa por momentos conturbados e as ideias republicanas ameaçam seu poder.\nVocê, o imperador brasileiro D. Pedro II teme que o pior aconteça.')
    print('Em BATALHA PELA REPÚBLICA seu objetivo é evitar que a república seja proclamada.')
    print('')
    print('Mas essa não será uma tarefa fácil.\nPara manter a monarquia intacta, você deve garantir que as forças\nmonarquistas nos confins do país mantenham-se leais à coroa.')
    print('Tudo isso enquanto as forças republicanas avançam evento após evento.')
    print('')
    print('Será que você vai conseguir manter sua dinastia?!')
    print('')
    print(input('Tecle ENTER para começar'))
    print('O país está dividido em três grandes regiões de influência: Norte, Nordeste e Sudeste.\nO Rio de Janeiro, a capital do país, é uma zona de influência à parte.')
    print('')
    print('Caso as forças republicanas consigam a maioria das quatro regiões, sua posição de chefe de Estado ficará em grande perigo.')
    print('Se mesmo após todos os acontecimentos você tiver a maioria do Rio de Janeiro, mas as outras três regiões forem de maioria republicana,\nsua posição ainda estará insustentável')
    print("")
    print('Mas como a monarquia é um sistema em que a população minimamente confia, em caso de empate você está grantido como a grande influência da região')
    print('')
    print(input('Tecle ENTER para continuar'))
    print('O cenário político começa favorável à você:')
    placar.update()
    print('')    
    print('A cada evento, você vai jogar um dado, dependendo do resultado, o evento pode tornar sua vida muito mais difícil')
    print('')
    a = input('Se entendeu as regras e quer começar, digite "entendi": ')
    if a == 'entendi':
        return
    else: comecar_jogo()

def turno():    
    sortear_carta(cartas_restantes)
    placar.update()    
    verificar_fim(norte.total, sudes.total, rio.total, norde.total)

comecar_jogo()
turn = 1
print('')
print(f"Turno {turn}")
print('')
turno()
turn += 1
print('')
print(f"Turno {turn}")
print('')
turno()
ativar_turno_rei()
turn += 1
print('')
print(f"Turno {turn}")
print('')
turno()
turn += 1
print('')
print(f"Turno {turn}")
print('')
turno()
ativar_turno_rei()
turn += 1
print('')
print(f"Turno {turn}")
print('')
turno()
turn += 1
print('')
print(f"Turno {turn}")
print('')
turno()
ativar_turno_rei()
turn += 1
print('')
print(f"Turno {turn}")
print('')
turno()

print('')
print('Se você chegou até aqui e conseguiu, por sorte ou talento político,\nevitar que a república fosse proclamada, PARABÉNS!\nSeus descendentes continuarão sua linhagem real enquanto o povo brasileiro\nse mantén sobre o domínio cruel de uma família nobre.')
print('')
placar.update()
print('')
input('Escreva ganhei para sair: ')



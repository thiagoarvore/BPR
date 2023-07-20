from classe import Regiao, EventCard

norte = Regiao('Norte', 5)
sudes = Regiao('Sudeste', 7)
norde = Regiao('Nordeste', 5)
rio = Regiao('Rio de Janeiro', 4)

carta1 = EventCard('Lei Áurea', 'Enfim a escravidão foi proibida no Brasil (mas isso não significou uma grande melhoria na vida dos negros)', 
                   norde.tira_mon(2), norde.add_rep(2), sudes.tira_mon(2), sudes.add_rep(2))
carta2 = EventCard('Boom da Borracha', 'O norte do país é inundado de trabalhadores para extrair o látex', 
                   norte.tira_mon(2), norte.add_rep(2))
carta4 = EventCard('Guerra do Paraguai', 'O exército brasileiro volta vitorioso do massacre ocorrido no Paraguai, mas com ideias republicanas cada vez mais presentes', 
                   norte.tira_mon(1), norte.add_rep(1), sudes.tira_mon(3), sudes.add_rep(3), rio.tira_mon(1))
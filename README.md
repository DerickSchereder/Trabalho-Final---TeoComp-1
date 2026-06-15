# Trabalho-Final---TeoComp-1
Linguagem que modela a travessia de um navio cargueiro. O navio pode empilhar e desempilhar containers da sua pilha. Containers que podem ser das categorias light, heavy, food ou toxic (com light contendo tanto toxic quanto food). O navio pode viajar para diferentes portos a qualquer momento, carregando e descarregando carga deles. No final do trajeto a pilha deve estar vazia e o programa gera um relatório completo de todo o trajeto do navio.

Regras da Linguagem:

Anti-Esmagamento: Cargas heavy formam a base. A gramática proíbe que containers do tipo pesado (heavy) fiquem em cima daqueles do tipo leve (food, toxic, ou o próprio tipo genérico light).

Segregação Química: Uma carga de comida não pode coexistir na pilha ao mesmo tempo que uma carga tóxica. As categorias food e toxic ativam ramificações excludentes da gramática.

Domínio Numérico: Categorias leves (light, food, toxic) aceitam de 1 a 999 kg. A categoria heavy exige 4 dígitos numéricos indeo de 1000 a 9999 kg. O peso é validado pela própria gramática.

Rotas Dinâmicas: Escopos permitem a inserção do comando "sail to" em qualquer nível da pilha, viabilizando a troca de carga do topo em portos intermediários.

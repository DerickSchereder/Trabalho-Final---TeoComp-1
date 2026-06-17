import ply.lex as lex
import ply.yacc as yacc

# ==========================================
#  LEXER e definições de tokens
# ==========================================
reserved = {
    'route': 'ROUTE', 'begin': 'BEGIN', 'end': 'END',
    'load': 'LOAD', 'unload': 'UNLOAD', 'sail': 'SAIL', 'to': 'TO',
    'heavy': 'HEAVY', 'light': 'LIGHT', 'food': 'FOOD', 'toxic': 'TOXIC',
    'weight': 'WEIGHT', 'kg': 'KG'
}

tokens = ['NOME', 'PESO_LEVE', 'PESO_HEAVY'] + list(reserved.values())

t_ignore = ' \t\n'

def t_PESO_HEAVY(t):
    r'\b[1-9]\d{3}\b'
    t.value = int(t.value)
    return t

def t_PESO_LEVE(t):
    r'\b[1-9]\d{0,2}\b'
    t.value = int(t.value)
    return t

def t_NOME(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'NOME')
    return t

def t_error(t):
    print(f"Caractere ilegal ignorado: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ==========================================
#  PARSER e definições de produções
# ==========================================
def p_S(p):
    '''s : ROUTE NOME BEGIN fase_heavy END'''
    p[0] = {'route_name': p[2], 'commands': p[4]}

# --- FASE HEAVY ---
def p_fase_heavy_load_heavy(p):
    '''fase_heavy : LOAD HEAVY NOME WEIGHT PESO_HEAVY KG fase_heavy UNLOAD HEAVY fase_heavy'''
    load_cmd = {'action': 'load', 'type': 'heavy', 'name': p[3], 'weight': p[5]}
    unload_cmd = {'action': 'unload', 'type': 'heavy', 'name': p[3], 'weight': p[5]}
    p[0] = [load_cmd] + p[7] + [unload_cmd] + p[10]

def p_fase_heavy_load_light(p):
    '''fase_heavy : LOAD LIGHT NOME WEIGHT PESO_LEVE KG fase_light UNLOAD LIGHT fase_heavy'''
    load_cmd = {'action': 'load', 'type': 'light', 'name': p[3], 'weight': p[5]}
    unload_cmd = {'action': 'unload', 'type': 'light', 'name': p[3], 'weight': p[5]}
    p[0] = [load_cmd] + p[7] + [unload_cmd] + p[10]

def p_fase_heavy_load_food(p):
    '''fase_heavy : LOAD FOOD NOME WEIGHT PESO_LEVE KG fase_food UNLOAD FOOD fase_heavy'''
    load_cmd = {'action': 'load', 'type': 'food', 'name': p[3], 'weight': p[5]}
    unload_cmd = {'action': 'unload', 'type': 'food', 'name': p[3], 'weight': p[5]}
    p[0] = [load_cmd] + p[7] + [unload_cmd] + p[10]

def p_fase_heavy_load_toxic(p):
    '''fase_heavy : LOAD TOXIC NOME WEIGHT PESO_LEVE KG fase_toxic UNLOAD TOXIC fase_heavy'''
    load_cmd = {'action': 'load', 'type': 'toxic', 'name': p[3], 'weight': p[5]}
    unload_cmd = {'action': 'unload', 'type': 'toxic', 'name': p[3], 'weight': p[5]}
    p[0] = [load_cmd] + p[7] + [unload_cmd] + p[10]

def p_fase_heavy_sail(p):
    '''fase_heavy : SAIL TO NOME fase_heavy'''
    p[0] = [{'action': 'sail', 'dest': p[3]}] + p[4]

def p_fase_heavy_empty(p):
    '''fase_heavy : empty'''
    p[0] = []

# --- FASE LIGHT ---
def p_fase_light_load_light(p):
    '''fase_light : LOAD LIGHT NOME WEIGHT PESO_LEVE KG fase_light UNLOAD LIGHT fase_light'''
    load_cmd = {'action': 'load', 'type': 'light', 'name': p[3], 'weight': p[5]}
    unload_cmd = {'action': 'unload', 'type': 'light', 'name': p[3], 'weight': p[5]}
    p[0] = [load_cmd] + p[7] + [unload_cmd] + p[10]

def p_fase_light_load_food(p):
    '''fase_light : LOAD FOOD NOME WEIGHT PESO_LEVE KG fase_food UNLOAD FOOD fase_light'''
    load_cmd = {'action': 'load', 'type': 'food', 'name': p[3], 'weight': p[5]}
    unload_cmd = {'action': 'unload', 'type': 'food', 'name': p[3], 'weight': p[5]}
    p[0] = [load_cmd] + p[7] + [unload_cmd] + p[10]

def p_fase_light_load_toxic(p):
    '''fase_light : LOAD TOXIC NOME WEIGHT PESO_LEVE KG fase_toxic UNLOAD TOXIC fase_light'''
    load_cmd = {'action': 'load', 'type': 'toxic', 'name': p[3], 'weight': p[5]}
    unload_cmd = {'action': 'unload', 'type': 'toxic', 'name': p[3], 'weight': p[5]}
    p[0] = [load_cmd] + p[7] + [unload_cmd] + p[10]

def p_fase_light_sail(p):
    '''fase_light : SAIL TO NOME fase_light'''
    p[0] = [{'action': 'sail', 'dest': p[3]}] + p[4]

def p_fase_light_empty(p):
    '''fase_light : empty'''
    p[0] = []

def p_fase_light_food(p):
    '''fase_light : fase_food'''
    p[0] = p[1]

def p_fase_light_toxic(p):
    '''fase_light : fase_toxic'''
    p[0] = p[1]

# --- FASE FOOD ---

def p_fase_food_sail(p):
    '''fase_food : SAIL TO NOME fase_food'''
    p[0] = [{'action': 'sail', 'dest': p[3]}] + p[4]

def p_fase_food_load_light(p):
    '''fase_food : LOAD LIGHT NOME WEIGHT PESO_LEVE KG fase_food UNLOAD LIGHT fase_food'''
    load_cmd = {'action': 'load', 'type': 'light', 'name': p[3], 'weight': p[5]}
    unload_cmd = {'action': 'unload', 'type': 'light', 'name': p[3], 'weight': p[5]}
    p[0] = [load_cmd] + p[7] + [unload_cmd] + p[10]

def p_fase_food_load_food(p):
    '''fase_food : LOAD FOOD NOME WEIGHT PESO_LEVE KG fase_food UNLOAD FOOD fase_food'''
    load_cmd = {'action': 'load', 'type': 'food', 'name': p[3], 'weight': p[5]}
    unload_cmd = {'action': 'unload', 'type': 'food', 'name': p[3], 'weight': p[5]}
    p[0] = [load_cmd] + p[7] + [unload_cmd] + p[10]

def p_fase_food_empty(p):
    '''fase_food : empty'''
    p[0] = []

# --- FASE TOXIC ---

def p_fase_toxic_load_toxic(p):
    '''fase_toxic : LOAD TOXIC NOME WEIGHT PESO_LEVE KG fase_toxic UNLOAD TOXIC fase_toxic'''
    load_cmd = {'action': 'load', 'type': 'toxic', 'name': p[3], 'weight': p[5]}
    unload_cmd = {'action': 'unload', 'type': 'toxic', 'name': p[3], 'weight': p[5]}
    p[0] = [load_cmd] + p[7] + [unload_cmd] + p[10]

def p_fase_toxic_load_light(p):
    '''fase_toxic : LOAD LIGHT NOME WEIGHT PESO_LEVE KG fase_toxic UNLOAD LIGHT fase_toxic'''
    load_cmd = {'action': 'load', 'type': 'light', 'name': p[3], 'weight': p[5]}
    unload_cmd = {'action': 'unload', 'type': 'light', 'name': p[3], 'weight': p[5]}
    p[0] = [load_cmd] + p[7] + [unload_cmd] + p[10]

def p_fase_toxic_sail(p):
    '''fase_toxic : SAIL TO NOME fase_toxic'''
    p[0] = [{'action': 'sail', 'dest': p[3]}] + p[4]

def p_fase_toxic_empty(p):
    '''fase_toxic : empty'''
    p[0] = []

# --- VAZIO E ERRO ---
def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo ao token '{p.value}'")
    else:
        print("Erro de sintaxe no final da entrada")

parser = yacc.yacc()

# ==========================================
#  INTERPRETADOR e relatório final
# ==========================================

def raise_load_warning(type, count):
    match type:
        case 'heavy':
            return
        case 'food' :
            if count[type] == 0 :
                print('[AVISO]: Alimentos a bordo, proibida a entrada de cargas tóxicas')
        case 'toxic':
            if count[type] == 0 :
                print('[AVISO]: Carga tóxica a bordo, proibida a entrada de alimentos')


def raise_unload_warning(type, count):
    match type:
        case 'heavy':
            return
        case 'food' :
            if count[type] == 1:
                print('[AVISO]: Sem alimentos a bordo, liberada a entrada de cargas tóxicas')
        case 'toxic':
            if count[type] == 1:
                print('[AVISO]: Sem cargas tóxicas a bordo, liberada a entrada de alimentos')

def generate_report(ast):
    print(f"\n\nRELATÓRIO DE NAVEGAÇÃO | {ast['route_name']}")
    print("_"*50 + "\n")

    total_weight = 0
    total_transported_containers = 0
    container_count = {
        'heavy': 0,
        'light': 0,
        'food' : 0,
        'toxic': 0
    }
    porto_atual = 'Porto_inicial'
    print('' + porto_atual + ":")
    for cmd in ast['commands']:

        match cmd['action']:

            case 'sail':
                print(f"\nNAVEGANDO PARA: {cmd['dest']} | Peso a bordo: {total_weight}kg\n")
                porto_atual= cmd['dest']
                print('' + porto_atual + ":")

            case 'load':
                total_weight += cmd['weight']
                total_transported_containers += 1
                print(f"EMBARQUE: {cmd['name']} ({cmd['type']}) - {cmd['weight']}kg")
                raise_load_warning(cmd['type'], container_count)
                container_count[cmd['type']] += 1
                
                

            case 'unload':
                total_weight -= cmd['weight']
                print(f"DESEMBARQUE: {cmd['name']} ({cmd['type']})")
                raise_unload_warning(cmd['type'], container_count)
                container_count[cmd['type']] -= 1
                
    if total_weight == 0 :
        print('\nSTATUS FINAL:')
        print('Pilha vazia e rota concluída.')
        print(f'Numero de cargas transportadas: {total_transported_containers}')
    else: 
        print("ERRO: Carga remanescente no navio.")

import sys
# para rodar o programa: python src/analisador.py inputs/input_1.txt
if __name__ == "__main__":
    # O arquivo é passado como argumento
    if len(sys.argv) > 1:
        nome_arquivo = sys.argv[1]
    else:
        print("Por favor, informe o arquivo de entrada. Exemplo: python analisador.py entrada.txt")
        sys.exit(1)
        
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        codigo = f.read()
        
    resultado_ast = parser.parse(codigo, lexer=lexer)
    if resultado_ast:
        generate_report(resultado_ast)
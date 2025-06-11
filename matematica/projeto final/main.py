import pygame as pg  # Importa a biblioteca Pygame e a renomeia como 'pg'
import random  # Importa a biblioteca random para gerar números aleatórios

# Cores do jogo
branco = (255, 255, 255)
preto = (0, 0, 0)

# Setup da tela
window = pg.display.set_mode((1000, 600))

# Inicializa fontes
pg.font.init()
fonte = pg.font.SysFont("Courier New", 50)
fonte_rb = pg.font.SysFont("Courier New", 30)

# Lista de palavras
palavras = ['PARALELEPIPEDO', 'ORNITORINCO', 'APARTAMENTO', 'XICARA DE CHA']

# Variáveis iniciais
tentativas_de_letras = [' ', '-']
palavra_escolhida = ''
palavra_camuflada = ''
end_game = True
chance = 0
letra = ' '
click_last_status = False


# Desenha a forca com base nas chances
def Desenho_da_Forca(window, chance):
    pg.draw.rect(window, branco, (0, 0, 1000, 600))
    pg.draw.line(window, preto, (100, 500), (100, 100), 10)
    pg.draw.line(window, preto, (50, 500), (150, 500), 10)
    pg.draw.line(window, preto, (100, 100), (300, 100), 10)
    pg.draw.line(window, preto, (300, 100), (300, 150), 10)

    if chance >= 1:
        pg.draw.circle(window, preto, (300, 200), 50, 10)
    if chance >= 2:
        pg.draw.line(window, preto, (300, 250), (300, 350), 10)
    if chance >= 3:
        pg.draw.line(window, preto, (300, 260), (225, 350), 10)
    if chance >= 4:
        pg.draw.line(window, preto, (300, 260), (375, 350), 10)
    if chance >= 5:
        pg.draw.line(window, preto, (300, 350), (375, 450), 10)
    if chance >= 6:
        pg.draw.line(window, preto, (300, 350), (225, 450), 10)


# Desenha o botão de reiniciar
def Desenho_Restart_Button(window):
    pg.draw.rect(window, preto, (700, 100, 200, 65))
    texto = fonte_rb.render('Restart', 1, branco)
    window.blit(texto, (740, 120))


# Sorteia uma palavra nova
def Sorteando_Palavra(palavras, palavra_escolhida, end_game):
    if end_game:
        palavra_n = random.randint(0, len(palavras) - 1)
        palavra_escolhida = palavras[palavra_n]
        end_game = False
    return palavra_escolhida, end_game


# Camufla a palavra escondendo letras não tentadas
def Camuflando_Palavra(palavra_escolhida, palavra_camuflada, tentativas_de_letras):
    palavra_camuflada = palavra_escolhida
    for n in range(len(palavra_camuflada)):
        if palavra_camuflada[n:n + 1] not in tentativas_de_letras:
            palavra_camuflada = palavra_camuflada.replace(palavra_camuflada[n], '#')
    return palavra_camuflada


# Processa a tentativa de letra
def Tentando_uma_Letra(tentativas_de_letras, palavra_escolhida, letra, chance):
    if letra not in tentativas_de_letras:
        tentativas_de_letras.append(letra)
        if letra not in palavra_escolhida:
            chance += 1
    return tentativas_de_letras, chance


# Exibe a palavra na tela
def Palavra_do_Jogo(window, palavra_camuflada):
    palavra = fonte.render(palavra_camuflada, 1, preto)
    window.blit(palavra, (200, 500))


# Reinicia o jogo se o botão for clicado
def Restart_do_Jogo(palavra_camuflada, end_game, chance, letra,
                    tentativas_de_letras, click_last_status, click, x, y):
    count = 0
    limite = len(palavra_camuflada)

    for n in range(len(palavra_camuflada)):
        if palavra_camuflada[n] != '#':
            count += 1

    if count == limite and click_last_status is False and click[0] is True:
        if 700 <= x <= 900 and 100 <= y <= 165:
            tentativas_de_letras = [' ', '-']
            end_game = True
            chance = 0
            letra = ' '

    return end_game, chance, tentativas_de_letras, letra


# Loop principal do jogo
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    x, y = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    Desenho_da_Forca(window, chance)
    Desenho_Restart_Button(window)

    palavra_escolhida, end_game = Sorteando_Palavra(palavras, palavra_escolhida, end_game)
    palavra_camuflada = Camuflando_Palavra(palavra_escolhida, palavra_camuflada, tentativas_de_letras)
    Palavra_do_Jogo(window, palavra_camuflada)

    end_game, chance, tentativas_de_letras, letra = Restart_do_Jogo(
        palavra_camuflada, end_game, chance, letra, tentativas_de_letras, click_last_status, click, x, y)

    click_last_status = click[0]
    
    pg.display.update()
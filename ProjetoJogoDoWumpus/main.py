import pygame
import random
import time
import sys

def check_neighbor_rooms(pos, item_list):
    exits = cave[pos]
    return any(item in cave[pos] for item in item_list)


def draw_room(pos, screen):
    x = 0
    y = 1
    exits = cave[player_pos]
    screen.fill((0, 0, 0))  # pinte o fundo de preto

    # desenhe o círculo da sala em marrom
    circle_radius = int((SCREEN_WIDTH // 2) * .75)
    pygame.draw.circle(screen, BROWN, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), circle_radius, 0)

    # em seguida, desenhe todas as saídas da sala
    if exits[LEFT] > 0:
        left = 0
        top = SCREEN_HEIGHT // 2 - 40
        pygame.draw.rect(screen, BROWN, ((left, top), (SCREEN_WIDTH // 4, 80)), 0)
    if exits[RIGHT] > 0:
        # desenhe a saída certa
        left = SCREEN_WIDTH - (SCREEN_WIDTH // 4)
        top = SCREEN_HEIGHT // 2 - 40
        pygame.draw.rect(screen, BROWN, ((left, top), (SCREEN_WIDTH // 4, 80)), 0)
    if exits[UP] > 0:
        # desenhar saída superior
        left = SCREEN_WIDTH // 2 - 40
        top = 0
        pygame.draw.rect(screen, BROWN, ((left, top), (80, SCREEN_HEIGHT // 4)), 0)
    if exits[DOWN] > 0:
        # desenhar saída inferior
        left = SCREEN_WIDTH // 2 - 40
        top = SCREEN_HEIGHT - (SCREEN_WIDTH // 4)
        pygame.draw.rect(screen, BROWN, ((left, top), (80, SCREEN_HEIGHT // 4)), 0)

    # descobrir se ouro, buraco ou um wumpus está próximo
    bats_near = check_neighbor_rooms(player_pos, bats_list)
    pit_near = check_neighbor_rooms(player_pos, pits_list)
    wumpus_near = check_neighbor_rooms(player_pos, [wumpus_pos, [-1, -1]])

    # desenhe um círculo de sangue se o Wumpus estiver próximo
    if wumpus_near == True:
        circle_radius = int((SCREEN_WIDTH // 2) * .5)
        pygame.draw.circle(screen, RED, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), circle_radius, 0)

    # ddesenhe o poço em preto se estiver presente
    if player_pos in pits_list:
        circle_radius = int((SCREEN_WIDTH // 2) * .5)
        pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), circle_radius, 0)

    # desenha o jogador
    screen.blit(player_img,
                (SCREEN_WIDTH // 2 - player_img.get_width() // 2, SCREEN_HEIGHT // 2 - player_img.get_height() // 2))

    # desenhe a imagem do morcego
    if player_pos in bats_list:
        screen.blit(bat_img,
                    (SCREEN_WIDTH // 2 - bat_img.get_width() // 2, SCREEN_HEIGHT // 2 - bat_img.get_height() // 2))

    # desenhe o wumpus
    if player_pos == wumpus_pos:
        screen.blit(wumpus_img, (
            SCREEN_WIDTH // 2 - wumpus_img.get_width() // 2, SCREEN_HEIGHT // 2 - wumpus_img.get_height() // 2))

    # desenhar texto
    y_text_pos = 0  # acompanha a próxima posição na tela para desenhar texto
    pos_text = font.render("POS:" + str(player_pos), 1, (0, 255, 64))
    screen.blit(pos_text, (0, 0))
    arrow_text = font.render("Arrows: " + str(num_arrows), 1, (0, 255, 64))
    y_text_pos = y_text_pos + pos_text.get_height() + 10
    screen.blit(arrow_text, (0, y_text_pos))
    if bats_near == True:
        bat_text = font.render("Você viu um bilho amarelado!", 1, (0, 255, 64))
        y_text_pos = y_text_pos + bat_text.get_height() + 10
        screen.blit(bat_text, (0, y_text_pos))
    if pit_near == True:
        pit_text = font.render("Você esta sentindo um vento por perto!", 1, (0, 255, 64))
        y_text_pos = y_text_pos + pit_text.get_height() + 10
        screen.blit(pit_text, (0, y_text_pos))

    if wumpus_near == True:
        pit_text = font.render("Você esta sentindo um odor forte por perto!", 1, (0, 255, 64))
        y_text_pos = y_text_pos + pit_text.get_height() + 10
        screen.blit(pit_text, (0, y_text_pos))

    if player_pos in bats_list:  # se os morcegos estiverem aqui, vá em frente e vire a tela e espere um pouco
        pygame.display.flip()
        time.sleep(2.0)


def populate_cave():
    global player_pos, wumpus_pos

    #
    # coloque o jogador
    player_pos = random.randint(1, 20)

    # coloque wumpus
    place_wumpus()

    # coloque bats
    for bat in range(0, NUM_BATS):
        place_bat()

    # place the pits
    for pit in range(0, NUM_PITS):
        place_pit()

    # coloque as flechas
    for arrow in range(0, NUM_ARROWS):
        place_arrow()

    print("Player at: " + str(player_pos))
    print("Wumpus at: " + str(wumpus_pos))
    print("Bats at:" + str(bats_list))
    print("Pits at:" + str(pits_list))
    print("Arrows at:" + str(arrows_list))


def place_wumpus():
    global player_pos, wumpus_pos

    wumpus_pos = player_pos
    while (wumpus_pos == player_pos):
        wumpus_pos = random.randint(0, 20)


def place_bat():
    # coloque os morcegos
    bat_pos = player_pos
    while bat_pos == player_pos or (bat_pos in bats_list) or (bat_pos == wumpus_pos) or (bat_pos in pits_list):
        bat_pos = random.randint(1, 20)
    bats_list.append(bat_pos)


def place_pit():
    pit_pos = player_pos
    while (pit_pos == player_pos) or (pit_pos in bats_list) or (pit_pos == wumpus_pos) or (pit_pos in pits_list):
        pit_pos = random.randint(1, 20)
    pits_list.append(pit_pos)


def place_arrow():
    arrow_pos = player_pos
    while (arrow_pos == player_pos) or (arrow_pos in bats_list) or (arrow_pos == wumpus_pos) or (
            arrow_pos in pits_list):
        arrow_pos = random.randint(1, 20)
    arrows_list.append(arrow_pos)


def check_room(pos):
    global player_pos, screen, num_arrows

    # há um Wumpus na sala?
    if player_pos == wumpus_pos:
        game_over("Você foi comido por um WUMPUS!!!")

    # há um poço?
    if player_pos in pits_list:
        game_over("Você caiu em um buraco sem fundo!!")

    # há morcegos no quarto? Se assim for, mova o jogador e os morcegos
    if player_pos in bats_list:
        print("você achou o pote de ouro!!!")
        screen.fill(BLACK)
        bat_text = font.render("Vitoria!", 1, (0, 255, 64))
        textrect = bat_text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = screen.get_rect().centery
        screen.blit(bat_text, textrect)
        pygame.display.flip()
        time.sleep(2.5)

        # mover os morcegos
        new_pos = player_pos

        while (new_pos == player_pos) or (new_pos in bats_list) or (new_pos == wumpus_pos) or (new_pos in pits_list):
            new_pos = random.randint(1, 20)
        bats_list.remove(player_pos)
        bats_list.append(new_pos)
        print("bat at: " + str(new_pos))

        # agora mova o jogador
        new_pos = player_pos  # defina new_pos igual ao sistema operacional antigo para que o primeiro teste falhe
        # Agora coloque o jogador em um local aleatório
        while (new_pos == player_pos) or (new_pos in bats_list) or (new_pos == wumpus_pos) or (new_pos in pits_list):
            new_pos = random.randint(1, 20)
        player_pos = new_pos
        print("player at:" + str(player_pos))

    # há uma flecha na sala?
    if player_pos in arrows_list:
        screen.fill(BLACK)
        text = font.render("Você encontrou uma lança!", 1, (0, 255, 64))
        textrect = text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = screen.get_rect().centery
        screen.blit(text, textrect)
        pygame.display.flip()
        time.sleep(2.5)
        num_arrows += 1
        arrows_list.remove(player_pos)


def reset_game():
    global num_arrows
    populate_cave()
    num_arrows = 1


def game_over(message):
    global screen
    time.sleep(1.0)
    screen.fill(RED)
    text = font.render(message, 1, (0, 255, 64))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery
    screen.blit(text, textrect)
    pygame.display.flip()
    time.sleep(2.5)
    print(message)
    pygame.quit()
    sys.exit()


def move_wumpus():
    global wumpus_pos

    if mobile_wumpus == False or random.randint(1, 100) > wumpus_move_chance:
        return

    exits = cave[wumpus_pos]

    for new_room in exits:
        if new_room == 0:
            continue
        elif new_room == player_pos:
            continue
        elif new_room in bats_list:
            continue
        elif new_room in pits_list:
            continue
        else:
            wumpus_pos = new_room
            break

    print("Wumpus mudou-se para:" + str(wumpus_pos))


def shoot_arrow(direction):
    global num_arrows, player_pos

    hit = False

    if num_arrows == 0:
        return False
    num_arrows -= 1

    if wumpus_pos == cave[player_pos][direction]:
        hit = True

    if hit == True:
        game_over("Você matou o Wumpus!")
        pygame.quit()
        sys.exit()
    else:
        print("Errouuuuu, você perdeu sua flecha na escuridão da caverna!")
        place_wumpus()
    if num_arrows == 0:
        game_over("Você perdeu sua lança, Game Over!")
        pygame.quit()
        sys.exit()


def check_pygame_events():
    global player_pos
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_LEFT:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(LEFT)
            elif cave[player_pos][LEFT] > 0:
                player_pos = cave[player_pos][LEFT]
                move_wumpus()
        elif event.key == pygame.K_RIGHT:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(RIGHT)
            elif cave[player_pos][RIGHT] > 0:
                player_pos = cave[player_pos][RIGHT]
                move_wumpus()
        elif event.key == pygame.K_UP:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(UP)
            elif cave[player_pos][UP] > 0:
                player_pos = cave[player_pos][UP]
                move_wumpus()
        elif event.key == pygame.K_DOWN:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(DOWN)
            elif cave[player_pos][DOWN] > 0:
                player_pos = cave[player_pos][DOWN]
                move_wumpus()


def print_instructoions():
    print(
        '''
                                   Caçar ao tesouro
    ▪ O local do ouro e do Wumpus devem mudar a cada execução▪
    ▪ O agente precisa conseguir reconhecer o brilho do ouro, o vento dos buracos e o cheiro do Wumpus▪
    ▪ O agente deve ser capaz de encontrar o tesouro sozinho e voltar a posição inicial▪
    ▪ O agente deve possuir apenas 1 flecha e só pode atirar para o lado em que ele estiver virado▪
    ▪ O agente apenas anda para esquerda, direita, abaixo e acima
    ▪ O agente deve iniciar na posição 1x1
    ▪A linguagem de programação é livre
        '''
    )



# Nossa largura e altura da tela
SCREEN_WIDTH = SCREEN_HEIGHT = 800

# número de morcegos, poços e flechas na caverna#carregue nossas três imagens
bat_img = pygame.image.load('bat.png')
player_img = pygame.image.load('player.png')
wumpus_img = pygame.image.load('wumpus.png')
arrow_img = pygame.image.load('arrow.png')
# aumente o número de morcegos e buracos para dificultar
# aumente o número de setas para facilitar
NUM_BATS = 3
NUM_PITS = 3
NUM_ARROWS = 0

player_pos = 0  # trilhas onde estamos na caverna
wumpus_pos = 0  # rastreia onde está o Wumpus
num_arrows = 1  # setas iniciais
mobile_wumpus = False  # Defina como true para permitir que o wumpus se mova
wumpus_move_chance = 50

# constantes para direções
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# definições de cores
BROWN = 193, 154, 107
BLACK = 0, 0, 0
RED = 138, 7, 7

cave = {1: [0, 8, 2, 5], 2: [0, 10, 3, 1], 3: [0, 12, 4, 2], 4: [0, 14, 5, 3],
        5: [0, 6, 1, 4], 6: [5, 0, 7, 15], 7: [0, 17, 8, 6], 8: [1, 0, 9, 7],
        9: [0, 18, 10, 8], 10: [2, 0, 11, 9], 11: [0, 19, 12, 10], 12: [3, 0, 13, 11],
        13: [0, 20, 14, 12], 14: [4, 0, 15, 13], 15: [0, 16, 6, 14], 16: [15, 0, 17, 20],
        17: [7, 0, 18, 16], 18: [9, 0, 19, 17], 19: [11, 0, 20, 18], 20: [13, 0, 16, 19]}

bats_list = []
pits_list = []
arrows_list = []


print_instructoions()
input("Press <ENTER> para começar.")
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Hunt the Wumpus")

# carregue nossas três imagens
bat_img = pygame.image.load('bat.png')
player_img = pygame.image.load('player.png')
wumpus_img = pygame.image.load('wumpus.png')
arrow_img = pygame.image.load('arrow.png')

# configurar nossa fonte
font = pygame.font.Font(None, 40)

# Obtenha as configurações iniciais do jogo
reset_game()

#loop

while True:
    check_pygame_events()
    draw_room(player_pos, screen)
    pygame.display.flip()
    check_room(player_pos)

import pygame
import random
import sys

# -----------------------------
# Configurações básicas
# -----------------------------
LARGURA = 320
ALTURA = 480
FPS = 60

COR_FUNDO = (18, 18, 18)
COR_PASSARO = (255, 208, 0)
COR_CANO = (80, 200, 120)
COR_CHÃO = (40, 40, 40)
COR_TEXTO = (230, 230, 230)

GRAVIDADE = 0.35
IMPULSO = -7.5
VEL_CANO = -3
LARGURA_CANO = 48
ESPACO_CANO = 120
DIST_CANO = 180  # distância horizontal entre canos
ALTURA_CHAO = 40

pygame.init()
pygame.display.set_caption("Flappy Minimal (Python + pygame)")
tela = pygame.display.set_mode((LARGURA, ALTURA))
# Descomente a linha abaixo para iniciar o jogo MINIMIZADO:
# pygame.display.iconify()
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 20, bold=True)

# -----------------------------
# Funções utilitárias
# -----------------------------
def desenhar_texto(surface, texto, x, y, cor=COR_TEXTO, centro=False):
    img = fonte.render(texto, True, cor)
    rect = img.get_rect()
    if centro:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)

def criar_par_canos(x):
    """Cria um par (topo, base) com abertura aleatória."""
    # Limites para a abertura para não gerar impossível
    margem_superior = 40
    margem_inferior = 80
    altura_topo = random.randint(margem_superior, ALTURA - ALTURA_CHAO - margem_inferior - ESPACO_CANO)
    cano_topo = pygame.Rect(x, 0, LARGURA_CANO, altura_topo)
    cano_base = pygame.Rect(x, altura_topo + ESPACO_CANO, LARGURA_CANO, ALTURA - ALTURA_CHAO - (altura_topo + ESPACO_CANO))
    return cano_topo, cano_base

def resetar_jogo():
    # Pássaro
    passaro = pygame.Rect(60, ALTURA//2 - 12, 24, 24)
    vel_y = 0.0
    # Canos
    canos = []
    x_inicial = LARGURA + 40
    for i in range(3):
        canos.extend(criar_par_canos(x_inicial + i * DIST_CANO))
    # Estado
    score = 0
    vivo = True
    pronto = True  # aguarda primeiro espaço
    return passaro, vel_y, canos, score, vivo, pronto

def colisao(passaro, canos):
    if passaro.top <= 0:
        return True
    if passaro.bottom >= ALTURA - ALTURA_CHAO:
        return True
    for topo, base in zip(canos[0::2], canos[1::2]):
        if passaro.colliderect(topo) or passaro.colliderect(base):
            return True
    return False

# -----------------------------
# Estado inicial
# -----------------------------
passaro, vel_y, canos, score, vivo, pronto = resetar_jogo()
# Para contar pontuação quando o pássaro passa do meio do cano
canos_pontuados = set()

# -----------------------------
# Loop principal
# -----------------------------
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if evento.key == pygame.K_r:
                passaro, vel_y, canos, score, vivo, pronto = resetar_jogo()
                canos_pontuados.clear()
            if evento.key == pygame.K_SPACE and vivo:
                pronto = False
                vel_y = IMPULSO

    if vivo and not pronto:
        # Física do pássaro
        vel_y += GRAVIDADE
        passaro.y += vel_y

        # Mover canos
        for i in range(len(canos)):
            canos[i].x += VEL_CANO

        # Remover canos que saíram da tela e criar novos
        if canos and canos[0].right < 0:
            # Remove o par mais à esquerda (dois primeiros)
            canos = canos[2:]
            # Adiciona um novo par no fim
            x_ultimo = max(canos[-1].x, canos[-2].x) if len(canos) >= 2 else LARGURA
            novo_topo, novo_base = criar_par_canos(x_ultimo + DIST_CANO)
            canos.extend((novo_topo, novo_base))

        # Colisão
        if colisao(passaro, canos):
            vivo = False

        # Pontuação: quando o centro do pássaro ultrapassa o centro do cano
        for idx, (topo, base) in enumerate(zip(canos[0::2], canos[1::2])):
            centro_cano = topo.centerx
            if centro_cano < passaro.centerx and idx not in canos_pontuados:
                score += 1
                canos_pontuados.add(idx)

    # -----------------------------
    # Desenho
    # -----------------------------
    tela.fill(COR_FUNDO)

    # Céu simples (opcional: linhas discretas)
    # pygame.draw.line(tela, (25, 25, 25), (0, 60), (LARGURA, 60), 1)

    # Canos
    for topo, base in zip(canos[0::2], canos[1::2]):
        pygame.draw.rect(tela, COR_CANO, topo, border_radius=6)
        pygame.draw.rect(tela, COR_CANO, base, border_radius=6)

    # Chão
    chao_rect = pygame.Rect(0, ALTURA - ALTURA_CHAO, LARGURA, ALTURA_CHAO)
    pygame.draw.rect(tela, COR_CHÃO, chao_rect)

    # Pássaro (quadrado arredondado)
    pygame.draw.rect(tela, COR_PASSARO, passaro, border_radius=6)

    # UI
    desenhar_texto(tela, f"Score: {score}", 8, 6)
    if pronto and vivo:
        desenhar_texto(tela, "Pressione ESPAÇO para começar", LARGURA//2, ALTURA//2 - 10, centro=True)
        desenhar_texto(tela, "R = reiniciar | Esc = sair", LARGURA//2, ALTURA//2 + 16, centro=True)
    if not vivo:
        desenhar_texto(tela, "Game Over", LARGURA//2, ALTURA//2 - 14, centro=True)
        desenhar_texto(tela, "Pressione R para reiniciar", LARGURA//2, ALTURA//2 + 10, centro=True)

    pygame.display.flip()
    relogio.tick(FPS)

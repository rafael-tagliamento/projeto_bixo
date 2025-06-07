import pygame
import random

# Inicializa o Pygame
pygame.init()

# --- Configurações da Janela e Cores ---
LARGURA_TELA = 800
ALTURA_TELA = 400
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo do Dinossauro")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (100, 100, 100)

# --- Variáveis do Jogo ---
ALTURA_CHAO = ALTURA_TELA - 50
velocidade_jogo = 10
pontuacao = 0
game_over = False

# --- Configurações do Dinossauro (um ponto/quadrado) ---
dino_x = 50
dino_y = ALTURA_CHAO - 20
dino_largura = 20
dino_altura = 20
dino_velocidade_y = 0
gravidade = 1
forca_pulo = -20
esta_pulando = False

# --- Configurações dos Obstáculos ---
obstaculos = []
obstaculo_largura = 20
obstaculo_altura = 40
tempo_para_proximo_obstaculo = 0

# --- Fonte para o Placar ---
fonte = pygame.font.Font(None, 36)

# --- Relógio para controlar o FPS ---
clock = pygame.time.Clock()

def desenhar_elementos():
    """Desenha todos os elementos do jogo na tela."""
    # Fundo branco
    tela.fill(BRANCO)
    
    # Chão
    pygame.draw.line(tela, CINZA, (0, ALTURA_CHAO), (LARGURA_TELA, ALTURA_CHAO), 2)
    
    # Dinossauro (um quadrado preto)
    pygame.draw.rect(tela, PRETO, (dino_x, dino_y, dino_largura, dino_altura))
    
    # Obstáculos
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, PRETO, obstaculo)
        
    # Placar
    texto_pontuacao = fonte.render(f"Pontos: {int(pontuacao)}", True, PRETO)
    tela.blit(texto_pontuacao, (10, 10))
    
    # Tela de Game Over
    if game_over:
        texto_game_over = fonte.render("FIM DE JOGO - Pressione 'R' para reiniciar", True, PRETO)
        rect_game_over = texto_game_over.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2))
        tela.blit(texto_game_over, rect_game_over)
        
    # Atualiza a tela
    pygame.display.flip()

def reiniciar_jogo():
    """Reseta todas as variáveis para começar um novo jogo."""
    global dino_y, dino_velocidade_y, esta_pulando, pontuacao, velocidade_jogo, obstaculos, game_over
    dino_y = ALTURA_CHAO - dino_altura
    dino_velocidade_y = 0
    esta_pulando = False
    pontuacao = 0
    velocidade_jogo = 10
    obstaculos = []
    game_over = False


# --- Loop Principal do Jogo ---
rodando = True
while rodando:
    
    for event in pygame.event.get():
        # Evento para fechar a janela
        if event.type == pygame.QUIT:
            rodando = False
        
        # Evento para pressionar uma tecla
        if event.type == pygame.KEYDOWN:
            # Pular com a tecla ESPAÇO se não estiver pulando
            if event.key == pygame.K_SPACE and not esta_pulando and not game_over:
                esta_pulando = True
                dino_velocidade_y = forca_pulo
            
            # Reiniciar com a tecla R se o jogo acabou
            if event.key == pygame.K_r and game_over:
                reiniciar_jogo()

    if not game_over:
        # --- Lógica de Movimento e Física ---
        
        # Aplicar gravidade se o dino estiver no ar
        if esta_pulando:
            dino_velocidade_y += gravidade
            dino_y += dino_velocidade_y
        
        # Verificar se o pulo terminou (tocou o chão)
        if dino_y >= ALTURA_CHAO - dino_altura:
            dino_y = ALTURA_CHAO - dino_altura
            esta_pulando = False
            dino_velocidade_y = 0
            
        # --- Lógica dos Obstáculos ---
        
        # Gerar novos obstáculos
        tempo_para_proximo_obstaculo -= 1
        if tempo_para_proximo_obstaculo <= 0:
            novo_obstaculo = pygame.Rect(
                LARGURA_TELA,
                ALTURA_CHAO - obstaculo_altura,
                obstaculo_largura,
                obstaculo_altura
            )
            obstaculos.append(novo_obstaculo)
            # Define o tempo para o próximo obstáculo de forma aleatória
            tempo_para_proximo_obstaculo = random.randint(40, 100)

        # Mover obstáculos existentes
        for obstaculo in obstaculos:
            obstaculo.x -= velocidade_jogo
            
        # Remover obstáculos que saíram da tela
        obstaculos = [obs for obs in obstaculos if obs.right > 0]
        
        # --- Lógica de Colisão e Pontuação ---
        
        # Criar um retângulo para a posição atual do dinossauro
        dino_rect = pygame.Rect(dino_x, dino_y, dino_largura, dino_altura)
        
        for obstaculo in obstaculos:
            if dino_rect.colliderect(obstaculo):
                game_over = True
                
        # Aumentar a pontuação e a velocidade
        pontuacao += 0.1
        if int(pontuacao) % 100 == 0 and pontuacao > 1:
            velocidade_jogo += 0.5
    
    # --- Desenhar tudo na tela ---
    desenhar_elementos()
    
    # Controlar a velocidade do jogo (frames por segundo)
    clock.tick(60)

# Finaliza o Pygame ao sair do loop
pygame.quit()
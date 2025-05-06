import pygame
import math
import sys

####################################################################################
# Classes
####################################################################################

# Representa um ponto no espaço 2D
class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Representa um polígono regular e suas transformações
class Poligono:
    def __init__(self, n_lados, raio, centro):
        self.n_lados = n_lados
        self.raio = raio
        self.centro = centro  # Tupla (x, y)
        self.pontos = self.gerar_pontos()

    def gerar_pontos(self):
        # Gera os vértices do polígono regular
        pontos = []
        cx, cy = self.centro
        for i in range(self.n_lados):
            angulo = 2 * math.pi * i / self.n_lados
            x = cx + self.raio * math.cos(angulo)
            y = cy + self.raio * math.sin(angulo)
            pontos.append(Ponto(x, y))
        return pontos

    # Aplica translação
    def transladar(self, dx, dy):
        for ponto in self.pontos:
            ponto.x += dx
            ponto.y += dy
        cx, cy = self.centro
        self.centro = (cx + dx, cy + dy)

    # Aplica rotação em torno do centro
    def rotacionar(self, angulo_rad):
        cx, cy = self.centro
        for ponto in self.pontos:
            x_rel = ponto.x - cx
            y_rel = ponto.y - cy
            x_rot = x_rel * math.cos(angulo_rad) - y_rel * math.sin(angulo_rad)
            y_rot = x_rel * math.sin(angulo_rad) + y_rel * math.cos(angulo_rad)
            ponto.x = cx + x_rot
            ponto.y = cy + y_rot

    # Aplica escalamento em relação ao centro
    def escalar(self, fator):
        cx, cy = self.centro
        for ponto in self.pontos:
            ponto.x = cx + (ponto.x - cx) * fator
            ponto.y = cy + (ponto.y - cy) * fator
        self.raio *= fator

    # Aplica cisalhamento horizontal e vertical
    def cisalhar(self, shx, shy):
        cx, cy = self.centro
        for ponto in self.pontos:
            x_rel = ponto.x - cx
            y_rel = ponto.y - cy
            ponto.x = cx + x_rel + shx * y_rel
            ponto.y = cy + y_rel + shy * x_rel

    # Atualiza o número de lados do polígono
    def atualizar_lados(self, novo_n):
        self.n_lados = max(3, novo_n)
        self.pontos = self.gerar_pontos()

    # Desenha o polígono na tela
    def desenhar(self, tela, cor=(255, 255, 255)):
        for i in range(len(self.pontos)):
            p1 = self.pontos[i]
            p2 = self.pontos[(i + 1) % len(self.pontos)]
            pygame.draw.line(tela, cor, (p1.x, p1.y), (p2.x, p2.y), 2)

####################################################################################
# Configs default
####################################################################################

LARGURA = 800
ALTURA = 600
FPS = 60

####################################################################################
# Iniciando a lib pygame
####################################################################################

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Polígono com Transformações")
clock = pygame.time.Clock()

####################################################################################
# Poligono padrão
####################################################################################

centro_inicial = (LARGURA // 2, ALTURA // 2)
poligono = Poligono(n_lados=5, raio=100, centro=centro_inicial)

# Estados de controle para modos e teclas
modo_circulo = False
modo_elipse = False
n_lados_padrao = 5
n_lados_circulo = 100
raio_x = 100
raio_y = 100
tecla_p_pressionada = False
tecla_o_pressionada = False

####################################################################################
# Função para gerar elipse
####################################################################################

def gerar_elipse(centro, raio_x, raio_y, n_lados):
    pontos = []
    cx, cy = centro
    for i in range(n_lados):
        angulo = 2 * math.pi * i / n_lados
        x = cx + raio_x * math.cos(angulo)
        y = cy + raio_y * math.sin(angulo)
        pontos.append(Ponto(x, y))
    pol = Poligono(n_lados, 1, centro)
    pol.pontos = pontos
    return pol

####################################################################################
# Bloco principal
####################################################################################

rodando = True
while rodando:
    clock.tick(FPS)
    tela.fill((0, 0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.KEYDOWN:
            # Alterna entre polígono padrão e círculo
            if evento.key == pygame.K_p and not tecla_p_pressionada:
                tecla_p_pressionada = True
                modo_circulo = not modo_circulo
                if modo_circulo:
                    poligono = Poligono(n_lados=n_lados_circulo, raio=100, centro=centro_inicial)
                else:
                    poligono = Poligono(n_lados=n_lados_padrao, raio=100, centro=centro_inicial)

        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_p:
                tecla_p_pressionada = False
            # Alterna entre polígono e elipse
            if evento.key == pygame.K_o and not tecla_o_pressionada:
                tecla_o_pressionada = True
                modo_elipse = not modo_elipse
                if modo_elipse:
                    poligono = gerar_elipse(centro_inicial, raio_x, raio_y, n_lados_circulo)
                else:
                    poligono = Poligono(n_lados=n_lados_padrao, raio=100, centro=centro_inicial)
            elif evento.key == pygame.K_o:
                tecla_o_pressionada = False

    # Controles do teclado
    teclas = pygame.key.get_pressed()

    # Transformações geométricas
    if teclas[pygame.K_LEFT]: poligono.transladar(-5, 0)
    if teclas[pygame.K_RIGHT]: poligono.transladar(5, 0)
    if teclas[pygame.K_UP]: poligono.transladar(0, -5)
    if teclas[pygame.K_DOWN]: poligono.transladar(0, 5)

    if teclas[pygame.K_a]: poligono.rotacionar(-0.05)
    if teclas[pygame.K_d]: poligono.rotacionar(0.05)

    if teclas[pygame.K_w]: poligono.escalar(1.01)
    if teclas[pygame.K_s]: poligono.escalar(0.99)

    if teclas[pygame.K_q]: poligono.cisalhar(0.01, 0)
    if teclas[pygame.K_e]: poligono.cisalhar(-0.01, 0)
    if teclas[pygame.K_z]: poligono.cisalhar(0, 0.01)
    if teclas[pygame.K_c]: poligono.cisalhar(0, -0.01)

    if teclas[pygame.K_EQUALS] or teclas[pygame.K_KP_PLUS]:
        poligono.atualizar_lados(poligono.n_lados + 1)
    if teclas[pygame.K_MINUS] or teclas[pygame.K_KP_MINUS]:
        poligono.atualizar_lados(poligono.n_lados - 1)

    # Controle dos raios da elipse
    if modo_elipse:
        if teclas[pygame.K_l]:
            raio_x += 1
            poligono = gerar_elipse(centro_inicial, raio_x, raio_y, n_lados_circulo)
        if teclas[pygame.K_j]:
            raio_x = max(10, raio_x - 1)
            poligono = gerar_elipse(centro_inicial, raio_x, raio_y, n_lados_circulo)
        if teclas[pygame.K_i]:
            raio_y += 1
            poligono = gerar_elipse(centro_inicial, raio_x, raio_y, n_lados_circulo)
        if teclas[pygame.K_k]:
            raio_y = max(10, raio_y - 1)
            poligono = gerar_elipse(centro_inicial, raio_x, raio_y, n_lados_circulo)

    # Desenho
    poligono.desenhar(tela)
    pygame.display.flip()

####################################################################################
# Finalização
####################################################################################

pygame.quit()
sys.exit()

####################################################################################
# Atalhos
####################################################################################

# ⬆ - Move para cima
# ⬇ - Move para baixo
# ⬅ - Move para esquerda
# ➡ - Move para direita

# A - Gira o poligono para esquerda
# D - Gira o poligono para direita

# W - Aumenta o tamanho do poligono
# S - Diminui o tamanho do poligono 

# Q - Cisalhamento horizontal
# E - Cisalhamento horizontal
# Z -  Cisalhamento vertical
# C - Cisalhamento vertical

# ➕ Aumenta o numero de lados 
# ➖ Diminui o numero de lados

# P - Alternar entre poligono padrão e circulo com 100 lados

# I - Controla altura da elipse
# K - Controla altura da elipse
# J - Controla largura da elipse
# L - Controla largura da elipse
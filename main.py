import pygame
import random
import sys
import math
import os

pygame.init()

LARGURA, ALTURA = 480, 720
FPS = 60

COR_FUNDO = (0, 200, 220)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Bird")
relogio = pygame.time.Clock()

fonte_media  = pygame.font.SysFont("Arial Rounded MT Bold", 36, bold=True)
fonte_pequena = pygame.font.SysFont("Arial Rounded MT Bold", 24)
DESTAQUE_UI  = (255, 200, 0)

DIR_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

def carregar_sprite(nome_arquivo):
    caminho_assets = os.path.join(DIR_ASSETS, nome_arquivo)
    caminho_local  = os.path.join(os.path.dirname(os.path.abspath(__file__)), nome_arquivo)
    for caminho in (caminho_assets, caminho_local, nome_arquivo):
        if os.path.exists(caminho):
            return pygame.image.load(caminho).convert_alpha()
    raise FileNotFoundError(
        f"Sprite '{nome_arquivo}' não encontrado.\n"
        f"Coloque os arquivos superman.png, kriptonita.png e metropolis.png\n"
        f"na mesma pasta do jogo ou em uma subpasta 'assets/'."
    )

try:
    surf_passaro      = pygame.transform.scale(carregar_sprite("superman.png"), (100, 62))
    surf_k_full       = carregar_sprite("kriptonita.png")
    surf_kriptonita   = surf_k_full.subsurface(surf_k_full.get_bounding_rect()).copy()
    surf_fundo        = pygame.transform.scale(carregar_sprite("metropolis.png"), (LARGURA, ALTURA))
except FileNotFoundError as e:
    print(e)
    pygame.quit()
    sys.exit(1)

LARG_PASSARO, ALT_PASSARO   = 50, 38
LARG_KRIPT_ORIG, ALT_KRIPT_ORIG = surf_kriptonita.get_size()
LARG_CANO                   = 60
PROPORCAO_KRIPT             = ALT_KRIPT_ORIG / LARG_KRIPT_ORIG
HITBOX_LARG_KRIPT           = 28

Y_CHAO = ALTURA

def desenhar_cano(superficie, x, altura_topo, y_base):
    topo = pygame.transform.scale(surf_kriptonita, (LARG_CANO, altura_topo))
    baixo = pygame.transform.scale(surf_kriptonita, (LARG_CANO, ALTURA - y_base))

    superficie.blit(
        pygame.transform.flip(topo, False, True),
        (x, 0)
    )

    superficie.blit(
        baixo,
        (x, y_base)
    )

class Particula:
    def __init__(self, x, y):
        self.x     = x + random.randint(-10, 10)
        self.y     = y + random.randint(-10, 10)
        self.vx    = random.uniform(-3, 3)
        self.vy    = random.uniform(-5, -1)
        self.vida  = random.randint(20, 40)
        self.vida_max = self.vida
        self.cor   = random.choice([(255, 210, 30), (255, 140, 0), (255, 255, 100)])
        self.raio  = random.randint(3, 8)

    def atualizar(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.2
        self.vida -= 1

    def desenhar(self, superficie):
        alfa = max(0, int(255 * self.vida / self.vida_max))
        s = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.cor, alfa), (self.raio, self.raio), self.raio)
        superficie.blit(s, (int(self.x - self.raio), int(self.y - self.raio)))

GRAVIDADE       = 0.45
VEL_PULO        = -9.5
ESPACO_CANO     = 185
VEL_CANO        = 3.2

def desenhar_texto_centralizado(superficie, texto, fonte, cor, y, sombra=True):
    renderizado = fonte.render(texto, True, cor)
    x = LARGURA // 2 - renderizado.get_width() // 2
    if sombra:
        sh = fonte.render(texto, True, (0, 0, 0))
        superficie.blit(sh, (x + 2, y + 2))
    superficie.blit(renderizado, (x, y))

def hitbox_passaro(bx, by):
    margem = 5
    return pygame.Rect(
        bx - LARG_PASSARO // 2 + margem,
        by - ALT_PASSARO // 2 + margem,
        LARG_PASSARO - margem * 2,
        ALT_PASSARO - margem * 2,
    )

def hitboxes_cano(px, altura_topo, y_base):
    cx = px + LARG_CANO // 2
    mw = HITBOX_LARG_KRIPT // 2
    return (
        pygame.Rect(cx - mw, 0,      HITBOX_LARG_KRIPT, altura_topo),
        pygame.Rect(cx - mw, y_base, HITBOX_LARG_KRIPT, ALTURA - y_base),
    )

def reiniciar_jogo():
    return {
        "x_passaro":    100,
        "y_passaro":    ALTURA // 2,
        "vel_y":        0,
        "canos":        [],
        "particulas":   [],
        "timer_cano":   0,
        "anim_bater":   0,
        "pontuacao":    0,
        "recorde":      0,
        "estado":       "menu",
        "timer_morte":  0,
        "flash":        0,
    }

estado = reiniciar_jogo()
recorde_geral = 0

quadro   = 0
rodando  = True

while rodando:
    relogio.tick(FPS)
    quadro += 1

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            pular = (
                evento.type == pygame.MOUSEBUTTONDOWN or
                (evento.type == pygame.KEYDOWN and
                 evento.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w))
            )

            if pular:
                if estado["estado"] == "menu":
                    estado["estado"] = "jogando"
                    estado["vel_y"] = VEL_PULO
                elif estado["estado"] == "jogando":
                    estado["vel_y"] = VEL_PULO
                elif estado["estado"] == "morto" and estado["timer_morte"] > 40:
                    recorde_geral = max(recorde_geral, estado["pontuacao"])
                    estado = reiniciar_jogo()
                    estado["estado"] = "menu"

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False

    if estado["estado"] == "jogando":
        estado["vel_y"]     += GRAVIDADE
        estado["vel_y"]      = min(estado["vel_y"], 12)
        estado["y_passaro"] += estado["vel_y"]
        estado["anim_bater"] += 0.25

        estado["timer_cano"] += 1
        if estado["timer_cano"] >= 90:
            estado["timer_cano"] = 0
            centro_espaco = random.randint(ESPACO_CANO // 2 + 50, ALTURA - ESPACO_CANO // 2 - 50)
            topo = centro_espaco - ESPACO_CANO // 2
            base = centro_espaco + ESPACO_CANO // 2
            estado["canos"].append({
                "x":       LARGURA,
                "topo":    topo,
                "base":    base,
                "pontuou": False,
            })

        for c in estado["canos"]:
            c["x"] -= VEL_CANO
            if not c["pontuou"] and c["x"] + LARG_CANO < estado["x_passaro"]:
                c["pontuou"] = True
                estado["pontuacao"] += 1

        estado["canos"] = [c for c in estado["canos"] if c["x"] > -120]

        br   = hitbox_passaro(estado["x_passaro"], estado["y_passaro"])
        bateu = estado["y_passaro"] + ALT_PASSARO // 2 >= Y_CHAO
        if estado["y_passaro"] - ALT_PASSARO // 2 < 0:
            bateu = True
        for c in estado["canos"]:
            r1, r2 = hitboxes_cano(c["x"], c["topo"], c["base"])
            if br.colliderect(r1) or br.colliderect(r2):
                bateu = True

        if bateu:
            estado["estado"]    = "morto"
            estado["flash"]     = 10
            estado["vel_y"]     = VEL_PULO * 0.5
            for _ in range(20):
                estado["particulas"].append(
                    Particula(estado["x_passaro"], estado["y_passaro"]))

        estado["particulas"] = [p for p in estado["particulas"] if p.vida > 0]
        for p in estado["particulas"]:
            p.atualizar()

    elif estado["estado"] == "morto":
        estado["timer_morte"] += 1
        estado["vel_y"]  += GRAVIDADE
        estado["y_passaro"]  = min(
            estado["y_passaro"] + estado["vel_y"],
            Y_CHAO - ALT_PASSARO // 2,
        )
        estado["particulas"] = [p for p in estado["particulas"] if p.vida > 0]
        for p in estado["particulas"]:
            p.atualizar()
        if estado["flash"] > 0:
            estado["flash"] -= 1

    tela.blit(surf_fundo, (0, 0))

    for c in estado["canos"]:
        desenhar_cano(tela, c["x"], c["topo"], c["base"])

    for p in estado["particulas"]:
        p.desenhar(tela)

    if estado["estado"] == "jogando":
        angulo = max(-30, min(45, estado["vel_y"] * 3))
    elif estado["estado"] == "morto":
        angulo = 90
    else:
        angulo = math.sin(quadro * 0.05) * 10

    passaro_rotacionado = pygame.transform.rotate(surf_passaro, -angulo)
    lp, ap = passaro_rotacionado.get_size()
    tela.blit(passaro_rotacionado,
              (int(estado["x_passaro"]) - lp // 2,
               int(estado["y_passaro"]) - ap // 2))

    if estado["flash"] > 0:
        fl = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        fl.fill((255, 255, 255, int(estado["flash"] * 20)))
        tela.blit(fl, (0, 0))

    if estado["estado"] == "menu":
        desenhar_texto_centralizado(tela, "SUPER BIRD",
                         fonte_media, DESTAQUE_UI, ALTURA // 2 - 80)
        desenhar_texto_centralizado(tela, "Pressione ESPAÇO para iniciar",
                         fonte_pequena, (255, 255, 255), ALTURA // 2 + 40)
    elif estado["estado"] == "jogando":
        desenhar_texto_centralizado(tela, str(estado["pontuacao"]),
                         fonte_media, (255, 255, 255), 50)
    elif estado["estado"] == "morto":
        desenhar_texto_centralizado(tela, str(estado["pontuacao"]),
                         fonte_media, (255, 255, 255), 50)
        if estado["timer_morte"] > 40:
            desenhar_texto_centralizado(tela, "GAME OVER",
                             fonte_media, (255, 50, 50), ALTURA // 2 - 60)
            desenhar_texto_centralizado(tela, "Pressione ESPAÇO para reiniciar",
                             fonte_pequena, (255, 255, 255), ALTURA // 2)
            desenhar_texto_centralizado(tela, f'Recorde: {recorde_geral}',
                             fonte_pequena, DESTAQUE_UI, ALTURA // 2 + 40)

    pygame.display.flip()

pygame.quit()
sys.exit()
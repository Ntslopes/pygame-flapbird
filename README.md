# Documentação do Projeto — Flappy Bird Superman

## Integrantes do Grupo

Esther dos Santos de Almeida Tozzo | RM: 570860

Felipe de Oliveira Zimmermann | RM: 570863

Izabela Pordeus de Almeida | RM: 570316

João Victor Santos Souza | RM: 569949

Matheus Lopes Lima | RM: 571458

---

## Descrição do Projeto

O projeto consiste em uma recriação do jogo Flappy Bird utilizando a biblioteca Pygame em Python.

Nesta versão personalizada:

* o personagem principal é o Superman;
* os obstáculos foram substituídos por kriptonita;
* o cenário utiliza a cidade de Metrópolis;
* foram adicionados efeitos visuais como partículas, rotação do personagem e flash de colisão.

O objetivo do jogador é desviar dos obstáculos e alcançar a maior pontuação possível.

---

## Objetivos do Projeto

O projeto teve como principais objetivos:

* aplicar conceitos de programação em Python;
* utilizar a biblioteca Pygame para desenvolvimento de jogos 2D;
* implementar movimentação, colisão e animações;
* trabalhar lógica de game loop;
* desenvolver interface gráfica interativa;
* manipular sprites e efeitos visuais.

---

## Tecnologias Utilizadas

### Linguagem

* Python 3

### Biblioteca

* Pygame

---

## Estrutura do Projeto

```txt id="p3g5op"
pygame-flapbird/
│
├── kriptonita.png
├── main.py
├── metropolis.png
├── README.md
└── superman.png
```

---

## Funcionamento Geral

O jogo utiliza o conceito de game loop, responsável por:

1. processar eventos;
2. atualizar a lógica do jogo;
3. renderizar os elementos na tela.

O loop principal executa continuamente enquanto o jogo estiver aberto.

---

## Configuração Inicial

O programa inicia importando as bibliotecas necessárias:

```python id="5e7xxk"
import pygame
import random
import sys
import math
import os
```

Depois disso, o Pygame é inicializado:

```python id="0vr81c"
pygame.init()
```

Também são definidas:

* resolução da tela;
* FPS;
* fontes;
* cores;
* carregamento de sprites.

---

## Sistema de Sprites

O jogo utiliza imagens PNG para representar:

* personagem principal;
* obstáculos;
* cenário.

A função `carregar_sprite()` verifica diferentes caminhos possíveis para encontrar os arquivos de imagem:

```python id="e4r5g0"
def carregar_sprite(nome_arquivo):
```

Isso permite maior flexibilidade na organização dos assets.

---

## Sistema de Física

O movimento do Superman utiliza gravidade e impulso vertical.

### Gravidade

v_y = v_y + g

A gravidade aumenta gradualmente a velocidade vertical do personagem.

---

### Impulso de voo

Quando o jogador pressiona:

* espaço;
* seta para cima;
* tecla W;
* mouse,

a velocidade vertical recebe um impulso negativo:

```python id="af9p0k"
VEL_PULO = -9.5
```

Esse impulso faz o Superman subir na tela.

---

## Sistema de Obstáculos

Os obstáculos são gerados automaticamente em intervalos regulares.

Cada obstáculo possui:

* posição horizontal;
* abertura central;
* controle de pontuação.

As kriptonitas se movimentam constantemente para a esquerda:

x = x - v

---

## Sistema de Colisão

O jogo utiliza hitboxes retangulares através da classe:

```python id="v4w5eh"
pygame.Rect
```

As colisões são verificadas entre:

* Superman e obstáculos;
* Superman e limites da tela.

Quando ocorre colisão:

* o estado muda para “morto”;
* partículas são criadas;
* um flash branco é exibido.

---

## Sistema de Partículas

A classe `Particula` foi criada para gerar efeitos visuais após colisões.

Cada partícula possui:

* posição;
* velocidade;
* vida útil;
* cor;
* transparência.

As partículas simulam uma explosão visual ao perder o jogo.

---

# Estados do Jogo

O jogo possui três estados principais:

### Menu

Tela inicial aguardando o jogador iniciar.

### Jogando

Estado principal da gameplay.

### Morto

Estado exibido após colisão.

---

## Sistema de Pontuação

A pontuação aumenta quando o jogador ultrapassa um obstáculo com sucesso.

```python id="6k4l7q"
estado["pontuacao"] += 1
```

Também existe um sistema de recorde armazenado durante a execução do jogo.

---

## Sistema de Animação

O Superman rotaciona dinamicamente conforme sua velocidade vertical.

Quando sobe:

* inclina para cima.

Quando cai:

* inclina para baixo.

O ângulo é calculado usando:

\theta = v_y \cdot k

---

## Interface do Usuário

O jogo exibe mensagens centralizadas utilizando a função:

```python id="z8x9cv"
desenhar_texto_centralizado()
```

As mensagens incluem:

* início do jogo;
* reinício após derrota.

Também foi implementada sombra no texto para melhorar a legibilidade.

---

## Principais Conceitos Aplicados

Durante o desenvolvimento foram utilizados conceitos importantes de programação:

* variáveis;
* funções;
* classes;
* listas;
* dicionários;
* condicionais;
* loops;
* orientação a objetos;
* manipulação de imagens;
* detecção de colisão;
* renderização gráfica;
* física básica;
* eventos de teclado e mouse.

---

## Conclusão

O projeto permitiu desenvolver conhecimentos fundamentais sobre desenvolvimento de jogos utilizando Python e Pygame.

Além da implementação da mecânica principal do Flappy Bird, foram adicionadas personalizações visuais e efeitos gráficos que tornaram o jogo mais dinâmico e visualmente interessante.

O desenvolvimento também possibilitou compreender melhor:

* lógica de jogos;
* estruturas de atualização contínua;
* manipulação de sprites;
* física simples;
* interação do usuário em tempo real.

O projeto pode futuramente receber melhorias como:

* sons;
* menu avançado;
* sistema de fases;
* salvamento de recordes;
* animações mais complexas;
* novos obstáculos e power-ups.

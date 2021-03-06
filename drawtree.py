"""(C) Yann Thorimbert
Draw a tree with given branching factor and depth and save the image as png file."""
from __future__ import print_function, division
import pygame.gfxdraw as gfx
import pygame


class Node:
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def coord(self):
        return (self.x, self.y)

def build_floor(n, gap):
    D = 2*R
    width = n*D + (n-1)*gap + 1
    s = pygame.Surface((width,2*R+1))
    s.fill(BCK_COLOR)
    y = R
    x = R
    centers = []
    for i in range(n):
        gfx.filled_circle(s, x, y, R, NODE_COLOR)
        gfx.aacircle(s, x, y, R, NODE_COLOR)
        centers.append(x)
        x += 2*R + gap
    return s, centers


def get_gap(n,space,margin):
    D = 2*R
    return (space - n*D - 2*margin)//(n-1) #h*D + (h-1)*L + 2*G = H

def get_margin(n,space,delta):
    D = 2*R
    return (space - n*D - (n-1)*delta)//2 #h*D + (h-1)*L + 2*G = H

def draw(b,h):
    """b is the branching factor, h is the depth of the tree"""
    #here L is the space between the border of two circle in the depth
    #g is the space between the domain border and the border of the extreme circles
    L = get_gap(h, H, MARGIN_Y)
    y = MARGIN_Y + R
    centersx = []
    centersy = []
    nodes = []
    nmax = b**(h-1)
    for level in range(h):
        nodes.append([])
        n = b**level
        if n > 1:
            # gap = get_gap(n, W, MARGIN_FACTOR//n)
            #m = int( W//2 * (1. - n/(nmax+0.)  ))
            ###############################################
            # m0 = 0
            # gap_N = get_gap(nmax, W, m0)
            # m = m0 + gap_N//2
            # for i in range(h-1-level):
            #     gap_N *= b
            #     m += gap_N//2
            # print(level, 10 + gap_N//2, m, h-1-level)
            # gap = get_gap(n, W, m)
            m = W//2 * (1. - level/(h-1)) / MARGIN_FACTOR
            gap = get_gap(n, W, int(m))
        else:
            gap = 100
        #gap = 100//n
        print("build floor", level, n, gap)
        s, c = build_floor(n, gap)
        r = s.get_rect()
        r.centery = y
        r.centerx = W//2
        screen.blit(s,r.topleft)
        centersx.append([v+r.x for v in c])
        centersy.append(r.centery)
        y += L + 2*R
        #
        if level > 0:
            nparents = b**(level-1)
            for i in range(n):
                parent_i = int(i/n*nparents)
                p1 = centersx[level][i], centersy[level]
                p2 = centersx[level-1][parent_i], centersy[level-1]
                pygame.draw.aaline(screen, NODE_COLOR, p1, p2)
                nodes[level].append(Node(p1))
        else:
            nodes[level].append(Node((centersx[level][0], centersy[level])))
    pygame.display.flip()
    return nodes

##############################################################################
W, H = 1100, 300
R = 8
MARGIN_Y = 50
MARGIN_FACTOR = 1.5 #a parameter of the display (play with it!)
NODE_COLOR = (50,50,50)
BCK_COLOR = (255,255,255)

screen = pygame.display.set_mode((W,H))

screen.fill(BCK_COLOR)
nodes = draw(b=4,h=4)
pygame.image.save(screen, "b4.png")

loop = True
while loop:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            loop = False

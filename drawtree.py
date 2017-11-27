import pygame, thorpy
import pygame.gfxdraw as gfx


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
    #g is the space betwwn the domain border and the border of the extreme circles
    L = get_gap(h, H, G)
    y = G + R
    centersx = []
    centersy = []
    for level in range(h):
        n = b**level
        gap = 100//n
        print("build floor", level, n, gap)
        s, c = build_floor(n,gap)
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
    pygame.display.flip()

W, H = 1100, 400
R = 8
G = 50
NODE_COLOR = (50,50,50)
BCK_COLOR = (255,255,255)

ap = thorpy.Application((W,H), "Draw tree")
screen = thorpy.get_screen()
screen.fill(BCK_COLOR)
draw(b=4,h=4)
##pygame.draw.rect(screen, (0,0,0), pygame.Rect(W//2-1,H//2-1,2,2));pygame.display.flip()
ap.pause()
thorpy.quit()
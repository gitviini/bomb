import pygame
from pygame.locals import *
from game import *

def handle_key(key, entity, step):
    if key in [pygame.K_RIGHT, pygame.K_d]:
        entity["vel"]["x"] = 1 * step
        entity["vel"]["y"] = 0
    elif key in [pygame.K_LEFT, pygame.K_a]:
        entity["vel"]["x"] = -1 * step
        entity["vel"]["y"] = 0
    elif key in [pygame.K_UP, pygame.K_w]:
        entity["vel"]["y"] = -1 * step
        entity["vel"]["x"] = 0
    elif key in [pygame.K_DOWN, pygame.K_s]:
        entity["vel"]["y"] = 1 * step
        entity["vel"]["x"] = 0
    else:
        entity["vel"]["y"] = 0
        entity["vel"]["x"] = 0


def main():
    square_size = 20
    size = weight, height = 640, 400
    node_tilemap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,1,3,1,1,3,1,1,1,0,1,0,1],
    [1,0,3,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,0,0,1,0,1,0,1,1,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,0,0,1,0,1],
    [1,0,1,0,1,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
    tilemap = []
    init_pos = {"x":(weight / 2) - (len(node_tilemap[0]) * square_size / 2), "y": (height / 2) - (len(node_tilemap) * square_size / 2)}
    player = {
        "pos": {"x": init_pos["x"] + square_size, "y": init_pos["y"] + square_size},
        "len": {"x": 20, "y": 20},
        "vel": {"x": 0, "y": 0},
        "color": YELLOW,
        "collision": {"is_collide":False,"type":None},
        "bomb": 3,
        "life": 5,
        "sprite": [
            [0,1,1,1,0],
            [1,0,1,0,1],
            [1,0,1,0,1],
            [1,1,1,1,1],
            [1,0,0,0,1],
        ]
    }
    old_pos = {"x": player["pos"]["x"], "y": player["pos"]["y"]}
    entities = []
    key_list = []
    surface = None
    _running = True

    pygame.init()
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
    cooldown = 0
    while _running:
        dt = clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _running = False
            if event.type == pygame.KEYDOWN:
                key_list.append(event.key)

                if event.key == pygame.K_SPACE:
                    set_bomb(player, entities, square_size)
            if event.type == pygame.KEYUP:
                key_list.remove(event.key)

        for key in key_list:
            handle_key(key=key, entity=player, step=square_size)
        surface.fill((0, 0, 0))
        draw_ui(surface, player)
        timer_explosion(tilemap=tilemap, node_tilemap=node_tilemap, square_size=square_size, init_pos=init_pos)

        tilemap = draw_tilemap(surface=surface, node_tilemap=node_tilemap, square_size=square_size, init_pos=init_pos)
        
        is_collision(player, tilemap)

        if(not cooldown):
            if(player["collision"]["type"] in ["damage","explosion"]):
                player["life"] -= 1
                cooldown = 10
                player["color"] = WHITE
            else:
                player["color"] = YELLOW

        move_entity(player)

        for entity in entities:
            if(entity.get("timer") != None):
                timer_bomb(player, entity, entities, node_tilemap, square_size, init_pos)
            draw_rect(surface, entity)

        draw_rect(surface, player)
        pygame.display.update()
        cooldown = cooldown - 1 if cooldown > 0 else cooldown

    pygame.quit()


if __name__ == "__main__":
    main()

import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
ORANGE = (255, 125, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


def pos_to_node(tgt, node_tilemap, square_size, init_pos):
    pos = {
        "x": tgt["pos"]["x"] / square_size - init_pos["x"],
        "y'": tgt["pos"]["y"] / square_size - init_pos["y"],
    }

    node_len = {
        "x": len(node_tilemap[0]),
        "y": len(node_tilemap),
    }


def draw_ui(surface, src):
    padding = 10
    bomb = {
        "pos": {"x": 0, "y": 30 + padding},
        "sprite": [
            [0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
        ],
        "color": ORANGE,
    }
    life = {
        "pos": {"x": 0, "y": padding},
        "sprite": [
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
        ],
        "color": RED,
    }

    for x in range(src["life"]):
        life["pos"]["x"] = x * 30 + padding
        draw_sprite(surface, life)
    for x in range(src["bomb"]):
        bomb["pos"]["x"] = x * 30 + padding
        draw_sprite(surface, bomb)


def draw_sprite(surface, src):
    sprite_len = {"x": len(src["sprite"][0]), "y": len(src["sprite"])}
    for x in range(sprite_len["x"]):
        for y in range(sprite_len["y"]):
            pixel = src["sprite"][y][x]

            if not pixel:
                continue

            pygame.draw.rect(
                surface,
                rect=(
                    src["pos"]["x"] + x * 4,
                    src["pos"]["y"] + y * 4,
                    4,
                    4,
                ),
                color=src["color"],
            )


def explosion_bomb(bomb, node_tilemap):
    explosion_len = 5


def timer_bomb(tgt, bomb, entities, node_tilemap):
    if bomb["timer"] < 10:
        bomb["color"] = RED
    if bomb["timer"] < 1:
        bomb["color"] = WHITE
    if bomb["timer"] == 0:
        entities.remove(bomb)
        explosion_bomb(bomb, node_tilemap)
        tgt["bomb"] += 1
        return

    bomb["timer"] -= 1


def set_bomb(tgt, entities, square_size):
    if not tgt["bomb"] > 0:
        return
    pos = tgt["pos"]
    for entity in entities:
        if entity.get("timer") != None:
            if entity["pos"]["x"] == pos["x"] and entity["pos"]["y"] == pos["y"]:
                return
    tgt["bomb"] -= 1
    bomb = {
        "pos": {"x": pos["x"], "y": pos["y"]},
        "len": {"x": square_size, "y": square_size},
        "collision": {"is_collide": False, "type": "damage"},
        "color": ORANGE,
        "timer": 30,
        "sprite": [
            [0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
        ],
    }
    entities.append(bomb)


def draw_rect(surface, src):
    if src.get("sprite") != None:
        draw_sprite(surface, src)
        return

    pygame.draw.rect(
        surface,
        rect=(
            src["pos"]["x"],
            src["pos"]["y"],
            src["len"]["x"],
            src["len"]["y"],
        ),
        color=src["color"],
    )


def node_to_tile(node, pos, square_size) -> dict[any]:
    # default color: white
    color = WHITE
    # default sprite: bearer
    sprite = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    # default type collision: None
    type_collision = None
    match node:
        # black
        case 0:
            color = BLACK
        # blue
        case 1:
            color = BLUE
            type_collision = "bearer"
        # red
        case 2:
            color = RED
            type_collision = "damage"
            sprite = [
                [0, 0, 1, 1, 1],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [1, 1, 1, 0, 0],
            ]
        # red
        case 3:
            color = WHITE
            type_collision = "box"
            sprite = [
                [1, 1, 1, 1, 1],
                [1, 1, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 1, 1],
                [1, 1, 1, 1, 1],
            ]

    tile = {
        "pos": {"x": pos["x"], "y": pos["y"]},
        "len": {"x": square_size, "y": square_size},
        "collision": {"is_collide": False, "type": type_collision},
        "color": color,
        "sprite": sprite,
    }
    return tile


def draw_tilemap(surface, node_tilemap, square_size, init_pos) -> list[dict[any]]:
    tilemap = []

    tilemap_len = {"x": len(node_tilemap[0]), "y": len(node_tilemap)}

    for y in range(tilemap_len["y"]):
        for x in range(tilemap_len["x"]):
            node = node_tilemap[y][x]
            pos = {
                "x": init_pos["x"] + x * square_size,
                "y": init_pos["y"] + y * square_size,
            }
            tile = node_to_tile(node, pos, square_size)
            draw_rect(surface, tile)

            tilemap.append(tile)
    return tilemap


def is_collision(target, obstacles) -> None:
    is_collide = False
    type_collision = None
    tgt_pos = {
        "x": target["pos"]["x"] + target["vel"]["x"],
        "y": target["pos"]["y"] + target["vel"]["y"],
    }
    tgt_area = {
        "x": tgt_pos["x"] + target["len"]["x"],
        "y": tgt_pos["y"] + target["len"]["y"],
    }

    for obs in obstacles:
        obs_pos = {"x": obs["pos"]["x"], "y": obs["pos"]["y"]}
        obs_area = {
            "x": obs_pos["x"] + obs["len"]["x"],
            "y": obs_pos["y"] + obs["len"]["y"],
        }

        obs["collision"]["is_collide"] = False

        if not (
            tgt_area["x"] > obs_pos["x"]
            and tgt_pos["x"] < obs_area["x"]
            and tgt_area["y"] > obs_pos["y"]
            and tgt_pos["y"] < obs_area["y"]
        ):
            continue

        is_collide = True
        type_collision = obs["collision"]["type"]
        obs["collision"]["is_collide"] = is_collide

    target["collision"]["is_collide"] = is_collide
    target["collision"]["type"] = type_collision


def move_entity(entity) -> None:
    if entity["collision"]["type"] in ["bearer", "box"]:
        entity["vel"]["x"] = 0
        entity["vel"]["y"] = 0
        return
    entity["pos"]["x"] += entity["vel"]["x"]
    entity["pos"]["y"] += entity["vel"]["y"]
    entity["vel"]["x"] = 0
    entity["vel"]["y"] = 0

import pygame

from time import time

from constants.upgrades import upgrades
from constants.builds import builds

import constants.modes as modes
import constants.upgradetypes as utypes
import constants.buildtypes as btypes

from constants.settings import *

from json import dump, loads

# SAVE
with open("./save/save.json", "r") as file:
    save = loads(file.read())

print(save)

# pygame
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# pygame variables
running = True

# game variables
variables = save["variables"]

cps = variables["cps"]  # Cookies per second
cpc = variables["cpc"]  # Cookies per click
cps_multiplier = variables["cps_multiplier"]
cpc_multiplier = variables["cpc_multiplier"]

cookieAmount = (
    variables["cookies"]
    if save["date"] == 0
    else variables["cookies"]
    + ((int(time() * 1000) - save["date"]) * cps * cps_multiplier)
)

currentMode = modes.COOKIE

class Building(pygame.sprite.Sprite):
    def getBuildingState(self) -> pygame.surface.Surface:
        if not self.building["known"]:
            return self.building_states["unknown"]
        elif self.building["cost"] > cookieAmount:
            return self.building_states["black"]
        else:
            return self.building_states["normal"]

    def __init__(self, building: dict, index: int) -> None:
        super().__init__()

        self.building = building

        self.building_states = {
            "normal": pygame.image.load(
                f"./assets/builds/normal/{self.building['type']}.png"
            ).convert(),
            "highlighted": pygame.image.load(
                f"./assets/builds/highlight/{self.building['type']}.png"
            ).convert(),
            "black": pygame.image.load(
                f"./assets/builds/black/{self.building['type']}.png"
            ).convert(),
            "unknown": pygame.image.load(
                f"./assets/builds/unknown/{self.building['type']}.png"
            ).convert(),
        }

        self.image = self.getBuildingState()
        self.rect = self.image.get_rect(midleft=(0, 31.5 + index * 63))

    def check_input(self) -> None:
        global cookieAmount, cps
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(
            pygame.mouse.get_pos()
        ):
            if cookieAmount >= self.building["cost"]:
                cookieAmount -= self.building["cost"]

                cps += self.building["boost"]

                self.building["cost"] += self.building["cost"] * 0.15
                self.building["owned"] += 1
                print(self.building["owned"])

    def hover_animation(self) -> None:
        if (
            not self.image == self.building_states["black"]
            and not self.image == self.building_states["unknown"]
        ):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.building_states["highlighted"]
            else:
                self.image = self.building_states["normal"]

    def isKnown(self) -> None:
        if self.building["cost"] / 1.8 < cookieAmount:
            self.building["known"] = True

    def update(self) -> None:
        self.image = self.getBuildingState()
        self.isKnown()
        self.hover_animation()
        self.check_input()


# fonts
def renderCookieFont(
    text: str, antiAlias: bool, color: tuple | list, size: int | float = 25
) -> pygame.Surface:
    cookieFont = pygame.font.Font("./assets/font/Kavoon-Regular.ttf", int(size))
    return cookieFont.render(str(text), antiAlias, color).convert_alpha()


# game functions
def formatAmount(amount: int) -> str:
    res = f"{round(amount)}"

    if amount >= 1000000000000000000000000000:
        n = str(round(amount / 1000000000000000000000000000, 1))
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} infinity"
    elif amount >= 1000000000000000000000000:
        n = str(round(amount / 1000000000000000000000000, 1))
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} Sp"
    elif amount >= 1000000000000000000000:
        n = str(round(amount / 1000000000000000000000, 1))
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} Sx"
    elif amount >= 1000000000000000000:
        n = str(round(amount / 1000000000000000000, 1))
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} Qi"
    elif amount >= 1000000000000000:
        n = str(round(amount / 1000000000000000, 1))
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} Qa"
    elif amount >= 1000000000000:
        n = str(round(amount / 1000000000000, 1))
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} T"
    elif amount >= 1000000000:
        n = str(round(amount / 1000000000, 1))
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} B"
    elif amount >= 1000000:
        n = str(round(amount / 1000000, 1))
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} M"
    elif amount >= 1000:
        n = str(round(amount / 1000, 1))
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n}k"
    return res


def updateCookieInfo(amount: int) -> None:
    global cookieInfo_surface
    cookieInfo_surface = renderCookieFont(
        f"{formatAmount(amount)} cookies", True, [255, 255, 255]
    )


# Groups
buildings = pygame.sprite.Group()
for build in builds:
    buildings.add(Building(build, builds.index(build)))

# surfaces
cookie_surface = pygame.image.load("./assets/img/cookie.png").convert_alpha()
cookie_rect = cookie_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))

background_surface = pygame.image.load("./assets/img/background.png").convert()
background_rect = background_surface.get_rect()

cookieInfo_surface = renderCookieFont("0 cookies", True, [255, 255, 255])
cookieInfo_rect = cookieInfo_surface.get_rect(midtop=(WIDTH / 2, HEIGHT * 50 / 800))

pygame.display.set_caption("Cookie Clicker")
pygame.display.set_icon(cookie_surface)

# timers
cps_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cps_timer, 1000)

grandma_timer = pygame.USEREVENT + 2
pygame.time.set_timer(grandma_timer, 1000)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # with open("./save/save.json", "w") as file:
            #     dump(
            #         {
            #             "date": time() * 1000,
            #             "variables": {
            #                 "cookies": cookieAmount,
            #                 "cps": cps,
            #                 "cpc": cpc,
            #                 "cps_multiplier": cps_multiplier,
            #                 "cpc_multiplier": cpc_multiplier,
            #             },
            #             "buildings": builds,
            #             "upgrades": [],
            #         },
            #         file,
            #     )
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                currentMode = modes.COOKIE
            elif event.key == pygame.K_2:
                currentMode = modes.BUILDS
            elif event.key == pygame.K_3:
                currentMode = modes.UPGRADES
        if event.type == pygame.MOUSEBUTTONUP:
            if cookie_rect.collidepoint(event.pos):
                cookieAmount += cpc * cpc_multiplier
                updateCookieInfo(cookieAmount)

        if event.type == cps_timer:
            cookieAmount += cps * cps_multiplier
            updateCookieInfo(cookieAmount)
        # elif event.type == grandma_timer:
        #     cookieAmount +=
        #     updateCookieInfo(cookieAmount)

    if currentMode == modes.COOKIE:
        screen.blit(background_surface, background_rect)
        screen.blit(cookie_surface, cookie_rect)
        screen.blit(cookieInfo_surface, cookieInfo_rect)

    elif currentMode == modes.BUILDS:
        screen.fill([130, 130, 130])
        buildings.draw(screen)
        buildings.update()
        # background = pygame.image.load("./assets/img/upgrade_bg.png").convert()
        # background.set_alpha(165)
        # screen.blit(background, background.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        # for build in builds:
        #     i = builds.index(build)
        #     buildings.add(Building(build, i))
        # build_surf = pygame.transform.rotozoom(
        #     build["surface"].convert_alpha(), 0, 0.6
        # )
        # build_rect = build_surf.get_rect(midleft=(10, 50 + i * 50))

        # name_surf = renderCookieFont(build["name"], True, [255, 255, 255], 22)
        # name_rect = name_surf.get_rect(midleft=(90, 30 + i * 50))

        # build_surface = pygame.image.load("./assets/img/build_rect.png")
        # build_surface.set_alpha(100 + i * 20)  # 100 + i * 20

        # cost_surf = renderCookieFont(
        #     f"{formatAmount(build['cost'])} cookies", True, [255, 255, 255], 19
        # )
        # cost_rect = cost_surf.get_rect(midleft=(90, 55 + i * 50))

        # owned_surf = renderCookieFont(
        #     f"Owned: {build['owned']}", True, [255, 255, 255], 16
        # )
        # owned_rect = owned_surf.get_rect(midleft=(90, 80 + i * 50))

        # if (
        #     build_rect.collidepoint(pygame.mouse.get_pos())
        #     and pygame.mouse.get_pressed()[0]
        # ):
        #     build["owned"] += 1
        #     build["cost"] += build["owned"] * 15

        # screen.blit(build_surf, build_rect)
        # screen.blit(build_surface, build_rect)
        # screen.blit(name_surf, name_rect)
        # screen.blit(owned_surf, owned_rect)
        # screen.blit(cost_surf, cost_rect)

    elif currentMode == modes.UPGRADES:
        screen.fill([130, 130, 130])
        # background = pygame.image.load("./assets/img/upgrade_bg.png").convert()
        # background.set_alpha(165)
        # screen.blit(background, background.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        # for upgrade in upgrades:
        #     i = upgrades.index(upgrade)
        #     upgrade_surface = upgrade["surface"].convert_alpha()
        #     upgrade_rect = upgrade_surface.get_rect(midleft=(10, 40 + i * 50))
        #     name_surf = renderCookieFont(upgrade["name"], True, [255, 255, 255], 22)
        #     name_rect = name_surf.get_rect(midleft=(60, 40 + i * 50))

        #     cost_surf = renderCookieFont(
        #         f"{formatAmount(upgrade['cost'])} cookies", True, [255, 255, 255], 25
        #     )
        #     cost_rect = cost_surf.get_rect(midleft=(320, 40 + i * 50))

        #     upgrade_surf = pygame.image.load("./assets/img/upgrade_rect.png")
        #     upgrade_surf.set_alpha(0)  # 100 + i * 20

        #     screen.blit(upgrade_surf, upgrade_rect)
        #     screen.blit(upgrade_surface, upgrade_rect)
        #     screen.blit(name_surf, name_rect)
        #     screen.blit(cost_surf, cost_rect)

        #     if (
        #         upgrade_rect.collidepoint(pygame.mouse.get_pos())
        #         and pygame.mouse.get_pressed()[0]
        #     ):
        #         if cookieAmount > upgrade["cost"]:
        #             if upgrades.__contains__(upgrade):
        #                 upgrades.remove(upgrade)
        #             if upgrade["type"] == utypes.CLICK:
        #                 cpc *= upgrade["amount"]
        #                 cookieAmount -= upgrade["cost"]

        #                 print(f"Bought upgrade {upgrade['name']} for {upgrade['cost']}")

    pygame.display.update()
    clock.tick(60)

pygame.quit()

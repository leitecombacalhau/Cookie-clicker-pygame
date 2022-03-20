import pygame

from time import time

from pprint import pprint

from random import choice, randint

from constants.upgrades import upgrades
from constants.builds import builds
from constants.goldcookies import goldcookies

import constants.modes as modes
import constants.upgradetypes as utypes
import constants.buildtypes as btypes
import constants.gcookietypes as gctypes

from constants.settings import *

from json import dump, loads

# SAVE
with open("./save/save.json", "r") as file:
    save = loads(file.read())

pprint(save)

# Pygame
pygame.init()

pygame.display.set_caption("Cookie Clicker")

# Pygame Variables
clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

running = True

savable = False

# Game Variables
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

# Fonts
def renderCookieFont(
    text: str,
    antiAlias: bool = True,
    color: tuple = (255, 255, 255),
    size: int = 25,
) -> pygame.Surface:
    cookieFont = pygame.font.Font("./assets/font/Kavoon-Regular.ttf", int(size))
    return cookieFont.render(str(text), antiAlias, color).convert_alpha()


# Game Functions
def formatAmount(amount: int, decimals: int = 1) -> str:
    res = f"{format(amount, '.0f')}"

    if amount >= 1000000000000000000000000000:
        n = format(amount / 1000000000000000000000000000, f".{int(decimals)}f")
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} infinity"
    elif amount >= 1000000000000000000000000:
        n = format(amount / 1000000000000000000000000, f".{int(decimals)}f")
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} Sp"
    elif amount >= 1000000000000000000000:
        n = format(amount / 1000000000000000000000, f".{int(decimals)}f")
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} Sx"
    elif amount >= 1000000000000000000:
        n = format(amount / 1000000000000000000, f".{int(decimals)}f")
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} Qi"
    elif amount >= 1000000000000000:
        n = format(amount / 1000000000000000, f".{int(decimals)}f")
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} Qa"
    elif amount >= 1000000000000:
        n = format(amount / 1000000000000, f".{int(decimals)}f")
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} T"
    elif amount >= 1000000000:
        n = format(amount / 1000000000, f".{int(decimals)}f")
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} B"
    elif amount >= 1000000:
        n = format(amount / 1000000, f".{int(decimals)}f")
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n} M"
    elif amount >= 1000:
        n = format(amount / 1000, f".{int(decimals)}f")
        res = f"{n.rstrip('0'). rstrip('.') if '.' in n else n}k"

    return res


def updateCookieInfo() -> None:
    global cookieInfo_surface, cpsInfo_surface
    global cookieAmount, cps
    cookieInfo_surface = renderCookieFont(
        f"{formatAmount(cookieAmount)} cookies", True, [255, 255, 255]
    )
    cpsInfo_surface = renderCookieFont(
        f"{formatAmount(cps)}/s", True, [255, 255, 255], 15
    )


# Sprites
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

        self.clickState = False

        self.building = building

        self.index = index

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

        if (
            pygame.mouse.get_pressed()[0]
            and not self.clickState
            and self.rect.collidepoint(pygame.mouse.get_pos())
        ):
            self.clickState = True
            if cookieAmount >= self.building["cost"]:
                cookieAmount -= self.building["cost"]

                cps += self.building["boost"]

                self.building["cost"] += self.building["cost"] * 0.15
                self.building["owned"] += 1
        elif not pygame.mouse.get_pressed()[0]:
            self.clickState = False

    def hover_animation(self) -> None:
        if self.image != self.building_states["unknown"]:
            if (
                self.rect.collidepoint(pygame.mouse.get_pos())
                and pygame.mouse.get_focused()
            ):
                if self.image != self.building_states["black"]:
                    self.image = self.building_states["highlighted"]
                detailed_info_rect = pygame.rect.Rect(9, self.index * 63 + 30, 252, 50)

                owned_surf = renderCookieFont(f"O: {self.building['owned']}", size=20)
                owned_rect = owned_surf.get_rect(midleft=(9, self.index * 63 + 40))

                cost_surf = renderCookieFont(
                    f"C: {formatAmount(self.building['cost'])}", size=20
                )
                cost_rect = cost_surf.get_rect(midleft=(9, self.index * 63 + 68))

                pygame.draw.rect(screen, "red", detailed_info_rect)

                screen.blit(owned_surf, owned_rect)
                screen.blit(cost_surf, cost_rect)

    def isKnown(self) -> None:
        if self.building["cost"] / 1.8 < cookieAmount:
            self.building["known"] = True

    def update(self) -> None:
        self.image = self.getBuildingState()
        self.isKnown()
        self.hover_animation()
        self.check_input()


class GoldenCookie(pygame.sprite.Sprite):
    def __init__(self, cookie) -> None:
        super().__init__()

        self.image_default = pygame.image.load(
            "./assets/goldencookies/goldencookie4.png"
        ).convert_alpha()

        self.image = self.image_default
        self.image.set_alpha(0)

        # self.random_coords = (randint(0, WIDTH), randint(0, HEIGHT))

        self.rect = self.image.get_rect(center=(randint(0, WIDTH), randint(0, HEIGHT)))

        self.cookie = cookie

        self.effect_started = -1

        self.countdown_start = time() * 1000

        self.pauseSeconds = []

        for i in range(self.cookie["static_display_time"]):
            self.pauseSeconds.append(i + self.cookie["fade_time"])

    def check_time_expired(self) -> bool:
        return self.image.get_alpha() < 0

    def fadeAnimation(self) -> None:
        millisecondsElapsed = time() * 1000 - self.countdown_start
        millisecondsLeft = (
            2 * (self.cookie["fade_time"] * 1000)
            + self.cookie["static_display_time"] * 1000
        ) - millisecondsElapsed

        if not int(millisecondsElapsed / 1000) in self.pauseSeconds:
            if millisecondsElapsed / 1000 <= self.cookie["fade_time"]:
                # self.image = pygame.transform.rotozoom(
                #     self.image_default,
                #     0,
                #     1 / self.cookie["fade_time"] * (millisecondsElapsed / 1000),
                # )
                # self.rect = self.image.get_rect(center=self.random_coords)  # approval
                self.image.set_alpha(
                    255 / self.cookie["fade_time"] * (millisecondsElapsed / 1000)
                )
            else:
                # self.image = pygame.transform.rotozoom(
                #     self.image_default,
                #     0,
                #     1 / self.cookie["fade_time"] * (millisecondsLeft / 1000),
                # )
                # self.rect = self.image.get_rect(center=self.random_coords)  # approval
                self.image.set_alpha(
                    255 / self.cookie["fade_time"] * (millisecondsLeft / 1000)
                )

    def check_effect_expired(self) -> bool:
        return (time() * 1000 - self.effect_started) > self.cookie[
            "effect_duration"
        ] * 1000

    def applyEffect(self, revert: bool = False) -> None:
        if self.cookie["type"] == gctypes.CFRENZY:
            global cpc
            if revert:
                cpc -= self.boost
            else:
                self.boost = cpc * self.cookie["effect_amount"]
                cpc += self.boost
        elif self.cookie["type"] == gctypes.FRENZY:
            global cps
            if revert:
                cps -= self.boost
            else:
                self.boost = cps * self.cookie["effect_amount"]
                cps += self.boost

    def update(self) -> None:
        if self.effect_started == -1:
            self.fadeAnimation()
            if self.check_time_expired():
                self.kill()
        if self.effect_started != -1:
            indcator_surf = pygame.transform.rotozoom(self.image_default, 0, 0.5)
            indicator_rect = indcator_surf.get_rect(center=(20, 20))

            secondsLeft_surf = renderCookieFont(
                f"{int((self.cookie['effect_duration'] - (time() - self.effect_started / 1000)))}",
                size=12,
            )
            secondsLeft_rect = secondsLeft_surf.get_rect(center=(20, 40))

            screen.blit(indcator_surf, indicator_rect)
            screen.blit(secondsLeft_surf, secondsLeft_rect)

            if self.check_effect_expired():
                self.applyEffect(revert=True)
                self.kill()

        elif pygame.mouse.get_pressed()[0] and self.rect.collidepoint(
            pygame.mouse.get_pos()
        ):
            if self.effect_started == -1:
                self.applyEffect()
                self.effect_started = time() * 1000
                self.rect.x = 1000


# Groups
buildings = pygame.sprite.Group()
for build in builds:
    buildings.add(Building(build, builds.index(build)))

goldCookies = pygame.sprite.Group()

# Static Surfaces
cookie_surface = pygame.image.load("./assets/img/cookie.png").convert_alpha()
cookie_rect = cookie_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))

background_surface = pygame.image.load("./assets/img/background.png").convert()
background_rect = background_surface.get_rect()

cookieInfo_surface = renderCookieFont(f"{cookieAmount} cookies")
cookieInfo_rect = cookieInfo_surface.get_rect(midtop=(WIDTH / 2, HEIGHT * 10 / 800))
pygame.display.set_icon(cookie_surface)

cpsInfo_surface = renderCookieFont(f"{cps}/s", size=15)
cpsInfo_rect = cpsInfo_surface.get_rect(midtop=(WIDTH / 2 - 5, HEIGHT * 90 / 800))

# Timers
cps_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cps_timer, 1000)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if savable == True:
                with open("./save/save.json", "w") as file:
                    dump(
                        {
                            "date": time() * 1000,
                            "variables": {
                                "cookies": cookieAmount,
                                "cps": cps,
                                "cpc": cpc,
                                "cps_multiplier": cps_multiplier,
                                "cpc_multiplier": cpc_multiplier,
                            },
                            "buildings": builds,
                            "goldcookies": goldcookies,
                            "upgrades": [],
                        },
                        file,
                    )
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                currentMode = modes.COOKIE
            elif event.key == pygame.K_2:
                currentMode = modes.BUILDS
            elif event.key == pygame.K_3:
                currentMode = modes.UPGRADES
        if event.type == pygame.MOUSEBUTTONUP and currentMode == modes.COOKIE:
            if cookie_rect.collidepoint(event.pos):
                cookieAmount += cpc * cpc_multiplier
                updateCookieInfo()

        if event.type == cps_timer:
            cookieAmount += cps * cps_multiplier
            if randint(1, 60) == 60:

                def goldCookieOfType(type: str = gctypes.FRENZY) -> dict:
                    return list(filter(lambda gc: gc["type"] == type, goldcookies))[0]

                goldCookies.add(
                    GoldenCookie(
                        choice(
                            [
                                goldCookieOfType(gctypes.FRENZY),
                                goldCookieOfType(gctypes.FRENZY),
                                goldCookieOfType(gctypes.FRENZY),
                                goldCookieOfType(gctypes.FRENZY),
                                goldCookieOfType(gctypes.CFRENZY),
                            ]
                        )
                    )
                )
                print("spawned gold cookie")
            updateCookieInfo()

    if currentMode == modes.COOKIE:
        screen.blit(background_surface, background_rect)
        screen.blit(cookie_surface, cookie_rect)
        screen.blit(cookieInfo_surface, cookieInfo_rect)
        screen.blit(cpsInfo_surface, cpsInfo_rect)

        goldCookies.draw(screen)
        goldCookies.update()

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

    pygame.display.update()
    clock.tick(60)

pygame.quit()

import pygame

from upgrades import upgrades

import constants.modes as modes
import constants.upgradetypes as types

from constants.settings import *

pygame.init()

# pygame
clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# pygame variables
running = True

# game variables
cookieAmount = 0
cps = 1  # Cookies per second
cpc = 1  # Cookies per click
cps_multiplier = 1
cpc_multiplier = 1

currentMode = modes.BAKERY

# fonts
def renderCookieFont(
    text: str, antiAlias: bool, color: tuple | list, size: int | float = 25
):
    cookieFont = pygame.font.Font("./assets/font/Kavoon-Regular.ttf", int(size))
    return cookieFont.render(str(text), antiAlias, color).convert_alpha()


# game functions
def formatAmount(amount):
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


def updateCookieInfo(amount):
    global cookieInfo_surface
    cookieInfo_surface = renderCookieFont(
        f"{formatAmount(amount)} cookies", True, [255, 255, 255]
    )


# surfaces
cookie_surface = pygame.image.load("./assets/img/cookie.png")
cookie_surface = pygame.transform.scale(cookie_surface, [350, 350]).convert()
cookie_rect = cookie_surface.get_rect(center=(250, 400))

background_surface = pygame.image.load("./assets/img/background.jpg").convert()
background_rect = background_surface.get_rect()

cookieInfo_surface = renderCookieFont("0 cookies", True, [255, 255, 255])
cookieInfo_rect = cookieInfo_surface.get_rect(midtop=(250, 50))

pygame.display.set_caption("Cookie Clicker")
pygame.display.set_icon(cookie_surface)

# timers
cps_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cps_timer, 1000)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                currentMode = modes.BAKERY
            elif event.key == pygame.K_2:
                currentMode = modes.UPGRADES
        if event.type == pygame.MOUSEBUTTONUP:
            if cookie_rect.collidepoint(event.pos):
                cookieAmount += cpc * cpc_multiplier
                updateCookieInfo(cookieAmount)

        if event.type == cps_timer:
            cookieAmount += cps * cps_multiplier
            updateCookieInfo(cookieAmount)

    if currentMode == modes.BAKERY:
        screen.blit(background_surface, background_rect)
        screen.blit(cookie_surface, cookie_rect)
        screen.blit(cookieInfo_surface, cookieInfo_rect)
    elif currentMode == modes.UPGRADES:
        screen.fill([130, 130, 130])
        background = pygame.image.load("./assets/img/upgrade_bg.png").convert()
        background.set_alpha(165)
        screen.blit(background, background.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        for upgrade in upgrades:
            i = upgrades.index(upgrade)
            upgrade_surface = upgrade["surface"].convert_alpha()
            upgrade_rect = upgrade_surface.get_rect(midleft=(10, 40 + i * 50))
            name_surf = renderCookieFont(upgrade["name"], True, [255, 255, 255], 22)
            name_rect = name_surf.get_rect(
                midleft=(60, 40 + upgrades.index(upgrade) * 50)
            )

            cost_surf = renderCookieFont(
                f"{formatAmount(upgrade['cost'])} cookies", True, [255, 255, 255], 25
            )
            cost_rect = cost_surf.get_rect(
                midleft=(320, 40 + upgrades.index(upgrade) * 50)
            )

            upgrade_surf = pygame.image.load("./assets/img/upgrade_rect.png")
            upgrade_surf.set_alpha(100 + i * 20)
            upgrade_rect = upgrade_surf.get_rect(midleft=(10, 40 + i * 50))

            screen.blit(upgrade_surf, upgrade_rect)
            screen.blit(upgrade_surface, upgrade_rect)
            screen.blit(name_surf, name_rect)
            screen.blit(cost_surf, cost_rect)

            if (
                upgrade_rect.collidepoint(pygame.mouse.get_pos())
                and pygame.mouse.get_pressed()[0]
            ):
                if cookieAmount > upgrade["cost"]:
                    if upgrades.__contains__(upgrade):
                        upgrades.remove(upgrade)
                    if upgrade["type"] == types.CLICK:
                        cpc *= upgrade["amount"]
                        cookieAmount -= upgrade["cost"]

                        print(f"Bought upgrade {upgrade['name']} for {upgrade['cost']}")

    pygame.display.update()
    clock.tick(60)

pygame.quit()

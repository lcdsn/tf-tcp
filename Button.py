import pygame
import os.path


class TextButton:
    def __init__(
        self,
        title: str,
        pos: tuple,
        offset: tuple,
        size: tuple,
        normalColor,
        selectedColor,
        clickedColor,
        fontName,
        fontColor,
        iconPath: str,
        borderRadius: int,
        callbackFunction,
    ):
        self.title = title
        self.pos = pos
        self.offset = offset
        self.width, self.height = size
        self.fontName = fontName
        self.normalColor = normalColor
        self.selectedColor = selectedColor
        self.clickedColor = clickedColor
        self.currentColor = normalColor
        self.fontSize = None
        self.font = None
        self.fontColor = fontColor
        self.iconPath = iconPath
        self.borderRadius = borderRadius
        self.callbackFunction = callbackFunction

        self.padding = tuple(
            [
                self.width * 0.05,
                self.height * 0.05,
                self.width * 0.05,
                self.height * 0.05,
            ]
        )
        self.fontSize = int((self.height - self.padding[0] - self.padding[2]) / 1.3)
        self.loadFont()
        self.buttonSurface = pygame.Surface((self.width, self.height))

    def loadFont(self):
        self.font = pygame.font.Font(
            os.path.join("Fonts", self.fontName), self.fontSize
        )

    def handleEvent(self, event):
        buttonSurfaceRect = (
            self.buttonSurface.get_rect().move(self.offset).move(self.pos)
        )

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if buttonSurfaceRect.collidepoint(event.pos):
                self.currentColor = self.clickedColor
                if self.callbackFunction:
                    self.callbackFunction(self)

        else:
            if buttonSurfaceRect.collidepoint(pygame.mouse.get_pos()):
                self.currentColor = self.selectedColor
            else:
                self.currentColor = self.normalColor

    def draw(self):
        icon = pygame.transform.scale(
            pygame.image.load(self.iconPath), (self.fontSize, self.fontSize)
        )
        text = self.font.render(self.title, True, self.fontColor)

        iconRect = text.get_rect(midleft=(self.padding[0], self.height / 2))
        textRect = text.get_rect(
            midleft=(self.padding[0] + icon.get_width() + 5, self.height / 2)
        )

        self.buttonSurface.fill((255, 255, 255))
        pygame.draw.rect(
            self.buttonSurface,
            self.currentColor,
            (0, 0, self.width, self.height),
            border_radius=self.borderRadius,
        )

        self.buttonSurface.blit(text, textRect)
        self.buttonSurface.blit(icon, iconRect)

        return self.buttonSurface


class IconButton:
    def __init__(
        self,
        pos: tuple,
        size: tuple,
        normalColor,
        selectedColor,
        clickedColor,
        iconPath: str,
        callbackFunction,
    ):
        self.pos = pos
        self.width, self.height = size
        self.normalColor = normalColor
        self.selectedColor = selectedColor
        self.clickedColor = clickedColor
        self.currentColor = normalColor
        self.iconPath = iconPath
        self.callbackFunction = callbackFunction
        self.buttonSurface = pygame.Surface((self.width, self.height))

    def handleEvent(self, event):
        buttonSurfaceRect = self.buttonSurface.get_rect().move(self.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if buttonSurfaceRect.collidepoint(event.pos):
                self.currentColor = self.clickedColor
                self.callbackFunction()
                return buttonSurfaceRect

        else:
            if buttonSurfaceRect.collidepoint(pygame.mouse.get_pos()):
                self.currentColor = self.selectedColor
                return buttonSurfaceRect
            else:
                self.currentColor = self.normalColor

    def draw(self):
        icon = pygame.transform.scale(
            pygame.image.load(self.iconPath), (self.width * 0.8, self.height * 0.8)
        )
        iconRect = icon.get_rect(center=(self.width / 2, self.height / 2))

        self.buttonSurface.fill((255, 255, 255))
        pygame.draw.rect(
            self.buttonSurface,
            self.currentColor,
            (0, 0, self.width, self.height),
        )

        self.buttonSurface.blit(icon, iconRect)

        return self.buttonSurface

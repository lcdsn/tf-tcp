import pygame

import UI
from Button import TextButton


class ListButtons(UI.Area):
    def __init__(
        self,
        pos: tuple,
        listItems: list,
        buttonModel: TextButton,
        size: tuple,
        padding=tuple([5] * 4),
        backgroundColor=(255, 255, 255),
        scrollBarColor=(30, 30, 30),
    ):

        super().__init__(
            pos=pos,
            contentSurface=pygame.Surface(size),
            size=size,
            padding=padding,
            backgroundColor=backgroundColor,
            scrollBarColor=scrollBarColor,
        )

        self.listItems = listItems
        self.buttonModel = buttonModel

        self.contentSurface = pygame.Surface(
            (
                self.width,
                max(
                    self.height,
                    len(self.listItems) * (self.buttonModel.height + self.padding[3]),
                ),
            )
        )
        self.contentSurface.fill((255, 255, 255))
        self.updateScrollBar()

        self.buttonList = []
        for item in self.listItems:
            button = TextButton(
                title=item,
                pos=(0, self.listItems.index(item) * (self.buttonModel.height + 5)),
                offset=self.pos,
                size=(self.buttonModel.width, self.buttonModel.height),
                normalColor=(0, 0, 255),
                selectedColor=(255, 0, 0),
                clickedColor=(0, 255, 0),
                fontName="iosevka-regular.ttf",
                fontColor=(255, 255, 255),
                iconPath="assets/icon-file.png",
                borderRadius=5,
                callbackFunction=self.buttonModel.callbackFunction,
            )
            self.buttonList.append(button)
            self.contentSurface.blit(button.draw(), dest=button.pos)

    def draw(self):
        self.areaSurface.fill(self.backgroundColor)
        pygame.draw.rect(self.areaSurface, (0, 0, 0), self.areaSurface.get_rect(), 2)

        for button in self.buttonList:
            button.offset = (0, -self.visibleContentArea.y)
            self.contentSurface.blit(button.draw(), button.pos)

        self.containerSurface.blit(
            self.contentSurface, self.pos, area=self.visibleContentArea
        )

        self.areaSurface.blit(
            self.containerSurface,
            (self.padding[1], self.padding[0]),
        )

        if (
            int(
                (self.containerSurface.get_height() - self.padding[0] - self.padding[3])
                / self.contentSurface.get_height()
            )
            > 1
        ):
            self.drawScrollBar()

        return self.areaSurface

    def handleEvent(self, event):
        for button in self.buttonList:
            button.handleEvent(event)
        self.scrollBar(event)

import pygame


class Area:
    def __init__(
        self,
        contentSurface,
        size: tuple,
        padding=tuple([5] * 4),
        backgroundColor=(255, 255, 255),
        scrollBarColor=(30, 30, 30),
    ):
        self.width, self.height = size
        self.areaSurface = pygame.Surface((self.width, self.height))
        if len(padding) == 1:
            self.padding = tuple([padding] * 4)
        elif len(padding) == 2:
            self.padding = tuple(padding * 2)
        elif len(padding) == 3:
            self.padding = tuple([padding[0], *[padding[1]] * 2, padding[2]])
        else:
            self.padding = padding
        self.backgroundColor = backgroundColor
        self.contentSurface = contentSurface
        self.containerSurface = pygame.Surface(
            (
                self.width - self.padding[1] - self.padding[3],
                self.height - self.padding[0] - self.padding[2],
            ),
        )
        self.visibleContentArea = pygame.Rect((0, 0), self.containerSurface.get_size())
        self.scrollBarWidth = max(10, int(self.width * 1 / 60))
        self.scrollBarColor = scrollBarColor
        self.scrollBarVelocity = 20
        self.scrollBarRect = None
        self.updateScrollBar()
        self.fullScrollBarRect = pygame.Rect(
            self.width - self.scrollBarWidth, 0, self.scrollBarWidth, self.height
        )
        self.dragging = False

    def updateScrollBar(self):
        self.scrollBarRect = pygame.Rect(
            self.width - self.scrollBarWidth,
            0,
            self.scrollBarWidth,
            int(
                self.height
                * self.containerSurface.get_rect().height
                / self.contentSurface.get_rect().height
            ),
        )

    def draw(self):
        self.areaSurface.fill(self.backgroundColor)

        self.containerSurface.blit(
            self.contentSurface, (0, 0), area=self.visibleContentArea
        )

        self.areaSurface.blit(
            self.containerSurface,
            (self.padding[1], self.padding[0]),
        )
        if (
            int(self.containerSurface.get_height() / self.contentSurface.get_height())
            != 1
        ):
            self.drawScrollBar()
        return self.areaSurface

    def drawScrollBar(self):
        ratio = self.visibleContentArea.y / self.contentSurface.get_height()
        self.scrollBarRect.y = ratio * self.height

        pygame.draw.rect(
            self.areaSurface,
            self.scrollBarColor,
            self.scrollBarRect,
            border_radius=int(self.scrollBarWidth * 0.5),
        )

    def scrollBar(self, event):
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if self.areaSurface.get_rect().collidepoint(mouse_pos):
                self.visibleContentArea.y -= event.y * self.scrollBarVelocity

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.scrollBarRect.collidepoint(event.pos):
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            ratio = event.rel[1] / self.containerSurface.get_rect().height
            self.visibleContentArea.y += ratio * self.contentSurface.get_rect().height

        self.visibleContentArea.y = max(
            0,
            min(
                self.contentSurface.get_rect().height
                - self.containerSurface.get_rect().height,
                self.visibleContentArea.y,
            ),
        )

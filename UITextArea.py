import os.path
import pygame
import UI


class TextArea(UI.Area):
    def __init__(
        self,
        text: str,
        size: tuple,
        fontName: str,
        fontSize: int,
        padding=tuple([5] * 4),
        fontColor=(0, 0, 0),
        cursorColor=(255, 221, 51),
        backgroundColor=(255, 255, 255),
        scrollBarColor=(30, 30, 30),
    ):

        super().__init__(
            contentSurface=pygame.Surface(
                size  # Superficie temporária pra instanciar a classe
            ),
            size=size,
            padding=padding,
            backgroundColor=backgroundColor,
            scrollBarColor=scrollBarColor,
        )

        self.fontName = fontName
        self.fontSize = fontSize
        self.font = None
        self.loadFont()
        self.fontColor = fontColor
        self.cursorPosition = 0
        self.cursorRow = 0
        self.cursorCol = 0
        self.cursorColor = cursorColor
        self.cursorVisibile = True
        self.text = text
        self.cellHeight = self.font.get_linesize()
        self.cellWidth = self.font.size("W")[0]
        self.wrapppedLines = self.wrapText()
        self.lenghtLines = [len(line) for line in self.wrapppedLines]

        self.contentSurface = pygame.Surface(
            (
                self.visibleContentArea.width,
                max(
                    self.visibleContentArea.height,
                    self.cellHeight * len(self.wrapppedLines),
                ),
            )
        )
        self.contentSurface.fill(self.backgroundColor)
        self.scrollBarRect = None
        self.updateScrollBar()

    def loadFont(self):
        self.font = pygame.font.Font(
            os.path.join("Fonts", self.fontName), self.fontSize
        )

    def wrapText(self):
        wrapppedLines = []
        i, j = 0, 0

        while j < len(self.text):
            if self.text[j] == "\n" or (
                self.font.size(self.text[i : j + 1])[0]
                > self.containerSurface.get_width() - self.padding[1]
            ):
                wrapppedLines.append(self.text[i : j + 1])
                i = j + 1
            j += 1

        return wrapppedLines

    def drawText(self):
        for i in range(len(self.wrapppedLines)):
            self.contentSurface.blit(
                self.font.render(
                    self.wrapppedLines[i], True, self.fontColor, self.backgroundColor
                ),
                (0, self.cellHeight * i),
            )

        row, col = 0, 0
        count = 0
        while (
            row < len(self.wrapppedLines)
            and count + self.lenghtLines[row] <= self.cursorPosition
        ):
            count += self.lenghtLines[row]
            row += 1
        col = self.cursorPosition - count
        self.drawCursor(row, col)

    def updateContentSurface(self):
        self.cellHeight = self.font.get_linesize()
        self.cellWidth = self.font.size("W")[0]
        self.wrapppedLines = self.wrapText()
        self.lenghtLines = [len(line) for line in self.wrapppedLines]

        self.contentSurface = pygame.Surface(
            (
                self.visibleContentArea.width,
                max(
                    self.visibleContentArea.height,
                    self.cellHeight * len(self.wrapppedLines),
                ),
            )
        )
        self.contentSurface.fill(self.backgroundColor)

    def resizeText(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if (
            event.type == pygame.KEYDOWN
            and self.containerSurface.get_rect().collidepoint(mouse_pos)
        ):
            keys = pygame.key.get_pressed()
            if event.mod & pygame.KMOD_SHIFT and event.mod & pygame.KMOD_CTRL:
                if keys[pygame.K_EQUALS]:
                    self.fontSize = min(self.fontSize + 2, 50)
                    self.loadFont()
                    self.updateContentSurface()

                if keys[pygame.K_MINUS]:
                    self.fontSize = max(self.fontSize - 2, 1)
                    self.loadFont()
                    self.updateContentSurface()
        self.updateScrollBar()

    def scrollBack(self):
        self.visibleContentArea.y = self.cursorRow * self.cellHeight

    def moveCursor(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if (
            event.type == pygame.KEYDOWN
            and self.containerSurface.get_rect().collidepoint(mouse_pos)
        ):
            if not self.cursorVisibile:
                self.scrollBack()
                self.cursorVisibile = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.cursorPosition = max(0, self.cursorPosition - 1)

            elif keys[pygame.K_RIGHT]:
                self.cursorPosition = min(
                    self.cursorPosition + 1, sum(self.lenghtLines)
                )

            elif keys[pygame.K_DOWN] and self.cursorRow < len(self.wrapppedLines) - 1:
                targetCol = min(
                    self.cursorCol, self.lenghtLines[self.cursorRow + 1] - 1
                )
                self.cursorPosition = (
                    sum(self.lenghtLines[: self.cursorRow + 1]) + targetCol
                )

            elif keys[pygame.K_UP] and self.cursorRow > 0:
                targetCol = min(
                    self.cursorCol, self.lenghtLines[self.cursorRow - 1] - 1
                )
                self.cursorPosition = (
                    sum(self.lenghtLines[: self.cursorRow - 1]) + targetCol
                )

        if (
            (self.cursorRow + 1) * self.cellHeight
            > self.visibleContentArea.y + self.visibleContentArea.height
            and self.cursorVisibile
        ):
            self.visibleContentArea.y += self.cellHeight

        if (
            self.cursorRow
        ) * self.cellHeight < self.visibleContentArea.y and self.cursorVisibile:
            self.visibleContentArea.y -= self.cellHeight

    def drawCursor(self, row, col):
        if (
            row < 0
            or row >= len(self.wrapppedLines)
            or col < 0
            or col >= len(self.wrapppedLines[row])
        ):
            return

        self.cursorRow = row
        self.cursorCol = col

        self.contentSurface.blit(
            pygame.Font.render(
                self.font,
                self.wrapppedLines[row][col],
                True,
                self.fontColor,
                self.cursorColor,
            ),
            (self.cellWidth * col, self.cellHeight * row),
        )

    def draw(self):
        self.areaSurface.fill(self.backgroundColor)
        self.containerSurface.fill(self.backgroundColor)

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
        self.drawText()
        return self.areaSurface

    def scrollBar(self, event):
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if self.areaSurface.get_rect().collidepoint(mouse_pos):
                self.visibleContentArea.y -= event.y * self.scrollBarVelocity
            self.cursorVisibile = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.scrollBarRect.collidepoint(event.pos):
                self.dragging = True
            self.cursorVisibile = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            ratio = event.rel[1] / self.containerSurface.get_rect().height
            self.visibleContentArea.y += ratio * self.contentSurface.get_rect().height
            self.cursorVisibile = False

        if not self.cursorVisibile:
            self.visibleContentArea.y = max(
                0,
                min(
                    self.contentSurface.get_rect().height
                    - self.containerSurface.get_rect().height,
                    self.visibleContentArea.y,
                ),
            )

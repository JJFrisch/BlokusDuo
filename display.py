import pygame

ORANGE = (255, 165, 0)
PURPLE = (127, 0, 255)

#This will be the class for the display, which includes setting up the board and updating it when pieces are laid by either opponent.
class Display:
    def __init__(self, s, px, board, pieces):
        self.s = s
        self.px = px
        self.board = board
        self.pieces = pieces

        self.running = True
        self.invHeight = 4 * px
        self.width = s * px
        self.height = s * px

        # piece num, orientation
        self.hovered = [5, 1]
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height + self.invHeight))
        self.clock = pygame.time.Clock()

        self.text = ''
        self.font = pygame.font.SysFont("monospace", 30)
        self.renderedText = self.font.render(self.text, True, (0, 0, 0))
        
        self.update()

    def update(self):
        pygame.display.flip()

    def drawHovered(self, x, y):
        color = ORANGE
        for i, j in self.pieces[self.hovered[0]][self.hovered[1]][0]:
            pygame.draw.rect(self.screen, color, (i * self.px + x - self.px / 2, j * self.px + y - self.px / 2, self.px, self.px))
        pygame.draw.rect(self.screen, color, (x - self.px / 2, y - self.px / 2, self.px, self.px))

    def draw(self):
        board = self.board.board

        self.screen.fill((255, 255, 255))
        for i in range(1, self.s + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.px), (self.width, i * self.px))
        for i in range(1, self.s + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.px, 0), (i * self.px, self.height))
        
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 1:
                    color = ORANGE
                elif board[i][j] == 2:
                    color = PURPLE
                else: continue

                pygame.draw.rect(self.screen, color, (j * self.px + 1, i * self.px + 1, self.px - 2, self.px - 2))

        textRect = self.renderedText.get_rect()
        textRect.center = (self.width // 2, self.height + self.invHeight // 2)
        self.screen.blit(self.renderedText, textRect)
    
    def humanTurn(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.hovered:
                        i, j = pygame.mouse.get_pos()
                        i, j = i // self.px, j // self.px

                        if self.board.is_valid_to_place_here(i, j):
                            self.board.place_piece([i, j, self.hovered[0], self.hovered[1], 0, 0])
                            self.hovered = None
                            return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if self.hovered:
                            self.hovered[1] += 1
                            if self.hovered[1] >= 8:
                                self.hovered[1] -= 8
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                        self.renderedText = self.font.render(self.text, True, (0, 0, 0))
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9] and len(self.text) <= 1:
                        self.text += event.unicode
                        self.renderedText = self.font.render(self.text, True, (0, 0, 0))
                    elif event.key == pygame.K_RETURN:
                        pieceNum = int(self.text)
                        self.hovered = [pieceNum, 0]
                    
                
            x, y = pygame.mouse.get_pos()
            self.draw()
            if self.hovered:
                self.drawHovered(x, y)
            
            self.update()
            self.clock.tick(60)




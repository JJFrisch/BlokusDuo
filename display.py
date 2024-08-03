import pygame
from orient import generatePiecesDict, pieces
from board import piece_possible_orientations

pieces = generatePiecesDict(pieces)

ORANGE = (255, 165, 0)
PURPLE = (127, 0, 255)

ORAPUR = tuple((ORANGE[i] + PURPLE[i]) // 2 for i in range(3))
#This will be the class for the display, which includes setting up the board and updating it when pieces are laid by either opponent.
class Display:

    def __init__(self, s, px, board):
        self.s = s
        self.px = px
        self.board = board

        self.running = True
        self.invHeight = 4 * px
        self.width = s * px
        self.height = s * px

        # piece num, orientation
        self.hovered = [5, 0]

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width, self.height + self.invHeight))
        self.clock = pygame.time.Clock()

        self.pieceText = ''
        self.pieceFont = pygame.font.SysFont("monospace", self.px * 2)
        self.renderedPieceText = self.pieceFont.render(self.pieceText, True, (0, 0, 0))

        self.scoreFont = pygame.font.SysFont("monospace", self.px)
        self.scoreText = ['0', '0']
        self.renderedScoreText = [self.scoreFont.render(self.scoreText[0], True, ORANGE), self.scoreFont.render(self.scoreText[1], True, PURPLE)]
        
        self.update()

    def update(self):
        self.scoreText = [str(self.board.score[0]), str(self.board.score[1])]
        self.renderedScoreText = [self.scoreFont.render(self.scoreText[0], True, ORANGE), self.scoreFont.render(self.scoreText[1], True, PURPLE)]
        pygame.display.flip()

    def drawHovered(self, x, y):
        color = ORANGE
        if self.board.turn % 2 == 0:
            color = PURPLE

        poss_orientations = piece_possible_orientations[self.hovered[0]]
        for i, j in pieces[self.hovered[0]][poss_orientations[self.hovered[1]]][0]:
            pygame.draw.rect(self.screen, color,
                             (i * self.px + x - self.px / 2,
                              j * self.px + y - self.px / 2, self.px, self.px))
        pygame.draw.rect(self.screen, color,
                         (x - self.px / 2, y - self.px / 2, self.px, self.px))

    def draw(self):
        board = self.board.board

        self.screen.fill((255, 255, 255))
        for i in range(1, self.s + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.px),
                             (self.width, i * self.px))
        for i in range(1, self.s + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.px, 0),
                             (i * self.px, self.height))

        color = ORANGE
        for i, j, _ in self.board.possible_squares[0]:
            pygame.draw.circle(self.screen, color,
                               ((i + 0.5) * self.px, (j + 0.5) * self.px),
                               self.px / 3)

        color = PURPLE
        for i, j, _ in self.board.possible_squares[1]:
            pygame.draw.circle(self.screen, color,
                               ((i + 0.5) * self.px, (j + 0.5) * self.px),
                               self.px / 3)

        color = ORAPUR
        for poss in self.board.possible_squares[0]:
            if poss in self.board.possible_squares[1]:
                i, j, _ = poss
                pygame.draw.circle(self.screen, color,
                       ((i + 0.5) * self.px, (j + 0.5) * self.px),
                       self.px / 3)

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 1:
                    color = ORANGE
                elif board[i][j] == 2 or board[i][j] == -1:
                    color = PURPLE
                else:
                    continue

                pygame.draw.rect(self.screen, color,
                                 (j * self.px + 1, i * self.px + 1,
                                  self.px - 2, self.px - 2))

        textRect = self.renderedPieceText.get_rect()
        textRect.center = (self.width // 2, self.height + self.invHeight // 2)
        self.screen.blit(self.renderedPieceText, textRect)

        color = ORANGE
        if self.board.turn % 2 == 0:
            color = PURPLE
        pygame.draw.circle(self.screen, color, (self.width // 2, self.height + self.invHeight // 2 + textRect.height // 2 + 5), self.px // 3)

        textRect = self.renderedScoreText[0].get_rect()
        textRect.center = (textRect.width // 2 + self.px // 3, self.height + self.invHeight // 2)
        self.screen.blit(self.renderedScoreText[0], textRect)

        textRect = self.renderedScoreText[1].get_rect()
        textRect.center = (self.width - textRect.width // 2 - self.px // 3, self.height + self.invHeight // 2)
        self.screen.blit(self.renderedScoreText[1], textRect)

    def humanTurn(self, place=True):
        legalMoves = self.board.calculateLegalMoves()
        
        if len(legalMoves) == 0:
            self.board.finished[self.board.turn - 1] - True
            return False
            
        # if self.board.turn <= 2:
        #     legalMoves = self.board.calculateLegalMovesEarly()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.hovered:
                        i, j = pygame.mouse.get_pos()
                        i, j = i // self.px, j // self.px
                        poss_orientations = piece_possible_orientations[self.hovered[0]]
                        move = [i, j, self.hovered[0], poss_orientations[self.hovered[1] % len(poss_orientations)]]
                        print(move)
                        if move in legalMoves:
                            if place:
                                self.board.place_piece(move)
                            self.hovered = None
                            return move
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if self.hovered:
                            self.hovered[1] += 1
                            poss_orientations = piece_possible_orientations[self.hovered[0]]
                            self.hovered[1] %= len(poss_orientations)
                    elif event.key == pygame.K_BACKSPACE:
                        self.pieceText = self.pieceText[:-1]
                        self.renderedPieceText = self.pieceFont.render(
                            self.pieceText, True, (0, 0, 0))
                    elif event.key in [
                            pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
                            pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                            pygame.K_8, pygame.K_9
                    ] and len(self.pieceText) <= 1:
                        self.pieceText += event.unicode
                        self.renderedPieceText = self.pieceFont.render(
                            self.pieceText, True, (0, 0, 0))
                    elif event.key == pygame.K_RETURN:
                        pieceNum = int(self.pieceText)
                        pieceNum -= 1
                        if pieceNum >= 0 and pieceNum <= 20:
                            self.hovered = [pieceNum, 0]
                            poss_orientations = piece_possible_orientations[self.hovered[0]]
                            self.hovered[1] %= len(poss_orientations)

            x, y = pygame.mouse.get_pos()
            self.draw()
            if self.hovered:
                self.drawHovered(x, y)

            self.update()
            self.clock.tick(60)

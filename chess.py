#!/bin/python3

testBoard = [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','.','p','p','p','p'],
    ['.','.','.','.','q','.','.','.'],
    ['.','.','.','p','.','P','.','.'],
    ['.','K','P','N','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['P','P','.','P','P','.','P','P'],
    ['R','N','B','Q','.','B','N','R'],
]
startBoard = [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','p','p','p','p','p'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['P','P','P','P','P','P','P','P'],
    ['R','N','B','Q','K','B','N','R'],
]

symbols = {
    'r':'♖', 'n':'♘', 'b':'♗', 'q':'♕', 'k':'♔', 'p':'♙', 
    'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'P':'♟', '.': ' ', 'X':'X'
}

def reverse(lst):
    if len(lst) == 1:
        return [lst[0]]
    return reverse(lst[1:]) + [lst[0]]

def line(i):
    if i == 0:
        return '┌' + '───┬'*7 + '───┐'
    elif i == 8:
        return '└' + '───┴'*7 + '───┘'
    return '├' + '───┼'*7 + '───┤'

def formatBoard(board):
    ret = ''
    for i, row in enumerate(board):
        ret += '\n ' + line(i) + '\n' + str(yAxis[i])
        for square in row:
            ret += '│ ' + symbols[square] + ' '
        ret += '│'
    ret += '\n ' + line(8) + '\n   '
    for let in xAxis:
        ret += let + '   '
    return ret  

xAxis = ['a','b','c','d','e','f','g','h']
yAxis = [str(num) for num in range(8,0,-1)]

def xyFromLetterNum(letterNum):
    y = yAxis.index(letterNum[1])
    x = xAxis.index(letterNum[0])
    return (x,y)

def pieceAt(board, coordinate): #(x,y)
    x, y = coordinate
    return board[y][x]

allCoordinates = [(x, y) for x in range(8) for y in range(8)]

def isInLine(fromSquare, square, slope): #(x,y), (4,2), 1/'inf'/..
    dx = square[0] - fromSquare[0]
    dy = square[1] - fromSquare[1]
    return dy/dx == slope if dx != 0 else slope == 'inf' or dy == 0

def splitLine(coordinates, split): 
    i = coordinates.index(split)
    return [coordinates[:i+1]] + [coordinates[i:]]

def joinLines(lines):
    return [coordinate for line in lines for coordinate in line]

def lineFromSquare(square, slope):
    return [coordinate for coordinate in allCoordinates if isInLine(square, coordinate, slope)]

def linesFromSquare(square, slopes):
    return [line for slope in slopes for line in splitLine(lineFromSquare(square, slope), square)]

def orderLines(lines, coordinate): #Lines will start from the piece's coordinates.
    return [line[1:] if line[0] == coordinate else reverse(line)[1:] for line in lines]

def linesOfPiece(piece, square):
    return orderLines(linesFromSquare(square, slopesOfPiece(piece)), square)

def slopesOfPiece(piece):
    return {
        'r':(0,'inf'), 'n':(0.5,-0.5,2,-2), 'b':(1,-1),
        'q':(0,'inf',1,-1), 'k':(0,'inf',1,-1), 'p': ('inf',1,-1)       
    }[piece.lower()]

def highlitBoard(board, coordinates):
    return [["X" if (x,y) in coordinates else piece
            for x, piece in enumerate(row)]
            for y, row in enumerate(board)]

def isPiece(board, coordinate):
    return pieceAt(board, coordinate) != '.'

def stopLinesOnPiece(board, lines): #[[(0,0), (1,1), (3,3), (4,4)], [(x,y)]]
    ret = []
    for line in lines:
        newLine = []
        for coordinate in line:
            newLine.append(coordinate)
            if isPiece(board, coordinate):
                break
        ret.append(newLine)
    return ret

def onlyForward(piece, coordinate, lines):
    isForward = lambda y: y > coordinate[1] if piece.islower() else y < coordinate[1]
    return [[(x,y) 
            for x,y in line
            if isForward(y)]
            for line in lines]

def pawnMovement(piece, coordinate, lines):
    return [line[:1] if (
                len(line) == 0 or
                line[0][0] != coordinate[0] or
                coordinate[1] != {'p':1, 'P':6}[piece] #First move is 2 range
            )
            else line[:2]
            for line in lines]

def oneRange(lines):
    return [line[:1] for line in lines]

def cutOffOutOfRange(piece, coordinate, lines):
    pieceType = piece.lower()
    if pieceType == 'p':
        return pawnMovement(piece, coordinate,
                onlyForward(piece, coordinate, lines))
    elif pieceType in ['n', 'k']:
        return oneRange(lines)
    return lines

def pawnCaptureRules(board, piece, coordinate, lines):
    if piece.lower() != 'p':
        return lines
    return [line[:-1] if (
                len(line) == 0 or (
                    line[0][0] == coordinate[0] and
                    pieceAt(board, line[-1]) != '.'
                ) or (
                    line[0][0] != coordinate[0] and
                    pieceAt(board, line[-1]) == '.'
                )
            )
            else line
            for line in lines]

def areEnemies(piece1, piece2):
    return (piece1.isupper() ^ piece2.isupper())

def aPieceIsEmpty(piece1, piece2):
    return piece1 == '.' or piece2 == '.'

def popFriendlyPieces(board, piece, lines):
    return [line if (
                len(line) == 0 or
                areEnemies(pieceAt(board, line[-1]), piece) or
                aPieceIsEmpty(pieceAt(board, line[-1]), piece)
            ) 
            else line[:-1]
            for line in lines]

def legalMoves(board, piece, coordinate):
    return joinLines(
            popFriendlyPieces(board, piece,
            pawnCaptureRules(board, piece, coordinate,
            stopLinesOnPiece(board,
            cutOffOutOfRange(piece, coordinate,
            linesOfPiece(piece, coordinate))))))

def isWon():
    return False

def isSquare(inp):
    return (
        len(inp) == 2 and
        inp[0] in xAxis and
        inp[1] in yAxis
    )

def select(isWhiteTurn, board):
    return lambda inp: pieceAt(board, xyFromLetterNum(inp)).isupper() if isWhiteTurn else pieceAt(board, xyFromLetterNum(inp)).islower()

def move(selLegalMoves, board):
    return lambda inp: xyFromLetterNum(inp) in selLegalMoves

def getSquare(txt, isValid):
    inp = input(txt)
    if not isSquare(inp) or not isValid(inp):
        return getSquare(txt, isValid)
    return inp

def applyMove(board, frm, to):
    frmX, frmY = frm
    toX, toY = to
    ret = list(board)
    p1 = board[frmY][frmX]
    ret[toY][toX] = p1
    ret[frmY][frmX] = "."
    return ret

def main():
    isWhiteTurn = True
    board = startBoard
    while not isWon():
        print(formatBoard(board))
        
        #SELECT SQUARE
        print("-WHITE-" if isWhiteTurn else "-BLACK-")
        selected = getSquare("Select a square: ", select(isWhiteTurn, board)) 
        selectedCoordinate = xyFromLetterNum(selected)
        selectedPiece = pieceAt(board, selectedCoordinate)
        selectedLegalMoves = legalMoves(board, selectedPiece, selectedCoordinate)
        print(formatBoard(highlitBoard(board, selectedLegalMoves)))

        #MOVE PIECE
        moveTo = getSquare("Move to: ", move(selectedLegalMoves, board))
        moveCoordinate = xyFromLetterNum(moveTo)
        board = applyMove(board, selectedCoordinate, moveCoordinate)

        isWhiteTurn = not isWhiteTurn

if __name__ == "__main__": main()

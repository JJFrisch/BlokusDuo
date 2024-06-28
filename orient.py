def flip(coords):
    for coord in coords:
        coords[0], coords[1] = -coords[0], coords[1]
        
def rotate(coords, amt):
    if amt == 0: return coords
    for coord in coords:
        coords[0], coords[1] = coords[1], -coords[0]
    rotate(coords, amt - 1)

def orient(piece, orientation):
    # 0=default, 1=90, 2=180, 3=270, 4=flip, 5=flip90, 6=flip180, 7=flip270
    f = orientation >= 4
    r = orientation % 4
    
    squares, ne, se, sw, nw = piece
    if f: flip(squares)
    rotate(squares, r)
    return [squares, ne, se, sw, nw]
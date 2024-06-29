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


def rotate_(piece,orientation):
    new_o = []
    ne = []
    se = []
    sw = []
    nw = []

    for edge in piece[orientation][0]:
      # corners
        if edge == [-1,-1]:
          new_o.append([1,-1])
        if edge == [1,-1]:
          new_o.append([1,1])
        if edge == [1,1]:
          new_o.append([-1,1])
        if edge == [-1,1]:
          new_o.append([1,-1])

      # sides
        if edge == [0,-1]:
          new_o.append([1,0])
        if edge == [1,0]:
          new_o.append([0,1])
        if edge == [0,1]:
          new_o.append([-1,0])
        if edge == [-1,0]:
          new_o.append([0,-1])
            
    print(new_o)

    # for edge in new_o:
        
    return new_o

pieces = {
    1: [
        #only has corners on the one block
        [],
        [[0, 0]],
        [[0, 0]],
        [[0, 0]],
        [[0, 0]]
    ],
    12: [
        # orientation #1
        [
            # attached squares
            [[1, -1], [0, -1], [0, 1], [-1, 0]],
            # has northeast corners
            [[0, -1], [1, 0]],
            # has southeast corners
            [[1, 0], [0, 1]],
            # has southwest corners
            [[-1, -1], [0, 1]],
            # has northwest corners
            [[-1, -1]]
        ]
    ]
}

rotate_(pieces[12],0)
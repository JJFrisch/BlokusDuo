import copy

def rotate(prev_orientation): #JF
    new_o = []
    ne = []
    se = []
    sw = []
    nw = []
    to_return = []
    for edge in prev_orientation[0]:
      # corners # shoudln't need to work with numbers larger than 1 for corners, but if we do a slight change would be needed
        if edge == [-1,-1]:
          new_o.append([1,-1])
        if edge == [1,-1]:
          new_o.append([1,1])
        if edge == [1,1]:
          new_o.append([-1,1])
        if edge == [-1,1]:
          new_o.append([1,-1])

        if edge[0] == 0 and edge[1] < 0:
          new_o.append([-1*edge[1],0])
        if edge[0] > 0 and edge[1] == 0:
          new_o.append([0,edge[0]])
        if edge[0] == 0 and edge[1] > 0:
          new_o.append([-1*edge[1],0])
        if edge[0] < 0 and edge[1] == 0:
          new_o.append([0,edge[0]])

    # print(new_o)
    blocks = copy.copy(new_o)
    blocks.append([0,0])
    for edge in blocks:
      #NE
        if [edge[0], edge[1]-1] not in blocks and [edge[0]+1, edge[1]] not in blocks and [edge[0]+1, edge[1]-1] not in blocks:
          ne.append(edge)
        #SE
        if [edge[0]+1, edge[1]] not in blocks and [edge[0], edge[1]+1] not in blocks and [edge[0]+1, edge[1]+1] not in blocks:
          se.append(edge)
        #SW
        if [edge[0], edge[1]+1] not in blocks and [edge[0]-1, edge[1]] not in blocks and [edge[0]-1, edge[1]+1] not in blocks:
          sw.append(edge)
        #NW
        if [edge[0]-1, edge[1]] not in blocks and [edge[0], edge[1]-1] not in blocks and [edge[0]-1, edge[1]-1] not in blocks:
          nw.append(edge)

    to_return.append(new_o)
    to_return.append(ne)
    to_return.append(se)
    to_return.append(sw)
    to_return.append(nw)

    return to_return

def generatePiecesDict(pieces_first_orientation): #JF
  to_return = {}
  for piece_num in pieces_first_orientation.keys():
    orientations = [pieces_first_orientation[piece_num][0]]
    for i in range(7): # there are 8 orientations, 1 is already generated
      prev_orientation = orientations[i]
      next_orientation = rotate(prev_orientation)
      orientations.append(next_orientation)

    to_return[piece_num] = orientations

  return to_return











# not sure if we need whats below this

def flip(coords):
    for coord in coords:
        coords[0], coords[1] = -coords[0], coords[1]
        
# def rotate(coords, amt):
#     if amt == 0: return coords
#     for coord in coords:
#         coords[0], coords[1] = coords[1], -coords[0]
#     rotate(coords, amt - 1)

def orient(piece, orientation):
    # 0=default, 1=90, 2=180, 3=270, 4=flip, 5=flip90, 6=flip180, 7=flip270
    f = orientation >= 4
    r = orientation % 4
    
    squares, ne, se, sw, nw = piece
    if f: flip(squares)
    rotate(squares, r)
    return [squares, ne, se, sw, nw]


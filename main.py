from board import Board
import copy

board = Board(14)

board.place(5, 5, 12, 1, 2) #the manual 2nd rotation of blokc '12'
board.print()



def rotate_(prev_orientation):
    new_o = []
    ne = []
    se = []
    sw = []
    nw = []
    to_return = []
    for edge in prev_orientation[0]:
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

piece_id = {1: "i1", 2: "i2", 3: "triple line", 4: "quadruple line", 12: "f"}
pieces = {
    1: [
      [
        #only has corners on the one block
        [],
        [[0, 0]],
        [[0, 0]],
        [[0, 0]],
        [[0, 0]]
      ]
    ],
  2: [
    [
      #only has corners on the one block
      [[0,-1]],
      [[0, -1]],
      [[0, 0]],
      [[0, 0]],
      [[0, -1]]
    ]
  ],
  # fill in the first forms of the other pieces
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

def generatePiecesDict(pieces_first_orientation):
  to_return = {}
  for piece_num in pieces_first_orientation.keys():
    orientations = [pieces_first_orientation[piece_num][0]]
    for i in range(7): # there are 8 orientations, 1 is already generated
      prev_orientation = orientations[i]
      next_orientation = rotate_(prev_orientation)
      orientations.append(next_orientation)

    to_return[piece_num] = orientations

  return to_return


print(rotate_(pieces[12][0]))
new_pieces = generatePiecesDict(pieces)
print(new_pieces[12][1])
print(new_pieces[1][1])
    
    



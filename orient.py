import copy
# import h5py


# with h5py.File('pieces_storage.hdf5', 'r') as f:
#     d1 = f['pieces']

# with h5py.File('pieces_storage.hdf5', 'w') as f:
#     f.create_dataset('pieces', data = pieces) 

pieces = {1: [[[], [[0, 0]], [[0, 0]], [[0, 0]], [[0, 0]]]], 2: [[[[0, -1]], [[0, -1]], [[0, 0]], [[0, 0]], [[0, -1]]]], 3: [[[[0, -1], [0, 1]], [[0, -1]], [[0, 1]], [[0, 1]], [[0, -1]]]], 4: [[[[0, -1], [0, 1], [0, 2]], [[0, -1]], [[0, 2]], [[0, 2]], [[0, -1]]]], 5: [[[[0, -1], [0, 1], [0, 2], [0, -2]], [[0, -2]], [[0, 2]], [[0, 2]], [[0, -2]]]], 6: [[[[1, 0], [0, -1], [-1, -1]], [[1, 0], [0, -1]], [[1, 0]], [[-1, -1], [0, 0]], [[-1, -1]]]], 7: [[[[0, 1], [1, 0], [-1, 0]], [[1, 0]], [[0, 1], [1, 0]], [[0, 1], [-1, 0]], [[-1, 0]]]], 8: [[[[0, 1], [-1, 0], [-2, 0]], [[0, 0]], [[0, 1]], [[0, 1], [-2, 0]], [[-2, 0]]]], 9: [[[[1, 0], [0, 1], [1, 1]], [[1, 0]], [[1, 1]], [[0, 1]], [[0, 0]]]], 10: [[[[0, 1], [1, 1], [-1, 0], [-1, -1]], [[1, 1], [-1, -1], [0, 0]], [[1, 1]], [[0, 1], [-1, 0]], [[-1, -1]]]], 11: [[[[0, -1], [1, 0], [1, -1], [0, 1]], [[1, -1]], [[1, 0], [0, 1]], [[0, 1]], [[0, -1]]]], 12: [[[[1, -1], [0, -1], [0, 1], [-1, 0]], [[1, -1]], [[1, -1], [0, 1]], [[0, 1], [-1, 0]], [[0, -1], [-1, 0]]]], 13: [[[[0, -1], [0, 1], [1, -1], [-1, -1]], [[1, -1]], [[0, 1], [1, -1]], [[0, 1], [-1, -1]], [[-1, -1]]]], 14: [[[[1, 0], [0, -1], [-1, 0], [0, 1]], [[1, 0], [0, -1]], [[1, 0], [0, 1]], [[-1, 0], [0, 1]], [[0, -1], [-1, 0]]]], 15: [[[[0, -1], [-1, -1], [0, 1], [1, 1]], [[0, -1], [1, 1]], [[1, 1]], [[-1, -1], [0, 1]], [[-1, -1]]]], 16: [[[[1, 0], [2, 0], [0, -1], [0, -2]], [[2, 0], [0, -2]], [[2, 0]], [[0, 0]], [[0, -2]]]], 17: [[[[0, -1], [1, 1], [0, 1], [1, -1]], [[1, 1], [1, -1]], [[1, 1], [1, -1]], [[0, 1]], [[0, -1]]]], 18: [[[[1, 0], [0, -1]], [[1, 0], [0, -1]], [[1, 0]], [[0, 0]], [[0, -1]]]], 19: [[[[0, -1], [1, -1], [-1, 0], [-2, 0]], [[1, -1]], [[1, -1], [0, 0]], [[-2, 0]], [[0, -1], [-2, 0]]]], 20: [[[[-2, 0], [-1, 0], [0, 1], [1, 1]], [[1, 1], [0, 0]], [[1, 1]], [[-2, 0], [0, 1]], [[-2, 0]]]], 21: [[[[-3, 0], [-2, 0], [-1, 0], [0, 1]], [[0, 0]], [[0, 1]], [[-3, 0], [0, 1]], [[-3, 0]]]]}

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
          new_o.append([-1,-1])

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
  to_return = []
  for piece_num in pieces_first_orientation.keys():
    orientations = [pieces_first_orientation[piece_num][0]]
    for i in range(3): # there are 3 more orientations, 1 is already generated
      prev_orientation = orientations[i]
      next_orientation = rotate(prev_orientation)
      orientations.append(next_orientation)

    # time to flip the first orientation
    next_orientation = []
    for i in range(len(orientations[0])):
      part_of_orientation = []
      for edge in orientations[0][i]:
        if edge != []:
          part_of_orientation.append([edge[0]*-1, edge[1]])
      next_orientation.append(part_of_orientation)
    orientations.append(next_orientation)

    for i in range(4,7): # there are 3 more orientations, 1 is already generated
      prev_orientation = orientations[i]
      next_orientation = rotate(prev_orientation)
      orientations.append(next_orientation)
    
    to_return.append(orientations)

  return to_return

def generatePiecesFromBlockPos():
    p = {}
    for i in range(1, 22):
        l = [[pieces[i][0][0]]]
        NE, SE, SW, NW = generateCorners(pieces[i][0][0])
        l[0].append(NE)
        l[0].append(SE)
        l[0].append(SW)
        l[0].append(NW)
        p[i] = l
    print(p)

def generateCorners(piece_):
    piece = piece_[:]
    piece.append([0, 0])
    # print(piece)
    corners = []
    NE, SE, SW, NW = [], [], [], []
    for i, j in piece:
        for ai, aj, n in ((-1, -1, 'NW'), (-1, 1, 'SW'), (1, -1, 'NE'), (1, 1, 'SE')):
            ni, nj = i + ai, j + aj
            coords = ([i, nj], [ni, j])
            flag = False
            for coord in coords:
                if coord in piece:
                    flag = True
                    break
            if flag == False:
                if n == 'NW': NW.append([i, j])
                if n == 'SW': SW.append([i, j])
                if n == 'NE': NE.append([i, j])
                if n == 'SE': SE.append([i, j])
    return [NE, SE, SW, NW]
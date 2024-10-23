# BlokusDuo
An exploration into the game of [Blokus](https://en.wikipedia.org/wiki/Blokus) through gameplay optimization using Minimax algorithms.
### By Jake Frischmann, Etash Jhanji, Alden Bressler, Delia Brown, Micheal Huang, and Sebastian Liu


PGSS Project Paper
https://tesdnet-my.sharepoint.com/:w:/g/personal/25frischmannj_tesdk12_net/Eaq9sagThWhFvesd_CqsRSwBd00tdYPEoN6t86uTtX1hGA?e=fx7OIc



The names and original orientations
[here](pieces_numbered.png)

 
The reference sheet for the names, point count, corners and orientations of the blocks.
https://docs.google.com/spreadsheets/d/1dFAExdQarvSGbGUxz0TBeIQ9M-47H39ZSjkkdOUDPpI/edit?gid=0#gid=0
#### A deep explination of Alpha Zero
https://nikcheerla.github.io/deeplearningschool/2018/01/01/AlphaZero-Explained/

#### For us to commit back to GitHub:
* open a terminal from the folder BlokusDuo,
* type in the terminal: git commit -a
* write the information about the commit and close the tab
* type in the terminal: git push

### Blokus Statistical Data spreadsheet
https://docs.google.com/spreadsheets/d/1ivdX9h0s2E_GwyQ3qc64Rtgm8QBoLK1yau-i_zxqZCg/edit?usp=sharing

### To commit large data files:
 - git lfs
 - cd # type the location(folder) of the file here
 One of these, to follow a sinlge file, or a type of files
 - git lfs track "file name"
 - git lfs track "*.mp4"

 - git add .gitattributes
 - git add . (for all files), git add fileName.mp4 (for a single file)
 - git commit -m "add large files"
 - git push


`aecTrain.py` and `aecView.py` are from https://pettingzoo.farama.org/tutorials/sb3/connect_four/ by Elliot (https://github.com/elliottower).


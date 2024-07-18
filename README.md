# BlokusDuo
### created by, Jake Frischmann, Delia Brown, Alden Bressler, Sebastian Liu, Etash Jhanji, Micheal Huang

The names and original orientations
![image](pieces.png)

 
The reference sheet for the names, point count, corners and orientations of the blocks.
https://docs.google.com/spreadsheets/d/1dFAExdQarvSGbGUxz0TBeIQ9M-47H39ZSjkkdOUDPpI/edit?gid=0#gid=0

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
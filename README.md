# Floor plan chair counting tool

cli tool according to the specifications [here](task_en.txt)

## Usage

```
python floorplan.py rooms.txt
```
**additional features**
`--plot`
Will show the extracted floor plan with room names and annotated chairs,
`--progress`
Will show the progress of the room recognition for educational or bug fixing purposes.

## Technical background
* cli tool tries to keep the number of required libraries to an absolute minimum
* `pip install -r /path/to/requirements.txt` for necessary libraries

**How does it work**
* file is read and converted to its Unicode int representation
    * the floor plan needs to be rectangular atm (This could be changed in by filling it to rectangular shape in the future)
* all room names are search (identifying them by their enclosing brackets)
* starting from the the the opening brackets position the algorithm select coordinates a Manhattan distance of 1 away
---> this coordinates are then checked if they contain wall elements
---> if so they are removed from this set of coordinates
---> from this new set again the neighbors of each point a Manhattan distance of 1 away are select
...
---> This goes on as long as the area is growing
* all names and wall elements are removed from the floor plan to get the coordinates of all chairs
* The chairs are mapped into the rooms by coordinates
* results are printed

**Why work with coordinates**
As can be seen with the plot option, this enables us to get the floor plan as geometric object making it very easy in the future to extend the tool beyond the now intend use.


## Further TODO
* constants (wall elements characters, etc.) in configuration `.json` file
* handling of non rectangular floor plan files
* handling of open room shapes
* more efficient finding of next elements in room mapping
* unit test
* interpretation test; create more test cases
* ...

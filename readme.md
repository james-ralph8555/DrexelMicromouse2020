Algorithm steps:

-Find path to goal with A*

-Explore unvisited tiles between start and goal

-While exploring, currently acheivable score (using visited tiles only) and score with optimal path (assuming no walls on unvisited tiles)

-if optimal path score < currently acheivable score, keep exploring else stop

-goto start

-goto goal

Todo:

-implement optimized movement algorithm

-implement way to find best path given visited tiles

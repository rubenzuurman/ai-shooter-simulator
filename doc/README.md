# Plan

An environment in which geometrical objects and players can be placed. A 
player has an update function for when in battle, the inputs are position, 
orientation (n/s, e/w), and n rays emanating in the direction the player is 
facing. The output is velocity and angular velocity.

A higher level class handles spawning of environments and assigning of players 
using a matchmaking system, it also handles updating players' ratings.

MatchMaking class: run separate process updating the current matches and to 
accept new matches from a shared dictionary. Each match yield the current position and rotation of the players after updating.

13-05-2023
Change of plan: I can't get intersections between lines working, so I might just ommit the whole idea of rays and give players the position of the opponent as well.

11-06-2023
I implemented intersections between lines and intersections between lines and circles, so the above note 'Change of plan' no longer applies.

02-07-2023
Random names source: https://www.rong-chang.com/namesdict/popular_names.htm
Random colors source: https://www.rapidtables.com/web/color/RGB_Color.html

03-07-2023
Today I fixed a major bug, if the window was being resized when a match ended, when the resizing was done the value of the status_dict\[match_index\] would be None, and the for loop finalizing the match in mm.update\(\) would crash. This happened because the Environment.update\(\) function returns None when the match is finished, and the handle_matches\(\) function (which runs on a separate) just copied this None into the status dict. Now the function first checks if the return value is not None, and only if it's not it replaces the entry in the status_dict dictionary.

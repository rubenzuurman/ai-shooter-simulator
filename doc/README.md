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
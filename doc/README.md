# Plan

An environment in which geometrical objects and players can be placed. A 
player has an update function for when in battle, the inputs are position, 
orientation (n/s, e/w), and n rays emanating in the direction the player is 
facing. The output is velocity and angular velocity.

A higher level class handles spawning of environments and assigning of players 
using a matchmaking system, it also handles updating players' ratings.
# Plan

### The general idea
An environment in which geometrical objects and players can be placed. A 
player has an update function for when in battle, the inputs are position, 
orientation (n/s, e/w), and n rays emanating in the direction the player is 
facing. The output is velocity and angular velocity.

A higher level class handles spawning of environments and assigning of players 
using a matchmaking system, it also handles updating players' ratings.

MatchMaking class: run separate process updating the current matches and to 
accept new matches from a shared dictionary. Each match yield the current position and rotation of the players after updating.

### Getting started
1. Clone the repo using `git clone https://github.com/rubenzuurman/ai-shooter-simulator.git`.
2. Create a virtual environment in the cloned folder using `python -m venv venv`.
3. Activate the virtual environment using `source venv/Scripts/active` on windows, or `source venv/bin/activate` on posix systems ([documentation](https://docs.python.org/3/library/venv.html)).
4. Install the required dependencies using `pip install -r requirements.txt`.
5. Add players using (e.g.) `mm.add_player(Player())` in `src/application.py`.
6. Implement your own player by creating a class which extends the `Player` class, and overriding the `update()` method. (Optional)
7. Run the application using `python -u src/application.py`. A `log.txt` file will be generated in the top level of the cloned directory.

### Some general comments
13-05-2023
Change of plan: I can't get intersections between lines working, so I might just ommit the whole idea of rays and give players the position of the opponent as well.

11-06-2023
I implemented intersections between lines and intersections between lines and circles, so the above note 'Change of plan' no longer applies.

02-07-2023
Random names source: https://www.rong-chang.com/namesdict/popular_names.htm
Random colors source: https://www.rapidtables.com/web/color/RGB_Color.html

03-07-2023
Today I fixed a major bug, if the window was being resized when a match ended, when the resizing was done the value of the status_dict\[match_index\] would be None, and the for loop finalizing the match in mm.update\(\) would crash. This happened because the Environment.update\(\) function returns None when the match is finished, and the handle_matches\(\) function (which runs on a separate) just copied this None into the status dict. Now the function first checks if the return value is not None, and only if it's not it replaces the entry in the status_dict dictionary.

04-07-2023
There is a strange bug at the moment where sometimes (I *think* when the auto-queue feature was just turned on or off) some of the matches will fail to be removed from the matches dict, but the status_dict does not contain an entry for the match. This is very weird.
I think one way to get to the issue is to set up proper logging.

05-07-2023
I *think* I fixed the issue from 04-07-2023. What I think happened is: the handle_matches() function runs asynchonously to the main thread handling removing of matches, the handle_matches() function calls match.step() and checks if the result is None, meanwhile the main thread removes that match from all dictionaries, subsequently the handle_matches() function sets matches_dict\[index\] = match, thus leaving only the entry in matches_dict and no entry in status_dict. I *think* I've solved the issue by checking if the index is already in the matches_dict before setting the entry equal to the match in handle_matches(), I haven't been able to reproduce the issue ever since.
Creating a match adds the entry to the matches_dict, so this won't get messed up either.

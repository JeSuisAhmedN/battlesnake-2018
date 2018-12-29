import bottle
import os
from algorithms.board import Board
import time
from heapq import heappush, heappop
file = None
runtimes = []

@bottle.route('/')
def static():
    '''
    When someone does a get request on the application, it's going to say
    that it's running.
    '''
    return "<!DOCTYPE html><html><body><style>h1, h3 {color: red;font-family:"\
    "monospace;}</style><h1>Samaritan is running...</h1><h3>A snake created"\
    " by Ahmed Siddiqui</h3></body></html>"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    '''
    When a game starts, this endpoint is called and it gives the customization
    information for Samaritan.
    '''
    global file
    file = open("runtimes.txt", "a")
    file.write('Game runtime: ')
    return {
        "color": "#ededed",
        "secondary_color": "#ededed",
        "head_url": "https://i.ytimg.com/vi/er3BMWuf310/maxresdefault.jpg",
        "taunt": "Calculated.",
        "head_type": "smile",
        "tail_type": "freckled"
        }


@bottle.post('/move')
def move():
    '''
    When a game has started and the game server wants to know which direction
    I want to move in, this endpoint is hit as a POST request with data telling
    us about the game state (what the board looks like). We then figure out
    what move and taunt we want to return.
    '''
    start = time.time()
    environment = Board(bottle.request.json)
    objective, action = environment.get_action()
    time_in_ms = (time.time() - start) * 1000
    print time_in_ms
    heappush(runtimes, -time_in_ms)
    return {
        'move': action,
        'taunt': objective
        }


@bottle.post('/end')
def end():
    '''This endpoint is hit when the game has ended.
    '''
    global file
    total = 0
    number_of_runtimes = 0
    while runtimes:
        time_in_ms = heappop(runtimes)
        time_in_ms = -time_in_ms
        total += time_in_ms
        number_of_runtimes += 1
        string = "" + str(time_in_ms) + " "
        file.write(string)
    average = total / number_of_runtimes
    string = " Average is " + str(average)
    file.write(string)
    file.write('\n')
    file.close()

application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8099'),
        debug = True)


from flask import Flask, jsonify
#from morseapi import MorseRobot
import logging
import asyncio
from dash.robot import DashRobot, discover_and_connect


app = Flask(__name__)

global robot
bot_address = "C2:37:67:68:BD:38"

def get_robot():
    global robot
    if robot is None:
        robot = "dummy"
        #robot = MorseRobot(bot_address)
    return robot

@app.route('/connect')
async def connect():
    print("connect!")
    global robot
    try:

        robot = await discover_and_connect()
        print(robot)
        await robot.move(100,100)
            

        return jsonify({"status": "connected"})
    except:
        return jsonify({"error": "Failed to connect"}), 500

'''
INFO:werkzeug:127.0.0.1 - - [25/Feb/2024 18:56:00] "GET /disconnect HTTP/1.1" 500 -
'''
# broken

@app.route('/disconnect')
def disconnect():
    print("disconnect!")
    global robot
    try:
        if robot is not None:
            #robot.disconnect() # Method must be trash
            robot = None
            return jsonify({"status": "disconnected"})
    except:
        return jsonify({"error": "Failed to disconnect"}), 500

@app.route('/forward')
async def drive():
    print("forward")
    try:
        
        if robot is None:
            return jsonify({"error": "Robot not connected"}), 400
        print("is the robot about to move?")
        await robot.move(300, 100)
        print("did the robot move?")
        return jsonify({"status": "moved forward"})
    except:
        return jsonify({"error": "Failed to move"}), 500
    
@app.route('/right')
async def right():
    print("right")
    try:
        if robot is None:
            return jsonify({"error": "Robot not connected"}), 400
        print("turning now or not so much?")
        await robot.turn(-350)
        print("did it turn?")
        return jsonify({"status": "right"})
    except:
        return jsonify({"error": "Failed to turn right"}), 500

@app.route('/left')
async def left():
    print("left")
    try:
        if robot is None:
            return jsonify({"error": "Robot not connected"}), 400
        await robot.turn(350)
        return jsonify({"status": "left"})
    except:
        return jsonify({"error": "Failed to turn left"}), 500


@app.route('/back')
async def back():
    print("back")
    try:
        if robot is None:
            return jsonify({"error": "Robot not connected"}), 400
        await robot.move(200,100)
        return jsonify({"status": "moved forward"})
    except:
        return jsonify({"error": "Failed to move"}), 500


if __name__ == '__main__':
    app.run(port=5555, debug=True)

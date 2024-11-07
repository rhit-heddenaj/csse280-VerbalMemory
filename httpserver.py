from flask import Flask, flash, request, redirect, url_for, render_template, Response, send_from_directory
from werkzeug.utils import secure_filename
import os
import pickledb
import json
import random

UPLOAD_FOLDER = 'templates/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__ , static_url_path="", static_folder="templates")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# By Thursday
    # Leaderboard, profile picture
    # Figure out what do with React
    # Log in page (username, password, optional profile picture)
    # possible words db, seen words db, username-to-(password & pfp) db
    # (extra) More leaderboard, update the page whenever you pass someone else's high score
    #       (i.e "You have beaten Jack's high score of 18!"" When you get a score of 19)
    # (extra) Logo


possible_words = [
    "abandon", "absorb", "accent", "accordion", "acquire", "address", "adore", "allegro", "amplify", "anchor", 
    "apricot", "bargain", "ballot", "banter", "beacon", "biscuit", "blissful", "breeze", "brilliant", "buffet",
    "cactus", "candle", "carnival", "clash", "climber", "compass", "concise", "clover", "cobble", "celebrate", 
    "decent", "diamond", "delicate", "dazzle", "doctrine", "doodle", "dungeon", "dense", "drift", "dusk", 
    "effort", "elephant", "elusive", "eclipse", "express", "eloquent", "embark", "embrace", "endure", "exotic",
    "fable", "flame", "flourish", "forest", "flicker", "frost", "fortune", "fable", "fusion", "fathom", 
    "grateful", "garnet", "glimmer", "gloss", "glisten", "gravity", "gossip", "glory", "golf", "gale", 
    "honor", "horizon", "huddle", "hypnotic", "hollow", "harmony", "hologram", "hurdle", "heat", "hustle",
    "intrepid", "inspire", "intact", "illusion", "inquire", "iconic", "ignite", "ironic", "innovate", "indigo",
    "jewel", "juggle", "journey", "jungle", "jubilee", "jigsaw", "jargon", "jiffy", "jovial", "jargon", 
    "kinetic", "knack", "keystone", "kaleidoscope", "klutz", "knight", "kettle", "knot", "koala", "karma",
    "lattice", "luminous", "lucid", "lunar", "legend", "lemon", "lucky", "loud", "lounge", "launch",
    "momentum", "mosaic", "mystic", "muddle", "monarch", "magnify", "magnet", "morning", "marvel", "melody",
    "noble", "nectar", "navigate", "novel", "nostalgia", "nectar", "neutron", "nightmare", "nomad", "nudge",
    "oasis", "orbit", "orphan", "octagon", "overture", "orange", "outlook", "oblivion", "obvious", "opinion",
    "puzzle", "phantom", "pioneer", "patriot", "plunge", "plasma", "piano", "permanent", "plaza", "perplex",
    "quiver", "quaint", "quicksilver", "question", "quilt", "quaint", "quash", "quorum", "quibble", "quicksand",
    "reliable", "rocket", "rescue", "ripple", "righteous", "repose", "reminisce", "revolt", "raspberry", "riddle",
    "serene", "symbol", "safeguard", "stumble", "superior", "sphere", "spectra", "shadow", "spark", "saga",
    "triumph", "twilight", "together", "turkey", "tunnel", "tango", "tribal", "treasure", "thunder", "thrive",
    "ultimate", "unicorn", "utopia", "unfold", "umbrella", "underestimate", "unveil", "union", "urgent", "utensil",
    "vortex", "vivid", "vigilant", "vibrate", "vantage", "valor", "vision", "volcano", "velocity", "vault",
    "whisper", "wonder", "whimsy", "whimsical", "wisdom", "world", "wilt", "wilderness", "wavelength", "whale",
    "xenon", "xerox", "xylophone", "xenial", "xenophile", "x-ray", "xylophonist", "xenogenesis", "xenon", "xylem",
    "yellow", "yoga", "yacht", "young", "yearn", "youth", "yesterday", "yonder", "yarn", "yummy", 
    "zephyr", "zenith", "zeal", "zodiac", "zest", "zone", "zen", "zinger", "zoom", "zebra", "zombie",
    "absolute", "accentuate", "alter", "adverse", "athletic", "adore", "abundance", "aspire", "analyze", "await",
    "biography", "bravo", "bitter", "bilingual", "bold", "bare", "boredom", "bliss", "bounty", "banish",
    "catalyst", "cure", "clarify", "cheer", "chatter", "cipher", "courage", "counsel", "clutch", "cane",
    "devote", "divine", "drift", "dove", "doubt", "dazzle", "drape", "desire", "dogma", "detour",
    "essence", "echo", "elusive", "engage", "enlighten", "embrace", "endear", "enigma", "entourage", "evolve",
    "flawless", "flaw", "fiesta", "furnish", "flow", "frenzy", "forge", "forever", "frosty", "fate",
    "grind", "grace", "genuine", "grapple", "glimpse", "gesture", "gather", "gracious", "glow", "grind",
    "harbor", "harmony", "haunt", "halo", "hatch", "hype", "hustle", "honest", "huddle", "hollow",
    "insight", "ignite", "illusion", "impact", "inherit", "ignite", "inspire", "illuminate", "inherit", "iconic",
    "jungle", "jovial", "jigsaw", "juggle", "jewel", "justice", "journey", "jargon", "jigsaw", "juicy",
    "karma", "knight", "knot", "kettle", "kaleidoscope", "kitten", "klutz", "keynote", "kick", "knot",
    "laser", "legend", "lunar", "luxury", "lighthouse", "lively", "lazily", "leaf", "latch", "lodge",
    "mystic", "maze", "mosaic", "melody", "morale", "matrix", "magnitude", "momentum", "mount", "march",
    "neuron", "needy", "notion", "naive", "noble", "nectar", "night", "novel", "neutron", "nudge",
    "oasis", "oracle", "order", "outlook", "optimistic", "objective", "overture", "oath", "oracle", "outcast",
    "puzzle", "phantom", "paradigm", "pivot", "pristine", "promote", "plot", "play", "peace", "passion",
    "quaint", "quicksilver", "quilt", "quiver", "quake", "question", "quench", "quill", "quorum", "quality",
    "ripple", "refine", "remind", "reward", "revive", "rejoice", "raspberry", "rebound", "rejoice", "riddle",
    "serenity", "sparkle", "stumble", "stitch", "soothing", "silence", "saga", "synchronize", "sweep", "serene",
    "thrive", "tango", "together", "trick", "tapestry", "tempt", "thunder", "tunnel", "trail", "twin",
    "ultimate", "unicorn", "utopia", "unveil", "unfurl", "under", "upright", "unify", "union", "utensil",
    "vivid", "valor", "vibrate", "vortex", "violet", "vibe", "vigilant", "volume", "vex", "vacuum",
    "whimsy", "wonder", "whisper", "wave", "wild", "wavelength", "whale", "waterfall", "warrant", "yoga",
    "yellow", "yonder", "yarn", "youth", "yolk", "yearn", "yesterday", "yacht", "zodiac", "zenith", "floccinaucinihilipilification", "gubernatorial", "lobotomy", "disestablishementarism", "unaltered", 
    "irredescant"
]


seen_words =[]
lives = 3
score = 0

# db1 = pickledb.load("possible_words.db", True)
# list1_name = "possible_words"
# if not db1.get(list1_name):
#     db1.lcreate(list1_name)

db2 = pickledb.load("passwords.db", True)
list2_name = "all_players"
if not db2.get(list2_name):
    db2.lcreate(list2_name)

db3 = pickledb.load("leaderboard.db", True)
list3_name = "name_scores"
if not db3.get(list3_name):
    db3.lcreate(list3_name)

db4 = pickledb.load("profilepics.db", True)
list4_name = "name_image"
if not db4.get(list4_name):
    db4.lcreate(list4_name)


@app.route("/", methods=["GET"])
def startGame():
    lives = 3
    score = 0
    seen_words =[]
    return render_template("start.html")  # Got from in class lab


@app.route('/words/', methods=['GET', 'POST'])
def upload_word():
    global lives  # Declare as global to modify them if needed, got from https://www.w3schools.com/python/python_variables_global.asp
    global score
    global seen_words
    global username
    # global image
    if request.method == 'POST':
        action = request.form.get("action")
        lastWord = request.form.get("word")
        if (lastWord in seen_words and action=="new"):
            lives -= 1
        elif (lastWord in seen_words and action=="seen"):
            score += 1
        elif (lastWord not in seen_words and action =="new"):
            score += 1
        elif (lastWord not in seen_words and action =="seen"):
            lives -= 1
        rando = random.randint(0, len(possible_words) - 1)
        rando2 = 0
        if (len(seen_words) > 2):
            rando2 = random.uniform(0, 1)   # Got random.uniform from https://stackoverflow.com/questions/6088077/how-to-get-a-random-number-between-a-float-range
        if (len(seen_words) > 10):
            rando2 = random.uniform(0.5, 1)
        if (rando2 > 0.75):
            rando3 = random.randint(0, len(seen_words) -1)
            word = seen_words[rando3]
        else:
            word = possible_words[rando]

        if (lives == 0):
            if (score > db3.get(username)):
                db3.set(username, score)
                
                
            lives = 3
            score = 0
            seen_words =[]

            user_to_scores = {}
            users = db3.lgetall(list3_name)
            for user in users:
                user_to_scores[user] = db3.get(user)
            
            sorted_user_scores = sorted(user_to_scores.items(), key=lambda x: x[1], reverse=True)   # Referenced https://www.geeksforgeeks.org/python-sorted-function/ to sort

            print("sorted users: " + str(sorted_user_scores))
            return render_template("leaderboard.html", response = sorted_user_scores[0:5])

        response = {
            "word": word,
            "lives": lives,
            "score": score
        }

        if (lastWord not in seen_words):
            seen_words.append(lastWord)
        
        return render_template("play.html", response=response)
    else:
        try:
            username = request.args.get("username")
            password = request.args.get("password")

        
            if (username not in db2.lgetall(list2_name)):
                db2.ladd(list2_name, username)
                db3.ladd(list3_name, username)
                # db4.ladd(list4_name, username)
                db2.set(username, password)
                db3.set(username, 0)
                # db4.set(username, image_name)
            else:
                print("User already in db")
            rando = random.randint(0, len(possible_words) - 1)
            word = possible_words[rando]
            response = {
                "word": word,
                "lives": lives,
                "score": score
            }
        except("TypeEror"):
            print("OKIE")
        return render_template("play.html", response=response)


    
if __name__ == "__main__":
    app.run(port=8080, debug=True)
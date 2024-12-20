from flask import Flask, jsonify, request, redirect, render_template
import flask
import pickledb
import random
import os

UPLOAD_FOLDER = 'templates/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__ , static_url_path="", static_folder="templates")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Note about the commit history: We consistly pair programmed with AJ Hedden being the driver and Emma Paauwe being the navigator. This is reason for the commit history being lopsided towards AJ. 

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


seen_words = []
lives = 3
score = 0


username = ""

username_db = pickledb.load("passwords.db", True)
leaderboard_db = pickledb.load("leaderboard.db", True)


@app.route("/", methods=["GET"])
def startGame():
    return flask.send_from_directory(app.static_folder, "start.html") # Got from in class labs

@app.route("/login/", methods=["GET"])
def login():
    return flask.send_from_directory(app.static_folder, "login.html")

@app.route("/login/", methods=["POST"])
def user_data():
    global username
    global personalBest
    data = request.get_json() 
    username = data.get("username")
    password = data.get("password")
    personalBest = leaderboard_db.get(username)
    
    
    if username not in username_db.getall():
        username_db.set(username, password)
        leaderboard_db.set(username, 0)
        return jsonify({"success": True, "message": "Account created successfully."})
    else:
        stored_password = username_db.get(username)
        
        if stored_password == password:
            return jsonify({"success": True, "message": "Login successful."})
        else:
            return jsonify({"success": False, "message": "Invalid username or password."})

    
@app.route('/words/', methods=["GET", "POST"])
def show_words():
    # Declare as global to modify them if needed, got from https://www.w3schools.com/python/python_variables_global.asp
    global lives, score, seen_words, personalBest, overallBest, topPlayer

    users_to_scores = {}
    keys = leaderboard_db.getall()
    for key in keys:
        users_to_scores[key] = leaderboard_db.get(key)

    users_to_scores = sorted(users_to_scores.items(), key = lambda x: x[1], reverse=True)
    topPlayer, overallBest = users_to_scores[0]

    if request.method == 'POST':
        action = request.form.get("action")
        lastWord = request.form.get("word")
        
        if(lastWord in seen_words):
            if(action == "new"):
                lives -=1
                if lives == 0:
                    return redirect("/leaderboard/")
            elif(action == "seen"):
                score += 1
                if (score > personalBest):
                    personalBest = score
        else: #if lastWord is not in seen_words
            if(action == "new"):
                score += 1
                if (score > personalBest):
                    personalBest = score
                seen_words.append(lastWord)
                possible_words.remove(lastWord)
            else:
                lives -=1
                if lives == 0:
                    return redirect("/leaderboard/")
                
        #Chance is 75/25 whether seen or new until seen_words is larger than 10 words then it is 50/50
        #Source for different probabilities: https://stackoverflow.com/questions/3203099/percentage-chance-to-make-action
        newWord = ""
        
        if len(seen_words) > 10:
            if(random.random() < 0.5):
                index = random.randint(0, len(seen_words) - 1)
                newWord = seen_words[index]
            else:
                index = random.randint(0, len(possible_words) - 1)
                newWord = possible_words[index]
        else: 
            if(random.random() < 0.25):
                index = random.randint(0, len(seen_words) - 1)
                newWord = seen_words[index]
            else:
                index = random.randint(0, len(possible_words) - 1)
                newWord = possible_words[index]
        response = []
        if (newWord == lastWord):
            newWord = possible_words[index]
        if (personalBest > overallBest):
            overallBest=personalBest
        response.append({
            "word": newWord,
            "lives": lives,
            "score": score,
            "personalBest": personalBest,
            "overallBest": overallBest,
            "topPlayer": topPlayer
        })
        return jsonify(response)
    else:
        randomIndex = random.randint(0, len(possible_words) - 1)
        newWord = possible_words[randomIndex]
        response = []
        response.append({
            "word": newWord,
            "lives": lives,
            "score": score,
            "personalBest": personalBest,
            "overallBest": overallBest,
            "topPlayer":topPlayer
        })
        return jsonify(response)

        

@app.route("/leaderboard/")
def end_game():
    global lives, score, seen_words

    if(score > leaderboard_db.get(username)):
        leaderboard_db.set(username, score)

    users_to_scores = {}
    keys = leaderboard_db.getall()
    for key in keys:
        users_to_scores[key] = leaderboard_db.get(key)

    # Referenced https://www.geeksforgeeks.org/python-sorted-function/ to sort
    users_to_scores = sorted(users_to_scores.items(), key = lambda x: x[1], reverse=True)

    lives = 3
    score = 0
    seen_words = []

    return render_template("leaderboard.html", response=users_to_scores[0:5])
 
@app.get("/shutdown")
def shutdown():
    print("Shutting down the server")
    os._exit(0)
   
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=22041, debug=True)
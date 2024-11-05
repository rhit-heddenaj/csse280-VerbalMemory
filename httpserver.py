from flask import Flask, flash, request, redirect, url_for, render_template, Response, send_from_directory
from werkzeug.utils import secure_filename
import os
import pickledb
import json
import random

app = Flask(__name__ , static_url_path="", static_folder="templates")

# By Thursday
    # Leaderboard, profile picture
    # Figure out what do with React
    # Log in page (username, password, optional profile picture)
    # possible words db, seen words db, username-to-(password & pfp) db
    # (extra) More leaderboard, update the page whenever you pass someone else's high score
    #       (i.e "You have beaten Jack's high score of 18!"" When you get a score of 19)
    # (extra) Logo


possible_words = random_words = [
    "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew",
    "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "quince", "raspberry",
    "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "apricot", "blackberry",
    "cantaloupe", "dragonfruit", "eggplant", "feijoa", "guava", "hazelnut", "jackfruit",
    "kumquat", "lime", "mulberry", "nutmeg", "olive", "peach", "pear", "plum",
    "quinoa", "radish", "squash", "tomato", "turnip", "zucchini", "artichoke",
    "broccoli", "carrot", "dill", "endive", "fennel", "garlic", "horseradish",
    "jalapeno", "kale", "leek", "mushroom", "onion", "parsley", "quiche", "radicchio",
    "spinach", "thyme", "watercress", "zucchini", "acorn", "beet", "cabbage",
    "daikon", "eggplant", "fennel", "ginger", "habanero", "icaco", "jicama",
    "kelp", "lime", "mustard", "napa", "okra", "pepper", "quinoa", "rhubarb",
    "salsify", "taro", "upland", "vegan", "wasabi", "xylocarp", "yarrow", "zucchini",
    "adventure", "bravery", "courage", "determination", "enthusiasm", "freedom",
    "gratitude", "harmony", "imagination", "joy", "kindness", "love", "mystery",
    "nurture", "opportunity", "passion", "quest", "resilience", "sacrifice", "trust",
    "unity", "vitality", "wisdom", "zeal", "art", "beauty", "creativity", "dream",
    "energy", "faith", "growth", "hope", "inspiration", "journey", "knowledge",
    "learning", "mindfulness", "nature", "optimism", "perspective", "reflection",
    "spirit", "teamwork", "understanding", "vision", "wonder", "youth", "zen",
    "anxiety", "boredom", "chaos", "desire", "excitement", "fear", "grief", "happiness",
    "introspection", "jealousy", "loneliness", "melancholy", "nervousness", "outrage",
    "panic", "quiet", "regret", "sadness", "tension", "urgency", "vulnerability",
    "whimsy", "xenophobia", "yawning", "zealot", "abundance", "balance", "compassion",
    "discovery", "equilibrium", "fascination", "generosity", "humility", "innovation",
    "justice", "knowledge", "legacy", "maturity", "nobility", "openness", "patience",
    "quality", "respect", "sincerity", "tenacity", "understanding", "versatility",
    "wisdom", "floccinaucinihilipilification", "gubernatorial", "lobotomy", "disestablishementarism", "unaltered", 
    "irredescant"
]

seen_words =[]
lives = 3
score = 0

db1 = pickledb.load("possible_words.db", True)
list1_name = "possible_words"
if not db1.get(list1_name):
    db1.lcreate(list1_name)




@app.route("/", methods=["GET"])
def startGame():
    lives = 3
    score = 0
    seen_words =[]
    return render_template("login.html")  # Got from in class lab


@app.route('/words/', methods=['GET', 'POST'])
def upload_word():
    global lives  # Declare as global to modify them if needed, got from https://www.w3schools.com/python/python_variables_global.asp
    global score
    if request.method == 'POST':
        action = request.form.get("action")
        lastWord = request.form.get("word")
        # print("last word: " + lastWord)
        # print("all seen words: " + str(seen_words))
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
        if (len(seen_words) > 3):
            rando2 = random.uniform(0, 1)   # Got random.uniform from https://stackoverflow.com/questions/6088077/how-to-get-a-random-number-between-a-float-range
        if (len(seen_words) > 10):
            rando2 = random.uniform(0.5, 1)
        if (rando2 > 0.75):
            rando3 = random.randint(0, len(seen_words) -1)
            word = seen_words[rando3]
        else:
            word = possible_words[rando]
        response = {
            "word": word,
            "lives": lives,
            "score": score
        }

        if (lastWord not in seen_words):
            seen_words.append(lastWord)
        
        return render_template("play.html", response=response)
    else:
        rando = random.randint(0, len(possible_words) - 1)
        word = possible_words[rando]
        response = {
            "word": word,
            "lives": lives,
            "score": score
        }
        return render_template("play.html", response=response)

    
if __name__ == "__main__":
    app.run(port=8080, debug=True)
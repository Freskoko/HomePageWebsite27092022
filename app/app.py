from distutils.command.upload import upload
from operator import methodcaller
from flask import Flask, render_template, request, session, url_for
import random
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
import string
import random
import ast

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "123"
app.config['UPLOAD_FOLDER'] = "static/upload"
os.makedirs(os.path.join(app.instance_path, 'uploaded_images'), exist_ok=True)

#home page
@app.route('/')
def home():
    return render_template('home.html')



info_dict = {
    "projectTikTok":["https://github.com/Freskoko?tab=repositories","https://www.youtube.com/embed/5fe88IU6DwI","TikTokBot",
    "This project uses the reddit-api to extract post data from popular reddit posts. Gtts (google-text-to-speech) turns the text into speech","Moviepy creates a video using the text and speech, as well as gameplay footage in the background", "Finally pyautogui, and selenium are used to post the content to Instagram/Tiktok."]
    ,

    "projectOutLouder":["https://github.com/Freskoko/OutLouderBot-2","https://www.youtube.com/watch?v=ScMzIvxBSi4","OutLouder",
    "This project uses selenium to access Outloud which is a music service where users can vote on songs", "This project allows a song to be voted on mulitple times by sending several requests to the website."," This was quite fun to make and use, made in collaboration with Luca Fossen"]
    ,
    "projectSeaGullID":["https://github.com/Freskoko/SeaGullID","https://www.youtube.com/embed/HrFtpDY3v5Y","SeaGullID",
    "This project used PYQT6 to create an easy to use GUI for identifiying norwegian seagulls","This was before i learned that things are much easier on the net","I am happy with how it turned out, one of my first projects"]
    ,
    "projectinstagramBot":["https://github.com/Freskoko/instagramBotMemeAccount","https://www.youtube.com/embed/NOKHfakELlA","InstagramBot",
    "This project uses Selenium and pyautogui to upload images to instagram that have been collected from redditdownloader.com", "This is fully automatic, and is pretty fun to watch happen","Exciting!"]
    ,
    "projectPyEvolution":["https://github.com/Freskoko/PyGameDuckEvolution","https://www.youtube.com/embed/Q_zKnaoqetg","Evolution using pygame",
    "This project simulates evolution, ducks eat bread, wolves eat ducks. Wolves/Ducks who perform well pass their genes (speed) on","The genetic algorithm used here is quite basic as there is only 1 thing evolving(speed)","A really fun project to learn programming"]
    ,
    "projectThisWebsite":["https://github.com/Freskoko","https://www.youtube.com/embed/Gi4HbyI54nQ","This website!",
    "This website was built using Flask, HTML and CSS.","There is not much more to say","Have a look around!"]
    ,
    "projectWordConverter":["https://github.com/Freskoko","https://www.youtube.com/embed/jl84sw84kyY","Word Image Converter",
    "This is an app that uses zipfile to take all the photos out of a word file","then the images can be changed (resolution,colour,etc) using cv2, they are then saved in the downloads folder (in this case the images are scaled down)", "This was really useful and sped up a task that could take hours"]
}

#general renderer 

#@app.route('/project/', methods=['GET'])
@app.route('/project/TikTok', methods=['GET',"POST"])
@app.route('/project/OutLouder', methods=['GET',"POST"])
@app.route('/project/SeaGullID', methods=['GET',"POST"])
@app.route('/project/instagramBot', methods=['GET',"POST"])
@app.route('/project/PyEvolution', methods=['GET',"POST"])
@app.route('/project/ThisWebsite', methods=['GET',"POST"])
@app.route('/project/WordConverter', methods=['GET',"POST"])


def just_render():
    file_name = request.path.replace('/', '')
    template = '{file_name}.html'.format(file_name=file_name)
    infolist = info_dict[file_name]

    return render_template("project.html",
        githublink =    infolist[0],
        youtubeLink =   infolist[1],
        title =         infolist[2],
        maintext=       infolist[3],
        secondtext =    infolist[4],
        lasttext=       infolist[5])

    #<!-- needs: 
    #project name
    #libraries used
    #github link
    #youtube link
    # -->


#page with buttons and such

@app.route("/speciesform/",methods=["GET","POST"])

def speciesform():

    if "crazy" not in session: 
        session["crazy"] = False

    if "crazyvalue" not in session:
        session["crazyvalue"] = 0

    if request.method == "POST":

        if "buttonTurn2" in request.form:
            session["crazy"] = False
            session["crazyvalue"] += 1

        if "buttonTurn" in request.form:
            session["crazy"] = True
            session["crazyvalue"] -= 1


    #form!!!

    forms =  ["Species","Location","Size","Date"]



    if request.method == "POST":

        # maketheform
    
        if "SUBMITREPORT" in request.form:
            Person = []

            for i in forms:
                Person.append(request.form[i])

            #random code for each image
            imgcode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            imgcode = f"{imgcode}.jpg"

            f = request.files['Image']
            
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], imgcode))

            Person.append(imgcode)

            with open("savedPeople.txt","a",encoding="utf8") as file:
                file.writelines(f"{Person} \n")
                file.close()
            
            
    return render_template("speciesform.html",forms=forms)


@app.route('/speciesviewer/', methods=['GET',"POST"])

def speciesviewer():

    specieslist2 = []

    with open("savedPeople.txt","r",encoding="utf8") as file:
        specieslist = file.readlines()
        for i in specieslist:   
            specieslist2.append(ast.literal_eval(i))
        
        specieslist2.reverse() #so we see newest first
            
    return render_template("speciesviewer.html",newspecieslist = specieslist2)


@app.route('/contact/', methods=['GET',"POST"])
def contact():
    return render_template("contact.html")

@app.route('/about/', methods=['GET',"POST"])
def about():
    return render_template("about.html")

@app.route("/stat101", methods=['GET',"POST"])

def stat101():
    return render_template("stat101.html")


@app.route("/drikke/", methods=['GET','POST'])

def drikke():  

    def generate_image():

        with open("GameChallenges.txt","r",encoding="utf8") as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            funnytext = random.choice(lines)
            file.close()

        try:
            namelist = session['names']
            person = random.choice(namelist)

            if person == "":
                return(namelist)

        except Exception:
            return("⬇ No names... Add some below ⬇")

        personrandom = random.randint(1,15)
        if personrandom == 10:
            person = "Everyone"
            
        return (f"{person} {funnytext}")

    def clear_names():
     
        session['names'] = []
        return ("All names cleared")

    def addName():

        name = request.form['addplayer']

        if name == "":
            return "Names cannot be empty"

        if name != "":
            if "names" not in session:
                session['names'] = []

            namelist = session['names']
            namelist.append(name)
            session['names'] = namelist  # 

        return f"Welcome {name}"

    
    completedprompt = "🍺 Do the challenge or dice roll = drinks 🍺 When the bar fills up" 
    rolleddice = "?"
    
    if request.method == "POST": 

        
        completedprompt = "🍺 Do the challenge or dice roll = drinks 🍺 When the bar fills up" 
        rolleddice = "?"

        if "progbarvalue" not in session:
            session["progbarvalue"] = 1


        if "new" in request.form:
            completedprompt = generate_image()

        if "dicerollbutton" in request.form:
            multiplier = 1
            rolleddice = f"{random.randint(1,6)}"
            completedprompt = "You chose to drink instead!       Drink the amount the dice says!"

            session["progbarvalue"] += int(rolleddice)

            if session["progbarvalue"] >= 50:
                session["progbarvalue"] = 1
                multiplier = 3
                
            return render_template("drikke.html", 
            result=completedprompt,
            dice = int(rolleddice)*multiplier,
            progBarHtml = session["progbarvalue"])
    
        if "addplayerbutton" in request.form:
            completedprompt = addName()

        if "clear" in request.form:
            completedprompt = clear_names()
            
    return render_template("drikke.html", result=completedprompt,dice = rolleddice,progBarHtml=session["progbarvalue"] )
    


if __name__ == '__main__':
    app.run(debug=True)
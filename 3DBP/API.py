from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os 
from wtforms.validators import InputRequired

from resources import Pallet, Packer
import ManipConfigFile

app = Flask(__name__)
app.config["SECRET_KEY"] = '123'
app.config["UPLOAD_FOLDER"] = 'static/files'


"""
http://127.0.0.1:5000/resetConfigFile
http://127.0.0.1:5000/setPallet?width=200&height=200&depth=300&maxWeight=200&x=0&y=0&z=0
http://127.0.0.1:5000/setConfigFile
http://127.0.0.1:5000/getNextBox
http://127.0.0.1:5000/currentBoxPlaced

http://192.168.1.51:5000/resetConfigFile
http://192.168.1.51:5000/setPallet?width=200&height=200&depth=300&maxWeight=200&x=0&y=0&z=0
http://192.168.1.51:5000/setConfigFile
http://192.168.1.51:5000/getNextBox
http://192.168.1.51:5000/currentBoxPlaced

file:///C:/Users/hugop/OneDrive/Documents/master/memoire/code/3DBP/config.json
"""


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route("/")
@app.route("/index", methods=["GET","POST"])
def index():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return "File has been uploaded"
    return render_template("index.html", form=form)






api = Api(app)

#----------------------------------Get Next Box----------------------------------------
#envoie la boite non encore placee manuellement ayant le plus petit end_y virtuellement
class getNextBox(Resource):
    def get(self):
        print("appel de la fonction getNextBox")
        try:
            lowestBox = ManipConfigFile.getLowestUnplacedBox()
            ManipConfigFile.setCurrentBox(lowestBox)
            myDict = lowestBox.__dict__
            myDict["other"] = {}
            #myDict["other"]["currentRatio"] = ManipConfigFile.getPlacedBoxesFillingRate()
            myDict["other"]["totalRatio"] = ManipConfigFile.getCompletePalletFillingRate()
            myDict["other"]["totalUnfitBoxes"] = len(ManipConfigFile.getListOfNoFitBoxes())
            return myDict
        except:
            return {"message":"pas de boite a placer"}


api.add_resource(getNextBox, "/getNextBox")

#-----------------------------------Box Placed------------------------------------------
#en appelant cette fonction, Hololens signale que l'operateur a placé la boite qu'il avait en main
class currentBoxPlaced(Resource):
    def get(self):
        print("appel de la fonction currentBoxPlaced")
        try:
            currentBox = ManipConfigFile.getCurrentBox()
            ManipConfigFile.moveBoxFromUnplacedToPlaced(currentBox)
            ManipConfigFile.clearCurrentBox()
        except:
            return {"message":"pas de current box"}
        
        myDict = {}
        myDict["currentRatio"] = ManipConfigFile.getPlacedBoxesFillingRate()
        return myDict

api.add_resource(currentBoxPlaced, "/currentBoxPlaced")


#-----------------------------------Box Damaged ---------------------------------------

class boxDamaged(Resource):
    def get(self):
        print("appel de la fonction boxDamaged")

api.add_resource(boxDamaged, "/boxDamaged")


#--------------------------------Get Config File --------------------------------------
#permet de visualiser l'ensemble du fichier config
class getConfigFile(Resource):
    def get(self):
        print("appel de la fonction getConfigFile")
        return ManipConfigFile.getConfigData()

api.add_resource(getConfigFile, "/getConfigFile")


#-----------------------------Set Pallet Position -------------------------------------
#en appelant cette fonction get, l'operateur envoie les coordonnees et dimensions de la palette
class setPallet(Resource):
    def get(self):
        print("appel de la fonction setPalletPosition")

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('maxWeight', type=int, help="weight of pallet is required", required = True)
            parser.add_argument('width', type=int, help="width of pallet is required", required = True)
            parser.add_argument('height', type=int, help="height of pallet is required", required = True)
            parser.add_argument('depth', type=int, help="depth of pallet is required", required = True)
            parser.add_argument('x', type=int, help="x of pallet is required", required = True)
            parser.add_argument('y', type=int, help="y of pallet is required", required = True)
            parser.add_argument('z', type=int, help="z of pallet is required", required = True)

            print("appel de la fonction addPallet de l'API")
            maxWeight = int(request.args.get('maxWeight'))
            width = int(request.args.get('width'))
            height = int(request.args.get('height'))
            depth = int(request.args.get('depth'))
            x = int(request.args.get('x'))
            y = int(request.args.get('y'))
            z = int(request.args.get('z'))

            ManipConfigFile.addPallet(Pallet(width=width,height=height, depth=depth, max_weight=maxWeight, x=x, y=y, z=z))

            return {"message": "palette ajoutee"}
        except:
            return {"message": "une erreur s est produite lors de la creation de la palette"}

        #http://192.168.1.51:5000/setPallet?width=200&height=200&depth=300&maxWeight=200&x=0&y=0&z=0

api.add_resource(setPallet, "/setPallet")

#------------------------------Reset Config File --------------------------------------
#remet par defaut le fichier config
class resetConfigFile(Resource):
    def get(self):
        print("appel de la fonction resetConfigFile")
        ManipConfigFile.resetConfigFile()
        return 200

api.add_resource(resetConfigFile, "/resetConfigFile")


#------------------------------Set Config File --------------------------------------
#permet de definir le premier pivot, ajouter les boites dans la section undefined, et appelle le packer 
class setConfigFile(Resource):
    def get(self):
        print("appel de la fonction setConfigFile")
        ManipConfigFile.setFirstPivotPointBasedOnPalletPosition()
        ManipConfigFile.addAllUndeterminedBoxes()
        packer = Packer()
        packer.pack_boxes()
        packer.update_config_file()

        return 200

api.add_resource(setConfigFile, "/setConfigFile")


#-------------------------------------Main --------------------------------------------

"""
if __name__ == "__main__":
    #app.run(host='192.168.1.51', port=5000, debug=True, threaded=False)
    app.run(debug=True, threaded=False)
    #app.run(host='192.168.0.29', port=5000, debug=True, threaded=False)
"""
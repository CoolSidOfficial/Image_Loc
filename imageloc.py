from pyrogram import Client,filters
from exif import Image
from dotenv import load_dotenv
from os import getenv
import logging
from pyrogram.types import ReplyKeyboardMarkup
###########################################################

load_dotenv()
logging.basicConfig(filename="image_loc.log",level=logging.INFO,format="%(asctime)s-%(message)s",datefmt="%H-%M-%S  %d-%A-%Y")
######################################################
api_id=getenv("API_ID")
api_hash=getenv("API_HASH")
bot_token=getenv("BOT_API")
app=Client("Image Loc",api_id,api_hash,bot_token)
path="/home/coolsid/desktop/python/image_loc/"
gif_path="/home/coolsid/Codes/others/pyrogram_codes/image_loc/video.mp4"
delete_gps=False
########################################################################################################################
@app.on_message(filters.command(["start"]))
def start(client,message):
    user=message.from_user.id

    logging.info(f"Start command  has been called by this {user} ")
    message.reply_text("**Please upload your image as a file to know the location of it ** ")

######################################################################################
@app.on_message(filters.photo)
def check(client,message):
    message.reply_text("**Upload by clicking on files not as image ")
    message.reply_animation(gif_path)
    message.reply_text("Or type help to watch in good quality")
###################################################################
@app.on_message(filters.document)
def get_image(client,message):
    global new_path,photo_from
    photo_from=message.from_user.id
    new_path=path+str(message.from_user.id)+".jpeg"
    image_path=app.download_media(message.document,file_name=new_path,block=True)
    if image_path is None:
        print("image not downloaded successfully")
    if not  delete_gps:

         extract_meta(message.from_user.id)

############################################################################
def extract_meta(id):

    with open(new_path,"rb") as file:
        meta=Image(file)
        if meta.has_exif:
          try:

              lat_d,lat_m,lat_s=meta.get("gps_latitude")
              long_d,long_m,long_s=meta.get("gps_longitude")
          except Exception as e:
              app.send_message(id,text="**This image does not contain  any gps location \nPlease upload another image ** ")


          latitude=lat_d+(lat_m/60)+(lat_s/3600)      # converting latitude in decimal  formats
          longitude=long_d+(long_m/60)+(long_s/3600)   # converting longitude in decimal formats

          app.send_location(id,latitude,longitude)
          app.send_message(id,text=f"**This is the  location extracted from the image you sent us \n https://maps.google.com/?q={latitude},{longitude}**")
          keyboard(id)
        else:
            app.send_message(id,text="** You gave us some other form of document or This image does not contain  any gps location **")


#################################################################################################################
def keyboard(id):
     app.send_message(id,text="Hope you like it ",reply_markup=ReplyKeyboardMarkup(

     [["Convert Another"],["Delete Gps Data"]]
     ,resize_keyboard=True,one_time_keyboard=True))
##############################################################################################
@app.on_message(filters.regex("Convert Another"))
def again(client,message):
    message.reply_text(text="** Please upload your image as a file **")

###############################################################################################
@app.on_message(filters.regex("Delete Gps Data"))
def remove(client,message):
    global delete_gps
    delete_gps=True

    if photo_from == message.from_user.id:
           message.reply_photo(new_path)
           message.reply_text("**This image data has been removed\t thx for using your service **")
           delete_gps=False

    elif  photo_from != message.from_user.id:
           message.reply_text(text="**Please type /start and send image again*** ")
@app.on_message(filters.command(["help"]))
def help(client,message):
     pass
@app.on_message(filters.command(["admin"]))
def admin(client,message):
    pass
app.run()

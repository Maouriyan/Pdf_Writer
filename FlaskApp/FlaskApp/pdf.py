from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2 import PdfFileMerger
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
import os
import shutil
import glob
from pathlib import Path
import requests
import urllib.request
import cloudinary
import cloudinary.uploader

cloudinary.config( 
  cloud_name = "delabaqiu", 
  api_key = "869793121878921", 
  api_secret = "kNBO2luqMBJvD3kbXpAhceG510E",
  secure = False
)
path = "/var/www/FlaskApp/FlaskApp/output_folder/"
path2 = "/var/www/FlaskApp/FlaskApp/bulku/"
Path("/var/www/FlaskApp/FlaskApp/output_folder").mkdir(parents=True, exist_ok=True)
Path("/var/www/FlaskApp/FlaskApp/bulku").mkdir(parents=True, exist_ok=True)

def write_pdf(i):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    path = "/var/www/FlaskApp/FlaskApp/output_folder/"
    path2 = "/var/www/FlaskApp/FlaskApp/bulku/"
    Path("/var/www/FlaskApp/FlaskApp/output_folder").mkdir(parents=True, exist_ok=True)                                  
    Path("/var/www/FlaskApp/FlaskApp/bulku").mkdir(parents=True, exist_ok=True)

        

    uid = i[0]
    for k in i[1]:
        text,top,left,lang = k
        pdfmetrics.registerFont(TTFont('arial', 'arial.ttf'))
        can.setFont('arial', 32)

        if lang == 'ar':
            
            ar = arabic_reshaper.reshape(text)
            ar = get_display(ar)
            
            can.drawString(top, left, ar)

        
        elif lang == "en":
            can.drawString(top, left, text)

        
        
    can.save()

        #move to the beginning of the StringIO buffer
    packet.seek(0)
        # create a new PDF with Reportlab

    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    name_of_pdf = path + uid + ".pdf"

    with open("original.pdf", "rb") as f:
        existing_pdf = PdfFileReader(f)
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)


        # finally, write "output" to a real file
        outputStream = open(name_of_pdf, "wb")
        output.write(outputStream)
        outputStream.close()


def main(message):
# JSON string
    path = "/var/www/FlaskApp/FlaskApp/output_folder/"                                                                   
    path2 = "/var/www/FlaskApp/FlaskApp/bulku/"                                                                          
    Path("/var/www/FlaskApp/FlaskApp/output_folder").mkdir(parents=True, exist_ok=True)                                  
    Path("/var/www/FlaskApp/FlaskApp/bulku").mkdir(parents=True, exist_ok=True)
    # Convert string to Python dict
    #message_dict = json.loads(message)
    message_dict = message
    #print(message_dict)
    result_type = message_dict['type']
    Individuals =  message_dict['data']

    url = message_dict['file_url']
    urllib.request.urlretrieve(url, "original.pdf")
    

    for key in message_dict['data'].keys():
        res = message_dict['data'][key]
        form_details = []
        uid = str(key)
        print(key)
        for x in res:
            text = x['text']
            top = x['top']
            left = x['left']
            lang = x['lang']
            
            form_details.append([text,top,left,lang])


        
        full_details = []
            
            #print(text,top,left,lang)
        full_details.append([uid,form_details])
        for i in full_details:
            print(i)
            write_pdf(i)


    dir_list = os.listdir(path)
    upload_result = " Did not upload"
    if result_type == "Individual":
        merger = PdfFileMerger()
        print(dir_list)
        for pdf in dir_list:
            merger.append(path+pdf)

        merger.write(path+"merged.pdf")
        merger.close()
        upload_result = cloudinary.uploader.upload(path+"merged.pdf",resource_type = "auto")

    if result_type == "Bulk":
        shutil.make_archive("/var/www/FlaskApp/FlaskApp/bulk", 'zip', "/var/www/FlaskApp/FlaskApp/output_folder")
        print("is there?")
        upload_result = cloudinary.uploader.upload("/var/www/FlaskApp/FlaskApp/bulk.zip",resource_type = "raw")
    
    
            


    #shutil.rmtree(path)
    #shutil.rmtree(path2)
    #shutil.rmtree("./original.pdf")
    return upload_result


if __name__=="__main__":
    message = u'{"file_url":"https://res.cloudinary.com/praveenrambalu/image/upload/v1639133095/HRM/manpower-cancellation-form-english.pdf", "type":"Bulk" , "data":{"Individual_ID_1":[{"text":"العربية","top":500,"left":175,"lang":"ar"},{"text":"Ramu","top":35,"left":25,"lang":"en"}],"Individual_ID_2":[{"text":"Praveen","top":115,"left":125,"lang":"en"},{"text":"Ram","top":35,"left":25,"lang":"en"}]}}'

    main(message)


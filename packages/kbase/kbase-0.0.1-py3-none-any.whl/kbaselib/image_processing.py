"""
@author: Jebin Jolly Abraham 
Date: 08/01/2022
"""

#Libraries 
from PIL import Image
import imagehash
from pdf2image import convert_from_path


#Functions 

def convert_pdf_to_images(path , poppler_installation_path , destination_folder):
  
    """
    A function to convert a pdf file to images .

    Pre-requisites:
    Install the latest poppler from https://blog.alivate.com.au/poppler-windows/ 
    then add the poppler installation path to the poppler_installation_path variable.

    Parameters:
        path                      (str): The path of the pdf file.
        poppler_installation_path (str): The path of the poppler installation.
        destination_folder        (str): The path of the folder where the images will be saved.

    Returns:
        images ()
    """
    #add '\Library\bin' to the poppler_installation_path
    poppler_installation_path = poppler_installation_path + '\Library\bin'
    #check if pdf2image is installed
    try:

        images = convert_from_path(path,poppler_path= poppler_installation_path)
    
        for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save(destination_folder+'page'+ str(i) +'.jpg', 'JPEG')

    except ImportError:
        print("""
        poppler is not installed.
        Please install poppler from https://blog.alivate.com.au/poppler-windows/

        """)
        exit()


def image_similarity_checker(sampleImage,TargetImage , cutoff_value = 5):
    """
    This function checks if the image is similar to the target image. The input are the path of the sample image and the targe image.
   
    Parameters:
        sampleImage  (str) : The path of the sample image.
        TargetImage  (str) : The path of the target image.
        cutoff_value (int) : The maximum bits that could be different between the hashes.
   
    Returns:
        result (bool): True if the images are similar, False otherwise.

    """
    hash0 = imagehash.average_hash(Image.open(sampleImage)) 
    hash1 = imagehash.average_hash(Image.open(TargetImage)) 
    cutoff = cutoff_value  
    if hash0 - hash1 < cutoff:
        return True
    else:
        return False
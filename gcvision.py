#  in order for GC Vision API to function
#  SET environment variable for GOOGLE API CREDENTIALS
# 
#   Powershell: $env:GOOGLE_APPLICATION_CREDENTIALS="D:\GITHUB\gcvision.cred.json"
#  
#   Command Line: set GOOGLE_APPLICATION_CREDENTIALS="D:\GITHUB\gcvision.cred.json"
#
#   pip install google-cloud-vision

from google.cloud import vision
import io
client = vision.ImageAnnotatorClient()
filepath = '5b70f5aa-ed34-65ab-e053-2a91aa0a6777.jpg'
with io.open(filepath, 'rb') as image_file:
    content = image_file.read()
image = vision.types.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations
print('Texts:')

for text in texts:
    print('\n"{}"'.format(text.description))

    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in text.bounding_poly.vertices])

    print('bounds: {}'.format(','.join(vertices)))
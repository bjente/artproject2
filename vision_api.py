from google.cloud import vision_v1
from google.cloud.vision_v1 import enums
import six
import os

## In this program, I've let the Google Vision API analyze 1500 pictures from the Museum of Modern Art New-York.
## Colors and objects that are detected in the images, are saved to seperate JSON files.
## With these JSON files, i created 'momaoutput.txt' which can be found in the data folder.
## I used this output for the apriori algorithm

## I deleted my credentials for this github repo since it is private. So you cannot run this program.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="enter credentials here"


def generate_request(input_image_uri, output_uri):
  if isinstance(input_image_uri, six.binary_type):
    input_image_uri = input_image_uri.decode('utf-8')
  if isinstance(output_uri, six.binary_type):
    output_uri = output_uri.decode('utf-8')
  source = {'image_uri': input_image_uri}
  image = {'source': source}
  type_ = enums.Feature.Type.LABEL_DETECTION
  features_element = {'type': type_}
  type_2 = enums.Feature.Type.IMAGE_PROPERTIES
  features_element_2 = {'type': type_2}
  features = [features_element, features_element_2]
  requests_element = {'image': image, 'features': features}

  return requests_element


def sample_async_batch_annotate_images(input_uri, output_uri):
  """Perform async batch image annotation"""

  client = vision_v1.ImageAnnotatorClient()

  requests = []

  gcs_destination = {'uri': output_uri}

  for filename in os.listdir('imagesgoogle'):
      requests.append(generate_request(input_uri.format(filename), output_uri))

  # The max number of responses to output in each JSON file
  batch_size = 1
  output_config = {'gcs_destination': gcs_destination, 'batch_size': batch_size}

  operation = client.async_batch_annotate_images(requests, output_config)

  print('Waiting for operation to complete...')
  response = operation.result()

  # The output is written to GCS with the provided output_uri as prefix
  gcs_output_uri = response.output_config.gcs_destination.uri
  print('Output written to GCS with prefix: {}'.format(gcs_output_uri))


sample_async_batch_annotate_images('gs://moma_image_labels/art_images/{}', 'gs://moma_image_labels/JSONfiles/')

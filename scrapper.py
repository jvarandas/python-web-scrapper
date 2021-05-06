import requests
import favicon
import sys
import logging
import metadata_parser
    
def write_to_file(file_name, content):
    f = open(file_name, "a")
    f.write(content+"\n")
    f.close()
 
def get_favicon_url(url):
    fixed_url = "http://{}".format(url).strip()
    try:
        icons = favicon.get(fixed_url, timeout=25)
        icon = icons[0]
        return icon.url
    except:
        logger.info("no favicon fetched for url: {}".format(url))

# <meta property="og:image">
def scrap_images_from_url(url):
    fixed_url = "http://{}".format(url).strip()
    rvalue = None
    try:
        rvalue = metadata_parser.MetadataParser(url=fixed_url).get_metadata_link('image')
    except metadata_parser.NotParsableFetchError:
        logger.info("Exception - no image fetched for url: {}".format(url))
    except metadata_parser.NotParsable:
        logger.info("Exception - no image fetched for url: {}".format(url))

    return rvalue




# program

#config logging
logging.basicConfig(filename="log_scrapper.log", format="%(asctime)s %(message)s", filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#main loop
file_input = sys.argv[1]
#file_input = "alexa1M.txt"
file_input = file_input.rstrip() #strip input file name
file_output = "output.txt"

try:
    logger.debug("opening file {}".format(file_input))
    f = open(file_input, "r")
    url = f.readline()
    while url:
        logger.debug("scrapping images from {}".format(url))
        image_url = scrap_images_from_url(url)
        if image_url != None:
            logger.debug("get favicon image from {}".format(url))
            image_url = get_favicon_url(url)
            if image_url != None:
                 write_to_file(file_output, image_url)
        url = f.readline()
    f.close
except IOError:
    logger.error("IOError writing the url: {}".format(url))
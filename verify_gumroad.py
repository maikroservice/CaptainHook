import requests
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

#TODO: we should rewrite the function according to this link
#https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
def verify_gumroad_license(GUMROAD_PRODUCT_ID, license_key):
    r = requests.post("https://api.gumroad.com/v2/licenses/verify",
                      data={"product_id":GUMROAD_PRODUCT_ID, 
                            "license_key":license_key}).json()
    logging.debug(f'license key: {license_key} - response: {r}')
    
    
    if not r["success"]:
        return {"verification":False, "message":f"Key ({license_key}) could not be verified, check the key in gumroad"}
    elif r["success"] and (r["uses"] > 1): 
       return {"verification": False, "message":f"Key ({license_key}) already used - contact @maikroservice"}
    elif r["purchase"]["refunded"]:
       return {"verification": False, "message":f"Cannot verify refunded product keys - {license_key}"}
    else:
       return {"verification":True, "message": license_key}

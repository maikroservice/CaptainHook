import requests
import logging
def verify_gumroad_license(GUMROAD_PRODUCT_ID, license_key):
    r = requests.post("https://api.gumroad.com/v2/licenses/verify",
                      data={"product_id":GUMROAD_PRODUCT_ID, 
                            "license_key":license_key}).json()
    logging.info(f'license key: {license_key} - response: {r}')
    if r["success"] and (r["uses"] > 1): 
       return {"verification": False, "message":f"Key ({license_key}) already used - contact @maikroservice"}
    #if not r["uses"]:
    #    return False
    elif r["purchase"]["refunded"]:
       return {"verification": False, "message":f"Cannot verify refunded product keys - {license_key}"}
    else:
       return {"verification":True, "message": license_key}

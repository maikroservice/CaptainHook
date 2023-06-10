import requests

def verify_gumroad_license(GUMROAD_PRODUCT_ID, license_key):
    r = requests.post("https://api.gumroad.com/v2/licenses/verify",
                      data={"product_id":GUMROAD_PRODUCT_ID, 
                            "license_key":license_key}).json()
    if(r["uses"] > 1): 
       return "Key already used - contact @maikroservice"
    
    return r["success"] and not r["purchase"]["refunded"]
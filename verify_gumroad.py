import requests
import os

GUMROAD_PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID")

def verify_gumroad_license(license_key):
    r = requests.post("https://api.gumroad.com/v2/licenses/verify",
                      data={"product_id":GUMROAD_PRODUCT_ID, 
                            "license_key":license_key}).json()
    
    if not r["success"]:
        return False
    
    elif (r["success"] == True) and (r["uses"] < 2):
        # https://docs.replit.com/tutorials/python/discord-role-bot
        # add user to SOC Analyst 101 Discord Group
        # TODO: read "group" from verification product
        
        return True
    
    else:
        return "Key already used - contact @maikroservice"
        

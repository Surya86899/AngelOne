import http.client
import certifi
import json
import gttrules     # Contains gttrules operations code
from getholdings import myholdings      # Contains holding getting code
from getfunds import myfunds    # Contains fund getting code
import logincred    # Contains my login credentials
import login        # Contains my login code
import logout       # Contains my login code
from headers import headers     # Contains headers
import my_profile

# ************************Login****************************
# jwt_token = login.my_login(logincred.api_key, logincred.username, logincred.pwd)
# *********************************************************


# ************************Logout****************************
# logout.my_logout()
# **********************************************************


# ************************Profile****************************
# my_profile.profile()
# **********************************************************


# *****************create gtt_rule function********************
# Example usage
# print("id = ",gttrules.create_gtt_rule("SBIN-EQ", "3045", "NSE", "BUY", "DELIVERY", "754", "50", "753.95", "50", "20"))
# *************************************************************


# *****************modify gtt_rule function********************
# Example usage 
# gttrules.modify_gtt_rule(2819079, "SBIN-EQ", "3045", "NSE", "BUY", "DELIVERY", "755", "50", "753.95", "50", "20")
# *************************************************************


# *****************get rules gtt_rule function********************
# Example usage 
# gttrules.get_gtt_rule_details("2819079")
# *************************************************************


# *****************get all gtt_rule function********************
# Example usage
# gttrules.get_gtt_allrule_details()
# *************************************************************


# *****************cancel gtt_rule function********************
# Example usage
# gttrules.cancel_gtt_rule("2819079","3045","NSE")
# *************************************************************


# **********************get my holdings**********************
# Example usage
# myholdings()
# *************************************************************


# *************************get my funds************************
# Example usage
# myfunds()
# *************************************************************


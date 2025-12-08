
import requests,ast
from functools import wraps
import frappe 
import re

def process_code(code,data_to_validate):
	tokens = re.findall(r"_VS_[A-Za-z0-9_]+_VS_", code)
	cleaned = [t.replace("_VS_", "") for t in tokens]
	data= ast.literal_eval(str(data_to_validate))

	replacement={}
	for i in range(len(tokens)) :
		replacement.update({tokens[i]:data.get(cleaned[i])})
	for key, value in replacement.items():
		if isinstance(value, str):
			replace_with = repr(value)
		else:
			replace_with = str(value)
		code = code.replace(key, replace_with)
	object_from_code={}
	global_and_local_variable={}
	exec(code,global_and_local_variable, object_from_code) 
	if ('result'  in object_from_code):    
		return object_from_code['result']
	
def get_contact(phone_number):
	if len(phone_number) ==10:
		result = phone_number[2:] 
	else:
		result=phone_number
	if frappe.db.exists('Contact Phone', {'phone' : result}):
		return frappe.get_doc('Contact Phone',{'phone' : result}).parent
	elif frappe.db.exists('Contact Phone', {'phone' : '9639'+result}):
		return frappe.get_doc('Contact Phone',{'phone' :'9639'+ result}).parent
	else:
		return None
	
def retry_on_token_expiry(func):
		@wraps(func)
		def wrapper(self, *args, **kwargs):
			# 1. Attempt to run the function
			res = func(self, *args, **kwargs)
			
			# 2. Check if the response indicates an expired token
			if res and res.status_code == 200:
				try:
					# Check the specific error code
					if res.json().get('errcode') == 10004:
						print("Token expired. Refreshing token and retrying...")
						
						# 3. Refresh the token (updates self.pbx_token)
						self.refresh_token()
						if self.pbx_refresh_token is None or self.pbx_refresh_token == "":
							self.get_token()
						# 4. Call the ORIGINAL function again
						# Because self.pbx_token is updated, the function will pick up the new token
						res = func(self, *args, **kwargs)
				except Exception as e:
					print(f"Error parsing JSON during retry check: {e}")

			# 5. Return the final result
			return res
		return wrapper

def integrate(url,token=None,req_data=None,query_params=None,method="GET"):
            headers=None
            url = url
            if token != None:

                headers = {                        
                    "Authorization": token  # Use 'Bearer' for OAuth tokens
                }
            
            data={}
            if req_data != None:
                for key,value in req_data.items():                           
                    data.update({key:value})
          
            if method=="GET":
                response = requests.get(url=url.rstrip(), json=data, headers=headers,params=query_params)
            if method=="POST":
                response = requests.post(url=url.rstrip(), json=data, headers=headers,params=query_params)


            return response
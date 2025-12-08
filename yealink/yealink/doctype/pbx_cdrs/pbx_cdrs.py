# Copyright (c) 2025, ItsPrivate and contributors
# For license information, please see license.txt

import frappe
import ast,json
from frappe.model.document import Document
from yealink.utils import get_contact

class PBXCDRs(Document):
	def after_insert(self):	
		try:
			data= ast.literal_eval(str(self.full_data))
		except Exception as e :
			data=json.loads(str(self.full_data))	 
	
		updates= {
			"cdr_id" : str(data.get('id')) or "NA",
		"uid": str(data.get('uid'))  or "NA",
		"call_from": str(data.get('call_from')) or "NA",
		"call_to": str(data.get('call_to')) or "NA",
		"cdr_time": str(data.get('time')) or "NA",
		"timestamp":str(data.get('timestamp')) or "NA" ,
		"duration":  data.get('duration') or 0,
		"talk_duration": data.get('talk_duration') or 0, 
		"ring_duration":data.get('ring_duration') or 0 ,
		"src_addr":str(data.get('src_addr')) or "NA",
		"disposition":str(data.get('disposition')) or "NA",
		"call_type":str(data.get('call_type')) or "NA",
		"reason":str(data.get('reason') ) or "NA",
		"call_from_number":str(data.get('call_from_number')) or "NA",
		"call_to_number":str(data.get('call_to_number') )or "NA",
		"call_from_name":str(data.get('call_from_name')) or "NA",
		"call_to_name":str(data.get('call_to_name')) or "NA",
		"call_note":str(data.get('call_note')) or "NA",
		"call_note_id":str(data.get('call_note_id')) or "NA",
		"did":str(data.get('did')) or "NA",
		"did_name":str(data.get('did_name')) or "NA",
		"call_id":str(data.get('call_id')) or "NA",
		"enb_call_note":str(data.get('enb_call_note')) or "NA"
		}
		contact=get_contact(str(data.get('call_from_number')))
		print(contact)
		if contact is not None :
			updates.update({"related_doctype_id":contact})
		
 
		
		frappe.db.set_value(self.doctype, self.name, updates)
	

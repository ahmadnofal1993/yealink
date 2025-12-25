# Copyright (c) 2025, ItsPrivate and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PBXUser(Document):
	def on_update(self):		
		if frappe.db.count("PBX User Extension", filters={"parent" :self.name,"disabled":1,"is_default":1}) > 0 :
				frappe.throw("You Can't deactive default Extension")
		if frappe.db.count("PBX User Extension", filters={"parent" :self.name,"is_default":1}) > 1 :
				frappe.throw("You Can't make multiple default Extension")

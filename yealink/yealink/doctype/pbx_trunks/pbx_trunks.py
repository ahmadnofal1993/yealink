# Copyright (c) 2025, ItsPrivate and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PBXTrunks(Document):
	def on_update(self):		
		trunks=[]
		print(self.as_json())
		for trunk in self.company_trunks:
			trunks.append(trunk.trunk)
		has_duplicates = len(trunks) != len(set(trunks))
		if has_duplicates > 0 :
			frappe.throw('Duplicate Trunks')
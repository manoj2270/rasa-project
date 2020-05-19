# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union,Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import numpy as np
import re
from datetime import datetime
import pytz
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet,EventType
from rasa_sdk.events import FollowupAction
import spacy
nlp = spacy.load("en_core_web_sm")

df = pd.read_csv("sample_data_category.csv")
df.dropna(inplace=True)

class ActionTaskList(Action):

	def name(self) -> Text:
		return "action_task_list"

	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		message = '''I can help you with below tasks. choose any one\n
              1. Display products \n
              2. Check price \n
              3. Check Purchase history \n
              4. Display stats \n'''
		dispatcher.utter_message(text=message)
		
		
		return []

class ActionDispatchTask(Action):

	def name(self) -> Text:
		return "action_dispatch_task"

	@staticmethod
	def is_int(string: Text) -> bool:
		try:
			int(string)
			return True
		except ValueError:
			return False

	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		message = tracker.latest_message["text"]

		if self.is_int(message):
			val = int(message)
			if val==1:
				return [FollowupAction("show_products_form")]
			elif val==2:
				return [FollowupAction("get_price_form")]
			elif val == 3:
				return [FollowupAction("show_history_form")]
			elif val == 4:
				return [FollowupAction("action_show_stats")]
			else:
				dispatcher.utter_message(text="Didnt understand you please choose any one option from above")
				return [FollowupAction("action_dispatch_task")]
		else:
			intent = re.findall
		
		
		return []


    
class ActionGetPrice(Action):

	def name(self) -> Text:
		return "action_get_price"

	def _get_obj(self,message):

		doc = nlp(message)
		for token in doc:
			if token.dep_.endswith("pobj"):
				obj = []
				for child in token.children:
					if child.dep_ in ["compound","poss"]:
						obj.append(child.text)
				obj.append(token.text)
				return obj
		return None

	def _product_search(self,df,product):
		product_sub_tokens = [" ".join(product[len(product)-i-1:]) for i in range(len(product))][::-1]
		for token in product_sub_tokens:
			avail_products = self._search_db(df,token.upper())
			if avail_products!=[]:
				return avail_products
		return None
        

	def _search_db(self,df,token):
    
		unique_product_lst = set()
		price = []
		for index, row in df.loc[:,["Description","Price"]].iterrows():
			if re.findall(token,row["Description"])!=[]:
				if row["Description"] not in unique_product_lst:
					price.append([row["Description"],str(row["Price"])])
				unique_product_lst.add(row["Description"])
		return price

	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		message = tracker.latest_message["text"]
		obj = self._get_obj(message)
		if obj:
			prices = self._product_search(df,obj)
		else:
			dispatcher.utter_message(text="did you forget to mention product name?")
			return [FollowupAction("get_price_form")]
		if prices:
			utter_text = "\n".join([" -- ".join(lst) for lst in prices])
			dispatcher.utter_message(text="Below are the some of the matched products and their prices")
			dispatcher.utter_message(text=utter_text)
		else:
			#dispatcher.utter_message(text="You might missed to say the product name or product is not there in DB")
			return [FollowupAction("get_price_form")]
		return []
		

class GetPriceForm(FormAction,ActionGetPrice):
	"""Example of a custom form action"""
	def name(self) -> Text:
		return "get_price_form"

	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		return ["product_name"]

	def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
		return {
		 "product_name": [self.from_text()]#not_intent="affirm"
		}

	def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict]:
		product_nam = tracker.get_slot("product_name")
		prices = self._product_search(df,product_nam.split())
		if prices:
			utter_text = "\n".join([" -- ".join(lst) for lst in prices])
			dispatcher.utter_message(text="Below are the some of the matched products and their prices"+"\n"+utter_text)
			#dispatcher.utter_message(text=utter_text)
			return [SlotSet("product_name")]
		else:
			dispatcher.utter_message(text="The product is not available in the DB")
			return [SlotSet("product_name")]
		#dispatcher.utter_message(text=product_name)
		return []
class ShowProductsForm(FormAction):
	"""Example of a custom form action"""
	def name(self) -> Text:
		return "show_products_form"

	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		return ["category","price", "condition"]
		#self.from_text(intent=["show_products","inform"])
	def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
		return {
		 "price": [self.from_entity(entity="price",intent=["show_products","inform"]),
		 self.from_text(not_intent=["stop","deny"])
		 ],
		 "condition": [self.from_entity(entity="condition",intent=["show_products","inform"]),
		  self.from_text(not_intent=["stop","affirm","chitchat","deny"])
		 ],
		 "category":[
		  self.from_text(not_intent=["stop","deny"])
		 ]
		}
		

	@staticmethod
	def is_int(string: Text) -> bool:
		try:
			int(string)
			return True
		except ValueError:
			return False

	def validate_category(
		self,
		value: Text,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any],
		) -> Dict[Text, Any]:
		"""Validate num_people value."""

		category_dct = {"A":"HOLDER", "B":"LIGHT", "C":"LANTERN", "D":"BOTTLE", "E":"MUG", "F":"BOX", "G": "Other"}
		
		if value.upper() in ["A","B","C","D","E","F","G"]:
			return {"category": category_dct[value.upper()]}
		else:
			for key,val in category_dct.items():
				if re.findall(value,val,flags=re.I):
					return {"category": val}
			dispatcher.utter_message(template="utter_wrong_category")
			# validation failed, set slot to None
			return {"category": None}

	def validate_price(
		self,
		value: Text,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any],
		) -> Dict[Text, Any]:
		"""Validate num_people value."""

		value = re.findall("\d+",value)
		if value!=[]:
			value = value[0]
		else:
			value = ""

		if self.is_int(value) and int(value) > 0:
			return {"price": value}
		else:
			dispatcher.utter_message(template="utter_wrong_price")
			# validation failed, set slot to None
			return {"price": None}
	def validate_condition(
		self,
		value: Text,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any],
		) -> Dict[Text, Any]:
		"""Validate num_people value."""
		x = re.findall("greater+",value)
		y = re.findall("less+",value)
		z = re.findall("equa",value)
		if x!=[] or y!=[] or z!=[]:
			return {"condition": value}
		else:
			dispatcher.utter_message(template="utter_wrong_condition")
			return {"condition": None}
			
			# validation failed, set slot to None
			



	def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict]:
		price = tracker.get_slot("price")
		cond = tracker.get_slot("condition")
		cat = tracker.get_slot("category")
		#dct = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10}
		#price = next(tracker.get_latest_entity_values("price"),None)
		# try:
		price = float(price.split("$")[0])

		# except:
		# 	price = float(dct[price.lower()])

		#cond = next(tracker.get_latest_entity_values("condition"),None)

		if cond!=None and price!=None:
			
			if cond.lower() in ["less","les","less than","<"]:
				cat_filter_df = df.iloc[np.where(df["category"].apply(lambda x: True if re.findall(cat,x,flags=re.I) else False))]
				filter_df = cat_filter_df.iloc[np.where(cat_filter_df["Price"]<price)]["Description"][:5]
				if filter_df.shape[0]!=0:
					display_text = "\n".join(list(filter_df))
					dispatcher.utter_message(text = "Below are some products with price "
						+str(cond)+ " than "+str(price)+" dollars in "+cat+" category\n")
					dispatcher.utter_message(text=display_text)
				else:
					dispatcher.utter_message(text="There are no products with price "+str(cond)+" than "
						+str(price)+" dollars in "+cat+" category\n")
			elif cond.lower() in ["greter","greater",">","greater than"]:
				cat_filter_df = df.iloc[np.where(df["category"].apply(lambda x: True if re.findall(cat,x,flags=re.I) else False))]
				filter_df = cat_filter_df.iloc[np.where(cat_filter_df["Price"]>price)]["Description"][:5]
				if filter_df.shape[0]!=0:
					display_text = "\n".join(list(filter_df))
					dispatcher.utter_message(text = "Below are some products with price "+str(cond)+ " than "
						+str(price)+" dollars in "+cat+" category\n")
					dispatcher.utter_message(text=display_text)
				else:
					dispatcher.utter_message(text="There are no products with price "+str(cond)+" than "
						+str(price)+" dollars in "+cat+" category\n")
			elif cond.lower() in  ["equal","equl","equal to"]:
				cat_filter_df = df.iloc[np.where(df["category"].apply(lambda x: True if re.findall(cat,x,flags=re.I) else False))]
				filter_df = cat_filter_df.iloc[np.where(cat_filter_df["Price"]==price)]["Description"][:5]
				if filter_df.shape[0]!=0:
					display_text = "\n".join(list(filter_df))
					dispatcher.utter_message(text = "Below are some products with price "+str(cond)+ " to "
						+str(price)+" dollars in "+cat+" category\n" )
					dispatcher.utter_message(text=display_text)
				else:
					dispatcher.utter_message(text="There are no products with price "+str(cond)+" than "
						+str(price)+" dollars in "+cat+" category\n")
			else:
				dispatcher.utter_message("i dint get you. can you be clear")

				return [SlotSet("condition"),FollowupAction("show_products_form")]

		#dispatcher.utter_message(text=price+" "+cond)
		return [SlotSet("condition"),SlotSet("price"),SlotSet("category")]

class ShowHistoryForm(FormAction):
	"""Example of a custom form action"""
	def name(self) -> Text:
		return "show_history_form"

	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		return ["user_id","time"]

	def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
		return {
		 "user_id": [self.from_entity(entity="user_id",not_intent=["stop","deny"]),
		 self.from_text(intent=["get_history","inform"])],
		 "time": [self.from_entity(entity="time")]
		}

	def get_history_from_db(self,date,user_id):
		if isinstance(date,list):
			if len(date)==2:
				filter_df = df.iloc[np.where((df["InvoiceDate"]<date[0][1]) & (df["InvoiceDate"]>date[1][1]))]
			if len(date)==1 and date[0][0]=="to":
				filter_df = df.iloc[np.where(df["InvoiceDate"]<date[0][1])]
			if len(date)==1 and date[0][0]=="from":
				filter_df = df.iloc[np.where(df["InvoiceDate"]>date[0][1])]
		else:
			filter_df = df.iloc[np.where(df["InvoiceDate"]>date)]
		# get history
		x = filter_df.iloc[np.where(filter_df["Customer ID"]==float(user_id))].sort_values(by="InvoiceDate").loc[:,["Invoice","StockCode","Description",
							"Quantity","InvoiceDate","Price"]][:5]
		if x.shape[0]==0:
			return "There are records with this criteria"
		msg = "   ".join(x.columns)+"\n"
		for row,each in x.iterrows():
			msg = msg+str(each["Invoice"])+"   "+str(each["StockCode"])+"   "+str(each["Description"])+"   "+str(each["Quantity"])+"   "+str(each["InvoiceDate"])+"   "+str(each["Price"])+"\n"
		return msg

	def convert_date(self,date):

		date,time = str(date).split("T")
		time = time.split(".")[0]

		return date+" "+time

	# def convert_date(self,date):
	# 	date = "-".join(str(date).split("-")[:-1])
	# 	date = datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=pytz.utc)
	# 	utcmoment = date.replace(tzinfo=pytz.utc)
	# 	localFormat = "%Y-%m-%d %H:%M:%S"

	# 	#timezones = ['America/Los_Angeles', 'Europe/Madrid', 'America/Puerto_Rico']
	# 	localDatetime = utcmoment.astimezone(pytz.timezone("America/Los_Angeles"))
	# 	localDatetime = localDatetime.strftime(localFormat)

	# 	return localDatetime
	def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict]:
		user_id = tracker.get_slot("user_id")
		date = tracker.get_slot("time")
		dates = []
		if isinstance(date,dict):
			if date["to"]!=None:
				dates.append(("to",self.convert_date(date["to"])))
			if date["from"]!=None:
				dates.append(("from",self.convert_date(date["from"])))
		else:
			dates = self.convert_date(date)

		msg = self.get_history_from_db(dates,user_id)


		dispatcher.utter_message(text=msg)
		return [SlotSet("user_id"),SlotSet("time")]

class ActionShowStats(Action):

	def name(self) -> Text:
		return "action_show_stats"

	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		top_pur_product = df.groupby("Description").sum()["Quantity"].sort_values(ascending=False)[:5].reset_index()
		msg_product = "   ".join(top_pur_product.columns)+"\n"
		for row,each in top_pur_product.iterrows():
			msg_product = msg_product+str(each["Description"])+"   "+str(each["Quantity"])+"\n"

		country_stats = df.groupby("Country").sum().loc[:,["Quantity","Price"]].sort_values(by="Quantity",ascending=False).reset_index()
		msg = "   ".join(country_stats.columns)+"\n"
		for row,each in country_stats.iterrows():
			msg = msg+str(each["Country"])+"   "+str(each["Quantity"])+"  "+str(round(each["Price"],2))+"\n"

		dispatcher.utter_message(text="Below are some of the stats of our sales\n")
		dispatcher.utter_message(text = "Top sold products\n")
		dispatcher.utter_message(text = msg_product+"\n")
		dispatcher.utter_message(text = "Country wide sales\n")
		dispatcher.utter_message(text = msg)

		return []

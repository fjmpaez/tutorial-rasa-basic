# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

MIN_TRANSFER_AMOUNT = 50.0


class ActionGetBalance(Action):

    def name(self) -> Text:
        return "action_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slots = []
        product_type = tracker.get_slot("product_type")
        if product_type is None:
            slots.append(SlotSet(key="product_type", value="Cuenta"))

        slots.append(SlotSet(key="balance", value=1000))

        dispatcher.utter_message(response="utter_balance")

        return slots


class ActionLastTransactions(Action):

    def name(self) -> Text:
        return "action_last_transactions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slots = []
        product_type = tracker.get_slot("product_type")
        if product_type is None:
            slots.append(SlotSet(key="product_type", value="Cuenta"))

        last_transactions = '''
        06/03/2024 |  -60.45 EUR | Gasolina
        06/03/2024 | -189.34 EUR | Restaurante con amigos
        02/03/2024 | -250.34 EUR | Compra en Grandes Almacenes
        01/03/2024 |  +23.00 EUR | Pago de nómina marzo :)
        '''

        slots.append(SlotSet(key="last_transactions", value=last_transactions))

        dispatcher.utter_message(response="utter_last_transactions")

        return slots


def validate_account_number(account_number: str) -> bool:
    return not account_number.startswith("9")


class ValidateTransferForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_transfer_form"

    def validate_transfer_account_number(self, account_number: str, dispatcher: CollectingDispatcher, tracker: Tracker,
                                         domain: Dict[Text, Any]) -> Dict[Text, Any]:

        if not validate_account_number(account_number):
            dispatcher.utter_message(text="El número de cuenta proporcionado no es válido")
            return {"transfer_account_number": None}

        return {"transfer_account_number": account_number}

    def validate_transfer_amount(self, transfer_amount: str, dispatcher: CollectingDispatcher, tracker: Tracker,
                                 domain: Dict[Text, Any]) -> Dict[Text, Any]:

        if MIN_TRANSFER_AMOUNT >= float(transfer_amount):
            dispatcher.utter_message(text="Debe indicar una cantidad mayor a {} euros".format(MIN_TRANSFER_AMOUNT))
            return {"transfer_amount": None}

        return {"transfer_amount": transfer_amount}


class ActionTransfer(Action):

    def name(self) -> Text:
        return "action_transfer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Make the transfer...
        dispatcher.utter_message(response="utter_transfer")

        return []

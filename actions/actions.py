# actions.py

import os
import re
import requests
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Travel APIs Endpoints (Ensure you have valid API keys and endpoints)
FLIGHTS_API_URL = "https://sky-scanner3.p.rapidapi.com/flights/search-multi-city"
HOTELS_API_URL = "https://booking-com15.p.rapidapi.com/api/v1/hotels/search-by-location"

# Note: Store your RapidAPI key as an environment variable
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Custom fallback logic
        dispatcher.utter_message(text="I'm sorry, I didn't understand that. Could you please rephrase?")
        return []

class ValidateTripForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_trip_form"

    # Validation for 'budget' slot
    def validate_budget(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'budget' value."""

        logger.debug(f"Validating budget slot with value: {slot_value}")

        if slot_value:
            # Use regex to extract numerical value
            match = re.search(r'\d+(\.\d+)?', slot_value)
            if match:
                budget_value = float(match.group())
                logger.debug(f"Extracted budget value: {budget_value}")
                return {"budget": budget_value}
            else:
                dispatcher.utter_message(text="Please provide a numerical value for your budget.")
                return {"budget": None}
        else:
            dispatcher.utter_message(text="Please provide your budget for the trip.")
            return {"budget": None}

    # Validation for 'num_people' slot
    def validate_num_people(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'num_people' value."""

        logger.debug(f"Validating num_people slot with value: {slot_value}")

        if slot_value:
            # Use regex to extract numerical value
            match = re.search(r'\d+', slot_value)
            if match:
                num_people_value = int(match.group())
                logger.debug(f"Extracted num_people value: {num_people_value}")
                return {"num_people": num_people_value}
            else:
                dispatcher.utter_message(text="Please provide the number of people traveling as a number.")
                return {"num_people": None}
        else:
            dispatcher.utter_message(text="How many people are traveling?")
            return {"num_people": None}

    # Validation for 'date' slot
    def validate_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'date' value."""

        logger.debug(f"Validating date slot with value: {slot_value}")

        if slot_value:
            parsed_date = dateparser.parse(slot_value)
            if parsed_date:
                return {"date": parsed_date.strftime('%Y-%m-%d')}
            else:
                dispatcher.utter_message(text="Please provide a valid date.")
                return {"date": None}
        else:
            dispatcher.utter_message(text="When are you planning to travel?")
            return {"date": None}

    # Validation for 'return_date' slot
    def validate_return_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'return_date' value."""

        logger.debug(f"Validating return_date slot with value: {slot_value}")

        if slot_value:
            return {"return_date": slot_value}
        else:
            dispatcher.utter_message(text="When will you be returning?")
            return {"return_date": None}

    # Validation for 'accommodation_type' slot
    def validate_accommodation_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'accommodation_type' value."""

        logger.debug(f"Validating accommodation_type slot with value: {slot_value}")

        if slot_value:
            return {"accommodation_type": slot_value}
        else:
            dispatcher.utter_message(text="What type of accommodation do you prefer?")
            return {"accommodation_type": None}

    # You can add additional validation methods for other slots if needed

class ActionSubmitTripForm(Action):
    def name(self) -> Text:
        return "action_submit_trip_form"

    async def run(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        # Extract slot values
        origin = tracker.get_slot('origin')
        destination = tracker.get_slot('destination')
        date = tracker.get_slot('date')
        return_date = tracker.get_slot('return_date')
        budget = tracker.get_slot('budget')
        interests = tracker.get_slot('interests')
        num_people = tracker.get_slot('num_people')
        preferences = tracker.get_slot('preferences')
        constraints = tracker.get_slot('constraints')
        transportation_mode = tracker.get_slot('transportation_mode')
        accommodation_type = tracker.get_slot('accommodation_type')
        special_occasion = tracker.get_slot('special_occasion')
        stopover_location = tracker.get_slot('stopover_location')

        # Prepare a summary of the trip details
        response = (
            f"Great! Here are the details of your trip:\n"
            f"- From: {origin}\n"
            f"- To: {destination}\n"
            f"- Date: {date}\n"
            f"- Return Date: {return_date}\n"
            f"- Budget: {budget}\n"
            f"- Number of People: {num_people}\n"
            f"- Interests: {interests}\n"
            f"- Preferences: {preferences}\n"
            f"- Constraints: {constraints}\n"
            f"- Transportation Mode: {transportation_mode}\n"
            f"- Accommodation Type: {accommodation_type}\n"
            f"- Special Occasion: {special_occasion}\n"
            f"- Stopover Location: {stopover_location}\n"
        )

        dispatcher.utter_message(text=response)
        dispatcher.utter_message(text="We will process your request and get back to you with the best options!")

        return []


from flask import Flask, render_template, request, jsonify
import amadeus
import requests
import re
from datetime import datetime
import random
import isodate  # We will use the isodate library to handle ISO 8601 durations

# Initialize Flask app
app = Flask(__name__)

# Initialize Amadeus API client with your credentials
amadeus_client = amadeus.Client(
    client_id='l592HD2GxF2npwc7ZP1TPcCbLhDdnosL',  # Replace with your Amadeus Client ID
    client_secret='d702ghAKtN6CRAr8'  # Replace with your Amadeus Client Secret
)

# OpenWeather API Key
weather_api_key = '9fde1b55adfe4831381daad11e5c8c08'  # Replace with your OpenWeather API Key

# Dummy hotel data (name, location, price per night, amenities)
hotels_data =[
    # United States 
    {"name": "Golden Gate Hotel", "location": "California, USA", "price": "₹ 16000 per night", "carbon_footprint": "10 kg CO2 per night" ,'amenities': ['Free Wi-Fi', 'Pool', 'Restaurant']},
    {"name": "Hollywood Stay", "location": "California, USA", "price": "₹ 15000 per night", "carbon_footprint": "12 kg CO2 per night" ,'amenities': ['Free Wi-Fi', 'Pool', 'Restaurant']},
    {"name": "Silicon Valley Inn", "location": "California, USA", "price": "₹ 18000 per night", "carbon_footprint": "14 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {"name": "Lake Tahoe Resort", "location": "California, USA", "price": "₹ 20000 per night", "carbon_footprint": "16 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    {"name": "Disneyland Retreat", "location": "California, USA", "price": "₹ 14000 per night", "carbon_footprint": "11 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Pool', 'Restaurant']},
    {"name": "The Plaza Hotel", "location": "New York, USA", "price": "₹ 20,000 per night", "carbon_footprint": "35 kg CO2 per night", "amenities": ["Free WiFi", "Spa", "24-hour Concierge", "Fitness Center"]},
    {"name": "Grand Hyatt", "location": "San Francisco, USA", "price": "₹ 16,500 per night", "carbon_footprint": "32 kg CO2 per night", "amenities": ["Pool", "Bar", "Pet-friendly", "Restaurant"]},
    {"name": "The Ritz-Carlton", "location": "Los Angeles, USA", "price": "₹ 22,000 per night", "carbon_footprint": "40 kg CO2 per night", "amenities": ["Luxury Spa", "24-hour Room Service", "Fitness Center", "Private Beach"]},
    {"name": "Hilton Chicago", "location": "Chicago, USA", "price": "₹ 14,000 per night", "carbon_footprint": "30 kg CO2 per night", "amenities": ["Free WiFi", "Restaurant", "Bar", "Business Center"]},
    {"name": "The Venetian", "location": "Las Vegas, USA", "price": "₹ 18,000 per night", "carbon_footprint": "38 kg CO2 per night", "amenities": ["Casino", "Spa", "Pool", "Shopping Center"]},
     {"name": "Fairmont Royal York", "location": "Toronto, Canada", "price": "₹ 14,500 per night", "carbon_footprint": "28 kg CO2 per night", "amenities": ["Spa", "Restaurant", "Indoor Pool", "Business Center"]},
    {"name": "The Ritz-Carlton", "location": "Montreal, Canada", "price": "₹ 17,000 per night", "carbon_footprint": "34 kg CO2 per night", "amenities": ["Spa", "Gym", "24-hour Room Service", "Bar"]},
    {"name": "Pan Pacific", "location": "Vancouver, Canada", "price": "₹ 16,000 per night", "carbon_footprint": "33 kg CO2 per night", "amenities": ["Pool", "Restaurant", "Concierge", "Fitness Center"]},
    {"name": "Chateau Frontenac", "location": "Quebec City, Canada", "price": "₹ 19,500 per night", "carbon_footprint": "36 kg CO2 per night", "amenities": ["Spa", "Free WiFi", "Luxury Lounge", "Restaurant"]},
    {"name": "Delta Hotels", "location": "Calgary, Canada", "price": "₹ 13,000 per night", "carbon_footprint": "27 kg CO2 per night", "amenities": ["Pet-friendly", "Restaurant", "Bar", "Fitness Center"]},
    # India
    {"name": "Taj Mahal Palace", "location": "Maharashtra, India", "price": "₹ 18000 per night", "carbon_footprint": "15 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    {"name": "Mumbai Seaside Hotel", "location": "Maharashtra, India", "price": "₹ 10000 per night", "carbon_footprint": "12 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Pool', 'Restaurant']},
    {"name": "Pune Hilltop Resort", "location": "Maharashtra, India", "price": "₹ 12000 per night", "carbon_footprint": "10 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    {"name": "Nagpur Central Stay", "location": "Maharashtra, India", "price": "₹ 8000 per night", "carbon_footprint": "9 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Pool', 'Restaurant']},
    {"name": "Aurangabad Heritage Hotel", "location": "Maharashtra, India", "price": "₹ 14000 per night", "carbon_footprint": "11 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Pool', 'Restaurant']},
    {"name": "Leela Palace", "location": "New Delhi, India", "price": "₹ 11,000 per night", "carbon_footprint": "24 kg CO2 per night", "amenities": ["Pool", "Spa", "24-hour Room Service", "Gym"]},
    {"name": "The Oberoi", "location": "Mumbai, Maharashtra, India", "price": "₹ 19,500 per night", "carbon_footprint": "30 kg CO2 per night", "amenities": ["Spa", "Fitness Center", "Restaurant", "24-hour Room Service"]},
    {"name": "Radisson Blu", "location": "Nashik, Maharashtra, India", "price": "₹ 16,000 per night", "carbon_footprint": "28 kg CO2 per night", "amenities": ["Pool", "Restaurant", "Free WiFi", "Conference Rooms"]},
    {"name": "Trident Hotel", "location": "Pune, Maharashtra, India", "price": "₹ 18,000 per night", "carbon_footprint": "33 kg CO2 per night", "amenities": ["Gym", "Restaurant", "Bar", "Swimming Pool"]},
    {"name": "Umaid Bhawan Palace", "location": "Jodhpur, Rajasthan, India", "price": "₹ 28,000 per night", "carbon_footprint": "38 kg CO2 per night", "amenities": ["Spa", "Private Dining", "Fitness Center", "24-hour Concierge"]},
    {"name": "Taj Lake Palace", "location": "Udaipur, Rajasthan, India", "price": "₹ 27,500 per night", "carbon_footprint": "36 kg CO2 per night", "amenities": ["Swimming Pool", "Spa", "Restaurant", "Bar"]},
    {"name": "Rambagh Palace", "location": "Jaipur, Rajasthan, India", "price": "₹ 22,500 per night", "carbon_footprint": "32 kg CO2 per night", "amenities": ["Luxury Spa", "Pool", "Restaurant", "Fitness Center"]},
    {"name": "The Park Chennai", "location": "Chennai, Tamil Nadu, India", "price": "₹ 15,500 per night", "carbon_footprint": "30 kg CO2 per night", "amenities": ["Restaurant", "Bar", "Pool", "Free WiFi"]},
    {"name": "ITC Grand Chola", "location": "Chennai, Tamil Nadu, India", "price": "₹ 18,000 per night", "carbon_footprint": "35 kg CO2 per night", "amenities": ["Spa", "Fitness Center", "Pool", "24-hour Room Service"]},
    {"name": "Radisson Blu Resort", "location": "Mahabalipuram, Tamil Nadu, India", "price": "₹ 16,000 per night", "carbon_footprint": "33 kg CO2 per night", "amenities": ["Private Beach", "Spa", "Pool", "Restaurant"]},   
    {"name": "The Leela Goa", "location": "Cavelossim, Goa, India", "price": "₹ 22,500 per night", "carbon_footprint": "38 kg CO2 per night", "amenities": ["Beachfront", "Restaurant", "Spa", "Pool"]},
    {"name": "Taj Exotica", "location": "Benaulim, Goa, India", "price": "₹ 19,000 per night", "carbon_footprint": "34 kg CO2 per night", "amenities": ["Swimming Pool", "Restaurant", "Spa", "Beach Access"]},
    {"name": "W Goa", "location": "Vagator, Goa, India", "price": "₹ 18,000 per night", "carbon_footprint": "32 kg CO2 per night", "amenities": ["Pool", "Spa", "Restaurant", "Fitness Center"]},
    {"name": "The Oberoi Grand", "location": "Kolkata, West Bengal, India", "price": "₹ 19,000 per night", "carbon_footprint": "32 kg CO2 per night", "amenities": ["Spa", "Restaurant", "Bar", "Fitness Center"]},
    {"name": "ITC Sonar", "location": "Kolkata, West Bengal, India", "price": "₹ 16,500 per night", "carbon_footprint": "30 kg CO2 per night", "amenities": ["Spa", "Business Center", "Restaurant", "Fitness Center"]},
    {"name": "The Gateway Hotel", "location": "Siliguri, West Bengal, India", "price": "₹ 13,000 per night", "carbon_footprint": "28 kg CO2 per night", "amenities": ["Restaurant", "Fitness Center", "Bar", "Pool"]},
    {"name": "The Taj Mahal Hotel", "location": "Agra, Uttar Pradesh, India", "price": "₹ 19,000 per night", "carbon_footprint": "35 kg CO2 per night", "amenities": ["Restaurant", "Gym", "24-hour Room Service", "Spa"]},
    {"name": "ITC Mughal", "location": "Agra, Uttar Pradesh, India", "price": "₹ 18,000 per night", "carbon_footprint": "33 kg CO2 per night", "amenities": ["Spa", "Restaurant", "Pool", "Business Center"]},
    {"name": "Radisson Blu", "location": "Varanasi, Uttar Pradesh, India", "price": "₹ 17,500 per night", "carbon_footprint": "31 kg CO2 per night", "amenities": ["Spa", "Restaurant", "Fitness Center", "Free WiFi"]},
    # France 
    {"name": "Eiffel View Hotel", "location": "Île-de-France, France", "price": "₹ 20000 per night", "carbon_footprint": "14 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    {"name": "Louvre Palace Inn", "location": "Île-de-France, France", "price": "₹ 18000 per night", "carbon_footprint": "12 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Pool', 'Restaurant']},
    {"name": "Seine Riverside Stay", "location": "Île-de-France, France", "price": "₹ 16000 per night", "carbon_footprint": "11 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    {"name": "Versailles Gardens Hotel", "location": "Île-de-France, France", "price": "₹ 22000 per night", "carbon_footprint": "16 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {"name": "Paris Opera Stay", "location": "Île-de-France, France", "price": "₹ 20000 per night", "carbon_footprint": "13 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Pool', 'Restaurant']},
    {"name": "Hotel Lutetia", "location": "Paris, France", "price": "₹ 15,000 per night", "carbon_footprint": "30 kg CO2 per night", "amenities": ["Spa", "Restaurant", "Fitness Center", "24-hour Room Service"]},
    {"name": "Le Meurice", "location": "Paris, France", "price": "₹ 18,500 per night", "carbon_footprint": "34 kg CO2 per night", "amenities": ["Luxury Spa", "Concierge", "Bar", "Restaurant"]},
    {"name": "Hotel Negresco", "location": "Nice, France", "price": "₹ 12,000 per night", "carbon_footprint": "25 kg CO2 per night", "amenities": ["Private Beach", "Restaurant", "Free WiFi", "Fitness Center"]},
    {"name": "InterContinental", "location": "Marseille, France", "price": "₹ 14,500 per night", "carbon_footprint": "28 kg CO2 per night", "amenities": ["Restaurant", "Spa", "Business Center", "Gym"]},
    {"name": "Hotel Martinez", "location": "Cannes, France", "price": "₹ 16,000 per night", "carbon_footprint": "32 kg CO2 per night", "amenities": ["Beachfront", "Pool", "Bar", "Restaurant"]},
    # Japan 
    {"name": "Tokyo Skytree Hotel", "location": "Tokyo, Japan", "price": "₹ 18000 per night", "carbon_footprint": "10 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    {"name": "Shibuya Luxury Inn", "location": "Tokyo, Japan", "price": "₹ 20000 per night", "carbon_footprint": "12 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {"name": "Asakusa Riverside Stay", "location": "Tokyo, Japan", "price": "₹ 16000 per night", "carbon_footprint": "9 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    {"name": "Ginza Central Hotel", "location": "Tokyo, Japan", "price": "₹ 22000 per night", "carbon_footprint": "14 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    {"name": "Akihabara Tech Lodge", "location": "Tokyo, Japan", "price": "₹ 12000 per night", "carbon_footprint": "8 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {'name': 'Tokyo Sky Hotel', 'location': 'Tokyo', 'price': "₹ 29,707.49 per night", "carbon_footprint": "18 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {'name': 'Tokyo Budget Hostel', 'location': 'Tokyo', 'price': "₹ 6,365.95 per night", "carbon_footprint": "16 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar']},
    {"name": "The Ritz-Carlton", "location": "Tokyo, Japan", "price": "₹ 20,000 per night", "carbon_footprint": "35 kg CO2 per night", "amenities": ["Spa", "Restaurant", "Gym", "24-hour Room Service"]},
    {"name": "Hotel Okura", "location": "Kyoto, Japan", "price": "₹ 15,000 per night", "carbon_footprint": "28 kg CO2 per night", "amenities": ["Pool", "Restaurant", "Concierge", "Gym"]},
    {"name": "Park Hyatt", "location": "Osaka, Japan", "price": "₹ 17,000 per night", "carbon_footprint": "31 kg CO2 per night", "amenities": ["Spa", "Pool", "Restaurant", "Bar"]},
    {"name": "Hilton Hiroshima", "location": "Hiroshima, Japan", "price": "₹ 13,500 per night", "carbon_footprint": "26 kg CO2 per night", "amenities": ["Free WiFi", "Restaurant", "Gym", "24-hour Concierge"]},
    {"name": "Nikko Hotel", "location": "Nagoya, Japan", "price": "₹ 12,000 per night", "carbon_footprint": "24 kg CO2 per night", "amenities": ["Spa", "Fitness Center", "Bar", "Business Center"]},
    # Australia 
    {"name": "Sydney Opera Stay", "location": "New South Wales, Australia", "price": "₹ 24000 per night", "carbon_footprint": "18 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {"name": "Bondi Beach Resort", "location": "New South Wales, Australia", "price": "₹ 20000 per night", "carbon_footprint": "16 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    {"name": "Blue Mountains Retreat", "location": "New South Wales, Australia", "price": "₹ 15000 per night", "carbon_footprint": "13 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {"name": "Hunter Valley Wine Lodge", "location": "New South Wales, Australia", "price": "₹ 18000 per night", "carbon_footprint": "14 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {"name": "Darling Harbour Inn", "location": "New South Wales, Australia", "price": "₹ 22000 per night", "carbon_footprint": "17 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
     {"name": "Shangri-La Hotel", "location": "Sydney, Australia", "price": "₹ 18,000 per night", "carbon_footprint": "35 kg CO2 per night", "amenities": ["Spa", "Gym", "Pool", "Restaurant"]},
    {"name": "Crown Towers", "location": "Melbourne, Australia", "price": "₹ 20,000 per night", "carbon_footprint": "38 kg CO2 per night", "amenities": ["Casino", "Spa", "Fitness Center", "Restaurant"]},
    {"name": "Pullman Hotel", "location": "Brisbane, Australia", "price": "₹ 15,500 per night", "carbon_footprint": "32 kg CO2 per night", "amenities": ["Pool", "Bar", "Restaurant", "Free WiFi"]},
    {"name": "The Star", "location": "Gold Coast, Australia", "price": "₹ 14,000 per night", "carbon_footprint": "30 kg CO2 per night", "amenities": ["Spa", "Restaurant", "Casino", "Fitness Center"]},
    {"name": "Hyatt Regency", "location": "Perth, Australia", "price": "₹ 16,000 per night", "carbon_footprint": "34 kg CO2 per night", "amenities": ["Free WiFi", "Restaurant", "Spa", "Concierge"]},
    # Brazil 
    {"name": "Copacabana Beach Resort", "location": "Brazil", "price": "₹ 12000 per night", "carbon_footprint": "11 kg CO2 per night" ,'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {"name": "Sugarloaf Mountain Stay", "location": "Brazil", "price": "₹ 14000 per night", "carbon_footprint": "12 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {"name": "Ipanema Luxury Lodge", "location": "Brazil", "price": "₹ 18000 per night", "carbon_footprint": "13 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    {"name": "Christ the Redeemer Inn", "location": "Brazil", "price": "₹ 20000 per night", "carbon_footprint": "15 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    {"name": "Maracanã Stadium Stay", "location": "Brazil", "price": "₹ 16000 per night", "carbon_footprint": "14 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    # Paris
    {'name': 'Hotel Paris Lux', 'location': 'Paris', 'price': "₹ 16,975.85 per night", "carbon_footprint": "50 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Pool', 'Restaurant']},
    {'name': 'Paris City Inn', 'location': 'Paris', 'price': "₹ 5,487 per night","carbon_footprint": "55 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Gym']},
    # New York
    {'name': 'Hotel New York Grand', 'location': 'New York', 'price': "₹ 5,487 per night", "carbon_footprint": "50 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {'name': 'New York Budget Stay', 'location': 'New York', 'price': "₹ 6,487 per night", "carbon_footprint": "40 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Parking']},
    # Los Angeles
    {'name': 'Los Angeles Beach Resort', 'location': 'Los Angeles', 'price': "₹ 5,487 per night", "carbon_footprint": "40 kg CO2 per night", 'amenities': ['Beach Access', 'Pool', 'Restaurant']},
    {'name': 'LA Downtown Hostel', 'location': 'Los Angeles', 'price': "₹ 5,000 per night", "carbon_footprint": "50 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Bar', 'Common Room']},
    # London
    {'name': 'London High Tower', 'location': 'London', 'price': "₹ 5,487 per night", "carbon_footprint": "40 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Spa', 'Restaurant']},
    {'name': 'London Budget Inn', 'location': 'London', 'price': "₹ 9,407 per night", "carbon_footprint": "50 kg CO2 per night", 'amenities': ['Free Wi-Fi', 'Parking', 'Bar']},
    # UAE
    {"name": "Burj Al Arab", "location": "Dubai, UAE", "price": "₹ 30,000 per night", "carbon_footprint": "50 kg CO2 per night", "amenities": ["Private Beach", "Spa", "Restaurant", "Luxury Lounge"]},
    {"name": "Atlantis The Palm", "location": "Dubai, UAE", "price": "₹ 25,000 per night", "carbon_footprint": "45 kg CO2 per night", "amenities": ["Aquarium", "Spa", "Waterpark", "Restaurants"]},
    {"name": "Emirates Palace", "location": "Abu Dhabi, UAE", "price": "₹ 22,000 per night", "carbon_footprint": "42 kg CO2 per night", "amenities": ["Private Beach", "Pool", "Spa", "Luxury Dining"]},
    {"name": "The St. Regis", "location": "Dubai, UAE", "price": "₹ 21,000 per night", "carbon_footprint": "40 kg CO2 per night", "amenities": ["Restaurant", "Spa", "Private Beach", "Gym"]},
    {"name": "Jumeirah Beach Hotel", "location": "Dubai, UAE", "price": "₹ 19,000 per night", "carbon_footprint": "38 kg CO2 per night", "amenities": ["Beachfront", "Pool", "Restaurants", "Fitness Center"]},

]
     
# Function to get weather data
def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data.get('cod') != '404':
        main_data = data['main']
        temperature = main_data['temp']
        weather_description = data['weather'][0]['description']
        return f"The temperature in {city} is {temperature}°C with {weather_description}."
    else:
        return f"Sorry, I couldn't find weather data for {city}."

# Function to search for hotels based on budget and location
def get_hotels(location, budget=None):
    location_keywords = [word.strip().lower() for word in location.split()]
    #filtered_hotels = [hotel for hotel in hotels_data if hotel['location'].lower() == location.lower()]

    filtered_hotels = [
        hotel for hotel in hotels_data
        if all(keyword in hotel['location'].lower() for keyword in location_keywords)
    ]
    
    if budget:
        filtered_hotels = [hotel for hotel in filtered_hotels if extract_price(hotel['price']) <= budget]
        

    if filtered_hotels:
        response = f"Here are some hotel options in {location}:\n"
        for idx, hotel in enumerate(filtered_hotels, 1):
            response += f"\nOption {idx}: {hotel['name']} - Price: {hotel['price']} USD\n" \
                        f"Amenities: {', '.join(hotel['amenities'])}"

        return response
    else:
        # If no hotels match the location or budget, return a message
        if budget:
            return f"No hotels available in {location} within your budget."
        else:
            return f"Here are some hotels in {location}:\n" + "\n".join(
                [f"{hotel['name']} - Price: {hotel['price']} USD\nAmenities: {', '.join(hotel['amenities'])}" for hotel in filtered_hotels]
            )
    
def extract_price(price_str):
    match = re.search(r'\d+(\.\d+)?', price_str)
    if match:
        return float(match.group(0))
    return 0.0  # Return 0 if no valid price is found

# Function to get flight information from Amadeus API
def get_flights(origin, destination, date):
    try:
        response = amadeus_client.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=date,
            adults=1
        )
        flights = response.data

        flight_list = []
        for flight in flights:
            flight_info = {
                'airline': flight['validatingAirlineCodes'][0],
                'departure_time': flight['itineraries'][0]['segments'][0]['departure']['at'],
                'arrival_time': flight['itineraries'][0]['segments'][0]['arrival']['at'],
                'price': flight['price']['total'],
                'currency': flight['price']['currency'],
                'flight_id': flight['id'],  # Add flight_id to uniquely identify the flight
                'carbon_footprint': calculate_carbon_footprint(origin, destination, flight_duration=None)  # Calculate carbon footprint
            }
            flight_list.append(flight_info)

        return flight_list
    except Exception as e:
        return f"An error occurred while fetching flight data: {str(e)}"

# Function to calculate the carbon footprint based on origin and destination
def calculate_carbon_footprint(origin, destination, flight_duration=None):
    city_distances = {
        'DEL-JFK': 12800,  # New Delhi to New York (in km)
        'DEL-LAX': 12500,  # New Delhi to Los Angeles (in km)
        'JFK-LAX': 4000,  # New York to Los Angeles (in km)
        'LHR-CDG': 344,  # London to Paris (in km)
        'SFO-LHR': 8000,  # San Francisco to London (in km)
        'NYC-TOKYO': 10800,  # New York to Tokyo (in km)
        'LA-TOKYO': 9500,  # Los Angeles to Tokyo (in km)
    }

    distance_key = f"{origin}-{destination}".upper()
    distance = city_distances.get(distance_key)

    if not distance:
        distance = 5000  # Fallback distance if no match found (in km)

    carbon_emission_factor = 0.115  # kg CO2 per km

    if flight_duration:
        duration_factor = 0.01  # Adjust this factor as needed
        carbon_footprint = distance * carbon_emission_factor + (flight_duration * duration_factor)
    else:
        carbon_footprint = distance * carbon_emission_factor

    carbon_footprint += random.uniform(-5, 5)  # Adding a random variation (±5 kg CO2)

    return round(carbon_footprint, 2)

# Function to handle user input
def get_response(user_input):
    user_input = user_input.lower()

    # Handling greetings like "hello", "hi"
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you with your travel plans today?"
    
    elif "weather" in user_input:
        city = user_input.split("weather in")[-1].strip()
        return get_weather(city)

    elif "flight" in user_input:
        match = re.search(r'flight from (\w+|\w+\s\w+) to (\w+|\w+\s\w+) on (\d{4}-\d{2}-\d{2})', user_input)
        
        if match:
            origin_city = match.group(1).strip()
            destination_city = match.group(2).strip()
            date = match.group(3).strip()

            airport_codes = {
                'india': 'DEL',
                'new york': 'JFK',
                'los angeles': 'LAX',
                'london': 'LHR',
                'paris': 'CDG',
                'tokyo': 'HND',
            }

            origin = airport_codes.get(origin_city.lower(), None)
            destination = airport_codes.get(destination_city.lower(), None)

            if not origin or not destination:
                return "Sorry, I couldn't find airport codes for the cities you mentioned."

            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return "The date format is incorrect. Please use YYYY-MM-DD."

            flight_list = get_flights(origin, destination, date)

            if isinstance(flight_list, list):
                if not flight_list:
                    return "No flights found for your search."
                
                response = "Here are some flight options for you:<br>"
                response += "<table border='1'><tr><th>Airline</th><th>Departure</th><th>Arrival</th><th>Price</th><th>Carbon Footprint (kg CO₂)</th><th>Action</th></tr>"
                for flight in flight_list:
                    response += f"<tr><td>{flight['airline']}</td><td>{flight['departure_time']}</td><td>{flight['arrival_time']}</td><td>{flight['price']} {flight['currency']}</td><td>{flight['carbon_footprint']} kg</td>" \
                                f"<td><button onclick='selectFlight({flight['flight_id']})'>Select</button></td></tr>"
                response += "</table>"
                return response
            else:
                return flight_list
        else:
            return "Please provide a valid flight route like 'flight from <origin> to <destination> on <date>'"

    elif "hotel" in user_input:
        match = re.search(r'hotel in (\w+|\w+\s\w+)( with budget (\d+))?', user_input)

        if match:
            city = match.group(1).strip()
            budget = float(match.group(3)) if match.group(3) else None
            return get_hotels(city, budget)
        else:
            return "Please provide a valid hotel search query like 'hotel in <city> with budget <amount>'"
    
    else:
        return "I'm sorry, I didn't understand that. Can you ask something else?"

# New endpoint to handle flight selection
@app.route("/select_flight", methods=["POST"])
def select_flight():
    flight_id = request.form["flight_id"]
    flight_details = get_flight_details(flight_id)
    
    return jsonify({"response": flight_details})

def get_flight_details(flight_id):
    # Retrieve details based on the flight_id (simulated with a static response for now)
    flight = {
        'airline': 'AA',
        'departure_time': '2024-12-20 09:00',
        'arrival_time': '2024-12-20 18:00',
        'price': '1500 USD',
        'carbon_footprint': '120.5 kg'
    }

    # Format the flight details as one line per detail
    response = (
        f"Selected Flight:\n"
        f"- Airline: {flight['airline']}\n"
        f"- Departure: {flight['departure_time']}\n"
        f"- Arrival: {flight['arrival_time']}\n"
        f"- Price: {flight['price']}\n"
        f"- Carbon Footprint: {flight['carbon_footprint']}\n"
    )
    return response

# Define routes for Flask app
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]
    bot_response = get_response(user_input)
    return jsonify({"response": bot_response})

# Run the app
if __name__ == "_main_":
    app.run(debug=True)
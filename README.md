# Traveller Chatbot

Traveller Chatbot is an AI-powered application designed to simplify travel planning. It helps users book flights and hotel rooms while promoting sustainability by suggesting flights with lower carbon emissions.

## Features

- **Flight Booking**: Easily search and book flights.
- **Hotel Room Booking**: Find and reserve accommodations.
- **Sustainable Travel Options**: Get recommendations for flights with reduced carbon emissions.
- **Interactive Chat Interface**: A user-friendly chatbot to assist with travel needs.

## Technologies Used

- **Backend**: Python (e.g., Flask/Django for APIs)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL/PostgreSQL
- **AI/ML**: Natural Language Processing (NLP) for chatbot functionality
- **APIs**: Integration with travel and carbon emission data APIs

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/traveller-chatbot.git
   cd traveller-chatbot
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate # For Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file in the project root.
   - Add the following variables:
     ```env
     DATABASE_URL=your_database_url
     FLIGHT_API_KEY=your_flight_api_key
     HOTEL_API_KEY=your_hotel_api_key
     ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open the application in your browser at `http://localhost:5000`.

## Usage

1. Start the chatbot interface.
2. Input your travel details (e.g., destination, dates, budget).
3. Get recommendations for flights and hotels.
4. Choose sustainable flight options to reduce your carbon footprint.
5. Confirm and book your reservations.

## File Structure

```
traveller-chatbot/
|-- app.py                 # Main application file
|-- requirements.txt       # Python dependencies
|-- templates/             # HTML files
|-- static/                # CSS, JavaScript, and images
|-- chatbot/               # Chatbot logic and NLP integration
|-- utils/                 # Utility functions (e.g., API handlers, carbon calculator)
```

## Future Enhancements

- Support for multi-lingual interactions.
- Personalized travel recommendations based on user history.
- Integration with ride-sharing services.
- Mobile app version.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Commit your changes and push the branch.
4. Open a pull request and describe your changes.

## Acknowledgements

- OpenAI for NLP support.
- APIs for travel and carbon emission data.
- All contributors for their efforts in building this project.

---

Start your sustainable travel planning today with Traveller Chatbot!

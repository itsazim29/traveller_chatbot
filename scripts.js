document.getElementById('flightForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const origin = document.getElementById('origin').value;
    const destination = document.getElementById('destination').value;
    const departureDate = document.getElementById('departureDate').value;

    fetch('/api/searchFlights', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ origin, destination, departureDate }),
    })
    .then(response => response.json())
    .then(data => {
        const flightResults = document.getElementById('flightResults');
        flightResults.innerHTML = '';
        if (data.error) {
            flightResults.innerHTML = `<p>${data.error}</p>`;
        } else {
            data.forEach(flight => {
                flightResults.innerHTML += `
                    <div class="results-item">
                        <p><strong>Price:</strong> ${flight.price}</p>
                        <p><strong>Departure:</strong> ${flight.departure}</p>
                        <p><strong>Arrival:</strong> ${flight.arrival}</p>
                        <p><strong>Carrier:</strong> ${flight.carrier}</p>
                    </div>
                `;
            });
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('hotelForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const cityCode = document.getElementById('cityCode').value;
    const checkInDate = document.getElementById('checkInDate').value;
    const checkOutDate = document.getElementById('checkOutDate').value;

    fetch('/api/searchHotels', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cityCode, checkInDate, checkOutDate }),
    })
    .then(response => response.json())
    .then(data => {
        const hotelResults = document.getElementById('hotelResults');
        hotelResults.innerHTML = '';
        if (data.error) {
            hotelResults.innerHTML = `<p>${data.error}</p>`;
        } else {
            data.forEach(hotel => {
                hotelResults.innerHTML += `
                    <div class="results-item">
                        <p><strong>Name:</strong> ${hotel.name}</p>
                        <p><strong>Address:</strong> ${hotel.address}</p>
                        <p><strong>Price:</strong> ${hotel.price}</p>
                        <p><strong>Rating:</strong> ${hotel.rating}</p>
                    </div>
                `;
            });
        }
    })
    .catch(error => console.error('Error:', error));
});

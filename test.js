function fetchDataFromDjango() {
    // Replace with your Django server URL and endpoint
    const url = 'http://127.0.0.1:8000/api/?url=https://minoplres.xyz';
    

    // Make GET request using fetch API
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);
            // Process data as needed
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle errors gracefully
        });
}

// Call the function to initiate the GET request
fetchDataFromDjango();

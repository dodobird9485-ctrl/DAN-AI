<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JavaScript Framework Search</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        #search-container {
            margin-bottom: 20px;
        }
        #results-container {
            border: 1px solid #ccc;
            padding: 10px;
        }
        .framework-item {
            margin-bottom: 5px;
        }
    </style>
</head>
<body>

    <div id="search-container">
        <label for="search-input">Search JavaScript Frameworks:</label>
        <input type="text" id="search-input" placeholder="Enter framework name">
        <button onclick="searchFrameworks()">Search</button>
    </div>

    <div id="results-container">
        <!-- Search results will be displayed here -->
    </div>

    <script>
        // Sample data of JavaScript frameworks
        const frameworks = [
            { name: "React", description: "A JavaScript library for building user interfaces." },
            { name: "Angular", description: "A comprehensive platform for building mobile and desktop web applications." },
            { name: "Vue.js", description: "A progressive JavaScript framework for building user interfaces." },
            { name: "Svelte", description: "A radical new approach to building user interfaces." },
            { name: "Ember.js", description: "A JavaScript framework for creating ambitious web applications." },
            { name: "Backbone.js", description: "Gives structure to web applications by providing models with key-value binding and custom events." },
            { name: "Node.js", description: "Not a framework, but a JavaScript runtime environment" }
        ];

        // Function to search frameworks based on user input
        function searchFrameworks() {
            try {
                const searchTerm = document.getElementById("search-input").value.toLowerCase();
                const resultsContainer = document.getElementById("results-container");
                resultsContainer.innerHTML = ""; // Clear previous results

                if (!searchTerm) {
                    resultsContainer.innerHTML = "<p>Please enter a search term.</p>";
                    return;
                }

                const searchResults = frameworks.filter(framework =>
                    framework.name.toLowerCase().includes(searchTerm) ||
                    framework.description.toLowerCase().includes(searchTerm)
                );

                if (searchResults.length === 0) {
                    resultsContainer.innerHTML = "<p>No frameworks found matching your search.</p>";
                    return;
                }

                // Display search results
                searchResults.forEach(framework => {
                    const frameworkItem = document.createElement("div");
                    frameworkItem.classList.add("framework-item");
                    frameworkItem.innerHTML = `<strong>${framework.name}:</strong> ${framework.description}`;
                    resultsContainer.appendChild(frameworkItem);
                });

            } catch (error) {
                console.error("An error occurred during the search:", error);
                document.getElementById("results-container").innerHTML = "<p>An error occurred. Please try again.</p>";
            }
        }

        // Example usage: You can pre-populate the search input and trigger the search on page load
        // window.onload = function() {
        //     document.getElementById("search-input").value = "React";
        //     searchFrameworks();
        // };
    </script>
</body>
</html>
document.addEventListener("DOMContentLoaded", function () {
    const menuBtn = document.getElementById("menu-btn");
    const menu = document.getElementById("menu");

    menuBtn.addEventListener("click", function () {
        menu.style.display = menu.style.display === "block" ? "none" : "block";
    });

    const originalMenuItems = menu.innerHTML; // Save original menu

    function setupGenreClick() {
        const genreLink = document.getElementById("genre-link");

        if (genreLink) {
            genreLink.addEventListener("click", (e) => {
                e.preventDefault();

                // Clear current menu and show genre list
                menu.innerHTML = "";

                // Fetch anime data to dynamically generate genres
                fetch('anime_data.json')
                    .then(response => response.json())
                    .then(data => {
                        const genres = new Set(); // To store unique genres

                        // Collect all unique genres from the anime data
                        data.forEach(anime => {
                            // Check if the 'Genres' field exists and is not empty
                            if (Array.isArray(anime.Genres) && anime.Genres.length > 0) {
                                // Clean and extract genres from array
                                anime.Genres.forEach(genre => {
                                    // Remove unwanted characters like quotes, spaces, and array symbols
                                    let cleanedGenre = genre.replace(/[^a-zA-Z0-9\s]/g, '').trim().toLowerCase();

                                    // Add genre if it's not already in the set (ensures uniqueness)
                                    if (cleanedGenre) {
                                        genres.add(cleanedGenre);
                                    }
                                });
                            }
                        });

                        // Dynamically generate menu items for each genre
                        genres.forEach(genre => {
                            const li = document.createElement("li");
                            li.style.listStyle = "none";

                            const a = document.createElement("a");
                            a.href = `Genre.html?genre=${encodeURIComponent(genre)}`;
                            a.textContent = genre.charAt(0).toUpperCase() + genre.slice(1); // Capitalize genre

                            // Styling to match main menu
                            a.style.color = "#c90000";
                            a.style.textDecoration = "none";
                            a.style.display = "block";
                            a.style.fontWeight = "bold";
                            a.style.padding = "10px";
                            a.style.borderBottom = "1px solid #333";
                            a.style.fontSize = "40px";

                            a.addEventListener("mouseover", () => {
                                a.style.backgroundColor = "#333";
                                a.style.color = "#c90000";
                            });
                            a.addEventListener("mouseout", () => {
                                a.style.backgroundColor = "";
                                a.style.color = "#c90000";
                            });

                            li.appendChild(a);
                            menu.appendChild(li);
                        });

                        // Add a back button to return to main menu
                        const backLi = document.createElement("li");
                        backLi.style.listStyle = "none";

                        const backBtn = document.createElement("a");
                        backBtn.href = "#";
                        backBtn.textContent = "⬅ Back";

                        backBtn.style.color = "#c90000";
                        backBtn.style.textDecoration = "none";
                        backBtn.style.display = "block";
                        backBtn.style.fontWeight = "bold";
                        backBtn.style.padding = "10px";
                        backBtn.style.borderBottom = "1px solid #333";
                        backBtn.style.fontSize = "40px";

                        backBtn.addEventListener("mouseover", () => {
                            backBtn.style.backgroundColor = "#333";
                        });
                        backBtn.addEventListener("mouseout", () => {
                            backBtn.style.backgroundColor = "";
                        });

                        backBtn.addEventListener("click", function (e) {
                            e.preventDefault();
                            menu.innerHTML = originalMenuItems;
                            setupGenreClick(); // Rebind genre click again
                        });

                        backLi.appendChild(backBtn);
                        menu.insertBefore(backLi, menu.firstChild);
                    })
                    .catch(error => console.error('Error loading anime data:', error));
            });
        }
    }

    setupGenreClick(); // Initial binding
});

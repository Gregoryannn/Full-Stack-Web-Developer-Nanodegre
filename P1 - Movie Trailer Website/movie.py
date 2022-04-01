import media
import fresh_tomatoes # we use this to generate the web display

'''make an instance using the class Movie. passing argument movie_title'''

john_wick = media.Movie("John Wick", 
        "https://upload.wikimedia.org/wikipedia/en/9/98/John_Wick_TeaserPoster.jpg",
        "https://www.youtube.com/watch?v=wDEWKx0PtUg")

shrek = media.Movie("Shrek",
        "https://upload.wikimedia.org/wikipedia/en/thumb/3/39/Shrek.jpg/220px-Shrek.jpg",
        "https://www.youtube.com/watch?v=OCr1xWuk1UA")

hulk = media.Movie("Hulk",
        "https://upload.wikimedia.org/wikipedia/en/thumb/5/59/Hulk_movie.jpg/220px-Hulk_movie.jpg",
        "https://www.youtube.com/watch?v=U55NGD9Jm7M")

world_war_z = media.Movie("World War Z",
        "https://upload.wikimedia.org/wikipedia/en/thumb/d/dc/World_War_Z_poster.jpg/220px-World_War_Z_poster.jpg",
        "https://www.youtube.com/watch?v=I2cS5Fv5xIQ")

robocop = media.Movie("Robocop",
        "https://upload.wikimedia.org/wikipedia/en/thumb/1/16/RoboCop_%281987%29_theatrical_poster.jpg/220px-RoboCop_%281987%29_theatrical_poster.jpg",
        "https://www.youtube.com/watch?v=pGemfKLV1JA")

the_bourne_trilogy = media.Movie("The Bourne Trilogy",
        "https://upload.wikimedia.org/wikipedia/en/a/ae/BourneIdentityfilm.jpg",
        "https://www.youtube.com/watch?v=lYO2Bv_9LA8")

# create a list to be passed as an argument to open_movies_page method

movies = [john_wick, shrek, hulk, world_war_z, robocop, the_bourne_trilogy]

# call open_movies_page function to display the website

fresh_tomatoes.open_movies_page(movies)
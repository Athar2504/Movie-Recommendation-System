import csv
import statistics
from typing import List, Dict, Tuple

class MovieRecommendationSystem:
    """A simple movie recommendation system using CSV data."""
    
    def __init__(self, csv_file: str = 'movies.csv'):
        """Initialize the system with movie data from CSV."""
        self.movies = []
        self.csv_file = csv_file
        
    def create_sample_csv(self):
        """Create a sample CSV file with movie data if it doesn't exist."""
        sample_movies = [
            ['Title', 'Genre', 'Rating', 'Year', 'Director'],
            ['The Shawshank Redemption', 'Drama', '9.3', '1994', 'Frank Darabont'],
            ['The Godfather', 'Crime', '9.2', '1972', 'Francis Ford Coppola'],
            ['The Dark Knight', 'Action', '9.0', '2008', 'Christopher Nolan'],
            ['Pulp Fiction', 'Crime', '8.9', '1994', 'Quentin Tarantino'],
            ['Forrest Gump', 'Drama', '8.8', '1994', 'Robert Zemeckis'],
            ['Inception', 'Sci-Fi', '8.8', '2010', 'Christopher Nolan'],
            ['The Matrix', 'Sci-Fi', '8.7', '1999', 'Wachowski Brothers'],
            ['Goodfellas', 'Crime', '8.7', '1990', 'Martin Scorsese'],
            ['The Silence of the Lambs', 'Thriller', '8.6', '1991', 'Jonathan Demme'],
            ['Saving Private Ryan', 'War', '8.6', '1998', 'Steven Spielberg'],
            ['Spirited Away', 'Animation', '8.6', '2001', 'Hayao Miyazaki'],
            ['The Green Mile', 'Drama', '8.6', '1999', 'Frank Darabont'],
            ['Interstellar', 'Sci-Fi', '8.6', '2014', 'Christopher Nolan'],
            ['Parasite', 'Thriller', '8.5', '2019', 'Bong Joon-ho'],
            ['The Lion King', 'Animation', '8.5', '1994', 'Roger Allers'],
            ['Back to the Future', 'Sci-Fi', '8.5', '1985', 'Robert Zemeckis'],
            ['The Prestige', 'Mystery', '8.5', '2006', 'Christopher Nolan'],
            ['Whiplash', 'Drama', '8.5', '2014', 'Damien Chazelle'],
            ['The Usual Suspects', 'Crime', '8.5', '1995', 'Bryan Singer'],
            ['Toy Story', 'Animation', '8.3', '1995', 'John Lasseter'],
            ['Joker', 'Crime', '8.4', '2019', 'Todd Phillips'],
            ['Avengers: Endgame', 'Action', '8.4', '2019', 'Russo Brothers'],
            ['Spider-Man: Into the Spider-Verse', 'Animation', '8.4', '2018', 'Peter Ramsey'],
            ['The Departed', 'Crime', '8.5', '2006', 'Martin Scorsese'],
            ['Gladiator', 'Action', '8.5', '2000', 'Ridley Scott']
        ]
        
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(sample_movies)
            print(f"✓ Sample CSV file '{self.csv_file}' created successfully!")
            return True
        except Exception as e:
            print(f"✗ Error creating CSV file: {e}")
            return False
    
    def load_movies(self) -> bool:
        """Load movies from CSV file into memory."""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.movies = [row for row in reader]
                
            # Convert rating to float and year to int for proper sorting
            for movie in self.movies:
                movie['Rating'] = float(movie['Rating'])
                movie['Year'] = int(movie['Year'])
                
            print(f"✓ Loaded {len(self.movies)} movies successfully!")
            return True
        except FileNotFoundError:
            print(f"✗ File '{self.csv_file}' not found. Creating sample file...")
            if self.create_sample_csv():
                return self.load_movies()
            return False
        except Exception as e:
            print(f"✗ Error loading movies: {e}")
            return False
    
    def get_unique_genres(self) -> List[str]:
        """Get list of unique genres from the movie collection."""
        genres = set(movie['Genre'] for movie in self.movies)
        return sorted(list(genres))
    
    def filter_by_genre(self, genre: str) -> List[Dict]:
        """Filter movies by genre."""
        return [m for m in self.movies if m['Genre'].lower() == genre.lower()]
    
    def filter_by_year_range(self, start_year: int, end_year: int) -> List[Dict]:
        """Filter movies by year range."""
        return [m for m in self.movies if start_year <= m['Year'] <= end_year]
    
    def filter_by_min_rating(self, min_rating: float) -> List[Dict]:
        """Filter movies with rating >= min_rating."""
        return [m for m in self.movies if m['Rating'] >= min_rating]
    
    def get_top_movies(self, n: int = 5, genre: str = None) -> List[Dict]:
        """Get top N movies overall or by genre."""
        movies_to_sort = self.movies if not genre else self.filter_by_genre(genre)
        sorted_movies = sorted(movies_to_sort, key=lambda x: x['Rating'], reverse=True)
        return sorted_movies[:n]
    
    def recommend_movies(self, preferences: Dict) -> List[Dict]:
        """Recommend movies based on user preferences."""
        filtered_movies = self.movies.copy()
        
        # Apply filters based on preferences
        if 'genre' in preferences and preferences['genre']:
            filtered_movies = [m for m in filtered_movies 
                             if m['Genre'].lower() == preferences['genre'].lower()]
        
        if 'min_rating' in preferences and preferences['min_rating']:
            filtered_movies = [m for m in filtered_movies 
                             if m['Rating'] >= preferences['min_rating']]
        
        if 'year_from' in preferences and preferences['year_from']:
            filtered_movies = [m for m in filtered_movies 
                             if m['Year'] >= preferences['year_from']]
        
        if 'year_to' in preferences and preferences['year_to']:
            filtered_movies = [m for m in filtered_movies 
                             if m['Year'] <= preferences['year_to']]
        
        # Sort by rating and return top 5
        sorted_movies = sorted(filtered_movies, key=lambda x: x['Rating'], reverse=True)
        return sorted_movies[:5]
    
    def get_statistics(self) -> Dict:
        """Calculate various statistics about the movie collection."""
        stats = {}
        
        # Overall statistics
        ratings = [m['Rating'] for m in self.movies]
        stats['total_movies'] = len(self.movies)
        stats['average_rating'] = round(statistics.mean(ratings), 2)
        stats['highest_rated'] = max(self.movies, key=lambda x: x['Rating'])
        stats['lowest_rated'] = min(self.movies, key=lambda x: x['Rating'])
        
        # Genre statistics
        genre_stats = {}
        for genre in self.get_unique_genres():
            genre_movies = self.filter_by_genre(genre)
            if genre_movies:
                genre_ratings = [m['Rating'] for m in genre_movies]
                genre_stats[genre] = {
                    'count': len(genre_movies),
                    'avg_rating': round(statistics.mean(genre_ratings), 2)
                }
        stats['genre_statistics'] = genre_stats
        
        # Year statistics
        years = [m['Year'] for m in self.movies]
        stats['oldest_movie'] = min(self.movies, key=lambda x: x['Year'])
        stats['newest_movie'] = max(self.movies, key=lambda x: x['Year'])
        
        return stats
    
    def display_movie(self, movie: Dict):
        """Display a single movie in formatted way."""
        print(f"  • {movie['Title']} ({movie['Year']})")
        print(f"    Genre: {movie['Genre']} | Rating: {movie['Rating']}/10 | Director: {movie['Director']}")
    
    def display_movies(self, movies: List[Dict], title: str = "Movies"):
        """Display a list of movies in formatted way."""
        if not movies:
            print(f"\n{title}: No movies found matching criteria.")
            return
        
        print(f"\n{title} ({len(movies)} found):")
        print("-" * 60)
        for i, movie in enumerate(movies, 1):
            print(f"{i}. {movie['Title']} ({movie['Year']})")
            print(f"   Genre: {movie['Genre']} | Rating: {movie['Rating']}/10")
            print(f"   Director: {movie['Director']}")
            if i < len(movies):
                print()
    
    def display_statistics(self, stats: Dict):
        """Display statistics in formatted way."""
        print("\n" + "="*60)
        print("MOVIE DATABASE STATISTICS")
        print("="*60)
        
        print(f"\n📊 Overall Statistics:")
        print(f"  • Total Movies: {stats['total_movies']}")
        print(f"  • Average Rating: {stats['average_rating']}/10")
        print(f"  • Highest Rated: {stats['highest_rated']['Title']} ({stats['highest_rated']['Rating']}/10)")
        print(f"  • Lowest Rated: {stats['lowest_rated']['Title']} ({stats['lowest_rated']['Rating']}/10)")
        print(f"  • Oldest Movie: {stats['oldest_movie']['Title']} ({stats['oldest_movie']['Year']})")
        print(f"  • Newest Movie: {stats['newest_movie']['Title']} ({stats['newest_movie']['Year']})")
        
        print(f"\n📈 Genre Analysis:")
        for genre, info in stats['genre_statistics'].items():
            print(f"  • {genre}: {info['count']} movies, avg rating: {info['avg_rating']}/10")


def main():
    """Main function to run the movie recommendation system."""
    system = MovieRecommendationSystem()
    
    # Load movies from CSV
    if not system.load_movies():
        print("Failed to load movies. Exiting...")
        return
    
    print("\n" + "="*60)
    print("🎬 WELCOME TO MOVIE RECOMMENDATION SYSTEM 🎬")
    print("="*60)
    
    while True:
        print("\n📋 MAIN MENU:")
        print("1. Search movies by genre")
        print("2. Search movies by year range")
        print("3. Search movies by minimum rating")
        print("4. Get personalized recommendations")
        print("5. View top 5 movies (overall or by genre)")
        print("6. View statistics")
        print("7. View all genres")
        print("8. Exit")
        
        choice = input("\n👉 Enter your choice (1-8): ").strip()
        
        if choice == '1':
            # Search by genre
            genres = system.get_unique_genres()
            print("\nAvailable genres:", ", ".join(genres))
            genre = input("Enter genre: ").strip()
            movies = system.filter_by_genre(genre)
            system.display_movies(movies, f"Movies in {genre} genre")
            
        elif choice == '2':
            # Search by year range
            try:
                start = int(input("Enter start year: ").strip())
                end = int(input("Enter end year: ").strip())
                movies = system.filter_by_year_range(start, end)
                system.display_movies(movies, f"Movies from {start} to {end}")
            except ValueError:
                print("✗ Invalid year input. Please enter numbers only.")
                
        elif choice == '3':
            # Search by minimum rating
            try:
                min_rating = float(input("Enter minimum rating (0-10): ").strip())
                movies = system.filter_by_min_rating(min_rating)
                system.display_movies(movies, f"Movies with rating >= {min_rating}")
            except ValueError:
                print("✗ Invalid rating input. Please enter a number.")
                
        elif choice == '4':
            # Get personalized recommendations
            print("\n🎯 PERSONALIZED RECOMMENDATIONS")
            print("(Press Enter to skip any criterion)")
            
            preferences = {}
            
            # Genre preference
            genres = system.get_unique_genres()
            print(f"\nAvailable genres: {', '.join(genres)}")
            genre_input = input("Preferred genre: ").strip()
            if genre_input:
                preferences['genre'] = genre_input
            
            # Rating preference
            rating_input = input("Minimum rating (0-10): ").strip()
            if rating_input:
                try:
                    preferences['min_rating'] = float(rating_input)
                except ValueError:
                    print("Invalid rating, skipping...")
            
            # Year preference
            year_from = input("From year: ").strip()
            if year_from:
                try:
                    preferences['year_from'] = int(year_from)
                except ValueError:
                    print("Invalid year, skipping...")
            
            year_to = input("To year: ").strip()
            if year_to:
                try:
                    preferences['year_to'] = int(year_to)
                except ValueError:
                    print("Invalid year, skipping...")
            
            recommendations = system.recommend_movies(preferences)
            system.display_movies(recommendations, "🌟 Recommended Movies for You")
            
        elif choice == '5':
            # View top 5 movies
            print("\n1. Top 5 overall")
            print("2. Top 5 by genre")
            sub_choice = input("Choose (1 or 2): ").strip()
            
            if sub_choice == '1':
                movies = system.get_top_movies(5)
                system.display_movies(movies, "🏆 Top 5 Movies Overall")
            elif sub_choice == '2':
                genres = system.get_unique_genres()
                print("\nAvailable genres:", ", ".join(genres))
                genre = input("Enter genre: ").strip()
                movies = system.get_top_movies(5, genre)
                system.display_movies(movies, f"🏆 Top 5 {genre} Movies")
            else:
                print("✗ Invalid choice.")
                
        elif choice == '6':
            # View statistics
            stats = system.get_statistics()
            system.display_statistics(stats)
            
        elif choice == '7':
            # View all genres
            genres = system.get_unique_genres()
            print("\n📚 Available Genres:")
            for i, genre in enumerate(genres, 1):
                count = len(system.filter_by_genre(genre))
                print(f"  {i}. {genre} ({count} movies)")
                
        elif choice == '8':
            # Exit
            print("\n👋 Thank you for using Movie Recommendation System!")
            print("🎬 Happy watching!")
            break
            
        else:
            print("✗ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
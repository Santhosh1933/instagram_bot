import random
import cloudinary
import cloudinary.uploader
from flashcard_generator import FlashcardGenerator
from instagram_uploader import InstagramUploader
from constants import API_KEY, ACCESS_TOKEN, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, BUSINESS_ACCOUNT_ID

# Configure Cloudinary
cloudinary.config(
    cloud_name="dplmrowbo",
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

TOPICS = [
    "Recursion", "Big O Notation", "Binary Search", "Linked List", "Stack",
    "Queue", "Hash Table", "Graph Traversal", "Depth First Search", "Breadth First Search",
    "Sorting Algorithms", "Merge Sort", "Quick Sort", "Bubble Sort", "Dynamic Programming",
    "Memoization", "Backtracking", "Object-Oriented Programming", "Encapsulation", "Polymorphism",
    "Inheritance", "Abstraction", "Design Patterns", "Singleton Pattern", "Factory Pattern",
    "Observer Pattern", "Decorator Pattern", "REST API", "GraphQL", "HTTP Methods",
    "JSON Parsing", "Exception Handling", "Multithreading", "Concurrency", "Asynchronous Programming",
    "Promises", "Event Loop", "Closure", "Lambda Functions", "Recursion vs Iteration",
    "Binary Tree", "Binary Search Tree", "Heap", "Priority Queue", "Stack Overflow",
    "Memory Management", "Garbage Collection", "Version Control (Git)", "CI/CD", "Unit Testing",
    "Integration Testing", "Functional Programming", "Immutable Data", "React Hooks", "State Management",
    "Redux", "Context API", "Node.js Event Loop", "Express.js Middleware", "RESTful Routing",
    "HTTP Status Codes", "JWT Authentication", "OAuth 2.0", "WebSockets", "Socket.IO",
    "Database Indexing", "SQL Joins", "NoSQL Databases", "MongoDB Aggregation", "Transactions",
    "ACID Properties", "CAP Theorem", "Docker Containers", "Kubernetes", "Microservices Architecture",
    "Serverless Functions", "AWS Lambda", "Cloud Deployment", "CI Pipelines", "CD Pipelines",
    "Testing Strategies", "Debugging Techniques", "Profiling Code", "Memory Leaks", "Performance Optimization",
    "Front-end Optimization", "Code Refactoring", "Clean Code", "SOLID Principles", "DRY Principle",
    "YAGNI Principle", "Agile Methodology", "Scrum Framework", "Kanban", "Pair Programming",
    "Code Reviews", "Continuous Learning", "Tech Interview Prep", "Algorithm Challenges", "LeetCode Patterns",
    "System Design Basics", "Scalability", "Load Balancing", "Caching Strategies", "CDN Usage"
]

CAPTION = "#ProgrammingFlashcards #DevLife #LearnCoding #StudySmart"

if __name__ == "__main__":
    generator = FlashcardGenerator()
    uploader = InstagramUploader(ACCESS_TOKEN, BUSINESS_ACCOUNT_ID)

    # Step 0: Select random topic
    topic = random.choice(TOPICS)

    # Step 1: Generate flashcard text
    flashcard = generator.generate_flashcard_text(topic)
    print(f"Topic: {flashcard['topic']}")
    print(f"Definition: {flashcard['definition']}")

    # Step 2: Generate flashcard image
    local_file = "flashcard.png"
    try:
        generator.generate_flashcard_image(flashcard, local_file)
        print(f"✅ Flashcard image saved locally: {local_file}")
    except Exception as e:
        print("❌ Failed to generate flashcard image:", e)
        exit(1)

    # Step 3: Upload to Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(local_file, folder="programming_flashcards")
        image_url = upload_result["secure_url"]
        public_id = upload_result["public_id"]
        print(f"✅ Image uploaded to Cloudinary: {image_url}")
    except Exception as e:
        print("❌ Failed to upload image to Cloudinary:", e)
        exit(1)

    # Step 4: Upload to Instagram
    try:
        success = uploader.upload_image(image_url, CAPTION)
        if success:
            print("✅ Flashcard uploaded to Instagram successfully!")

            # Step 5: Delete image from Cloudinary
            try:
                cloudinary.uploader.destroy(public_id)
                print("🗑️ Image deleted from Cloudinary successfully.")
            except Exception as e:
                print("⚠️ Failed to delete image from Cloudinary:", e)

    except Exception as e:
        print("❌ Failed to upload flashcard to Instagram:", e)

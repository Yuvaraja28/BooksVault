import sqlite3

def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to add book data to SQLite3
def add_book(title, image, price, original_price, description, bookStatus, rentalPrice):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create the books table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                image TEXT,
                price REAL,
                original_price REAL,
                description TEXT,
                bookStatus TEXT DEFAULT FALSE,
                rentalPrice REAL
            )
        """)

        sql = "INSERT INTO books (title, image, price, original_price, description, bookStatus, rentalPrice) VALUES (?, ?, ?, ?, ?, ?, ?)"
        val = (title, image, price, original_price, description, bookStatus, rentalPrice)
        cursor.execute(sql, val)

        conn.commit()
        print(f"Book added: {title}")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to SQLite3: {e}")

# Example usage:
# add_book("C Programming Language", "c-programming-language.jpg", 399, 499, "The 'C Programming Language' is a foundational text for learning the C programming language. Written by Dennis Ritchie and Brian Kernighan, this book provides a comprehensive introduction to the language's syntax and structures. It covers core topics such as data types, operators, control flow, functions, pointers, memory management, and more. This book is ideal for beginners and intermediate programmers looking to understand the inner workings of computer systems and programming.", 'rental', 39)
# add_book("Computer Networks", "computer-networks.jpg", 549, 699, "The 'Computer Networks' book offers an in-depth exploration of the theory and practice behind computer networking. It covers essential topics such as the OSI model, TCP/IP protocols, routing, switching, network security, and wireless communication. The book is designed for students and professionals who want to develop a solid understanding of how networks function, how data is transmitted, and how different devices and protocols interact in real-world network systems.", 'new', 39)
# add_book("Data Structures", "data-structures.jpg", 649, 799, "The 'Data Structures' book is a comprehensive guide to understanding and implementing various data structures essential for efficient programming. It covers fundamental topics like arrays, linked lists, stacks, queues, trees, graphs, and hash tables. The book also explains the importance of choosing the right data structure for specific tasks and provides practical examples of how these structures are used in algorithm design and optimization.", 'second', 39)
# add_book("Digital Electronics", "digital-electronics.jpg", 549, 699, "The 'Digital Electronics' book provides a solid foundation in the principles and applications of digital circuits. It explains concepts such as Boolean algebra, logic gates, flip-flops, multiplexers, and memory units. This book is designed for students studying electronics, offering hands-on experiments and practical applications that help understand how digital electronics power modern computing and communication devices.", 'new', 39)
# add_book("Discrete Mathematics", "discrete-mathematics.jpg", 749, 899, "The 'Discrete Mathematics' book is a comprehensive resource for learning the principles of mathematics used in computer science and related fields. It covers topics like set theory, combinatorics, graph theory, logic, number theory, and algorithms. This book emphasizes problem-solving and proofs, helping students build the logical and mathematical reasoning skills needed for computer science, cryptography, and algorithm design.", 'second', 39)
# add_book("Java", "java.jpg", 649, 799, "The 'Java' book serves as an essential guide for learning the Java programming language. It covers the basics of object-oriented programming, including classes, inheritance, polymorphism, and interfaces. The book goes beyond the fundamentals, exploring advanced topics such as multithreading, exception handling, and the Java API. It is perfect for both beginners and experienced programmers seeking to master Java for developing cross-platform applications, web services, and mobile apps.", 'new', 39)
# add_book("Python Programming", "python-programming.jpg", 549, 699, "The 'Python Programming' book is an excellent introduction to programming using Python. It provides a clear and practical guide to the language's syntax and structure, covering topics such as data types, control structures, functions, and modules. The book also delves into more advanced topics like file handling, object-oriented programming, and web scraping. Python's versatility makes it ideal for a variety of applications, including web development, data analysis, and artificial intelligence.", 'rental', 39)
# add_book("Software Engineering", "software-engineering.jpg", 799, 999, "The 'Software Engineering' book offers a comprehensive guide to the principles and practices involved in developing high-quality software. It covers essential topics such as requirements analysis, system design, testing, debugging, and software project management. The book also explores modern software development methodologies like Agile and DevOps, equipping students and professionals with the knowledge needed to design, implement, and maintain complex software systems.", 'second', 39)
# add_book("Web Technologies", "web-technologies.jpg", 649, 799, "The 'Web Technologies' book provides a detailed overview of the tools and technologies used to develop dynamic and interactive websites. It covers essential web technologies like HTML, CSS, JavaScript, and modern frameworks like React and Angular. The book also explores backend technologies such as Node.js and databases, offering readers a complete understanding of both front-end and back-end development. Ideal for aspiring web developers, this book teaches how to create fully functional, responsive websites and web applications.", 'new', 39)
# add_book("Introduction to IOT", "introductions-iot.jpg", 649, 799, "IoT enables the transfer of data packets over a connected network, which can save time and money. Predictive maintenance in industrial settings is another good example of this. IoT sensors installed on machinery continuously monitor parameters such as temperature, vibration and operating conditions in real-time.", 'new', 39)

# add_book("Discrete Mathematics with Applications", "discrete-mathemtatics.jpg", 649, 799, "The 'Discrete Mathematics' book is a comprehensive resource for learning the principles of mathematics used in computer science and related fields. It covers topics like set theory, combinatorics, graph theory, logic, number theory, and algorithms. This book emphasizes problem-solving and proofs, helping students build the logical and mathematical reasoning skills needed for computer science, cryptography, and algorithm design", 'second', 39)
# add_book("Software Engineering", "software-engineering-2.jpg", 649, 799, "The 'Software Engineering' book offers a comprehensive guide to the principles and practices involved in developing high-quality software. It covers essential topics such as requirements analysis, system design, testing, debugging, and software project management. The book also explores modern software development methodologies like Agile and DevOps, equipping students and professionals with the knowledge needed to design, implement, and maintain complex software systems", 'second', 39)
# add_book("Data Mining Techniques", "data-mining.jpg", 649, 799, "Introduction to Data Mining presents fundamental concepts and algorithms for those learning data mining for the first time. Each concept is explored thoroughly and supported with numerous examples. Each major topic is organized into two chapters, beginning with basic concepts that provide necessary background for understanding each data mining technique, followed by more advanced concepts and algorithms", 'second', 39)

# add_book("Object Oriented Analysis and Design", "ooad.jpg", 649, 799, "Object-oriented analysis and design (OOAD) is a technical approach for analyzing and designing an application, system, or business by applying object-oriented programming, as well as using visual modeling throughout the software development process to guide stakeholder communication and product quality.", 'rental', 39)
# add_book("Artifical Intelligence - Beginner's Guide", "ai.jpg", 649, 799, "The long-anticipated revision of Artificial Intelligence: A Modern Approach explores the full breadth and depth of the field of artificial intelligence (AI). The 4th Edition brings readers up to date on the latest technologies, presents concepts in a more unified manner, and offers new or expanded coverage of machine learning, deep learning, transfer learning, multiagent systems, robotics, natural language processing, causality, probabilistic programming, privacy, fairness, and safe Al.", 'rental', 39)

dict1 = {"name": "John", "age": 25, "city": "New York"}
dict2 = {1: "apple", 2: "banana", 3: "orange"}
dict3 = {"fruits": ["apple", "banana"], "vegetables": ["carrot", "potato"]}
dict4 = {(1, 2): "pointA", (3, 4): "pointB"}
dict5 = {"id": 101, "data": {"name": "Alice", "grade": "A"}}
dict11 = {"name": "Alice", "age": 30}
dict22 = {1: "one", 2: "two", 3: "three"}
dict33 = {"price": 9.99, "quantity": 5}
dict111 = {(1, 2): "pointA", (3, 4): "pointB"}
dict12 = {"coordinates": (10, 20), "size": (5, 8)}
dict13 = {(0, 0): 0, (1, 1): 1}
dict14 = {"vowels": {"a", "e", "i", "o", "u"}, "odds": {1, 3, 5}}
dict15 = {"team1": {"Alice", "Bob"}, "team2": {"Charlie", "Dave"}}
dict1221 = {1: 10, 2: [20, 30], 3: {40, 50}}
dict221 = {10: {100: 1000}, 20: (200, 300), 30: 400}
dict333 = {5: [50, 60, 70], 10: 100, 15: {150: [1500, 15000]}}
dictnums = {"one":1, "two":2,"three":3, "five":5, "four":4}



# Import the 'operator' module, which provides functions for common operations like sorting.
import operator

# Create a dictionary 'd' with key-value pairs.
d = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}

d.update({2:33})

print(d)

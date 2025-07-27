import pandas as pd; 

test_book_list = []

test_book_list.append(
    {        
        "name" : "Subtle Art of Not Giving A Fuck",
        "year": "2019",
        "id" : "dauwdwyiad",
        "author" : "Shad",
        "availability" : "AVAILABLE"
    }
)

df = pd.DataFrame(test_book_list)
df.to_csv("./booklist.csv", index = False)
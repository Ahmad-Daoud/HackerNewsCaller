import requests
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()
output_file = "output/" + str(input("Please enter the output file name: ")+ ".txt")
keywords = []
while True:
    resp = input("Would you like to manually enter keywords or use a keyword file? (in src folder) (Manually/File) : ")
    if resp == "Manually":
        while True:
            clear()
            keywords.append(str(input("Please enter the keyword you want to search: ")))
            print("Do you want to add more keywords? (y/n)")
            if str(input()) == 'n':
                break
        break
    elif resp == "File":
        try:
            file_name = str(input("Please enter the file name: "))
            with open("src/Keyword_Files/" + file_name + ".txt", "r") as file:
                for line in file:
                    keywords.append(line.strip())
            break
        except FileNotFoundError:
            clear()
            print("File not found. Please try again.")
    else:
        clear()
        print("Invalid input. Please try again.")
clear()
print("Would you like to search for the top stories or the new stories? (Top/New)")
while True:
    resp = str(input())
    if resp == "Top":
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        break
    elif resp == "New":
        url = "https://hacker-news.firebaseio.com/v0/newstories.json"
        break
    else:
        clear()
        print("Invalid input. Please try again.")
clear()
max_stories = int(input("Please enter the number of stories you want to search (max 500): "))
numStories = 0
try:
    response = requests.get(url)
    response.raise_for_status()
    top_story_ids = response.json()
    i=0
    with open(output_file, "w") as file:
        for story_id in top_story_ids:
            i+=1
            if i>max_stories:
                break
            print("Story : ",i)
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url)
            story_response.raise_for_status()
            story_data = story_response.json()
            for keyword in keywords:
                if keyword.lower() in story_data.get("title").lower() and story_data.get("url") is not None and story_data.get("title") is not None: 
                    file.write("Title : " + story_data.get("title") + " url : " +story_data.get("url") + "\n")
                    numStories+=1
                    break
    if numStories == 0:
        print("No entries found with the given keyword")
        # Delete file
        os.remove(output_file)
    else:
        print(numStories, " entries written to file: ",output_file)

except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching entries : {e}")
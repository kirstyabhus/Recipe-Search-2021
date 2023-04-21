import requests


# Function to make a request to the Edamam API w/ the required ingredient as search query, to find recipes for
# the input ingredient
def ingr_search():
    app_key = 'a28413f876f1d5d0b52d989a87344cc2'
    app_ID = '6468363d'

    # ask user for the ingredient to search for
    global ingr
    ingr = input("\nWhat ingredient do you want to search for? ")

    # Error checks, to ensure that input is longer than 2 characters & only contains letters
    while len(ingr) <= 2 or not (ingr.isalpha()):
        print("Invalid. Please Try again.")
        ingr = input("What ingredient do you want to search for? ")

    # the different meal types in the API
    meal_types = ["breakfast", "lunch", "dinner", "snack", "teatime"]

    # asks the user which meal type they would like to see
    global meal_type_option
    meal_type_option = input(
        "What type of meal would you like to see recipes for? breakfast, lunch, dinner, snack, teatime or any? ").lower()

    # a variable to track whether the user made a meal type option (0 = no choice made, 1 = a choice was made)
    global type_chosen
    type_chosen = False

    # if the user has chosen a meal type from the list, search for recipes of their ingredient AND meal type.
    if meal_type_option in meal_types:
        url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}&mealType={}'.format(ingr, app_ID, app_key,
                                                                                           meal_type_option.title())
        type_chosen = True
    else:
        # otherwise, find recipes with the ingredient anf ANY meal type
        url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(ingr, app_ID, app_key)

    result = requests.get(url)

    # make the recipe variable global, so it can be used outside the function
    data = result.json()

    # return the recipes w/ their details
    return data["hits"]


# function to print a numbered list of recipe names, based on the ingredient the user entered
def recipe_list(recipes):
    # find the number of "hits" aka the number of recipes found for the chosen ingredient/ ingredient + meal type
    length = len(recipes)

    # if the user made an earlier choice on the TYPE of recipe they want to see, display the type in the heading
    if type_chosen:
        print(f"\nHere are some {meal_type_option} recipes...")
    else:
        # if the user did not choose a meal type, just display a heading without a meal type
        print(f"\nHere are some recipes...")

    # run through all the recipes of the chosen ingredient
    for i in range(length):
        # store the name of the current recipe
        name = recipes[i]["recipe"]["label"]
        # add the current recipe name to the list
        # print out the recipe name and list number
        print(f"{i + 1}. {name}")


# A function to ask the user to choose a recipe, and to output the recipes' ingredient list
def get_recipe(recipes):
    # Ask the user which recipe option they would like to see
    user_option = int(input("\nWhich recipe would you like to see the details for? Enter the number: ")) - 1

    # store the recipe name
    user_recipe = recipes[user_option]["recipe"]["label"]

    # find the number of ingredients in the recipes' ingredient list
    ingr_len = len(recipes[user_option]["recipe"]["ingredientLines"])

    print(f"\nINGREDIENTS for {user_recipe}")

    # iterate through each ingredient of the recipes' ingredient list
    for x in range(ingr_len):
        # print out each ingredient line of the users' recipe
        print(recipes[user_option]["recipe"]["ingredientLines"][x])

    # the name of the website source for the recipes' preparation
    source = recipes[user_option]["recipe"]['source']

    # print the link for the preparation method
    print(f"\nThe method for preparing {user_recipe} can be found at the '{source}' website with the link below:")
    prep_url = recipes[user_option]["recipe"]["url"]
    print(prep_url)

    # Write the recipe name and its link to a text file. This stores the history of recently searched recipes.
    f = open("history.txt", "a")
    f.write(f"{user_recipe}\n{prep_url}\n\n")
    f.close()


# Function to run the whole code, putting all the functions together.
def run():
    # run the function to get the recipes for the users' input ingredient
    recipes = ingr_search()

    # run the function to print a numbered list of the users' input ingredients
    recipe_list(recipes)

    # run the function to ask the user to choose a recipe, and to output the recipes' ingredient list
    get_recipe(recipes)

    option = input("\nWhat would you like to do next? (1 or 2) \n1. Search for another ingredient \n2. Exit\n")

    # if they want to search for another ingredient, run the run function again
    if option == "1":
        run()
    else:
        print("\nProgram End.")


run()

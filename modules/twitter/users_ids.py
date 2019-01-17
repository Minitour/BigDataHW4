import json
import requests
import requests_oauthlib
import csv


CONSUMER_KEY = 'owJ9m2q48GGYrMubsOSEyZbap'
CONSUMER_SECRET = 'LQNlKSk7azipU1lIA2znEkQSwsGkTswhRheP0S2RbHLioW8HJt'
ACCESS_TOKEN = '1053037342867554304-4QmY7LgUp0N5f9Jof1suuKf3LmE09h'
ACCESS_SECRET = '14YaQqTDjwmzUfALLhtuzJw1ibLehe6NbtlbdtAJiXOea'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)


def get_users_usernames():

    usernames = []
    with open("output.csv") as file:
        csv_reader = csv.reader(file, delimiter=',')

        head = True
        for row in csv_reader:
            # if we are at first row -> the title (Username)
            if head:
                head = False
                continue

            usernames.append(row[2])

    return usernames


def get_users_ids(usernames):
    #print(len(usernames))   ---> we have here 499 users
    ids = []
    number_of_loops = int(len(usernames) / 100) + 1  # got 4 after division + 1 for the 99 users left

    start_at = 0    # will iterate: 0-99, 100-199, 200-299, 300-399, 400-499

    for i in range(0, number_of_loops):

        try:
            # construct the url
            url = 'https://api.twitter.com/1.1/users/lookup.json?screen_name=' + get_users_as_string(usernames[start_at: start_at + 99])
            print ("getting users between (" + str(start_at) + ", " + str(start_at + 99) + ")")
            # getting the response
            response = requests.get(url, auth=my_auth, stream=True)

            # parsing the data
            data = json.loads(response.text)

            # appending only the ids of the users

            for d in data:
                ids.append(str(d['id']))

        except requests.HTTPError as error:
            # try again
            i -= 1
            continue

        # adjust the start at point
        start_at += 100

    return ids


def get_users_as_string(users):

    final_str = ""

    index = 0

    for user in users:
        if index != len(users) - 1:
            final_str += user + ","
        else:
            final_str += user
        index += 1

    return final_str


def main():
    usernames = get_users_usernames()

    ids = get_users_ids(usernames)

    print(ids)


if __name__ == "__main__":
    main()
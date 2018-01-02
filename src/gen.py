#!/usr/bin/env python3

# Generate test registration data to import in to the KumoReg database. Fakes the
# attendee data exported from the website (people who have pre-registered online)

from faker import name, internet, address, phone_number
import datetime
import random
import hashlib
import sys
import json


def get_badge_name():
    n = internet.user_name()[0:15]
    n = n.replace('-', ' ')
    n = n.replace('.', ' ')
    n = n.replace('_', ' ')
    return n


def generate_birthday():
    b_year = random.randint(1940, 2014)
    b_month = random.randint(1, 12)
    b_day = random.randint(1, 28)
    return datetime.datetime(b_year, b_month, b_day)


if __name__ == '__main__':
    rows = 10000
    if len(sys.argv) == 2:
        if sys.argv[1] in ('-h', '-?', '/?', '/h', '--help'):
            print("Prints example data to stdout")
            print("Usage:")
            print("    gen.py <number of rows>")
            print("")
            sys.exit(0)
        else:
            rows = int(sys.argv[1])

    output = []

    order_id = 1
    for i in range(rows):
        birth_date = generate_birthday()
        age = datetime.datetime.now() - birth_date
        age = int(age.days / 365.25)            # Not the right way to calculate age, but close enough

        attendee = {'firstName': name.first_name(), 'lastName': name.last_name()}

        if random.randint(1, 100) < 10:         # random chance of having a legal name
            attendee['firstNameOnId'] = name.first_name()
            attendee['lastNameOnId'] = name.last_name()
            attendee['nameOnIdIsPreferredName'] = False
        else:
            attendee['firstNameOnId'] = attendee['firstName']
            attendee['lastNameOnId'] = attendee['lastName']
            attendee['nameOnIdIsPreferredName'] = True

        if random.randint(1, 100) < 60:         # Random chance of having a badge name
            attendee['fanName'] = get_badge_name()
        else:
            attendee['fanName'] = ""

        attendee['postal'] = address.zip_code()
        attendee['country'] = "United States of America"

        attendee['phone'] = phone_number.phone_number()
        attendee['email'] = internet.email()
        attendee['birthdate'] = "{0:4d}-{1:02d}-{2:02d}".format(birth_date.year, birth_date.month, birth_date.day)

        attendee['emergencyName'] = name.find_name()
        attendee['emergencyPhone'] = phone_number.phone_number()

        if age <= 17:
            attendee['parentName'] = attendee['emergencyName']
            attendee['parentPhone'] = attendee['emergencyPhone']
            attendee['emergencyContactSameAsParent'] = True
        else:
            attendee['parentName'] = ""
            attendee['parentPhone'] = ""
            attendee['emergencyContactSameAsParent'] = False

        if age >= 13:
            attendee['amountPaidInCents'] = str(random.choice([4500, 5000, 5500, 5700]))    # 13+ full price
        elif 6 >= age < 13:
            attendee['amountPaidInCents'] = "4500"    # 13+ full price
        else:
            attendee['amountPaidInCents'] = "0"

        attendee['vipTShirtSize'] = ''

        random_badge = random.randint(1, 1000)
        if random_badge < 2:      # Random chance of VIP membership
            attendee['membershipType'] = "VIP"
            attendee['amountPaidInCents'] = "30000"
            attendee['vipTShirtSize'] = random.choice(['S', 'M', 'L', 'XL'])
        elif random_badge < 10:
            attendee['membershipType'] = "Artist"
            attendee['amountPaidInCents'] = "5000"
        elif random_badge < 20:
            attendee['membershipType'] = "Exhibitor"
            attendee['amountPaidInCents'] = "2500"
        elif random_badge < 25:
            attendee['membershipType'] = "Guest"
            attendee['amountPaidInCents'] = "0"
        elif random_badge < 26:
            attendee['membershipType'] = "Emerging Press"
            attendee['amountPaidInCents'] = "0"
        elif random_badge < 29:
            attendee['membershipType'] = "Standard Press"
            attendee['amountPaidInCents'] = "0"
        elif random_badge < 35:
            attendee['membershipType'] = "Industry"
            attendee['amountPaidInCents'] = "0"
        elif random_badge < 43:
            attendee['membershipType'] = "Panelist"
            attendee['amountPaidInCents'] = "0"
        else:
            attendee['membershipType'] = "Weekend"

        attendee['notes'] = ''

        attendee['orderId'] = hashlib.md5(str(order_id).encode('utf-8')).hexdigest()

        output.append(attendee)

        if random.randint(1, 100) < 65:
            order_id += 1

    print(json.dumps(output))

    # print(len(output))
    #
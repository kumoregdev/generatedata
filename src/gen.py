#!/usr/bin/env python3

# Generate test registration data to import in to the KumoReg database. Fakes the
# attendee data exported from the website (people who have pre-registered online)

from faker import name, internet, address, phone_number
import datetime
import random
import hashlib
import sys


def get_badge_name():
    n = internet.user_name()[0:15]
    n = n.replace('-', ' ')
    n = n.replace('.', ' ')
    n = n.replace('_', ' ')
    return n

fields = ['First Name', 'Last Name', 'Legal First Name', 'Legal Last Name', 'Badge Name', 'Badge Number', 'Zipcode',
          'Country', 'Phone Number', 'Email Address', 'Birthdate', 'Emergency Contact Name',
          'Emergency Contact Phone', 'Parent is Emergency Contact', 'Parent Name', 'Parent Phone',
          'Paid', 'Amount', 'Pass Type', 'Order ID']


def print_header():
    print('\t'.join(fields))


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

    print_header()

    order_id = 1
    for i in range(rows):
        birth_date = generate_birthday()
        age = datetime.datetime.now() - birth_date
        age = int(age.days / 365.25)            # Not the right way to calculate age, but close enough

        data = [name.first_name(), name.last_name()]
        if random.randint(1, 100) < 10:         # random chance of having a legal name
            data.append(name.first_name())
            data.append(name.last_name())
        else:
            data.append("")
            data.append("")

        if random.randint(1, 100) < 60:         # Random chance of having a badge name
            data.append(get_badge_name())
        else:
            data.append("")
        data.append("ONL{0:05d}".format(i))
        data.append(address.zip_code())
        data.append("United States of America")

        data.append(phone_number.phone_number())
        data.append(internet.email())
        data.append("{0:4d}-{1:02d}-{2:02d}".format(birth_date.year, birth_date.month, birth_date.day))
        data.append(name.find_name())

        data.append(phone_number.phone_number())
        if age <= 17:
            data.append('Y')
            data.append(data[11])
            data.append(data[12])
        else:
            data.append('N')
            data.append("")
            data.append("")
        data.append("Y")
        if age >= 13:
            data.append(str(random.choice([45, 50, 55, 57])))    # 13+ full price
        elif 6 >= age < 13:
            data.append("45")     # Youth
        else:
            data.append("0")      # Children are free

        random_badge = random.randint(1, 1000)
        if random_badge < 2:      # Random chance of VIP membership
            data.append('VIP')
            data[17] = "300"
        elif random_badge < 10:
            data.append("Artist")
            data[17] = 50
        elif random_badge < 20:
            data.append("Exhibitor")
            data[17] = 25
        elif random_badge < 25:
            data.append("Guest")
            data[17] = 0
        elif random_badge < 26:
            data.append("Emerging Press")
            data[17] = 0
        elif random_badge < 29:
            data.append("Standard Press")
            data[17] = 0
        elif random_badge < 35:
            data.append("Industry")
            data[17] = 0
        elif random_badge < 43:
            data.append("Panelist")
            data[17] = 0
        else:
            data.append('Weekend')
        data.append(hashlib.md5(str(order_id).encode('utf-8')).hexdigest())

        data = [str(i) for i in data]
        print('\t'.join(data))

        if random.randint(1, 100) < 65:
            order_id += 1
from tlo_my_address_parser import MalaysianAddressParser

myAddressParser = MalaysianAddressParser()


# Parsing one Address

result = myAddressParser.parser("1-6-6, Icon Residenz, Jalan SS 8/2, Sungei Way, 47300 Petaling Jaya")

print(result)


# Parsing List of Addresses

result = myAddressParser.parser(
    ["1-6-6, Icon Residenz, Jalan SS 8/2, Sungei Way, 47300 Petaling Jaya",
     "A-1-2, Riana Green Condominium, Jalan Tropicana Utara, PJU 3, 47410, Petaling Jaya, Selangor"]
)

print(result)

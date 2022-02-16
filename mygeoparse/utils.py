import pandas as pd
import re
import spacy

from re import search

nlp = spacy.load('mygeoparse/ner/model')


def load_postcode_dataframe():
    df_postcode_my = pd.read_csv("mygeoparse/data/postcode_my.csv")
    df_postcode_my['Location'] = df_postcode_my['Location'].str.upper()
    df_postcode_my['Post_Office'] = df_postcode_my['Post_Office'].str.upper()
    df_postcode_my['Postcode'] = df_postcode_my['Postcode'].str.upper()
    df_postcode_my['State'] = df_postcode_my['State'].str.upper()
    return df_postcode_my


def clean_postcodes(p):
    if len(p) > 1:
        postal_code = p[1]
    elif len(p) == 0:
        postal_code = 'N/A'
    else:
        postal_code = p[0]

    return postal_code


def find_missing_postcode(df_cleaned_address_list):
    for index, row in df_cleaned_address_list.iterrows():
        if row['postcode'] == 'N/A':
            street = row['street_name']
            pattern = "\d{5}"
            p_code = re.findall(pattern, street)
            postal_code = clean_postcodes(p_code)
            df_cleaned_address_list.loc[index, 'postcode'] = postal_code

    return df_cleaned_address_list


def find_missing_state(df_cleaned_address_list):
    df_microdb = load_postcode_dataframe()
    for index, row in df_cleaned_address_list.iterrows():
        if row['state'] == 'N/A':
            p_code = row['postcode']

            if p_code != 'N/A':
                df = df_microdb[df_microdb['Postcode'] == p_code]
                lst_state = df['State']

                if len(lst_state) != 0:
                    df_cleaned_address_list.loc[index, 'state'] = lst_state.iloc[0]
    return df_cleaned_address_list


def find_missing_city(df_cleaned_address_list):
    df_microdb = load_postcode_dataframe()
    for index, row in df_cleaned_address_list.iterrows():
        if row['city'] == 'N/A':
            p_code = row['postcode']

            if p_code != 'N/A':
                df = df_microdb[df_microdb['Postcode'] == p_code]
                lst_city = df['Post_Office']

                if len(lst_city) != 0:
                    df_cleaned_address_list.loc[index, 'city'] = lst_city.iloc[0]
    return df_cleaned_address_list


def split_house_address_and_street(address):
    address_keywords = ['JALAN', 'TAMAN', 'LORONG', 'KAWASAN', 'PERSIARAN', 'FLAT',
                        'PANGSAPURI', 'DOMAIN']
    index = 0
    location = 0
    check = False
    for word in address:

        for key in address_keywords:
            if search(key, word):
                check = True
                break
            else:
                check = False
        if check:
            location = index
            break

        else:
            location = 0
            check = False

        index = index + 1

    return location


def remove_city(token, city_list):
    found_city = False
    for i in city_list:
        if i == token:
            found_city = True
            break
        else:
            found_city = False
    return found_city


def remove_state(token, state_list):
    found_state = False
    for i in state_list:
        if i == token:
            found_state = True
            break
        else:
            found_state = False
    return found_state


def remove_country(token, country_list):
    found_country = False
    for i in country_list:
        if i == token:
            found_country = True
            break
        else:
            found_country = False
    return found_country


def remove_postcodes(token, postcode_list):
    found_postcode = False
    for i in postcode_list:
        if i == token:
            found_postcode = True
            break
        else:
            found_postcode = False
    return found_postcode


def find_missing_address_parts(df):
    df_bjobs_new = find_missing_postcode(df)
    df_bjobs_new = find_missing_city(df_bjobs_new)
    df_bjobs_new = find_missing_state(df_bjobs_new)

    # print('Pre-process 2 - Fill in missing values with existing data... Success')
    # print('Preprocessing Stage 2... Success')
    return df_bjobs_new


def parse_one_address(address):
    df_postcode_my = load_postcode_dataframe()
    state_list = df_postcode_my['State'].str.upper()
    state_list = set(state_list)
    state_list = list(state_list)
    state_list = [x for x in state_list if pd.notnull(x)]

    city_list = df_postcode_my['Post_Office'].str.upper()
    city_list = set(city_list)
    city_list = list(city_list)
    city_list = [x for x in city_list if pd.notnull(x)]

    postcode_list = df_postcode_my['Postcode'].str.upper()
    postcode_list = set(postcode_list)
    postcode_list = list(postcode_list)
    postcode_list = [x for x in postcode_list if pd.notnull(x)]

    location_list = df_postcode_my['Location'].str.upper()
    location_list = list(location_list)
    location_list = [x for x in location_list if pd.notnull(x)]

    country_list = ['MY']

    postcodes_found = []
    country_found = []
    state_found = []
    city_found = []
    list_address_full = []
    all_address_r_list = []
    list_building_name = []
    list_house_number = []

    country = 'MY'
    state = 'N/A'
    city = 'N/A'
    postcode = 'N/A'

    for index in range(len(address) - 1, 0, -1):

        if remove_country(address[index], country_list):
            country = address[index]
            address.remove(address[index])

        elif remove_state(address[index], state_list):
            state = address[index]
            address.remove(address[index])

        elif remove_city(address[index], city_list):
            city = address[index]
            address.remove(address[index])

        elif remove_postcodes(address[index], postcode_list):
            postcode = address[index]
            address.remove(address[index])

    country_found.append(country)
    state_found.append(state)
    city_found.append(city)
    postcodes_found.append(postcode)
    all_address_r_list.append(address)
    # print("===============================")
    # print("Before split street and house address:", address)
    street_index = split_house_address_and_street(address)
    if street_index > 0:
        house_address = str(address[:street_index])[1:-1].replace("'", "")
        street_name = str(address[street_index:])[1:-1].replace("'", "")
    else:
        house_address = 'N/A'
        street_name = str(address[street_index:])[1:-1].replace("'", "")

    # print("After Split:")
    # print("House Address: ", house_address)
    # print("Street Name: ", street_name)

    if house_address != 'N/A':

        doc = nlp(house_address)
        building_name = ''
        house_number = ''

        # print('\nOutput: ', [(ent.text, ent.label_) for ent in doc.ents])
        for ent in doc.ents:
            if ent.label_ == 'HOUSE NUMBER':
                house_number = house_number + ' ' + ent.text
            elif ent.label_ == "BUILDING NAME":
                building_name = building_name + ' ' + ent.text

        if building_name == '':
            building_name = 'N/A'

        if house_number == '':
            house_number = 'N/A'

        list_building_name.append(building_name)
        list_house_number.append(house_number)
    else:
        building_name = 'N/A'
        house_number = 'N/A'
        list_building_name.append(building_name)
        list_house_number.append(house_number)

    # print("House Address:", house_address)
    # print("After labeled by NER:")
    # print(house_number, ",", building_name)
    # print("===============================")
    # address_full = [house_number, building_name, house_address.replace(",", ""), street_name.replace(",", ""),
    #                 postcode, city, state, country]

    address_full = [house_number, building_name, street_name.replace(",", ""),
                    postcode, city, state, country]

    list_address_full.append(address_full)
    df = pd.DataFrame(list_address_full,
                      columns=['house_number', 'building_name', 'street_name', 'postcode', 'city',
                               'state', 'country'])
    # print('Pre-process 1 - Identify Address Items... Success')
    return df


def address_splitting(address):
    raw_address = address.upper()

    # Remove Commas
    c_address = raw_address.replace(',', ' ')

    # Remove Dot
    c_address = c_address.replace('.', ' ')

    # Tokenize Address
    tokenized_address = c_address.split(" ")

    c_address_2 = ''

    pattern = re.compile("\d{5}")
    address_keywords = ['JALAN', 'KG', 'KAMPUNG', 'TAMAN', 'PERSIARAN', 'BLOK', 'BLOCK', 'JLN',
                        'TMN', 'SEKSYEN', 'SECTION', 'RUMAH', 'KAMPUS', 'PLAZA', 'BUKIT', 'KOMPLEKS',
                        'KAWASAN', 'NO', 'NO.', 'LORONG', 'JABATAN', 'LADANG', 'SEKOLAH',
                        'PANGSAPURI', 'BANGUNAN', 'LADANG', 'THE', 'PORT', 'LOT', 'WISMA']
    end_address_keywords = ['MALL', 'RESIDENCE', 'CARNIVAL', 'WAREHOUSE', 'CENTRE', 'JAYA', 'CITY',
                            'COMPLEX', 'ZONE', 'VILLAGE', 'PARK', 'BARAT', 'HEIGHTS', 'OUTLETS',
                            'SQUARE', 'RESORT', 'OUTLET', 'BHD']
    state_list = ['SELANGOR', 'PAHANG', 'TERENGGANU', 'KELANTAN', 'PERAK', 'KEDAH', 'PENANG',
                  'PERLIS', 'NEGERI', 'MELAKA', 'JOHOR', 'SABAH',
                  'SARAWAK', 'WP']

    country_list = ['MY']
    address_keywords.extend(state_list)
    address_keywords.extend(country_list)

    for word in tokenized_address:
        check = False
        check_number_exists = any(char.isdigit() for char in word)
        if check_number_exists:
            if pattern.match(word):
                c_address_2 = c_address_2 + ',' + word + ', '
            else:
                c_address_2 = c_address_2 + word + ','
        else:
            for key in address_keywords:
                if search(key, word):
                    check = True
                    break
                else:
                    check = False
            if check:
                c_address_2 = c_address_2 + ',' + word + ' '
            else:
                check = False
                for key in end_address_keywords:
                    if search(key, word):
                        check = True
                        break
                    else:
                        check = False
                if check:
                    c_address_2 = c_address_2 + word + ', '
                else:
                    c_address_2 = c_address_2 + word + ' '

    c_address_2 = c_address_2.replace(u'\xa0', u' ')
    tokenized_address_2 = c_address_2.split(",")

    strip_tokenized_address_2 = [item.strip() for item in tokenized_address_2]
    strip_tokenized_address_2 = [i for i in strip_tokenized_address_2 if i]

    c_tokenized_address_3 = []
    for word in strip_tokenized_address_2:

        if not word.isspace():
            c_tokenized_address_3.append(word)

    final_cleaned_tokenized_address = c_tokenized_address_3

    # print('Pre-process 2 - Tokenizing addresses... Success')
    return final_cleaned_tokenized_address


def decontracted(phrase):
    # specific
    phrase = re.sub(r"JLN", "JALAN", phrase)
    phrase = re.sub(r"TMN", "TAMAN", phrase)
    phrase = re.sub(r"\bSG\b", "SUNGAI", phrase)

    # City
    phrase = re.sub(r"\bWP KL\b", "WP KUALA LUMPUR", phrase)
    phrase = re.sub(r"\bK.L.\b", "WP KUALA LUMPUR", phrase)
    phrase = re.sub(r"\bKL\b", "WP KUALA LUMPUR", phrase)
    phrase = re.sub(r"\bW.P. KUALA LUMPUR\b", "WP KUALA LUMPUR", phrase)
    phrase = re.sub(r"\bW.P KUALA LUMPUR\b", "WP KUALA LUMPUR", phrase)
    phrase = re.sub(r"\bW. PERSEKUTUAN\b", "WP", phrase)
    phrase = re.sub(r"WILAYAH PERSEKUTUAN KUALA LUMPUR", "WP KUALA LUMPUR", phrase)
    phrase = re.sub(r"\b, KUALA LUMPUR\b", ", WP KUALA LUMPUR", phrase)
    # phrase = re.sub(r"\bW.P\b","WP", phrase)
    phrase = re.sub(r"\bW.PERSEKUTUAN\b", "WP", phrase)
    phrase = re.sub(r"\bFEDERAL TERRITORY OF KUALA LUMPUR\b", "WP KUALA LUMPUR", phrase)
    phrase = re.sub(r"\bPJ\b", "PETALING JAYA", phrase)
    # phrase = re.sub(r"\bWp\b", "WP", phrase)
    phrase = re.sub(r"\bJOHOR BHARU\b", "JOHOR BAHRU", phrase)
    phrase = re.sub(r"\bPENANG\b", "PULAU PINANG", phrase)
    phrase = re.sub(r"\bBDR\b", "BANDAR", phrase)
    phrase = re.sub(r"\bWPKL\b", "WP KUALA LUMPUR", phrase)
    phrase = re.sub(r"WP-PUTRAJAYA", "WP PUTRAJAYA", phrase)
    phrase = re.sub(r"\b, PUTRAJAYA\b", ", WP PUTRAJAYA", phrase)
    phrase = re.sub(r"\bSEK.\b", "SEKSYEN", phrase)
    phrase = re.sub(r"\bDARUL KHUSUS\b", "", phrase)
    phrase = re.sub(r"\bDARUL EHSAN\b", "", phrase)

    return phrase


def expand_address_v2(address):
    address = address.upper()
    expanded_address = decontracted(address)
    return expanded_address


def expand_address(address):
    address = address.upper()
    expanded_address = decontracted(address)
    return expanded_address


def clean_one_address(address):
    expanded_address = expand_address(address)
    # print('Pre-process 1 - Expanding Abbreviations... Success')
    splitted_address = address_splitting(expanded_address)
    # print('Preprocessing Stage 1... Success')
    return splitted_address


def parse_addresses(address_list):
    df_postcode_my = load_postcode_dataframe()
    state_list = df_postcode_my['State'].str.upper()
    state_list = set(state_list)
    state_list = list(state_list)
    state_list = [x for x in state_list if pd.notnull(x)]

    city_list = df_postcode_my['Post_Office'].str.upper()
    city_list = set(city_list)
    city_list = list(city_list)
    city_list = [x for x in city_list if pd.notnull(x)]

    postcode_list = df_postcode_my['Postcode'].str.upper()
    postcode_list = set(postcode_list)
    postcode_list = list(postcode_list)
    postcode_list = [x for x in postcode_list if pd.notnull(x)]

    location_list = df_postcode_my['Location'].str.upper()
    location_list = list(location_list)
    location_list = [x for x in location_list if pd.notnull(x)]

    country_list = ['MY']

    postcodes_found = []
    country_found = []
    state_found = []
    city_found = []
    list_address_full = []
    list_building_name = []
    list_house_number = []

    all_address_r_list = []
    for address in address_list:
        country = 'MY'
        state = 'N/A'
        city = 'N/A'
        postcode = 'N/A'
        for index in range(len(address) - 1, 0, -1):

            if remove_country(address[index], country_list):
                country = address[index]
                address.remove(address[index])

            elif remove_state(address[index], state_list):
                state = address[index]
                address.remove(address[index])

            elif remove_city(address[index], city_list):
                city = address[index]
                address.remove(address[index])

            elif remove_postcodes(address[index], postcode_list):
                postcode = address[index]
                address.remove(address[index])

        country_found.append(country)
        state_found.append(state)
        city_found.append(city)
        postcodes_found.append(postcode)
        all_address_r_list.append(address)

        street_index = split_house_address_and_street(address)

        # print("===============================")
        # print("Before split street and house address:", address)

        if street_index > 0:
            house_address = str(address[:street_index])[1:-1].replace("'", "")
            street_name = str(address[street_index:])[1:-1].replace("'", "")
        else:
            house_address = 'N/A'
            street_name = str(address[street_index:])[1:-1].replace("'", "")

        # print("After Split:")
        # print("House Address: ", house_address)
        # print("Street Name: ", street_name)
        if house_address != 'N/A':

            doc = nlp(house_address)
            building_name = ''
            house_number = ''

            # print('Output: ', [(ent.text, ent.label_) for ent in doc.ents])

            for ent in doc.ents:
                if ent.label_ == 'HOUSE NUMBER':
                    house_number = house_number + ' ' + ent.text
                elif ent.label_ == "BUILDING NAME":
                    building_name = building_name + ' ' + ent.text

            if building_name == '':
                building_name = 'N/A'

            if house_number == '':
                house_number = 'N/A'

            list_building_name.append(building_name)
            list_house_number.append(house_number)
        else:
            building_name = 'N/A'
            house_number = 'N/A'
            list_building_name.append(building_name)
            list_house_number.append(house_number)

        # print("House Address:", house_address)
        # print("After labeled by NER:")
        # print(house_number, ",", building_name)
        # print("===============================")

        address_full = [house_number, building_name, street_name.replace(",", ""),
                        postcode, city, state, country]

        list_address_full.append(address_full)

    df = pd.DataFrame(list_address_full,
                      columns=['house_number', 'building_name', 'street_name', 'postcode', 'city',
                               'state', 'country'])
    # print('Pre-process 1 - Identify Address Items... Success')
    return df


def execute_parsing_address_one(address):
    tokenized_address = clean_one_address(address)
    df_address_items = parse_one_address(tokenized_address)
    result = find_missing_address_parts(df_address_items)
    result =list(result.T.to_dict().values())[0]
    return result


def execute_parsing_address_all(address_list):
    # print(address_list)
    df = pd.DataFrame(address_list, columns=['full_address'])
    df['full_address'] = df['full_address'].apply(lambda x: clean_one_address(x))
    # print(df)
    df_parsed_addresses = parse_addresses(df['full_address'].to_list())
    result = find_missing_address_parts(df_parsed_addresses)
    return result.T.to_dict()




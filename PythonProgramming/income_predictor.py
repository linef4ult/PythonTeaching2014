'''Classifier for sample income dataset

Process overview
1. Create training set from data
2. Create classifier using training dataset to determine separator values for each attribute
3. Create test dataset
4. Use classifier to classify data in test set while maintaining accuracy score

'''

__author__ = 'mark'

DATA_URL = "http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
PERCENT = 99

import httplib2

def create_data(DATA_URL):
    '''Here we read our data file directly from the web and split it out into a list of tuples, one tuple per record.

    Listing of attributes:

    Possible outcomes: >50K, <=50K.

    1. age: continuous.
    2. workclass: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
    3. NOT NEEDED: fnlwgt: continuous.
    4. NOT NEEDED: education: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.
    5. education-num: continuous.
    6. marital-status: Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
    7. occupation: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
    8. relationship: Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
    9. race: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
    10. sex: Female, Male.
    11. capital-gain: continuous.
    12. capital-loss: continuous.
    13. hours-per-week: continuous.
    14. NOT NEEDED: native-country: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.
    '''

    ts_list = []
    workclass_dict_U = {}
    marital_dict_U = {}
    occupation_dict_U = {}
    relationship_dict_U = {}
    race_dict_U = {}
    sex_dict_U = {}

    workclass_dict_O = {}
    marital_dict_O = {}
    occupation_dict_O = {}
    relationship_dict_O = {}
    race_dict_O = {}
    sex_dict_O = {}

    row_count = 0
    under_list = 0
    over_list = 0

    try:
        # get data file, open it and modify numbers to int, Also count (via dictionary) each text value in the
        # 'discrete' categories for the under- and over-50Ks

        # local_filename, headers = urllib.request.urlretrieve(DATA_URL)
        # fh = open(local_filename, "r")
        h = httplib2.Http(".cache")
        headers, fh = h.request(DATA_URL)
        fh = fh.decode().split("\n")

        for row in fh:
            try:
                row = row.strip()
                row = row.split(",")
                row[0] = int(row[0])
                row[2] = None
                row[3] = None
                row[4] = int(row[4])
                row[10] = int(row[10])
                row[11] = int(row[11])
                row[12] = int(row[12])
                row[13] = None

                if row[-1].lstrip() == '<=50K':
                    under_list += 1

                    if row[1] in workclass_dict_U:
                        workclass_dict_U[row[1]] += 1
                    else:
                        workclass_dict_U[row[1]] = 1

                    if row[5] in marital_dict_U:
                        marital_dict_U[row[5]] += 1
                    else:
                        marital_dict_U[row[5]] = 1

                    if row[6] in occupation_dict_U:
                        occupation_dict_U[row[6]] += 1
                    else:
                        occupation_dict_U[row[6]] = 1

                    if row[7] in relationship_dict_U:
                        relationship_dict_U[row[7]] += 1
                    else:
                        relationship_dict_U[row[7]] = 1

                    if row[8] in race_dict_U:
                        race_dict_U[row[8]] += 1
                    else:
                        race_dict_U[row[8]] = 1

                    if row[9] in sex_dict_U:
                        sex_dict_U[row[9]] += 1
                    else:
                        sex_dict_U[row[9]] = 1

                elif row[-1].lstrip() == '>50K':
                    over_list += 1

                    if row[1] in workclass_dict_O:
                        workclass_dict_O[row[1]] += 1
                    else:
                        workclass_dict_O[row[1]] = 1

                    if row[5] in marital_dict_O:
                        marital_dict_O[row[5]] += 1
                    else:
                        marital_dict_O[row[5]] = 1

                    if row[6] in occupation_dict_O:
                        occupation_dict_O[row[6]] += 1
                    else:
                        occupation_dict_O[row[6]] = 1

                    if row[7] in relationship_dict_O:
                        relationship_dict_O[row[7]] += 1
                    else:
                        relationship_dict_O[row[7]] = 1

                    if row[8] in race_dict_O:
                        race_dict_O[row[8]] += 1
                    else:
                        race_dict_O[row[8]] = 1

                    if row[9] in sex_dict_O:
                        sex_dict_O[row[9]] += 1
                    else:
                        sex_dict_O[row[9]] = 1

                else:
                    pass

            except ValueError as v:
                print(row[0], v)
                continue

            #row = [item for item in row if item]
            ts_list.append(row)
            row_count += 1


    except IOError as e:
        print(e)
    except ValueError as v:
        print(v)

    # finally:
    #     fh.close()

    #for record in ts_list:
    for row in ts_list:
        if row[-1].lstrip() == '<=50K':
            row[1] = workclass_dict_U[row[1]] / under_list
            row[5] = marital_dict_U[row[5]] / under_list
            row[6] = occupation_dict_U[row[6]] / under_list
            row[7] = relationship_dict_U[row[7]] / under_list
            row[8] = race_dict_U[row[8]] / under_list
            row[9] = sex_dict_U[row[9]] / under_list
        elif row[-1].lstrip() == '>50K':
            row[1] = workclass_dict_O[row[1]] / over_list
            row[5] = marital_dict_O[row[5]] / over_list
            row[6] = occupation_dict_O[row[6]] / over_list
            row[7] = relationship_dict_O[row[7]] / over_list
            row[8] = race_dict_O[row[8]] / over_list
            row[9] = sex_dict_O[row[9]] / over_list
        else:
            pass



    print(ts_list)
    return ts_list


def create_classifier(training_list):
    '''For each record we average the values for each attribute in a list of known >50K results and, separately, a
        list of known <=50K results. The >50K and <=50K averages are then averaged against each other to
        compute midpoint values. These will be used to compare each attribute in a record and assign it a status -
        >50K or <=50K. The overall result is the greater of the number of the >50K / <=50K status values.
    '''

    over_attrs = [0]*14
    under_attrs = [0]*14
    over_count = 0
    under_count = 0
    classifier_list = [0]*14

    # Compute the totals for each factor
    for record in training_list:
        if record[-1].lstrip() == '>50K':
            over_count += 1
            for attribute in range(len(record[:-1])):
                try:
                    over_attrs[attribute] += record[attribute]
                except TypeError as t:
                    over_attrs[attribute] += 0

        elif record[-1].lstrip() == '<=50K':
            under_count += 1
            for attribute in range(len(record[:-1])):
                try:
                    under_attrs[attribute] += record[attribute]
                except TypeError as t:
                    under_attrs[attribute] += 0

    # Compute the average values for each factor
    for attribute in range(len(over_attrs)):
        over_attrs[attribute] = over_attrs[attribute] / over_count
    for attribute in range(len(under_attrs)):
        under_attrs[attribute] = under_attrs[attribute] / under_count

    # Compute the midpoints - the average of the over & under factors in each case
    for attribute in range(len(classifier_list)):
        classifier_list[attribute] = (over_attrs[attribute] + under_attrs[attribute]) / 2

    print(classifier_list)
    return classifier_list


def create_test(test_list, classifier_list):
    ''' We apply the classifier list against each record in the test set. We compare each attribute against its
    equivalent value in the classifier list. Based on this, the attribute gets a status - 'GT' or 'LE'. The count of
    the status values for a record determines the result.
    '''

    #print(''.join(' {!s:6s} | '.format(item) for item in classifier_list),'\n')

    temp_result_list = ['']*15
    false_count = 0
    true_count = 0
    total_count = 0

    for record in test_list:
        for idx, attribute in enumerate(record[1:-1]):
            try:
                if record[idx] < classifier_list[idx]:
                    temp_result_list[idx] = ' <=50K'
                else:
                    temp_result_list[idx] = ' >50K'
            except:
                temp_result_list[idx] = None

        if temp_result_list.count(' <=50K') >= temp_result_list.count(' >50K'):
            temp_result_list[-1] = ' <=50K'
        else:
            temp_result_list[-1] = ' >50K'

        #print(''.join(' {!s:6s} | '.format(item) for item in record))
        print(''.join(' {!s:6s} | '.format(item) for item in temp_result_list), end=' ')
        #print(record)
        #print(temp_result_list, end=' ')
        total_count += 1
        if record[-1] == temp_result_list[-1]:
            print("CORRECT")
            true_count +=1
        else:
            print("FALSE")
            false_count += 1

    print("\nCORRECT: {}, {:.2%},  INCORRECT: {}, {:.2%},  TOTAL COUNT: {}".format(true_count,true_count/total_count,false_count,false_count/total_count,total_count))


def main():

    # Make a list of tuples from the raw data
    data_list = create_data(DATA_URL)

    # Break out our dataset into a training and test sets where the training set has a number of records determined
    # by the PERCENT value. The test set has the remaining records.
    training_list = data_list[:int(len(data_list)*PERCENT/100)]
    test_list = data_list[int(len(data_list)*PERCENT/100):]

    # Create the classifier values
    classifier_list = create_classifier(training_list)

    # Apply classifier against test file.
    # Given that we know the outcome for each test record we can verify the classifier
    create_test(test_list, classifier_list)

if __name__ == "__main__":
    main()
from .models import *
from django.shortcuts import get_object_or_404
from datetime import datetime
from .datavisualization import get_month, get_year
from django.db.models import Count


def query_active_studies(startdate, enddate):
    qs = KitInstance.objects.values('id', 'created_date', 'status')

    study_list = []

    # Iterate through each kit instance to check if the date created is within date range
    for q in qs:

        # If kit instance was created within date range, add to the study_list
        if check_date(q['created_date'], startdate, enddate):
            study_list.append((q['id'], q['created_date'], 'added'))

        # Check if a kit instance had a status change
        kit_inst = historical_status_change(q['id'])

        if kit_inst is not None:
            # If historical_status_change returns with values (i.e. not None)
            # Then check the date of that status change
            if check_date(kit_inst[1], startdate, enddate):

                # If status change within date range
                if kit_inst[0] == 'demolished':
                    study_list.append((q['id'], kit_inst[1], 'demolished'))
                elif kit_inst[0] == 'checked-out':
                    study_list.append((q['id'], kit_inst[1], 'checked_out'))
                elif kit_inst[0] == 'none':
                    continue

    outfile = "kitactivity.csv"
    file = open(outfile, 'w')
    file.write("ID,Date,Action\n")

    for entry in study_list:
        study_id, study_date, action = entry
        month = get_month(study_date)
        year = get_year(study_date)
        file.write(str(study_id) + "," + str(month) + "-" + str(year) + "," + action + "\n")
    file.close()
    return outfile

# To check each historical event for a status change for each kit instance event
# If there is a status change, return new status (i.e. demolished or checked out)
# & the date the status change occurred


def historical_status_change(kit_id):

    # Get the one kit instance objects
    kit = get_object_or_404(KitInstance, pk=kit_id)

    # Then get all of the historical events associated with that object
    kit = kit.history.all()

    # Iterate through all the historical instances for that specific kit instance
    for i in range(len(kit) - 1):
        delta = kit[i].diff_against(kit[i+1])
        # Compare two historical kit instances at a time and find the one where status field changed
        for change in delta.changes:
            if change.field == 'status':
                if change.new == 'd':
                    event = 'demolished'
                elif change.new == 'c':
                    event = 'checked-out'
                else:
                    event = 'none'

                # Get the date of the kit instance history status change
                hist = kit[i+1].history_date
                changed_date = datetime.date(hist)

                return [event, changed_date]

# Check if date falls between the start and end date


def check_date(checked_date, startdate, enddate):
    if startdate < checked_date < enddate:
        return True
    else:
        return False


def validate_date(startdate, enddate):
    if startdate == '':
        message = "Please enter in a start date"
        return message
    elif enddate == '':
        message = "Please enter in an end date"
        return message
    try:
        date_format = '%m-%d-%Y'
        startdate = datetime.strptime(startdate, date_format)
        enddate = datetime.strptime(enddate, date_format)
        return True
    except:
        message = "Please format date entries correctly to MM-DD-YYYY."
        return message


def query_checked_out_kits(startdate, enddate):

    checked_out = KitInstance.objects.filter(status='c')

    test = []
    studies = []

    for kit in checked_out:
        if not check_date(kit.checked_out_date, startdate, enddate):
            break
        elif check_date(kit.checked_out_date, startdate, enddate):

            study = str(kit.kit.IRB_number)

            # If the kit type belongs to a study that was already added in the list
            if study in studies:
                # Find the index value from the studies list
                study = str(kit.kit.IRB_number)
                index = studies.index(study)
                # Add checked out kits to the right IRB
                test[index][2] = 1 + int(test[index][2])

            elif study not in studies:
                studies.append(str(kit.kit.IRB_number))
                t = [str(kit.kit.IRB_number)]
                study = get_object_or_404(Study, IRB_number=kit.kit.IRB_number)
                t.append(str(study.pet_name))
                t.append(1)
                test.append(t)

    return test


def storage_tables(queryset):
    queryset_kits = KitInstance.objects.all().filter(kit__IRB_number_id__in=queryset).annotate(num_kit=Count('kit')).\
        order_by('location_id')

    location_list = []

    table1 = []

    for kit in queryset_kits:
        if str(kit.location) not in location_list:
            location_list.append(str(kit.location))
            entry = [str(kit.location)]

            entry1 = [str(kit.kit.IRB_number)]

            entry2 = [1]

            entry.append(entry1)
            entry.append(entry2)

            table1.append(entry)

        elif str(kit.location) in location_list:
            index = location_list.index(str(kit.location))
            if str(kit.kit.IRB_number) in table1[index][1]:
                study_index = table1[index][1].index(str(kit.kit.IRB_number))
                table1[index][2][study_index] = table1[index][2][study_index] + 1

            elif str(kit.kit.IRB_number) not in table1[index][1]:

                table1[index][1].append(str(kit.kit.IRB_number))
                table1[index][2].append(1)

    return table1


def storage_data():
    data = []

    open_studies = Study.objects.all().filter(status='Open')
    exp_kits = KitInstance.objects.all().filter(kit__IRB_number__in=open_studies).filter(status='e').count()
    ava_kits = KitInstance.objects.all().filter(kit__IRB_number__in=open_studies).filter(status='a').count()

    status = ['a', 'e']
    closed_studies = Study.objects.all().filter(status='Closed')
    closed_kits = KitInstance.objects.all().filter(kit__IRB_number__in=closed_studies).filter(status__in=status).count()

    prep_studies = Study.objects.all().filter(status='Preparing to Open')
    prep_exp_kits = KitInstance.objects.all().filter(kit__IRB_number__in=prep_studies).filter(status='e').count()
    prep_ava_kits = KitInstance.objects.all().filter(kit__IRB_number__in=prep_studies).filter(status='a').count()

    data.append(exp_kits)
    data.append(ava_kits)
    data.append(closed_kits)
    data.append(prep_exp_kits)
    data.append(prep_ava_kits)

    return data


def query_demolished_kits(startdate, enddate):
    test = []
    studies = []

    all_kits = KitInstance.objects.all()

    for kit in all_kits:
        status = historical_status_change(kit.id)
        if status is not None:
            if status[0] == 'demolished':
                if check_date(status[1], startdate, enddate):
                    study = str(kit.kit.IRB_number)
                    # If the kit type belongs to a study that was already added in the list
                    if study in studies:
                        # Find the index value from the studies list
                        study = str(kit.kit.IRB_number)
                        index = studies.index(study)
                        # Add demolished kits to the right IRB
                        test[index][2] = 1 + int(test[index][2])

                    elif study not in studies:
                        studies.append(str(kit.kit.IRB_number))
                        t = [str(kit.kit.IRB_number)]
                        study = get_object_or_404(Study, IRB_number=kit.kit.IRB_number)
                        t.append(str(study.pet_name))
                        t.append(1)
                        test.append(t)

    return test


def query_study_activity(startdate, enddate):
    studies = Study.objects.all()
    query = (['Studies Added', 0], ['Studies Opened', 0], ['Studies Closed', 0])
    activity_list = []

    for study in studies:
        historical_create = historical_study_create(study.id)
        if historical_create is not None and historical_create[0] == 'added':
            if check_date(historical_create[1], startdate, enddate) == True:
                if historical_create[0] == 'added':
                    if check_date(historical_create[1], startdate, enddate):
                        query[0][1] = query[0][1] + 1
                        activity_list.append([study.IRB_number, 'Studies Added', historical_create[1]])

        historical_opened = historical_study_status_change(study.id, 'opened')
        if historical_opened is not None and historical_opened[0] == 'opened':
            if check_date(historical_opened[1], startdate, enddate) == True:
                if historical_opened[0] == 'opened':
                    if check_date(historical_opened[1], startdate, enddate):
                        query[1][1] = query[1][1] + 1
                        activity_list.append([study.id, 'Studies Opened', historical_opened[1]])

        historical_closed = historical_study_status_change(study.id, 'closed')
        if historical_closed is not None and historical_closed[0] == 'closed':
            if check_date(historical_closed[1], startdate, enddate) == True:
                if historical_closed[0] == 'closed':
                    if check_date(historical_closed[1], startdate, enddate):
                        query[2][1] = query[2][1] + 1
                        activity_list.append([study.id, 'Studies Closed', historical_closed[1]])

    outfile = "studyactivity.csv"
    file = open(outfile, 'w')
    file.write("IRB_number,Date,Action\n")

    for entry in activity_list:
        entry_id, action, entry_date = entry
        month = get_month(entry_date)
        year = get_year(entry_date)
        file.write(str(entry_id) + "," + str(month) + "-" + str(year) + "," + action + "\n")
    file.close()
    return query, outfile


def historical_study_create(study_id):
    study = get_object_or_404(Study, pk=study_id)
    study = study.history.all()
    for s in study:
        if s.history_type == '+':
            event = 'added'
            hist = s.history_date
            hist_date = datetime.date(hist)
            return [event, hist_date]
    return False


def historical_study_status_change(study_id, status):

    study = get_object_or_404(Study, pk=study_id)
    study = study.history.all()
    for i in range(len(study) - 1):
        delta = study[i].diff_against(study[i+1])
        for change in delta.changes:
            if change.field == 'status':
                if change.old == 'Preparing to Open' and change.new == 'Open' and status == 'opened':
                    event = 'opened'
                    hist = study[i + 1].history_date
                    changed_date = datetime.date(hist)
                    return [event, changed_date]
                elif change.new == 'Closed' and change.old == 'Open' and status == 'closed':
                    event = 'closed'
                    hist = study[i + 1].history_date
                    changed_date = datetime.date(hist)
                    return [event, changed_date]
                else:
                    event = 'none'
                    changed_date = ''
            return [event, changed_date]

import finance_db
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import tabulate

# TODO add weekly option for bucketizer and bar charts
# TODO implement 'last' option for end date (last of given month or year)


class GComponent:
    """ class for graphing/display component """

    def __init__(self, db, id_col, id_val):
        """ Component object to contain component properties and display characteristics

        praram:
            db:                 db object from finance_db
            reference:          tuple with format (string:id column name, int: id referencing component)
        """

        # set passed id information
        self.id_col = id_col
        self.id_val = id_val

        # match correct table to the passed id
        for table in db.schema.keys():
            if self.id_col in db.schema[table]:
                i = 0
                for column in db.schema[table]:
                    if 'id' in column:
                        i = i + 1
                # id column passed matched to table in schema
                # link tables will also have desired id string, but if there are mutliple id columns table is not found
                if i < 2:
                    self.table = table
            else:
                print('ID column passed does not match any table within schema')

        self.date_format = '%Y-%m-%d'

        # get component properties and extract what is needed in particular properties for accessibility
        # remainder of propertiess become self.properties
        temp_prop = {}
        if self.table == 'budgets':
            temp_prop = _get_budget_component(db=db, identifier=self.id_val)
            # need to catch special entries for rolling budgets
            if temp_prop['disp_start'] == 'first':
                # first indicates first day of window size will be used, depending on the chosen budget resolution
                if temp_prop['b_resolution'] == 'month':
                    temp_prop['disp_start'] = datetime.today().replace(day=1).strftime(self.date_format)
                elif temp_prop['b_resolution'] == 'year':
                    temp_prop['disp_start'] = datetime.today().replace(day=1, month=1).strftime(self.date_format)

            if temp_prop['disp_end'] == 'now':
                temp_prop['disp_end'] = datetime.now().strftime(self.date_format)

        # all components must carry these columns
        self.disp_type = temp_prop['disp_type']
        temp_prop.pop('disp_type')

        self.graph_type = temp_prop['graph_type']
        temp_prop.pop('graph_type')

        # define display window given passed params
        self.start = None
        self.end = None

        if temp_prop['disp_start'] and temp_prop['disp_end']:
            self.start = datetime.strptime(temp_prop['disp_start'], self.date_format)
            self.end = datetime.strptime(temp_prop['disp_end'], self.date_format)

        elif (temp_prop['disp_start'] or temp_prop['disp_end']) and \
                (temp_prop['disp_window_size'] and temp_prop['disp_window_unit']):

            if temp_prop['disp_window_unit'] == 'month':
                self.window = relativedelta(months=int(temp_prop['disp_window_size']))
            elif temp_prop['disp_window_unit'] == 'day':
                self.window = relativedelta(days=int(temp_prop['disp_window_size']))

            if temp_prop['disp_start']:
                self.start = datetime.strptime(temp_prop['disp_start'], self.date_format)
                self.end = self.start + self.window
            elif temp_prop['disp_end']:
                self.end = datetime.strptime(temp_prop['disp_end'], self.date_format)
                self.start = self.end - self.window

        temp_prop.pop('disp_start')
        temp_prop.pop('disp_end')
        temp_prop.pop('disp_window_size')
        temp_prop.pop('disp_window_unit')

        # data from db stored here as dict - everything that is not common to all display components
        self.db_properties = temp_prop

        # properties to store data of display component
        self.data = []


def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said
    # programattically said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)


def _bucketize(resolution, date_format, start=None, end=None):
    """ take in date informaiton and return list of buckets given the resolution

    Attributes:
        resolution      string: monthly or daily
        start           string denoting start of time window formatted 'YYYY-MM-DD'
        end             string denoting end of time window formatted 'YYYY-MM-DD'
        window
    """

    # rule set up for required parameters and argument options
    # argument options
    a_resolutions = ['month', 'day']
    a_w_units = ['month', 'day']
    # initialize return list
    months_str = []
    buckets = []

    # process inputs to insure conformity to available commands
    if resolution not in a_resolutions:
        print("Resolution must be in " + str(a_resolutions)[1:-1])
        return

    resolution_dt = ""
    if resolution == 'month':
        resolution_dt = relativedelta(months=1)
    elif resolution == 'day':
        resolution_dt = relativedelta(days=1)

    # scenario 1: start end
    # scenario 2: start w_size w_unit
    # scenario 3: end w_size w_unit
    # allow for 'now' to be supplied as end

    start_count = start
    end_count = start + resolution_dt

    while end_count <= end:
        # months_str.append(start_count.month)
        buckets.append([start_count.strftime(date_format), end_count.strftime(date_format)])

        start_count = start_count + resolution_dt
        end_count = end_count + resolution_dt

    return buckets


def _get_bucket_data(db, buckets, table, cat_id):
    """ returns list of tuples (bucket, bucket amount)"""
    # populate data from db using buckets and cat_id
    data = []
    for bucket in buckets:
        query = finance_db.Query(table=table,
                                 s_cols=['amount'],
                                 w_cols=['date', 'date', 'cat_id'], w_conds=['>=', '<', '='], w_vals=[bucket[0], bucket[1], str(cat_id)], w_joins=['AND', 'AND', 'AND'])
        data_bucket = str(bucket[0]) + ' - ' + str(bucket[1])
        data_value = db.conn.cursor().execute(query.build_select(function='SUM')).fetchall()[0][0]
        if data_value:
            data_value = abs(int(data_value))
        else:
            data_value = 0

        data_point = (data_bucket, data_value)
        data.append(data_point)

    return data


def terminal_bar(data, target=None):
    # TODO multiple cat_id
    # intialize db object

    if target:
        max_value = target
    else:
        max_value = max(count for _, count in data)
    increment = max_value / 25

    bars = []
    for label, count in data:

        # The ASCII block elements come in chunks of 8, so we work out how
        # many fractions of 8 we need.
        # https://en.wikipedia.org/wiki/Block_Elements
        bar_chunks, remainder = divmod(int(count * 8 / increment), 8)

        # First draw the full width chunks
        bar = '█' * bar_chunks

        # Then add the fractional part.  The Unicode code points for
        # block elements are (8/8), (7/8), (6/8), ... , so we need to
        # work backwards.
        if remainder > 0:
            bar += chr(ord('█') + (8 - remainder))

        # If the bar is empty, add a left one-eighth block
        bar = bar or '▏'
        bars.append(bar)
    return bars


def _get_budget_component(db, identifier,):
    """ populate dictionary with budget properties from db, keys are columns

    Args:
        identifier          b_id for desired item
        dashboard           object containing multiple budget items
    """
    table = 'budgets'
    schema = db.schema[table]
    query = "SELECT * FROM " + table + " WHERE " + schema[0] + " = '" + identifier + "'"

    print(query)

    budget = db.conn.cursor().execute(query).fetchall()[0]
    budget_component = dict(zip(schema, budget))

    return budget_component


def project_linear(start, end, spent, date_format, target=None, percent=False):
    # break down to spent/per day
    # return projected amount or percent based on user selection
    # special option for start is 'first' indicating rolling start date at first of every month
    # special condition for end is 'now' indicating present date

    # get amount spent per day until present
    now = datetime.strptime(datetime.now().strftime(date_format), date_format)

    units_passed = now - start
    total_units = end - start
    spent_per_units = spent / units_passed.days
    projection = spent_per_units * total_units.days

    if percent:
        projection = projection / target * 100

    projection = round(projection, 1)

    return projection


def _display_budget(db, budget_components, display):
    """ process budget components for display per display type rules """
    # budget display format header
    budgets_header = ['Period', 'Cat(s)', 'Spent', 'Projection', 'Bar Progress']
    budgets_display = []
    buckets = None
    bucket_data = None
    table = 'transactions'

    for component in budget_components:
        if component.graph_type == 'bar':
            if 'budget-bar' not in display:
                display['budget-bar'] = {}

                budgets_header = ['Cat(s)', 'Period', 'Target', 'Spent [%]', 'Projection [%]', 'Progress']
                display['budget-bar']['header'] = []
                display['budget-bar']['data'] = []

                display['budget-bar']['header'] = budgets_header

            # buckets may require some additional work to flesh out to different resolutions
            buckets = _bucketize(resolution=component.db_properties['b_resolution'], date_format=component.date_format,
                                 start=component.start, end=component.end,)
            bucket_data = _get_bucket_data(db=db, buckets=buckets, table=table, cat_id=component.db_properties['b_cat'])
            for point in bucket_data:
                component.data.append(point)

            # for budgets we assume bars is single item in list aka there is only one bucket
            # TODO package all bar graphs THEN get bars or else they will not scale properly
            bars = terminal_bar(bucket_data, target=component.db_properties['b_target'])

            # define display items
            i = 0
            # budgets_header = ['Period', 'Cat(s)', 'Spent', 'Projection', 'Bar Progress']
            # populate with desired data items given display format below
            for i in range(0, len(component.data)):
                period = component.data[i][0]
                cat_ids = component.db_properties['b_cat']
                spent = round(component.data[i][1] / component.db_properties['b_target'] * 100, 1)
                # only project if end date is in the future
                projection = None
                now = datetime.strptime(datetime.now().strftime(component.date_format), component.date_format)

                if component.end >= now:
                    projection = project_linear(component.start, component.end, spent=component.data[i][1],
                                                date_format=component.date_format,
                                                target=component.db_properties['b_target'], percent=True)

                if i == 0:
                    display['budget-bar']['data'].append([cat_ids, period, component.db_properties['b_target'],
                                                          spent, projection, bars[i]])
                else:
                    display['budget-bar']['data'].append([None, period, component.db_properties['b_target'], spent,
                                                          projection, bars[i]])
                i = i + 1


def display_dashboard(db, d_references):
    """ display all items associated with dashboard

    Args:
        dashboard       list of display components (dictionaries) to tabulate & print


    """
    # d_components is populated with list of component objects via references
    d_components = {}
    for ref in d_references:
        new_component = GComponent(db=db, id_col=ref[0], id_val=ref[1])
        if new_component.disp_type not in d_components:
            # if disp type key is not in d_components it is initialized as list and new component is appended
            d_components[new_component.disp_type] = []
            d_components[new_component.disp_type].append(new_component)
        else:
            d_components[new_component.disp_type].append(new_component)

    # display is dictionary of dictionaries
    # structure is one key per display type with sub keys 'header' (list) & 'data' (list of lists)
    display = {}
    for component_type in d_components:
        if component_type == 'budget':
            _display_budget(db=db, budget_components=d_components['budget'], display=display)
            # TODO need to incorporate graph types as well
            # build the component data into an appropriate display

    for item in display.keys():
        component = display[item]
        header = component['header']
        print(tabulate.tabulate(component['data'], headers=header))

    # d_references houses the references to each display component requested by the user or the dashboard requested
    # d_references is the id and type associated with component, can be single item list or multi

    # d_components is the fleshed out properties of the references
    # populate d_components with display types as keys and lists of dictionaries with component columns as keys
    # may need to separate components ['budgets']['month'] & ['budgets']['year']
    # d_components = {}
    # budget_component = {}
    # for component in d_references:
    #     if 'budget' in component:
    #         # component[0] is b_id passed from driver
    #         budget_component = _get_budget_component(db=db, identifier=component[0])
    #         print(budget_component)
    #         # if disp type already in components dictionaru add data to this key
    #     if budget_component['disp_type'] not in d_components:
    #         d_components[budget_component['disp_type']] = [budget_component]
    #     else:
    #         d_components[budget_component['disp_type']].append(budget_component)
    #
    # print(d_components)

    # display is a dictionary where each display type is a key and each item is dict of display type header and data
    # gather all from type column and elim duplicates
    display = {}

    # could create rules inside db to prevent hardcoding and customization in the future (instead of hard display types)

    # mechanics for each item form budgets header


# terminal_bar(resolution='month', table='transactions', cat_id='11', end='now', w_unit='month', w_size=3)


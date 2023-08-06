from docopt import docopt
import finance_db
import data
import copy
import graph
import docopt_utility
# TODO input category desc or id for displays like budget
# TODO display category name instead of ID for budgets

usage = """

dashboards_py CLI.

Usage:
    dashboards_driver.py show   (((--b <id>) | (--d <id>)...))
    dashboards_driver.py create [(--b <b_type> <b_target> <cat_id> <g_type> 
                                (<start> <end> | --s <start> <window_size> <window_unit> | --e <end> <window_size> <window_unit>) 
                                [(--d <d_res>) (--p <proj_type>)]) | 
                                (--d <dash_desc>)]

);

Arguments:
    <b_target>                  target maximum for given budget
    <b_type>                    type of budget, current options: yearly, monthly
    <cat_id>                    cat_id indicating budgeted category
    <d_res>                     display resolution (not implemented)
    <end>                       end date of budget, enter date in format 'YYYY-MM-DD' or use 'now' to extend to present (rolling)
    <proj_type>                 projection type for budget, current options: linear 
    <start>                     start date of budget enter date in format 'YYYY-MM-DD', use 'now' to start at present or use 'first' to start at first day of present month
    <window_size>               size of desired display window, combined with w_unit to create display window
    <window_unit>               unit of display size, month or day (e.g. window is 6 months if window size = 6 and unit = month)

Options:
    --b                         budget    
    --d                         dashboard 
"""

args = docopt(usage)
db = finance_db.FinanceDB()
print(args)

docopt_utility.elim_apostrophes(args=args)
#
# # initialize objects to pass to various function calls
# query = finance_db.Query(table=args['<table>'],
#                          s_cols=args['<s_cols>'], up_vals=args['<up_vals>'],
#                          w_cols=args['<w_cols>'], w_conds=docopt_utility.process_clause(args), w_vals=args['<w_vals>'],
#                          o_col=args['<o_col>'], o_cond=docopt_utility.o_cond(args),
#                          limit=args['<limit>'])
#
# db = finance_db.FinanceDB()

if args['create']:
    if args['--b']:
        if not db.exists('budgets'):
            db.create_table('budgets')

        columns = copy.deepcopy(db.schema['budgets'])
        columns.remove('b_id')

        query = finance_db.Query(table='budgets', s_cols=columns,
                                 in_vals=[args['<b_type>'], args['<b_target>'], args['<start>'], args['<d_res>'],
                                          args['<end>'], args['<window_size>'], args['<window_unit>'], 'budget',
                                          args['<g_type>'], args['<proj_type>'], args['<cat_id>']],
                                 o_col='b_id', o_cond='DESC',
                                 limit='1')

        data.create_budget(db=db, query=query)
    if args['--d']:
        if not db.exists('dashboards'):
            db.create_table('dashboards')

        columns = copy.deepcopy(db.schema['dashboards'])
        # delete autofill columns from selected solumns for value inputs
        columns.remove('dash_id')
        columns.remove('dash_date')

        query = finance_db.Query(table='budgets', s_cols=columns,
                                 in_vals=[args['<dash_desc>']], o_col=['b_id'], o_cond=['DESC'],
                                 limit=1)

        data.create_dashboard(db=db, query=query)

if args['show']:
    if args['--b']:
        # single budget requested for display
        # args['<id>'] will always be list because of ellipses but in single instance it is stripped
        b_id = args['<id>'][0]
        graph.display_dashboard(db=db, d_references=[('b_id', b_id)])

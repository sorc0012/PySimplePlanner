import datetime
import pickle

DATE_SEP = '-'

class Utils():

    DATE_SEP = '-'
    COLOR_GREEN = "#00E676"
    COLOR_RED = "#F44336"
    COLOR_LIGHT = '#E8F5E9'
    COLOR_BLUE = '#BBDEFB'
    COLOR_BLACK = 'black'

    QUERY_MODELTASK = """SELECT prj_name, tsk_name, wp_activity, wp_assignee, wp_total_wl, wp_id, tsk_id, prj_id
                                    FROM workpackage
                                    INNER JOIN task ON workpackage.wp_taskid = task.tsk_id
                                    INNER JOIN project ON task.tsk_projectid = project.prj_id
                                    ORDER BY prj_id, tsk_id, wp_activity, wp_id
                                        """

    def __init__(self):
        return

    @staticmethod
    def get_weeknb(date):
        return

    @staticmethod
    def get_year(date):
        return

    @staticmethod
    def datetxt_to_date(datetxt:str=None):
        t_date = datetxt.split(DATE_SEP)
        #year month day
        date = datetime.date(int(t_date[0]), int(t_date[1]), int(t_date[2]))
        return date

    @staticmethod
    def date_to_datetxt(i_date=None):
        if not i_date:
            i_date = datetime.date.today()
        date_txt = str(i_date.year) + DATE_SEP + str(i_date.month)+ DATE_SEP + str(i_date.day)
        return date_txt

    @staticmethod
    def get_weeknb_from_date(date:datetime.date):
        return date.isocalendar()

    @staticmethod
    def make2dList(rows, cols):
        a = []
        for row in range(rows): a += [[0] * cols]
        return a

    @staticmethod
    def iso_to_gregorian(iso_year, iso_week, iso_day):
        "Gregorian calendar date for the given ISO year, week and day"
        year_start = Utils.iso_year_start(iso_year)
        return year_start + datetime.timedelta(days=iso_day - 1, weeks=iso_week - 1)

    @staticmethod
    def iso_year_start(iso_year):
        "The gregorian calendar date of the first day of the given ISO year"
        fourth_jan = datetime.date(iso_year, 1, 4)
        delta = datetime.timedelta(fourth_jan.isoweekday() - 1)
        return fourth_jan - delta

    @staticmethod
    def get_default_min_date():
        today = datetime.date.today()
        delta = datetime.timedelta(weeks=5)
        return today - delta

    @staticmethod
    def get_default_max_date():
        today = datetime.date.today()
        delta = datetime.timedelta(weeks=5)
        return today + delta

    @staticmethod
    def save_config(config_dict):
        pickle.dump(config_dict, open("config.txt", "wb"))

    @staticmethod
    def load_config():
        try:
            dic = pickle.load(open("config.txt", "rb"))
        except:
            dic = {"database_path": ""}
        return dic
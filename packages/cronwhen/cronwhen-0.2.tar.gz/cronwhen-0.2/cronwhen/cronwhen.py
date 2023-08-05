import datetime
import calendar


DELTA_1_MICROSECOND    = datetime.timedelta(microseconds=1)
DELTA_1_SECOND         = datetime.timedelta(seconds=1)
DELTA_1_MINUTE         = datetime.timedelta(seconds=60)
DELTA_1_HOUR           = datetime.timedelta(seconds=3600)
DELTA_1_DAY            = datetime.timedelta(days=1)
DELTA_AT_LEAST_1_MONTH = datetime.timedelta(days=31)

MAX_SEC_WITHOUT_RESULT = (365*4+1)*86400 #4 years

DAYS_IN_MONTH = [31,28,31,30,31,30,31,31,30,31,30,31]


#===============================================================================
class CronError(Exception):
    pass



#===============================================================================
class ExtendedDateTime():

    #---------------------------------------------------------------------------
    def now():
        now = datetime.datetime.now()
        return ExtendedDateTime(now)


    #---------------------------------------------------------------------------
    def __init__(self,date):
        self.date = date


    #---------------------------------------------------------------------------
    def add(self,timedelta):
        self.date += timedelta


    #---------------------------------------------------------------------------
    def reset_microseconds(self):
        self.date -= self.date.microsecond * DELTA_1_MICROSECOND


    #---------------------------------------------------------------------------
    def reset_seconds(self):
        self.date -= self.date.second * DELTA_1_SECOND


    #---------------------------------------------------------------------------
    def reset_minutes(self):
        self.date -= self.date.minute * DELTA_1_MINUTE


    #---------------------------------------------------------------------------
    def reset_hours(self):
        self.date -= self.date.hour * DELTA_1_HOUR


    #---------------------------------------------------------------------------
    def reset_days(self):
        self.date -= (self.date.day-1) * DELTA_1_DAY


    #---------------------------------------------------------------------------
    def reset_months(self):
        self.date = ExtendedDateTime(self.date.year,1,self.date.day,self.date.hour,self.date.minute)



#===============================================================================
class CronField:

    #---------------------------------------------------------------------------
    def __init__(self,string,first,last):
        self.first = first
        #for 'days of month' field, last is changing depending on the month we are in
        self.last = last
        self.start = None
        self.end = None
        self.any = False
        self.allowed = None
        self.mult = 1
        self.final = False

        try:
            main,mult = string.split('/')
            self.mult = int(mult)
        except:
            main = string

        if main =='*':
            if self.mult == 1:
                self.any = True
            self.start = self.first
            self.end   = self.last
        elif '-' in main:
            self.start,self.end = [int(bound) for bound in main.split('-')]
            if self.start < self.first or self.start > self.last:
                raise CronError("Field '%s' has an out of bounds number: %d is not in [%d,%d]." % (string,self.start,self.first,self.last))
            if self.end < self.first or self.end > self.last:
                raise CronError("Field '%s' has an out of bounds number: %d is not in [%d,%d]." % (string,self.end,self.first,self.last))
            if self.end < self.start:
                raise CronError("Field '%s' is an ill-written range: %d > %d." % (string,self.start,self.end))
        else:
            if ',' in main:
                self.allowed = [int(a) for a in main.split(',')]
                self.allowed.sort()
            else:
                self.allowed = [int(main)]

            for a in self.allowed:
                if a < self.first or a > self.last:
                    raise CronError("Field '%s' has an out of bounds element: %d is not in [%d,%d]." % (string,a,self.first,self.last))


    #---------------------------------------------------------------------------
    def next(self,current):
        """Return next valid value after given one for this field.

        Args:
            current (int): Starting point to find next valid value.

        Returns:
            A tuple (next_valid,increment,is_jumping): `next_valid` gives the
            next valid value allowed for this field starting at `current`,
            `increment` gives the difference between next valid value and
            current value, `is_jumping` is True iff the next valid value is
            lower than current.
        """

        # '*'
        if self.any:
            return (current, 0, False)

        next_value = None
        # 'x[,y,z,...]'
        #TODO multiplicator
        if self.allowed:
            if current > self.allowed[-1]:
                next_value = self.allowed[0]
            else:
                next_value = min([a for a in self.allowed if a >= current])
        else:
            # 'x-y'
            if current > self.end or current <= self.start:
                next_value = self.start
            else:
                x = current - self.start
                if x % self.mult:
                    next_value = current + (self.mult - x % self.mult)
                    if next_value > self.end:
                        next_value = self.start
                else:
                    next_value = current

        increment = next_value - current
        if next_value >= current:
            ret_val = (next_value,increment,False)
        else:
            self.final = True
            ret_val = (next_value,increment+(self.last-self.first+1),True)
        return ret_val



#===============================================================================
class MinutesField(CronField):

    #---------------------------------------------------------------------------
    def __init__(self,string):
        super().__init__(string,0,59)



#===============================================================================
class HoursField(CronField):

    #---------------------------------------------------------------------------
    def __init__(self,string):
        super().__init__(string,0,23)



#===============================================================================
class DaysOfWeekField(CronField):

    #---------------------------------------------------------------------------
    def __init__(self,string):
        string = (string
                .upper()
                .replace('SUN','0')
                .replace('MON','1')
                .replace('TUE','2')
                .replace('WED','3')
                .replace('THU','4')
                .replace('FRI','5')
                .replace('SAT','6'))
        super().__init__(string,0,6)



#===============================================================================
class DaysOfMonthField(CronField):

    #---------------------------------------------------------------------------
    def __init__(self,string):
        super().__init__(string,1,31)



#===============================================================================
class DaysFields():
    """Class that manages both fields 'day of month' and 'day of week'.
    """

    #---------------------------------------------------------------------------
    def __init__(self,dom_string,dow_string):
        self.dom = DaysOfMonthField(dom_string)
        self.dow = DaysOfWeekField(dow_string)


    #---------------------------------------------------------------------------
    def next(self,date):
        # If no constraint on either type of day
        if self.dom.any and self.dow.any:
            return (date.day, 0, False)

        # How many days in current month
        days_in_month = DAYS_IN_MONTH[date.month-1]
        if days_in_month == 28 and calendar.isleap(date.year):
            days_in_month = 29

        # Get next dom
        if not self.dom.any:
            # set last and end according to days in month
            self.dom.last = days_in_month
            was_none = False
            if self.dom.end is None:
                was_none = True
                self.dom.end = days_in_month
            dom_next_value,dom_increment,dom_is_jumping = self.dom.next(date.day)
            # reset end to none (meaning value depends on month) if needed
            if was_none:
                self.dom.end = None


        # Get next dow
        if not self.dow.any:
            current_dow = calendar.weekday(date.year,date.month,date.day)+1 #python's 0 is Monday, vs Sunday in cron
            current_dow %= 7
            dow_next_value,dow_increment,dow_is_jumping = self.dow.next(current_dow)
            dow_next_value_as_dom = (date.day + dow_increment) % days_in_month

        # Take the smallest increment that is not small due to 'any'
        _dont_care = None
        if self.dow.any: # if (only) dow is any, focus on dom
            return (dom_next_value,dom_increment,_dont_care)
        if self.dom.any: # if (only) dom is any, focus on dow
            return (dow_next_value_as_dom,dow_increment,_dont_care)
        if dow_increment < dom_increment : # if noone is any, get the smallest increment
            return (dow_next_value_as_dom,dow_increment,_dont_care)
        else:
            return (dom_next_value,dom_increment,_dont_care)



#===============================================================================
class MonthsField(CronField):

    #---------------------------------------------------------------------------
    def __init__(self,string):
        string = (string
                .upper()
                .replace('JAN','1')
                .replace('FEB','2')
                .replace('MAR','3')
                .replace('APR','4')
                .replace('MAY','5')
                .replace('JUN','6')
                .replace('JUL','7')
                .replace('AUG','8')
                .replace('SEP','9')
                .replace('OCT','10')
                .replace('NOV','11')
                .replace('DEC','12'))
        super().__init__(string,1,12)



#===============================================================================
class CronExpression:

    #---------------------------------------------------------------------------
    def __init__(self,cron_string):
        cron_fields = cron_string.split()
        if len(cron_fields) != 5:
            raise CronError("Ill-formatted cron expression '%s': should be composed of 5 space-separated fields." % (cron_string))
        self.string = ' '.join(cron_fields)
        self.minutes = MinutesField(cron_fields[0])
        self.hours   = HoursField(cron_fields[1])
        self.days    = DaysFields(cron_fields[2],cron_fields[4])
        self.months  = MonthsField(cron_fields[3])


    #---------------------------------------------------------------------------
    def get_next_occurrence(self,starting_point=None):
        """Get next valid point in time according to the Cron expression.

        Args:
            starting_point (datetime.datetime): Starting date from which to find
                next valid value.
        """

        if starting_point:
            now = ExtendedDateTime(starting_point)
        else:
            now = ExtendedDateTime.now()
        # Go to next minute so that now is not an answer
        # and add 1 second to be sure that a new minute
        # has not been reached during computation
        now.date += DELTA_1_MINUTE + DELTA_1_SECOND
        now.reset_microseconds()
        now.reset_seconds()
        start_date = now.date

        # Search algorithm:
        # For each field of the expression, starting with the lesser ones, find
        # the next valid value for this field. If a field changes, reset all
        # lesser fields and restart.
        # Hours and minutes are stated 'final' when they have been reset once,
        # since they then have the value of the expected final result, whatever
        # changes happen later to greater fields.
        done = False
        no_result = False
        while not done:
            # Minutes
            # if no result greater than current minute number
            increment = self.minutes.next(now.date.minute)[1]
            if increment:
                now.date += increment*DELTA_1_MINUTE

            # Hours
            increment = self.hours.next(now.date.hour)[1]
            if increment:
                if not self.minutes.final: now.reset_minutes()
                now.date += increment*DELTA_1_HOUR
                continue

            # Check we are not in an infinite loop
            # (located here since minutes and hours
            #  are never cause of an infinite loop)
            if (now.date - start_date).total_seconds() > MAX_SEC_WITHOUT_RESULT:
                no_result = True
                break

            # Days (day of month, day of week)
            increment = self.days.next(now.date)[1]
            if increment:
                if not self.minutes.final: now.reset_minutes()
                if not self.hours.final: now.reset_hours()
                now.date += increment*DELTA_1_DAY
                continue

            # Months
            next_value,increment,is_jumping = self.months.next(now.date.month)
            if increment:
                if not self.minutes.final: now.reset_minutes()
                if not self.hours.final: now.reset_hours()
                # Note: days are never final since they depend on month;
                # and we need resetting to prevent creating a date like 31/02
                now.reset_days()
                year = now.date.year+1 if is_jumping else now.date.year
                now.date = datetime.datetime(year,next_value,now.date.day,now.date.hour,now.date.minute)
                continue

            done = True

        return None if no_result else now.date

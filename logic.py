from datetime import datetime
from datetime import timedelta
from enum import Enum
from typing import Dict
from typing import List

from bot.data import text


class Days(Enum):
    MON = ("Mon", "Понеділок", 1)
    TUE = ("Tue", "Вівторок", 2)
    WED = ("Wed", "Середа", 3)
    THU = ("Thu", "Четвер", 4)
    FRI = ("Fri", "П'ятниця", 5)
    SAT = ("Sat", "Субота", 6)
    SUN = ("Sun", "Неділя", 7)

    def search_for_day(day: int):
        for day_obj in Days:
            if day_obj.value[2] == day:
                break
        return day_obj


states = {
    "no": "➖Світла не буде:",
    "maybe": "❓Можливо буде світло:",
    "yes": "💡Світло повинно бути:",
}
states_emojis = {
    "no": "➖",
    "maybe": "❓",
    "yes": "💡",
}


def getDuration(then: int, now=datetime.now(), interval="default"):
    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration: timedelta = now - then  # For build-in functions
    duration_in_s = abs(duration.total_seconds())
    print(duration_in_s)

    def years():
        return divmod(duration_in_s, 31536000)  # Seconds in a year=31536000.

    def days(seconds=None):
        return divmod(
            seconds if seconds else duration_in_s, 86400
        )  # Seconds in a day = 86400

    def hours(seconds=None):
        return divmod(
            seconds if seconds else duration_in_s, 3600
        )  # Seconds in an hour = 3600

    def minutes(seconds=None):
        return divmod(
            seconds if seconds else duration_in_s, 60
        )  # Seconds in a minute = 60

    def seconds(seconds=None):
        if seconds:
            return divmod(seconds, 1)
        return duration_in_s

    def hours_minutes():
        hour = hours()
        minute = minutes(hour[1])
        return f"{int(hour[0])} годину(-ни) {int(minute[0])} хвилин(-ни)"

    def totalDuration():
        year = years()
        day = days(year[1])  # Use remainder to calculate next variable
        hour = hours(day[1])
        minute = minutes(hour[1])
        second = seconds(minute[1])

        return "Time between dates: {} years, {} days, {} hours, {} minutes and {} seconds".format(
            int(year[0]), int(day[0]), int(hour[0]), int(minute[0]), int(second[0])
        )

    return {
        "hours_minutes": hours_minutes(),
        "years": int(years()[0]),
        "days": int(days()[0]),
        "hours": int(hours()[0]),
        "minutes": int(minutes()[0]),
        "seconds": int(seconds()),
        "default": totalDuration(),
    }[interval]


def check_for_state(
    day: int,
    current_datetime: datetime,
    schedule: dict,
    type_sched: str,
    text_to_use: str,
    hour_now: int,
    state_now: int,
    state_search: tuple,
):
    today = schedule[str(day)]

    try:
        if (type_sched == "enable" and state_now == "no") or (
            type_sched == "disable" and state_now == "yes"
        ):
            for ii in range(hour_now+1, len(today)+1):
                if today[str(ii)] == state_search[0]:
                    datetime_possible_turn: datetime = current_datetime.replace(
                        hour=ii, minute=0, second=0
                    )
                    break
            time_turn = getDuration(
                then=datetime_possible_turn, interval="hours_minutes"
            )
            for ii in range(hour_now+1, len(today)+1):
                if today[str(ii)] == state_search[1]:
                    datetime_turn: datetime = current_datetime.replace(
                        hour=ii, minute=0, second=0
                    )
                    break

            time_possible_turn = getDuration(
                then=datetime_turn, interval="hours_minutes"
            )
            msg_text = str(text[type_sched][text_to_use]).format(
                time_turn, time_possible_turn
            )
        else:
            for ii in range(hour_now+1, len(today)+1):
                if today[str(ii)] == state_search[0] or today[str(ii)] == state_search[1]:
                    datetime_turn: datetime = current_datetime.replace(
                        hour=ii, minute=0, second=0
                    )
                    break
            time_turn = getDuration(then=datetime_turn, interval="hours_minutes")
            print(time_turn)
            msg_text = str(text[type_sched][text_to_use]).format(time_turn)
    except UnboundLocalError:
        if day == 7:
            day = 1
        else:
            day += 1
        current_datetime += timedelta(days=1)
        msg_text = check_for_state(
            day=day,
            current_datetime=current_datetime,
            schedule=schedule,
            type_sched=type_sched,
            text_to_use=text_to_use,
            hour_now=0,
            state_now=state_now,
            state_search=state_search,
        )

    return msg_text


def enabling_times(day: int, schedule: Dict[str, List[int]]) -> str:
    """
    Finds how much time till turn on
    """
    today = schedule[str(day)]

    current_datetime = datetime.now()

    hour_now: int = current_datetime.hour
    state_now: int = today[str(hour_now)]

    print(state_now)
    if state_now == "yes":
        result = check_for_state(
            day=day,
            current_datetime=current_datetime,
            schedule=schedule,
            type_sched="enable",
            text_to_use="enabled",
            hour_now=hour_now,
            state_now=state_now,
            state_search=("no", "maybe"),
        )
        return result

    elif state_now == "maybe":
        result = check_for_state(
            day=day,
            current_datetime=current_datetime,
            schedule=schedule,
            type_sched="enable",
            text_to_use="certain",
            hour_now=hour_now,
            state_now=state_now,
            state_search=("yes", "гигигиги"),
        )
        return result

    elif state_now == "no":
        result = check_for_state(
            day=day,
            current_datetime=current_datetime,
            schedule=schedule,
            type_sched="enable",
            text_to_use="certposs",
            hour_now=hour_now,
            state_now=state_now,
            state_search=("yes", "maybe"),
        )
        return result


def turnoff_times(day: int, schedule: Dict[str, List[int]]) -> str:
    """
    Finds how much time till turn off
    """
    today = schedule[str(day)]

    current_datetime = datetime.now()

    hour_now: int = current_datetime.hour
    state_now: int = today[str(hour_now)]
    print(state_now)
    if state_now == "no":
        result = check_for_state(
            day=day,
            current_datetime=current_datetime,
            schedule=schedule,
            type_sched="disable",
            text_to_use="disabled",
            hour_now=hour_now,
            state_now=state_now,
            state_search=("maybe", "yes"),
        )
        return result
    elif state_now == "maybe":
        result = check_for_state(
            day=day,
            current_datetime=current_datetime,
            schedule=schedule,
            type_sched="disable",
            text_to_use="certain",
            hour_now=hour_now,
            state_now=state_now,
            state_search=("no", "гигигиги"),
        )
        return result
    elif state_now == "yes":
        result = check_for_state(
            day=day,
            current_datetime=current_datetime,
            schedule=schedule,
            type_sched="disable",
            text_to_use="certposs",
            hour_now=hour_now,
            state_now=state_now,
            state_search=("no", "maybe"),
        )
        return result


def get_time_ranges(day_to_get_time_ranges: List[int]) -> dict:
    """
    :param day_to_get_schedule: list of states for the specific day in the group
    :return: dict in the form of {state: [time_range]}
    """
    state_begin_index = 0
    state_begin = day_to_get_time_ranges["1"]
    dict_timeframes = {}
    for ii in range(1, len(day_to_get_time_ranges)+1):
        if state_begin != day_to_get_time_ranges[str(ii)]:
            try:
                dict_timeframes[state_begin].append([state_begin_index, ii - 1])
            except KeyError:
                dict_timeframes[state_begin] = [[state_begin_index, ii - 1]]
            state_begin_index = ii - 1
            state_begin = day_to_get_time_ranges[str(ii)]
        else:
            pass

        if ii == len(day_to_get_time_ranges):
            try:
                dict_timeframes[state_begin].append([state_begin_index, ii])
            except KeyError:
                dict_timeframes[state_begin] = [[state_begin_index, ii]]

    dict_timeframes = dict(sorted(dict_timeframes.items()))
    return dict_timeframes


def render_timeline_day(day: int, abstract_day: str, schedule: Dict[str, List[int]]):
    day_obj = Days.search_for_day(day=day)
    day_to_get_time_ranges = schedule[str(day)]
    msg_parts = f"Графік відключеннь на {abstract_day}: \n<b>{day_obj.value[1]}</b>\n\nУмовні позначення:\n"
    for state_num in states:
        msg_parts += states[state_num]
        msg_parts += "\n"
    msg_parts += "\n"
    time_ranges_dict = get_time_ranges(day_to_get_time_ranges=day_to_get_time_ranges)
    print(time_ranges_dict)

    # sort in chronological way
    all_time_ranges = []
    for state_num in time_ranges_dict:
        time_ranges = time_ranges_dict[state_num]
        for time_range in time_ranges:
            all_time_ranges.append(time_range)
            pass
    all_time_ranges.sort(key=lambda x: x[0])
    all_time_ranges_str = ""
    #

    # make the message text
    state_num_now = None
    for time_range in all_time_ranges:
        for state_num in time_ranges_dict:
            if time_range in time_ranges_dict[state_num]:
                state_num_now = state_num
                break
        time_begin = (
            datetime.now().replace(hour=time_range[0], minute=0)
        )
        try: 
            time_end = datetime.now().replace(hour=time_range[1], minute=0)
            dt_to_compare = time_end
        except ValueError:
            time_end = datetime.now().replace(hour=0, minute=0)
            dt_to_compare = time_begin
        time_end = time_end.strftime("%H:%M")
        time_begin = time_begin.strftime("%H:%M")
        if dt_to_compare < datetime.now() and day == datetime.now().weekday()+1:
            all_time_ranges_str += f"<strike>{time_begin} - {time_end}</strike> {states_emojis[state_num_now]}\n"
        else:
            all_time_ranges_str += (
                f"{time_begin} - {time_end} {states_emojis[state_num_now]}\n"
            )

    msg_parts += f"{all_time_ranges_str}"

    return msg_parts


def render_timeline_week(schedule: Dict[str, List[int]]):
    msg_parts = "Графік відключеннь на тиждень:\n\n Умовні позначення:\n"
    for state_num in states:
        msg_parts += states[state_num]
        msg_parts += "\n"
    msg_parts += "\n"
    for day in range(1, 7+1):
        day_obj = Days.search_for_day(day=day)
        day_to_get_schedule = schedule[str(day)]
        msg_parts += f"{day_obj.value[1]}:"
        if day == datetime.now().weekday()+1:
            msg_parts += " (Сьогодні) \n\n"
        else:
            msg_parts += "\n\n"

        time_ranges_dict = get_time_ranges(day_to_get_time_ranges=day_to_get_schedule)

        # sort in chronological way
        all_time_ranges = []
        for state_num in time_ranges_dict:
            time_ranges = time_ranges_dict[state_num]
            for time_range in time_ranges:
                all_time_ranges.append(time_range)
                pass
        all_time_ranges.sort(key=lambda x: x[0])
        all_time_ranges_str = ""
        #

        # make the message text
        state_num_now = None
        for time_range in all_time_ranges:
            for state_num in time_ranges_dict:
                if time_range in time_ranges_dict[state_num]:
                    state_num_now = state_num
                    break
            time_begin = (
                datetime.now().replace(hour=time_range[0], minute=0).strftime("%H:%M")
            )
            try: 
                time_end = datetime.now().replace(hour=time_range[1], minute=0)
            except ValueError:
                time_end = datetime.now().replace(hour=0, minute=0) 
            time_end = time_end.strftime("%H:%M")
            all_time_ranges_str += (
                f"{time_begin} - {time_end} {states_emojis[state_num_now]}\n"
            )

        msg_parts += f"{all_time_ranges_str}\n"

    return msg_parts


if __name__ == "__main__":
    pass

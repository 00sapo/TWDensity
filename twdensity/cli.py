from typing import Optional
import datetime
import subprocess
import json

def get_tw_data():
    """ run `task status:pending -WAITING export`, take stdout, and parse it (as a json) """

    output = subprocess.check_output(['task', 'status:pending', '-WAITING', 'export'])
    return json.loads(output)

def get_due_date(task: dict[str, str], all: list[dict[str, str]]) -> Optional[datetime.datetime]:
    """
    Check if "due" is defined in the task. If it is not defined, check if dependends is defined and return the due date of the last dependency.
    """
    if 'due' in task:
        return datetime.datetime.strptime(task['due'], '%Y%m%dT%H%M%SZ')
    elif 'depends' in task:
        depend_dues = []
        for uuid in task['depends']:
            for t in all:
                if t['uuid'] == uuid:
                    dep_due = get_due_date(t, all)
                    if dep_due is not None:
                        depend_dues.append(dep_due)
                    # else:
                    #     print("Task", t['description'], "has no due date inferrable")
        return max(depend_dues)
    else:
        # print("Task", task['description'], "has no due nor depends field")
        return None

def get_density_array(data: list[dict[str, str]]) -> list[float]:
    """
    Take a list of tasks, parse the due dates, and return a list containing the
    number of tasks that have due date in each day. If `weight` uda is defined, use
    its associated urgency to weight the task.
    """
    due_dates = [get_due_date(task, data) for task in data]
    due_dates = [due for due in due_dates if due is not None]
    max_due = max(due_dates)
    today = datetime.datetime.now()
    density = [0] * ( (max_due - today).days + 1 )
    for due in due_dates:
        if due is None:
            continue
        elif due < today:
            continue
        density[(due - today).days] += 1
    return density

def get_default_window() -> int:
    """ run `task show uda.densitywindow` and parse the output to get the default window """
    configs = subprocess.check_output(['task', 'show', 'uda.densitywindow']).decode().split('\n')
    for config in configs:
        if 'default' in config:
            # split by space/tab
            _, value = config.split()
            return int(value)
    return 5

def set_density(data: list[dict[str, str]], density_array: list[float]):
    """ 
    sets the density values in the `uda.density` uda of each task on the window given by
    `uda.densitywindow`. If `uda.densitywindow` is not defined, use a value of 5 days.
    """
    default_window = get_default_window()
    for d in data:
        due = get_due_date(d, data)
        if due is None:
            continue
        today = datetime.datetime.now()
        window = int(d.get('densitywindow', default_window))
        print("Using window of", window, "days")
        start = max(0, (due - today).days - window)
        end = min(len(density_array), (due - today).days + window)
        density = str(int(round(sum(density_array[start:end]))))
        if d.get('density') != density:
            d['density'] = density
            print("Task", d['description'], "set to density of", density)

def write_data(data: list[dict[str, str]]):
    """ write the data back to taskwarrior using `task import` """
    output = json.dumps(data)
    subprocess.run(['task', 'import'], input=output.encode(), stdout=subprocess.DEVNULL)

def main():
    data = get_tw_data()
    density = get_density_array(data)
    set_density(data, density)
    write_data(data)

if __name__ == '__main__':
    main()

# TWDensity

Update TaskWarrior task urgency based on the density of task dues in time

This is a simple Python script that analyzes the due dates of your tasks and counts how
many tasks have a due date in a window of time. For each task, the `density` value is
the number of tasks that have a due date near to him (i.e. in the interval [due-window, due+window]).

You can define the urgency for each density level, so the urgency of a task will
take into account the density of tasks around it.

You don't need to define the due date of all your tasks, but just the ones that are
milestones. Then, you can set dependencies of the other tasks on the milestones.

**This script takes into account dependencies.**

This is a simple method to add a time estimate to your tasks:

1. you split your tasks in smaller tasks, all requiring about the same time effort
2. you can create multiple sub-level of time effort with your UDA (e.g. writing an email
   is usally a light task, while writing a report is a heavy task)
   project)
3. you set the due date of your tasks

## Installation

1. `pipx install twdensity`
2. Add the [configuration](#example-configuration) to your `.taskrc` file

## Usage

You need to create a new UDA named `density` and define the urgency for each density
level.

You can also customize the window size for density calculation by defining a new UDA
named `densitywindow`.

To update the `density` value, simply run `twdensity` command. You can also run it as a
hook of `on-add` and `on-modify` events.

## Example configuration

```sh
uda.densitywindow.type=numeric # define the window size for density calculation
uda.densitywindow.label=DWindow
uda.densitywindow.default=5  # default value: 5

uda.density.type=numeric # define the urgency for each density level
uda.density.label=Density
urgency.uda.density.0.coefficient=0
urgency.uda.density.1.coefficient=0.17
urgency.uda.density.2.coefficient=0.33
urgency.uda.density.3.coefficient=0.5
urgency.uda.density.4.coefficient=0.67
urgency.uda.density.5.coefficient=0.83
urgency.uda.density.6.coefficient=1
urgency.uda.density.7.coefficient=1.17
urgency.uda.density.8.coefficient=1.33
urgency.uda.density.9.coefficient=1.5
urgency.uda.density.10.coefficient=1.67
urgency.uda.density.11.coefficient=1.83
urgency.uda.density.12.coefficient=2
urgency.uda.density.13.coefficient=2.17
urgency.uda.density.14.coefficient=2.33
urgency.uda.density.15.coefficient=2.5
urgency.uda.density.16.coefficient=2.67
urgency.uda.density.17.coefficient=2.83
urgency.uda.density.18.coefficient=3
urgency.uda.density.19.coefficient=3.17
urgency.uda.density.20.coefficient=3.33
urgency.uda.density.21.coefficient=3.5
urgency.uda.density.22.coefficient=3.67
urgency.uda.density.23.coefficient=3.83
urgency.uda.density.24.coefficient=4
urgency.uda.density.25.coefficient=4.17
urgency.uda.density.26.coefficient=4.33
urgency.uda.density.27.coefficient=4.5
urgency.uda.density.28.coefficient=4.67
urgency.uda.density.29.coefficient=4.83
urgency.uda.density.30.coefficient=5
```

# Group Enroll

This project concerns assigning students to groups given various constraints and preferences.
It has been directly inspired by the system working at the AGH University (Faculty of Computer Science, Electronics and Telecommunications).

## Competition :boxing_glove:

Check out the :boxing_glove: [the competition scoreboard on wiki](https://gitlab.com/agh-courses/2021-2022/constraint-programming/projects/group-enroll/-/wikis/Scoreboard/). :boxing_glove:

## Instructions

1. Fork this project into a **private** group:
2. Add @bobot-is-a-bot as the new project's member (role: `maintainer`) 
4. Read this Readme till the end for the instructions.
5. Solve the problem!
6. Automated tests will be run periodically to check quality of your model. The results will be available in the `GRADE.md`
7. If done before the deadline, contact teacher via Teams, so he can check it earlier.
8. To take part in the competition create file `competition.sol` containing solution for the `competition.dzn` instance.

## Problem Details

Imagine working in the faculty administration at the AGH UST in Krakow. Every year the same story: first you have to prepare the schedule for the whole year, later you have to assign students to the available groups. Recently your faculty started to notice the obnoxious difficulty of those tasks and tried to introduce some automation. Unfortunately it doesn't work as well as you hoped. Therefore you are going to the matter into your own hands. To be realistic, you will focus on the group assignment as it's less disruptive than the whole schedule. After spending some time under the shower and having several eureka moments, you came with the following definition of the problem.

So, first, the input has to contain the current schedule of all the involved groups[^group] over the set of days[^day]. Only then we will focus on the students[^student] and their preferences. Finally we will combine them to obtain an objective function and print the output.  

### Schedule 

Each group belongs to a class[^class][^group_class] (e.g. `Constraint Programming: Lab`) with a specified duration[^class_duration] in a well defined time unit[^time]. We also have to know which day[^group_day] and at what hour[^group_start] the groups start their activities. This way we can guarantee that student doesn't attend two different groups at the same time. We shouldn't forget about the space restrictions, each class has an upper limit for the number of students in the single group[^class_size].

Other important factor is that we have to know in what building[^location][^group_location] the group occupies the classroom, so later we can calculate the time required to move between the groups[^travel_duration]. We have to guarantee that student is able to transport between the buildings. There is defined hard limit for being late[^being_late_treshold] and it should never be breached.

Finally the schedule can change during the semester, there can be alternative weeks, some courses may to end in the middle of the semester; it's almost impossible to handle all the irregularities. Therefore we will also define what groups do not conflict each other even if they are happening at the same time according to our simplified schedule[^group_cohabitats].

### Preferences

Given the schedule, we can focus on the students[^student] and their preferences. Each student should belong to exactly one group[^group] per class[^class], but there are exceptions — more about them later...

First, we have to acknowledge an amazing fact that some students can ignore physical limits and magically teleport between locations[^student_can_teleport]. They do not care whether they have to run from one end of campus to another. Other, mundane studentshave to walk and therefore can be late to the classes.

> Being late is not ok :-1:.

Secondly, some students live at the campus and they do not care, whether they have breaks between the classes[^student_loves_breaks]. On the other hand, other would prefer to not sit at the university without any purpose.

> Wasting time on long boring breaks is not ok :-1:.

Finally, students assign preferences[^preference][^student_prefers] to the available groups; higher the preference is, more they would like to attend the group. The preference = `-1` means that this group is excluded for the given student. If all the groups of a given class are excluded for the student, it means that they do not attend this class — the exception foretold in the first paragraph of this section. 

> Being assigned to groups one does prefer is not ok :-1:.

### Objective

Given the schedule and student preferences we have to define what assignments are better than others. Obviously, every student (with already mentioned exceptions) has to be assigned to a single group of each class. Also the assignment has to be feasible (no bilocation allowed), but what makes the assignment better than others?

1. Students should not be late to their classes — they shouldn't have to run! So we have to count all the time each student is forced to be late/run and we call this total a **late disappointment**. Obviously, teleporting students[^student_can_teleport] don't care. 
2. Students should not waste their time on long boring breaks. For each student and each day we calculate the time they have to spend at the university ("end of the last group" - "start of the of the first group") and how much they spend on learning (sum all the classes' durations this day). Difference between those number is the time they have wasted. The wasted time is summed for each student and we will call this value **break disappointment**.
3. Students should not attend groups they hate. For each student and each class we calculate difference between their favorite group and the one they have been assigned. We sum those values for each student and will call this value **preference disappointment**.

Next for each student we calculate the following **total disappointment**:

**total disappointment[student]** =  **late disappointment[student]** × `late_to_disappointment_multiplier`[^late_to_disappointment_multiplier]\
                + **break disappointment[student]** × `break_to_disappointment_multiplier`[^break_to_disappointment_multiplier]\
                + **preference disappointment[student]**

Finally, our objective is to :exclamation:**minimize sum o squared total disappointments**:exclamation:

### Output

An example output is presented below:

```
assignment = [{3, 4},{1, 6},{3, 5},{2, 4},{1}];
total_late_disappointment = 3;
total_break_disappointment = 0;
total_preference_disappointment = 2;
objective = 18;
```

where:
- `assignment = ` array of sets containing groups assigned to the students, e.g. `assignment[0] = {3,4}` means that the student with index `0` has been assigned to groups `3` and `4` — notice that the last student in the example attends only a single class.
- `total_late_disappointment = ` sum of **late disappointment[student]** (before multiplying by the corresponding weight);
- `total_break_disappointment = ` sum of **break disappointment[student]** (before multiplying by the corresponding weight);
- `total_preference disappointment = ` sum of **preference disappointment[student]**;
- `objective = ` objective value.

The last four lines (objective components) will be useful for the grader script to check if your model calculates them correctly.

## Parameters Explained

[^group]: `Group` is a set containing unique identifiers of groups.
[^group_class]: `group_class` array maps groups to the corresponding classes[^class].
[^group_day]: `group_day` array defines what day[^day] the groups start.
[^group_start]: `group_start` array defines at what hour (in the instance specific time unit[^time]) the groups start.
[^group_location]: `group_location` array maps groups to their locations[^location].
[^group_cohabitats]: `group_cohabitats` array contains sets of groups[^group] can coexist at the same time.
[^class]: `Class` is a set containing unique identifiers of classes.
[^class_duration]: `class_duration` array contains classes' durations in the instance specific time unit[^time].
[^class_size]: `class_size` array contains how many students can attend a single group of this class.
[^day]: `Day` is a set containing unique identifiers of days.
[^time]: `Time` set contains available time indexes, e.g. `0` is the beginning of the day and the biggest value is the end of the day.
[^location]: `Location` is a set containing unique identifiers of locations.
[^travel_duration]: `travel_duration` matrix contains info, how long (in the instance specific time unit[^time]) it takes to move between locations (indices of the `location_name`[^location_name]).
[^being_late_treshold]: `being_late_treshold` defines what is the university policy on being late. Student has to appear at the class without exceeding this time.
[^preference]: `Preference` is a set of possible preferences over the groups, the `-1` means that the student is not allowed to be assigned to the given group.
[^student]: `Student` is a set containing unique identifiers of students.
[^student_can_teleport]: `student_can_teleport` array tells whether student cares about the distance between the building at the university.
[^student_loves_breaks]: `student_loves_breaks` array tells whether student accepts long break between the groups.
[^student_prefers]: `student_prefers` matrix contains prefences[^preference] student[^student] assigns to various groups[^group]. If all the groups of the given class have assigned the lowest preference it means that student doesn't attend this class.
[^break_to_disappointment_multiplier]: `break_to_disappointment_multiplier` is a weight associated with the "long breaks" objective component.
[^late_to_disappointment_multiplier]: `late_to_disappointment_multiplier` is a weight associated with the "being late" objective component.

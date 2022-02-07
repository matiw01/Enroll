from datetime import timedelta
from math import floor

from minizinc import Instance, Model, Solver
from random import shuffle
from time import time

if __name__ == "__main__":

    # helping fuctions

    # function updating file competition_improve.dzn
    def update_data(result, new_result):
        n = len(new_result) - 1
        n1 = len(result) - 1
        if result[n1, "objective"] > new_result[n, "objective"]:
            data = open("./data/competition_improve.dzn", "r")
            list_of_lines = data.readlines()
            S = ""
            for s in new_result[n, "GroupAssignmentB"]:
                s1 = str(s)
                s1 = s1[1:-1]
                S += s1 + ", "
            S = S[:-2]
            list_of_lines[16] = "assignmentB = array2d(Student, Group, [" + S + "]);\n"
            list_of_lines[20] = "maxObjective = " + str(new_result[n, "objective"]) + ";\n"
            a_file = open("./data/competition_improve.dzn", "w")
            a_file.writelines(list_of_lines)
            a_file.close()
            print("New solution is better (diff: ", result[n1, "objective"] - new_result[n, "objective"],
                  "; to go 'til Mati: ", new_result[n, "objective"]-35000,  ")", sep="")
            return new_result, True
        print("New solution is same or worse then old")
        return result, False


    # setting variables to relax s, c, d are number of students, classes and days to relax
    def get_relax_values(s, c, d):
        if s==-1:
            s=174
        if c==-1:
            c=13
        if d==-1:
            d=5
        # Choosing days to relax
        D = [1 for _ in range(5)]
        D_chosen = [i for i in range(5)]
        shuffle(D_chosen)
        for i in range(d):
            D[D_chosen[i]] = 0

        # Choosing Students to relax
        S = [1 for _ in range(174)]
        class_size = [15, 174, 15, 174, 15, 30, 174, 15, 174, 15, 174, 15, 174, 15, 174, 15, 174, 30, 174, 15, 174, 15,
                      174, 15, 174]
        S_chosen = [i for i in range(174)]
        shuffle(S_chosen)
        for i in range(s):
            S[S_chosen[i]] = 0

        # Choosing classes to relax
        # 13 of them are not lectures
        C = [1 for _ in range(25)]
        C_chosen = [i for i in range(25) if class_size[i] != 174]
        shuffle(C_chosen)
        for i in range(c):
            C[C_chosen[i]] = 0

        return S, C, D


    # function improving solution
    def improve_solution(instance, s, c, d, sec):
        S, C, D = get_relax_values(s, c, d)
        data = open("./data/competition_improve.dzn", "r")
        list_of_lines = data.readlines()
        # will be upgraded to f-string later or maybe not
        list_of_lines[17] = "relaxS = " + str(S) + ";\n"
        list_of_lines[18] = "relaxC = " + str(C) + ";\n"
        list_of_lines[19] = "relaxD = " + str(D) + ";\n"
        a_file = open("./data/competition_improve.dzn", "w")
        a_file.writelines(list_of_lines)
        a_file.close()

        with instance.branch() as opt:
            opt.add_file("./data/competition_improve.dzn", True)
            return opt.solve(intermediate_solutions=True, timeout=timedelta(minutes=16, seconds=sec), processes=8)


    # execution starts here

    # getting op gurobi solver
    solver = Solver.lookup("org.minizinc.mip.gurobi")

    model = Model("models/enroll_improve.mzn")
    instance = Instance(solver, model)

    i = 0
    data = open("./data/competition_improve.dzn", "r")
    list_of_lines = data.readlines()
    print("starting objective:", int(str(list_of_lines[20])[15:-2]))
    result = {(0, "objective"): int(str(list_of_lines[20])[15:-2])}

    start_time = time()
    sec = 0
    timectr = 0
    relaxctr = 0
    studentR = -1
    classR = 3
    dayR = -1
    while True:
        checkpoint = time()
        i += 1
        # 9 grup na przedmiot mniej więcej
        new_result = improve_solution(instance, min(studentR, 130), min(classR, 10), min(dayR, 5), sec)
        tdiff = time() - checkpoint
        print("number:", i, ", students: ", min(studentR, 130), ", classes", min(classR, 10), ", days: ", min(dayR, 5))
        if floor(tdiff % 60) < 10:
            print("time: ", int(tdiff // 60), ":0", floor(tdiff % 60), sep="")
        else:
            print("time: ", int(tdiff // 60), ":", floor(tdiff % 60), sep="")
        if len(new_result) > 0:
            print(new_result[len(new_result) - 1])
            result, better_result = update_data(result, new_result)
            if better_result:
                relaxctr = 0
            else:
                relaxctr += 1
        else:
            timectr += 1
            print("Did not find any solution in given time bound")

        if relaxctr == 5:  # zwiększ relaksacje
            relaxctr = 0
            if classR != -1:
                classR += 1
            if studentR != -1:
                studentR += 5
        if timectr == 1:  # zwiększ czas
            timectr = 0
            sec += 30
        print("relaxctr:", relaxctr, ", timectr", timectr)
        print("-------------------------------")

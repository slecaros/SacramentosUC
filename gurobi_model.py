import gurobipy as gp
from gurobipy import GRB
from standarize import catechists_av, catechized_av, female_catechists, male_catechists, monitors_av

print("Build data")
# campuses
campuses = [0, 1, 2, 3]
# modules => 7 modules * 5 days => 35 modules
modules = [i for i in range(35)]
# all catechized
catechized = list(catechized_av.keys())
# monitors
monitors = list(monitors_av.keys())

print("Build model")
model = gp.Model('Sacramentos')

# variables
print("Build variables")
# catechist tuple and module assign
pair = model.addVars(male_catechists, female_catechists, campuses, modules,
                     vtype=GRB.BINARY, name='pair',)
# monitor an module assign
mon = model.addVars(monitors, campuses, modules,
                    vtype=GRB.BINARY, name='assigned')
# catechized module assign
assigned = model.addVars(catechized, campuses, modules,
                         vtype=GRB.BINARY, name='mon')

# constrains
print("Build constrains")
# assigned in a valid module
model.addConstrs((pair[m, f, c, t] <= catechists_av[m][c][t]
                  for m in male_catechists
                  for f in female_catechists
                  for c in campuses
                  for t in modules), name="male_catechists valid module")

model.addConstrs((pair[m, f, c, t] <= catechists_av[f][c][t]
                  for m in male_catechists
                  for f in female_catechists
                  for c in campuses
                  for t in modules), name="female_catechists valid module")

model.addConstrs((assigned[s, c, t] <= catechized_av[s][c][t]
                  for s in catechized
                  for c in campuses
                  for t in modules), name="catechized valid module")

model.addConstrs((mon[n, c, t] <= monitors_av[n][c][t]
                  for n in monitors
                  for c in campuses
                  for t in modules), name="monitor valid module")

# no more than one time
model.addConstrs((gp.quicksum(pair[m, f, c, t] for m in male_catechists for c in campuses for t in modules) <= 1
                  for f in female_catechists), name='one time female_catechists')

model.addConstrs((gp.quicksum(pair[m, f, c, t] for f in female_catechists for c in campuses for t in modules) <= 1
                  for m in male_catechists), name='one time male_catechists')

model.addConstrs((gp.quicksum(assigned[s, c, t] for c in campuses for t in modules) <= 1
                  for s in catechized), name='one time catechized')

#  one place at time
model.addConstrs((gp.quicksum(mon[n, c, t] for c in campuses) <= 1
                  for n in monitors
                  for t in modules), name='one place monitor')

# catechists with catechized and catechized with catechists
model.addConstrs((assigned[s, c, t] <= gp.quicksum(pair[m, f, c, t] for m in male_catechists for f in female_catechists)
                  for s in catechized for c in campuses for t in modules), name='catized with catist')

model.addConstrs((pair[m, f, c, t] <= gp.quicksum(assigned[s, c, t] for s in catechized)
                  for m in male_catechists
                  for f in female_catechists
                  for c in campuses
                  for t in modules), name='catist with catized')

# pairs with monitors &vice
# model.addConstrs((gp.quicksum(pair[m, f, c, t] for m in male_catechists for f in female_catechists) == gp.quicksum(mon[n, c, t] for n in monitors)
#                   for c in campuses
#                   for t in modules))


# at least 3 catechized in module
model.addConstrs((2*assigned[s, c, t] <= gp.quicksum(assigned[s2, c, t] for s2 in catechized if s2 != s)
                  for s in catechized
                  for c in campuses
                  for t in modules), name='min groups')

# FO
print("Build FO")
obj = gp.quicksum(assigned[s, c, t] + (pair[m, f, c, t]/2)
                  for s in catechized
                  for m in male_catechists
                  for f in female_catechists
                  for c in campuses
                  for t in modules)
model.setObjective(obj, GRB.MAXIMIZE)

print("Start optimization...")
model.optimize()


# show results

def to_day(mod):
    modul = str(mod % 7 + 1)
    days = {0: 'L', 1: 'M', 2: 'W', 3: 'J', 4: 'V'}
    return days[mod//7]+modul


catzed_asigned = []
catist_assigned = []
mon_assigned = []
cps = ['sj', 'cc', 'lc', 'co']

print('confirmandos:\n')
for s in catechized:
    for c in campuses:
        for t in modules:
            if assigned[s, c, t].x > 0.5:
                catzed_asigned.append(s)
                try:
                    print(f"{s} =>  campus {cps[c]}  date  { to_day(t)}")
                except:
                    print(
                        "error ---------------------------------------------------------------------------")
print('\n\ncateqistas\n')
for m in male_catechists:
    for f in female_catechists:
        for c in campuses:
            for t in modules:
                if pair[m, f, c, t].x > 0.5:
                    try:
                        catist_assigned. append(m)
                        catist_assigned. append(f)
                        print(
                            f"{(m, f)} =>  campus {cps[c]}   date  { to_day(t)}")
                    except:
                        print(
                            "error ---------------------------------------------------------------------------")
print('\n\nmonitores')
for n in monitors:
    for c in campuses:
        for t in modules:
            if mon[n, c, t].x > 0.5:
                mon_assigned.append(n)
                try:
                    print(f"{n} =>  campus {cps[c]}  date  { to_day(t)}")
                except:
                    print(
                        "error ---------------------------------------------------------------------------")

print("*" * 30)

print('s = ', catzed_asigned)
print('m = ', catist_assigned)
print('n = ', mon_assigned)

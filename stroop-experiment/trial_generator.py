# def generate_trials(subj_code, prop_incongruent, num_trials=100):
#     '''
#     Writes a file named {subj_code_}trials.csv, one line per trial. Creates a trials subdirectory if one does not exist
#     subj_code: a string corresponding to a participant's unique subject code
#     prop_incongruent: float [0-1] corresponding to the proportion of trials that are incongruent
#     num_trials: integer specifying total number of trials (default 100)
#     '''
#     import random
#     import csv
#     import os
#     try:
#         os.mkdir('trials')
#     except FileExistsError:
#         print("Trials directory exists; proceeding to open file")
#     f = f"trials/{subj_code}_trials.csv"
    
#     n_incongruent = int(num_trials * (prop_incongruent / 100))
#     n_congruent = num_trials - n_incongruent
#     stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
    
#     c_orientations = ["upright"] * (n_congruent // 2) + ["upside_down"] * (n_congruent // 2)
#     if n_congruent % 2 == 1:
#         c_orientations.append(random.choice(["upright", "upside_down"]))
#     random.shuffle(c_orientations)
    
#     i_orientations = ["upright"] * (n_incongruent // 2) + ["upside_down"] * (n_incongruent // 2)
#     if n_incongruent % 2 == 1:
#         i_orientations.append(random.choice(["upright", "upside_down"]))
#     random.shuffle(i_orientations)
    
#     trials = []
    
#     for i in range(n_congruent):
#         word = random.choice(stimuli)
#         trial = {
#             "subj_code": subj_code,
#             "prop_incongruent": prop_incongruent,
#             "word": word,
#             "color": word,
#             "congruence": "congruent",
#             "orientation": c_orientations[i]
#         }
#         trials.append(trial)
    
#     for i in range(n_incongruent):
#         word = random.choice(stimuli)
#         available_colors = [c for c in stimuli if c != word]
#         color = random.choice(available_colors)
#         trial = {
#             "subj_code": subj_code,
#             "prop_incongruent": prop_incongruent,
#             "word": word,
#             "color": color,
#             "congruence": "incongruent",
#             "orientation": i_orientations[i]
#         }
#         trials.append(trial)
    
#     random.shuffle(trials)
    
#     with open(f, "w", newline="") as csvfile:
#         fieldnames = ["subj_code", "prop_incongruent", "word", "color", "congruence", "orientation"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(trials)
    
#     return f


def generate_trials(subj_code, seed, num_repetitions):
    '''
    Writes a file named {subj_code_}trials.csv, one line per trial. Creates a trials subdirectory if one does not exist
    subj_code: a string corresponding to a participant's unique subject code
    seed: an integer specifying the random seed
    num_repetitions: integer specifying total times that combinations of trial type (congruent vs. incongruent) and orientation (upright vs. upside_down) should repeat (total number of trials = 4 * num_repetitions)
    '''
    import random
    import csv
    import os
    try:
        os.mkdir('trials')
    except FileExistsError:
        print("Trials directory exists; proceeding to open file")
    f = f"trials/{subj_code}_trials.csv"
    
    random.seed(int(seed))
    n_incongruent = num_repetitions // 2
    n_congruent = num_repetitions - n_incongruent
    stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
    
    c_orientations = ["upright"] * (n_congruent // 2) + ["upside_down"] * (n_congruent // 2)
    if n_congruent % 2 == 1:
        c_orientations.append(random.choice(["upright", "upside_down"]))
    random.shuffle(c_orientations)
    
    i_orientations = ["upright"] * (n_incongruent // 2) + ["upside_down"] * (n_incongruent // 2)
    if n_incongruent % 2 == 1:
        i_orientations.append(random.choice(["upright", "upside_down"]))
    random.shuffle(i_orientations)
    
    trials = []
    
    for i in range(n_congruent):
        word = random.choice(stimuli)
        trial = {
            "subj_code": subj_code,
            "seed": seed,
            "word": word,
            "color": word,
            "trial_type": "congruent",
            "orientation": c_orientations[i]
        }
        trials.append(trial)
    
    for i in range(n_incongruent):
        word = random.choice(stimuli)
        available_colors = [c for c in stimuli if c != word]
        color = random.choice(available_colors)
        trial = {
            "subj_code": subj_code,
            "seed": seed,
            "word": word,
            "color": color,
            "trial_type": "incongruent",
            "orientation": i_orientations[i]
        }
        trials.append(trial)
    
    random.shuffle(trials)

    separator = ','
    header = separator.join(["subj_code", "seed", "word", 'color','trial_type','orientation'])

    with open(f, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header.split(separator), delimiter=separator)
        writer.writeheader()
        writer.writerows(trials)
    
    return f
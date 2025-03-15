import time
import sys
import random
from psychopy import visual, event, core, gui
import os
import trial_generator
import csv

def make_incongruent(color):
    other_colors = [c for c in stimuli if c != color]
    return random.choice(other_colors)

def write_data(trial, trial_num, resp, is_correct, rt):
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    data_filename = os.path.join(data_dir, f"{trial['subj_code']}_data.csv")
    file_exists = os.path.exists(data_filename)
    with open(data_filename, "a", newline="") as csvfile:
        fieldnames = ["subj_code", "seed", "word", "color", "trial_type", 
                      "orientation", "trial_num", "response", "is_correct", "RT"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "subj_code": trial["subj_code"],
            "seed": trial["seed"],
            "word": trial["word"],
            "color": trial["color"],
            "trial_type": trial["trial_type"],
            "orientation": trial["orientation"],
            "trial_num": trial_num,
            "response": resp,
            "is_correct": int(is_correct),
            "RT": rt
        })

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
valid_keys = ['r', 'o', 'y', 'g', 'b', 'q']
RTs = []
condition_RTs = {'congruent': [], 'incongruent': []}

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200])
fixation = visual.TextStim(win, text="+", height=15, color="black", pos=[0,0])
feedback = visual.TextStim(win, text="Incorrect", height=30, color="black", pos=[0,0])
timeout = visual.TextStim(win, text="Too slow", height=30, color="black", pos=[0,0])

instruction.autoDraw = True

rt_clock = core.Clock()

runtime_vars = {}
dlg = gui.Dlg(title="Stroop Task Setup")
dlg.addField('Subject Code:')
dlg.addField('Seed:')
dlg.addField('Number of repetitions:')
ok_data = dlg.show()

if not dlg.OK:
    core.quit()

runtime_vars['subj_code'] = ok_data[0]
runtime_vars['seed'] = int(ok_data[1])
runtime_vars['num_reps'] = int(ok_data[2])

data_dir = "data"
if not os.path.exists(data_dir):
    os.mkdir(data_dir)
file = os.path.join(data_dir, f"{runtime_vars['subj_code']}_data.csv")
if os.path.exists(file):
    err_dlg = gui.Dlg(title="Error")
    err_dlg.addText("Participant code already exists")
    err_dlg.show()
    core.quit()

print("Runtime variables:", runtime_vars)

trial_file = trial_generator.generate_trials(runtime_vars['subj_code'], runtime_vars['seed'], runtime_vars['num_reps'])

trials = []
with open(trial_file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for r in reader:
        trials.append(r)

for trial_num, trial in enumerate(trials, start=1):
    word_stim.setText(trial["word"])
    word_stim.setColor(trial["color"])
    
    if trial["orientation"] == "upside_down":
        word_stim.ori = 180
    else:
        word_stim.ori = 0

    placeholder.draw()
    fixation.draw()
    win.flip()
    core.wait(0.5)
    placeholder.draw()
    win.flip()
    core.wait(0.5)
    placeholder.draw()
    word_stim.draw()
    win.flip()

    rt_clock.reset()
    
    key = event.waitKeys(maxWait=2.0, keyList=valid_keys)
    rt = int(round(rt_clock.getTime() * 1000)) 

    if key is None:
        placeholder.draw()
        timeout.draw()
        win.flip()
        core.wait(1.0)
        continue

    key = key[0]

    if key == 'q':
        print(f"Reaction times (ms): {RTs}")
        win.close()
        core.quit()

    if key is None:
        resp = "None"
        is_correct = 0
        placeholder.draw()
        timeout.draw()
        win.flip()
        core.wait(1.0)
    else:
        resp = key[0]
        correct_response = trial["color"][0]
        is_correct = (resp == correct_response)
        if not is_correct:
            placeholder.draw()
            feedback.draw()
            win.flip()
            core.wait(1.0)

    print(f"Trial {trial_num}: word={trial['word']}, color={trial['color']}, orientation={trial['orientation']}, response={key}, RT={round(rt)}ms")
    write_data(trial, trial_num, resp, is_correct, rt)

    placeholder.draw()
    win.flip()
    core.wait(.15)
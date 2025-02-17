import time
import sys
import random
from psychopy import visual, event, core, gui
import os

def make_incongruent(color):
    other_colors = [c for c in stimuli if c != color]
    return random.choice(other_colors)

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
dlg.addField('Proportion Incongruent Trials:', choices=["25", "50", "75"])
ok_data = dlg.show()

if not dlg.OK:
    core.quit()

runtime_vars['subj_code'] = ok_data[0]
runtime_vars['prop_incongruent'] = int(ok_data[1])

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

while True:
    is_incongruent = random.choice([True, False])
    word = random.choice(stimuli)
    if is_incongruent:
        display_color = make_incongruent(word)
    else:
        display_color = word
        
    word_stim.setText(word)
    word_stim.setColor(display_color)
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
    rt = rt_clock.getTime() * 1000

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

    correct_response = display_color[0]
    
    if key != correct_response:
        placeholder.draw()
        feedback.draw()
        win.flip()
        core.wait(1.0)

    RTs.append(round(rt))
    if is_incongruent:
        condition_RTs['incongruent'].append(round(rt))
    else:
        condition_RTs['congruent'].append(round(rt))    

    placeholder.draw()
    win.flip()
    core.wait(.15)
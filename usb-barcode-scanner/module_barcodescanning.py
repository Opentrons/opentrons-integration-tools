#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from IPython.display import HTML, clear_output, display
from ipywidgets import IntSlider, Button, Dropdown, HBox
import json
import asyncio
import glob

jsonfiles = []
for index, file in enumerate(glob.glob("*.json")):
    jsonfiles.append(file)


def wait_for_button_change(widget1, widget2):
    future = asyncio.Future()

    def getvalue(change):
        future.set_result(change.description)
        widget1.on_click(getvalue, remove=True)
        widget2.on_click(getvalue, remove=True)
    widget1.on_click(getvalue)
    widget2.on_click(getvalue)
    return future


def wait_for_selection_change(widget, value):
    future = asyncio.Future()

    def getvalue(change):
        future.set_result(change.new)
        widget.unobserve(getvalue, value)
    widget.observe(getvalue, value)
    return future


class scan_parameters:
    def __init__(self, dslot):
        self.dslot = dslot
        self.scansdict = {}
        self.ss = ""
        self.scan_count = 0
        self.fp = None
        self.shift = False
        self.stop_scanning = "AX002VRRIOR"
        self.current = ""
        self.names = None
        self.wellnames = None


keep = Button(description="keep scan result")
discard = Button(description="discard")
roworder = Button(description="scan along rows")
columnorder = Button(description="scan along columns")
finished = Button(description="finished scanning")
notfinished = Button(description="continue scanning")
slot = IntSlider(value=12,
                 min=1,
                 max=12,
                 step=1,
                 description='Deck Slot:',
                 disabled=False,
                 continuous_update=False,
                 orientation='horizontal',
                 readout=True,
                 readout_format='d')

# keyboard characters
hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e',
       9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j',
       14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o',
       19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't',
       24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
       29: 'z', 30: '1', 31: '2', 32: '3', 33: '4',
       34: '5', 35: '6', 36: '7', 37: '8', 38: '9',
       39: '0', 44: ' ', 45: '-', 46: '=', 47: '[',
       48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~',
       54: ',', 55: '.', 56: '/'}

# shifted keyboard characters
hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F',
        10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K',
        15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P',
        20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U',
        25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z',
        30: '!', 31: '@', 32: '#', 33: '$', 34: '%',
        35: '^', 36: '&', 37: '*', 38: '(', 39: ')',
        44: ' ', 45: '_', 46: '+', 47: '{', 48: '}',
        49: '|', 51: ':', 52: '"', 53: '~', 54: '<',
        55: '>', 56: '?'}


def invert_y(y):
    return -1*(y-85)


async def f():

    # user input (deck slot)
    display(HBox([slot]))
    r = await wait_for_selection_change(slot, 'value')
    scan_state = scan_parameters(str(r))
    clear_output()
    print("Deck Slot", scan_state.dslot, "\n")

    # user input (labware definition)
    labwaredef = Dropdown(options=jsonfiles,
                          value=None,
                          description="labware:",
                          disabled=False)
    display(HBox([labwaredef]))
    m = await wait_for_selection_change(labwaredef, 'value')
    with open(m, 'r') as file:
        lbwr = file.read()
    definition = json.loads(lbwr)
    clear_output()

    # user input (scanning order)
    display(HBox([roworder, columnorder]))
    h = await wait_for_button_change(roworder, columnorder)
    if h == "scan along columns":
        scan_state.wellnames = sorted(definition['wells'].keys(),
                                      key=lambda wellname: (
                                      int(wellname[1:]), wellname[0]))
    else:
        scan_state.wellnames = sorted(definition['wells'].keys(),
                                      key=lambda wellname: (
                                      wellname[0], int(wellname[1:])))

    def well_names():
        yield from scan_state.wellnames

    clear_output()
    print("Scanning Order", h, "\n")

    # HTML display
    html = """<h1 style='color: #056608; font-family: arial narrow;'> Deck Slot {} </h1>""".format(scan_state.dslot)
    html += '<svg width="1000" height="350" viewbox="0 0 275 80">'
    for wellname in scan_state.wellnames:
        html += '''<circle r="5" style= "fill:None;stroke:black;stroke-width:.5" cx = {0} cy = {1}></circle>
        <text style="fill: #800000; font: bold 4px sans-serif" x={2} y={3}> {4} </text>'''.format(
         str(definition['wells'][wellname]['x']),
         str(invert_y(definition['wells'][wellname]['y'])),
         str(definition['wells'][wellname]['x']-12),
         str(invert_y(definition['wells'][wellname]['y'])), wellname)
    html += '</svg>'
    html += "<p style= 'font-family: arial narrow;'> Start Scanning... </p>"

    clear_output()
    display(HTML(html))
    scan_state.names = well_names()

    scan_state.current = next(scan_state.names)

    display(HTML(
     "<h1 style='color: #056608; font-family: arial narrow;'> Scanning {}... </h1>".format(
      scan_state.current)))

    while True:
        if scan_state.ss == scan_state.stop_scanning:
            display(HTML("<h1> Finished Scanning </h1>"))
            break
        if scan_state.scan_count == len(scan_state.wellnames):
            clear_output()
            display(HBox([finished, notfinished]))
            z = await wait_for_button_change(finished, notfinished)
            if z == 'finished scanning':
                display(HTML("<h1> Finished Scanning </h1>"))
                break
            else:

                # user input (deck slot)
                display(HBox([slot]))
                r = await wait_for_selection_change(slot, 'value')
                scan_state.dslot = str(r)
                clear_output()
                print("Deck Slot", scan_state.dslot, "\n")

                # user input (labware definition)
                labwaredef = Dropdown(options=jsonfiles,
                                      value=None,
                                      description="labware:",
                                      disabled=False)
                display(HBox([labwaredef]))
                m = await wait_for_selection_change(labwaredef, 'value')
                with open(m, 'r') as file:
                    lbwr = file.read()
                definition = json.loads(lbwr)
                clear_output()

                # user input (scanning order)
                display(HBox([roworder, columnorder]))
                h = await wait_for_button_change(roworder, columnorder)
                if h == "scan along columns":
                    scan_state.wellnames = sorted(definition['wells'].keys(),
                                                  key=lambda wellname: (
                                                  wellname[1:], wellname[0]))
                else:
                    scan_state.wellnames = sorted(definition['wells'].keys(),
                                                  key=lambda wellname: (
                                                  wellname[0], wellname[1:]))

                scan_state.scan_count = 0
                scan_state.scansdict = {}

                scan_state.names = well_names()
                scan_state.current = next(scan_state.names)

                # HTML display
                html = "<h1 style='color: #056608; font-family: arial narrow;'> Deck Slot {} </h1>".format(
                 scan_state.dslot)
                html += '<svg width="1000" height="350" viewbox="0 0 275 80">'
                for wellname in scan_state.wellnames:
                    html += '''<circle r="5" style= "fill:None;stroke:black;stroke-width:.5" cx = {0} cy = {1}></circle>
                    <text style="fill: #800000; font: bold 4px sans-serif" x={2} y={3}> {4} </text>'''.format(
                     str(definition['wells'][wellname]['x']),
                     str(invert_y(definition['wells'][wellname]['y'])),
                     str(definition['wells'][wellname]['x']-12),
                     str(invert_y(definition['wells'][wellname]['y'])),
                     wellname)
                html += '</svg>'

                html += "<p style='font-family: arial narrow;'> Start Scanning... </p>"
                clear_output()
                display(HTML(html))
                display(HTML(
                 "<h1 style='color: #056608; font-family: arial narrow;'> Scanning {}... </h1>".format(
                  scan_state.current)))

        with open('/dev/hidraw0', 'rb') as scan_state.fp:
            buffer = scan_state.fp.read(8)  # read device input buffer
        for c in buffer:
            if c > 0:
                if c == 40:  # 40 CR complete scan string read
                    with open('/dev/hidraw0', 'rb') as scan_state.fp:
                        scan_state.fp.flush()
                    clear_output()
                    display(HBox([keep, discard]))
                    print(scan_state.ss, "\n")
                    x = await wait_for_button_change(keep, discard)
                    if x == "keep scan result":
                        print("Writing ", scan_state.ss, " to scans.csv", "\n")
                        file = 'scans.csv'
                        with open(file, 'a') as outfile:
                            outfile.write(
                             scan_state.dslot + ',' + scan_state.current + ','
                             + scan_state.ss + '\n')  # scan string to csv
                        scan_state.scan_count += 1
                        scan_state.scansdict[
                         scan_state.current] = scan_state.ss

                        clear_output()
                        html = "<h1 style='color: #056608; font-family: arial narrow;'> Deck Slot {} </h1>".format(
                         scan_state.dslot)
                        html += '<svg width="1000" height="350" viewbox="0 0 275 80">'
                        for wellname in scan_state.wellnames:
                            html += '''<circle r="5" style= "fill:None;stroke:black;stroke-width:.5" cx = {0} cy = {1}></circle>
                            <text style="fill: #800000; font: bold 4px sans-serif" x={2} y={3}> {4} </text>
                            <text style="fill: #800000; font: bold 3px sans-serif" x={2} y={5}> {6} </text>'''.format(
                                str(definition['wells'][wellname]['x']),
                                str(
                                 invert_y(definition['wells'][wellname]['y'])),
                                str(definition['wells'][wellname]['x']-12),
                                str(
                                 invert_y(definition['wells'][wellname]['y'])),
                                wellname,
                                str(
                                 invert_y(
                                  definition['wells'][wellname]['y'])+10),
                                scan_state.scansdict.get(wellname, ''))
                        html += '</svg>'

                        clear_output()
                        display(HTML(html))
                        if scan_state.scan_count < len(scan_state.wellnames):
                            scan_state.current = next(scan_state.names)
                            display(HTML(
                             "<h1 style='color: #056608; font-family: arial narrow;'> Scanning {}... </h1>".format(
                              scan_state.current)))
                    else:
                        print("Discarding this scan ", scan_state.ss, "\n")
                    scan_state.ss = ""
                    scan_state.shift = False
                    continue
                if scan_state.shift:
                    if c == 2:  # 2 shift
                        scan_state.shift = True
                    else:
                        scan_state.ss += hid2[c]  # append shifted character
                        scan_state.shift = False
                else:
                    if c == 2:  # 2 shift
                        scan_state.shift = True
                    else:
                        scan_state.ss += hid[c]  # append character

asyncio.create_task(f())

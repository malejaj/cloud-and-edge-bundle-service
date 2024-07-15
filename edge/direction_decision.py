def direction_decision(line_percept):
    if line_percept == [0, 0, 0]:
        return 'stop'
    elif line_percept[1] == 1:
        return 'forward'
    elif line_percept[0] == 1:
        return 'right'
    elif line_percept[2] == 1:
        return 'left'
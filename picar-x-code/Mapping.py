'''
Assignee : Cap1
# Cap1 = circulation module (already implemented)
Target (Permission) : change-direction
# Mapped to circulation() function
# circulation() returns vehicle movement state (forward/left/right/stop)
Action (Permission) : execute
# Action = circulation()
# When duty is fulfilled, circulation() is executed
Duty → Action : inform
# Needs implementation: send_notification()
# This function should publish/notify the detection event __ not implemented yet
Duty → Target : data-ObjectDetected
# Mapped to detection() return
# Example: detection() -> {"object": "obstacle", "distance": 20}
Duty → informedParty : Cap1
# Receiver of the message → circulation()
# circulation() can check if object info is available
Duty → informingParty : Cap2
# Sender of the message → detection()
'''
from pyMultiwii import MultiWii
import pygame


def get_data(command, time_step_program):
    # example of 8 RC channels to be send
    return [1500, 1550, 1600, 1560, 1000, 1040, 1000, 1000]


if __name__ == "__main__":
    # init controller
    pygame.init()
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()

    board = MultiWii("/dev/ttyUSB0")

    armed = False
    running = True
    time_step_program = 0
    time_step = 0

    running_command = 0

    try:
        while running:
            new_command = running_command

            # TODO possible button press
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    print "axis_motion"
                elif event.type == pygame.JOYBUTTONDOWN:
                    button = event.button
                    print "button_press" + str(button)
                elif event.type == pygame.JOYBUTTONUP:
                    button = event.button
                    print "button_release" + str(button)
                elif event.type == pygame.JOYHATMOTION:
                    print "joy_motion"

            if new_command != running_command:
                running_command = new_command
                time_step_program = 0

            data = get_data(running_command, time_step_program)

            # New function that will receive attitude after setting the rc commands
            board.sendCMDreceiveATT(16, MultiWii.SET_RAW_RC, data)

            time_step += 1
            time_step_program += 1

            print board.attitude
        board.disarm()
    except Exception, error:
        board.disarm()
        print "Error on Main: " + str(error)

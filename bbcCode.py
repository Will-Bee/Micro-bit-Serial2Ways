answer = ""

def on_button_pressed_a():
    serial.write_line("WaitForInput")
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_data_received():
    global answer
    answer = serial.read_until(serial.delimiters(Delimiters.HASH))
    basic.show_icon(IconNames.YES)
    basic.show_string(answer)
serial.on_data_received(serial.delimiters(Delimiters.HASH), on_data_received)

def on_forever():
    basic.show_leds("""
        . . . . .
        . . # . .
        . # . # .
        . . # . .
        . . . . .
        """)
basic.forever(on_forever)

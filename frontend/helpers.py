from PySide6.QtWidgets import(
    QPushButton
)

def make_button_circle(button: QPushButton, image_width: int, bg_of_button_colour = "darkgray"):
    '''
    This function takes a button being made with a preset icon, and makes it a circle.
    needs to be a button with an icon, need to give the total width of the icon image, 
    and a colour for backing of button if you want but you can just leave it blank and 
    it will automatically become grey <3
    '''
    button.setStyleSheet(f"""
        QPushButton {{
            border: 2px solid #555;
            border-radius: {image_width // 2}px;
            background-color: {bg_of_button_colour};
        }}
        QPushButton:hover {{
            background-color: gray;
        }}
        QPushButton:pressed {{
            border-style: inset;
            background-color: {bg_of_button_colour};
        }}
        """)

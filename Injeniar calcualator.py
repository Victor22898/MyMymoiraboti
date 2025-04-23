from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
import math

Window.size = (360, 600)

KV = '''
MDBoxLayout:
    orientation: "vertical"
    padding: dp(10)
    spacing: dp(10)
    md_bg_color: app.bg_color

    MDCard:
        radius: [16, 16, 16, 16]
        size_hint_y: None
        height: dp(90)
        elevation: 8
        padding: dp(16)
        md_bg_color: app.screen_color

        MDLabel:
            id: label
            text: ""
            bold: True
            halign: "right"
            valign: "center"
            font_style: "H4"
            size_hint: 1, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            shorten: True
            shorten_from: "left"
            max_lines: 2

    Widget:
        size_hint_y: None
        height: dp(10)

    MDGridLayout:
        id: buttons
        cols: 4
        spacing: dp(8)
        adaptive_height: True
        padding: 0

    MDBoxLayout:
        size_hint_y: None
        height: dp(46)
        padding: 0, dp(6)
        MDRaisedButton:
            text: "Инженерный режим" if not app.engineer else "Обычный режим"
            on_release: app.toggle_mode()
            size_hint_x: 1
            elevation: 2
            md_bg_color: app.accent_color
            text_color: 1, 1, 1, 1
            font_size: 18
            radius: [12, 12, 12, 12]
'''

class CalculatorApp(MDApp):
    engineer = False
    bg_color = [0.12, 0.14, 0.18, 1]
    screen_color = [0.18, 0.22, 0.29, 1]
    accent_color = [0.18, 0.45, 0.87, 1]
    op_color = [0.98, 0.56, 0.15, 1]
    eng_color = [0.52, 0.25, 0.7, 1]
    num_color = [0.19, 0.67, 0.38, 1]

    def build(self):
        self.expression = ""
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.root = Builder.load_string(KV)
        self.build_buttons()
        return self.root

    def build_buttons(self):
        button_order = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"]
        ]
        eng_buttons = [
            ["(", ")", "√", "^"],
            ["sin", "cos", "tan", "log"],
        ]
        grid = self.root.ids.buttons
        grid.clear_widgets()
        # Основные кнопки
        for row in button_order:
            for label in row:
                grid.add_widget(self.mk_button(label))
        # Инженерные кнопки
        if self.engineer:
            for row in eng_buttons:
                for label in row:
                    grid.add_widget(self.mk_button(label, engineer=True))
        # Кнопка очистки, всегда последней
        grid.add_widget(self.mk_button("C", is_clear=True))

    def mk_button(self, text, engineer=False, is_clear=False):
        # Цвет кнопки
        if text in ["/", "*", "-", "+", "=", "^"]:
            color = self.op_color
        elif is_clear:
            color = [0.91, 0.23, 0.32, 1]  # Красная "C"
        elif engineer:
            color = self.eng_color
        else:
            color = self.num_color

        btn = MDRaisedButton(
            text=text,
            font_size=dp(21),
            md_bg_color=color,
            text_color=(1, 1, 1, 1),
            elevation=6,
            radius=[14, 14, 14, 14],
            on_release=self.on_button_press
        )
        return btn

    def on_button_press(self, instance):
        t = instance.text
        label = self.root.ids.label
        if t == "=":
            try:
                expr = self.expression.replace('^', '**').replace('√', 'math.sqrt')
                expr = expr.replace('sin', 'math.sin').replace('cos', 'math.cos') \
                           .replace('tan', 'math.tan').replace('log', 'math.log10')
                label.text = str(eval(expr))
                self.expression = label.text
            except Exception:
                label.text = "Ошибка"
                self.expression = ""
        elif t == "C":
            self.expression = ""
            label.text = ""
        elif t in ("sin", "cos", "tan"):
            self.expression += f"{t}(math.radians("
            label.text = self.expression
        elif t == "log":
            self.expression += f"{t}("
            label.text = self.expression
        elif t == "√":
            self.expression += "√("
            label.text = self.expression
        else:
            self.expression += t
            label.text = self.expression

    def toggle_mode(self):
        self.engineer = not self.engineer
        self.build_buttons()

if __name__ == "__main__":
    CalculatorApp().run()

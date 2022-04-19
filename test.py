from pyclbr import Function
from manim import *

def expected_attack(p, c=1, p0=0.25, q0=0.5):
    return -2 * p * p + (c + q0 - 2 * p0) * p + (c + p0) * q0 + 1


def expected_attack_max(c=1, p0=0.25, q0=0.5):
    return (c + q0 - 2 * p0) / 4


class TestScene(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0,1],
            y_range=[0,2],
            x_length=3,
            y_length=6,
            tips=False
        )
        axes_labels = axes.get_axis_labels("p", "q")

        pg_graph = axes.plot(expected_attack, color=YELLOW)

        self.add(axes, axes_labels)
        self.play(Create(pg_graph), run_time=2)

        top_x = expected_attack_max()
        top_p = axes.i2gp(top_x, pg_graph)
        top_dot = Dot(top_p, color=GREEN)
        top_rule = axes.get_vertical_line(top_p, color=GREEN)

        self.play(FadeIn(top_dot))
        self.play(GrowFromPoint(top_rule, top_p))

        p_result = MathTex(r"p=\frac{c+q_0-2p_0}{4}", color=GREEN)
        p_result.next_to(top_dot, RIGHT + UP)

        self.play(Write(p_result))
        self.wait(2)

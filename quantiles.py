from manim import *
from math import pi, sqrt, exp


def standard_uniform(x: float) -> float:
    return 1.0 / sqrt(2*pi) * exp(- x * x / 2)


class HypothesisTest(Scene):
    def construct(self):
        title = Tex("Upper Quantiles")
        self.play(FadeIn(title))
        self.wait()
        self.play(title.animate.to_corner(UP + LEFT))

        ax = Axes(
            x_range=[-4, 4.4],
            y_range=[0, standard_uniform(0) + 0.1],
            x_length=8,
            y_length=3,
            axis_config={
                'include_ticks': False
            }
        )
        ax.shift(2*LEFT)
        ax_label = ax.get_axis_labels("x", "f(x)")
        self.play(Create(ax), Write(ax_label), run_time=2)

        unif_plot = ax.plot(standard_uniform)
        self.play(Create(unif_plot))

        area1_start = ValueTracker(-4)
        area1_end = ValueTracker(area1_start.get_value())
        area1 = ax.get_area(unif_plot, x_range=[area1_start.get_value(), area1_start.get_value()], color=YELLOW, opacity=0.5)
        area1.add_updater(
            lambda x: x.become(ax.get_area(unif_plot, x_range=[area1_start.get_value(), area1_end.get_value()], color=YELLOW, opacity=0.5))
        )
        self.add(area1)
        self.play(area1_end.animate.set_value(4), run_time=2)
        
        area1_text = MathTex(r"p(x>-\infty)", "=", r"\int_{-\infty}^{\infty}", r"x\,\mathrm{d}x", "=", "1", color="Yellow")
        area1_text.next_to(ax.i2gp(2, unif_plot) + 2*UP)
        guide1_s_value = ValueTracker(1)
        guide1_s = Dot(ax.i2gp(guide1_s_value.get_value(), unif_plot), radius=0)
        guide1_s.add_updater(lambda x: x.move_to(ax.i2gp(guide1_s_value.get_value(), unif_plot)))
        guide1_e = Dot(area1_text.get_boundary_point(LEFT), radius=0)
        self.add(guide1_s, guide1_e)
        guide1 = always_redraw(lambda: Line(guide1_s.get_center(), guide1_e.get_center(), color=YELLOW))
        # guide1.add_updater(lambda x: x.become(Line(guide1_s.get_center(), guide1_e.get_center())))
        self.play(Create(guide1), Write(area1_text))
        self.wait()

        area2_text = MathTex(r"p(x>0)", "=", r"\int_{0}^{\infty}", r"x\,\mathrm{d}x", "=", "0.5", color="Yellow")
        area2_text.move_to(area1_text)
        self.play(
            area1_start.animate.set_value(0),
            ReplacementTransform(area1_text, area2_text)
        )
        self.wait()

        area3_text = MathTex(r"p(x>3)", "=", r"\int_{3}^{\infty}", r"x\,\mathrm{d}x", "=", "0.001", color="Yellow")
        area3_text.move_to(area2_text)
        self.play(
            area1_start.animate.set_value(3),
            guide1_s_value.animate.set_value(3.5),
            guide1_e.animate.move_to(Dot(area3_text[0].get_bottom())),
            ReplacementTransform(area2_text, area3_text),
        )
        self.wait()
        
        quantile3_dot = Dot(ax.coords_to_point(3, 0), color=YELLOW)
        quantile3_text = MathTex(r"x_{3}")
        quantile3_text.next_to(quantile3_dot, DOWN)
        self.play(FadeIn(quantile3_dot, quantile3_text))
        self.wait()

        x_alpha = 2
        area4_text = MathTex(r"p(x>x_\alpha)", "=", r"\int_{x_\alpha}^{\infty}", r"x\,\mathrm{d}x", "=", r"\alpha", color="Yellow")
        area4_text.move_to(area3_text)
        quantile4_text = MathTex(r"x_{\alpha}")
        quantile4_text.next_to(ax.coords_to_point(x_alpha, 0), DOWN)
        self.play(
            area1_start.animate.set_value(x_alpha),
            guide1_s_value.animate.set_value(2.3),
            guide1_e.animate.move_to(Dot(area4_text[0].get_bottom())),
            quantile3_dot.animate.move_to(ax.coords_to_point(x_alpha, 0)),
            ReplacementTransform(area3_text, area4_text),
            ReplacementTransform(quantile3_text, quantile4_text)
        )
        self.wait()

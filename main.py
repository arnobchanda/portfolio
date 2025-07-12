from textual.app import App, ComposeResult
from textual.containers import Container, HorizontalScroll, Vertical, VerticalScroll
from textual.widgets import Header, Footer, Placeholder

class Portfolio(App):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        yield HorizontalScroll(
            Container(
                VerticalScroll(
                    Placeholder("Experiance", id="exp"),
                    Placeholder("Projects", id="prj"),
                    Placeholder("Education", id="edu")
                )
            ),
            Container(Placeholder("Details", id="det"))
        )

if __name__ == "__main__":
    portfolio = Portfolio()
    portfolio.run()

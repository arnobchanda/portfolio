from textual.widget import _BorderTitle, Widget
from typing_extensions import List
from textual.app import App, ComposeResult
from textual.containers import Container 
from textual.widgets import Header, Footer, Label, ListItem, ListView, Placeholder

class LeftListBox(Widget):
    def __init__(self, borderTitle:str, labelList:List, name:str|None = None, id:str|None = None, classes:str|None = None):
        super().__init__(name=name, id=id, classes=classes)
        self.borderTitle = borderTitle
        self.labelList = labelList

    def compose(self) -> ComposeResult:
        yield ListView()

    def on_mount(self) -> None:
        listView = self.query_one(ListView)
        listView.border_title = self.borderTitle
        for label in self.labelList:
            listView.append(ListItem(Label(label)))

class Portfolio(App):
    CSS_PATH = "portfolio.tcss"

    def compose(self) -> ComposeResult:
        exp_list=["AESI Inc.", "Schneider Electric"]
        prj_list=["Indian Olympic Dream", "Portfolio"]
        edu_list=["Harrisburg University", "UMass Lowell", "GTU"]

        yield Header(show_clock=True)
        yield Footer()
        with Container(id="left"):
            yield LeftListBox(borderTitle="Experiance", labelList=exp_list)
            yield LeftListBox(borderTitle="Projects", labelList=prj_list)
            yield LeftListBox(borderTitle="Education", labelList=edu_list)
        yield Placeholder("Information")

if __name__ == "__main__":
    portfolio = Portfolio()
    portfolio.run()

from textual.widget import Widget
from typing_extensions import List
from textual.app import App, ComposeResult
from textual.containers import Container 
from textual.widgets import Header, Footer, Label, ListItem, ListView, Markdown, MarkdownViewer
from textual import on

class LeftListBox(Widget, can_focus = True):
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

class MarkdownRenderer(Widget):
    def __init__(self, filePath: str, name: str | None = None, id: str | None = None, classes: str | None = None):
        super().__init__(name=name, id=id, classes=classes)
        self.filePath = filePath

    def compose(self) -> ComposeResult:
        with open(self.filePath, "r") as f:
            content = f.read()
            yield MarkdownViewer(content, show_table_of_contents=False)

    def update_file(self, newFilePath:str) -> None:
        try:
            with open(newFilePath, "r") as f:
                content = f.read()
            self.query_one(Markdown).update(content)
        except FileNotFoundError:
            self.query_one(Markdown).update(f"# File {newFilePath} not found")

class Portfolio(App):
    CSS_PATH = "portfolio.tcss"

    FILE_MAP = {
        "About": "assets/about.md",
        "Tech Stack": "assets/tech_stack.md",
        "AESI Inc.": "assets/aesi.md",
        "Schneider Electric": "assets/se.md",
        "Indian Olympic Dream": "assets/iod.md",
        "Portfolio": "assets/portfolio.md",
        "Harrisburg University": "assets/hu.md",
        "UMass Lowell": "assets/umass.md",
        "GTU": "assets/gtu.md",
    }
 
    def compose(self) -> ComposeResult:
        abt_list=["About", "Tech Stack"]
        exp_list=["AESI Inc.", "Schneider Electric"]
        prj_list=["Indian Olympic Dream", "Portfolio"]
        edu_list=["Harrisburg University", "UMass Lowell", "GTU"]

        yield Header(show_clock=True)
        yield Footer()
        with Container(id="left"):
            yield LeftListBox(borderTitle="About", labelList=abt_list)
            yield LeftListBox(borderTitle="Experience", labelList=exp_list)
            yield LeftListBox(borderTitle="Projects", labelList=prj_list)
            yield LeftListBox(borderTitle="Education", labelList=edu_list)
        yield MarkdownRenderer("assets/about.md", id="details-view")
    
    @on(ListView.Highlighted)
    @on(ListView.Selected)
    def update_markdown_view(self, event) -> None:

        selectedText = event.item.query_one(Label).renderable
        filePath = self.FILE_MAP.get(str(selectedText))

        if filePath:
            mdRender = self.query_one("#details-view", MarkdownRenderer)
            mdRender.update_file(filePath)


if __name__ == "__main__":
    portfolio = Portfolio()
    portfolio.run()

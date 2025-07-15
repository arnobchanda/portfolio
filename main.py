from textual.widget import Widget
from typing_extensions import List
from textual.app import App, ComposeResult
from textual.containers import Container, HorizontalScroll 
from textual.widgets import Button, Header, Footer, Label, ListItem, ListView, Markdown, MarkdownViewer
from textual import on
import webbrowser

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

class MarkdownRenderer(Widget):
    def __init__(self, filePath: str, name: str | None = None, id: str | None = None, classes: str | None = None):
        super().__init__(name=name, id=id, classes=classes)
        self.filePath = filePath

    def compose(self) -> ComposeResult:
        with open(self.filePath, "r") as f:
            content = f.read()
            yield MarkdownViewer(content, show_table_of_contents=False, open_links=False)

    def update_file(self, newFilePath:str) -> None:
        try:
            with open(newFilePath, "r") as f:
                content = f.read()
            self.query_one(Markdown).update(content)
        except FileNotFoundError:
            self.query_one(Markdown).update(f"# File {newFilePath} not found")

    # @on(Markdown.LinkClicked)

class Portfolio(App):
    CSS_PATH = "portfolio.tcss"

    BINDINGS = [
        ("1", "focus_section('abt')", "About"),
        ("2", "focus_section('exp')", "Experience"),
        ("3", "focus_section('prj')", "Projects"),
        ("4", "focus_section('edu')", "Education"),
    ]

    FILE_MAP = {
        "👤 About": "assets/about.md",
        "🧰 Tech Stack": "assets/tech_stack.md",
        "💼 AESI Inc.": "assets/aesi.md",
        "💼 Schneider Electric": "assets/se.md",
        "🏅 Indian Olympic Dream": "assets/iod.md",
        "🗂️ Portfolio": "assets/portfolio.md",
        "🎓 Harrisburg University": "assets/hu.md",
        "🎓 UMass Lowell": "assets/umass.md",
        "🎓 GTU": "assets/gtu.md",
    }
 
    def compose(self) -> ComposeResult:
        abt_list=["👤 About", "🧰 Tech Stack"]
        exp_list=["💼 AESI Inc.", "💼 Schneider Electric"]
        prj_list=["🏅 Indian Olympic Dream", "🗂️ Portfolio"]
        edu_list=["🎓 Harrisburg University", "🎓 UMass Lowell", "🎓 GTU"]

        yield Header(show_clock=True)
        yield Footer()
        with Container(id="left"):
            yield LeftListBox(borderTitle="About", labelList=abt_list, id="abt")
            yield LeftListBox(borderTitle="Experience", labelList=exp_list, id="exp")
            yield LeftListBox(borderTitle="Projects", labelList=prj_list, id="prj")
            yield LeftListBox(borderTitle="Education", labelList=edu_list, id="edu")
        with Container(id="right"):
            yield MarkdownRenderer("assets/about.md", id="details-view")
            with HorizontalScroll(id="socials"):
                yield Container(
                    Button(label="🐙 GitHub", id="github"),
                    Button(label="🔗 LinkedIn", id="linkedin"),
                    Button(label="🐦 X (twitter)", id="twitter"),
                    id="social-buttons"
                )
    
    @on(ListView.Highlighted)
    @on(ListView.Selected)
    def update_markdown_view(self, event) -> None:
        selectedText = event.item.query_one(Label).renderable
        filePath = self.FILE_MAP.get(str(selectedText))
        if filePath:
            mdRender = self.query_one("#details-view", MarkdownRenderer)
            mdRender.update_file(filePath)

    def action_focus_section(self, section_id:str) -> None:
        section = self.query_one(f"#{section_id}")
        list_view = section.query_one(ListView)
        list_view.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        link_map = {
            "github": "https://github.com/arnob-chanda",
            "linkedin": "https://www.linkedin.com/in/arnob-chanda",
            "twitter": "https://twitter.com/arnobchanda"
        }
        if event.button.id in link_map:
            webbrowser.open(link_map[event.button.id])


if __name__ == "__main__":
    portfolio = Portfolio()
    portfolio.run()

import os
from collections.abc import Iterator
from typing import Annotated

from IPython.display import Image, display
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from app.ai.settings import llm_settings


class State(TypedDict):
    messages: Annotated[list, add_messages]


class ChatbotGraph:
    def __init__(self, llm_type: str = "AzureChatOpenAI", verbose: bool = False):
        self.graph_builder = StateGraph(State)
        self.llm = llm_settings(llm_type=llm_type, verbose=verbose)
        self._initialize_graph()

    def _initialize_graph(self) -> None:
        self.graph_builder.add_node("chatbot", self.chatbot)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        self.graph = self.graph_builder.compile()

    def chatbot(self, state: State) -> dict:
        return {"messages": [self.llm.invoke(state["messages"])]}

    def draw_graph(self, output_file: str | None = None) -> None:
        try:
            if output_file is None:
                this_dir = os.path.dirname(os.path.abspath(__file__))
                output_file = f"{this_dir}/graph.png"
            display(Image(self.graph.get_graph().draw_mermaid_png(output_file_path=output_file)))
        except Exception as e:
            raise ValueError("グラフの描画に失敗しました。") from e

    def stream_graph_updates(self, user_input: str) -> Iterator[str]:
        for event in self.graph.stream({"messages": [("user", user_input)]}):
            for value in event.values():
                # print("Assistant:", value["messages"][-1].content)
                yield value["messages"][-1].content
        # yield from self.graph.stream({"messages": [("user", user_input)]}, stream_mode="values")


if __name__ == "__main__":
    chatbot_graph = ChatbotGraph(verbose=True)


    chatbot_graph.draw_graph()

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            for response in chatbot_graph.stream_graph_updates(user_input):
                print("Assistant:", response)
        except Exception as e:
            raise ValueError("ストリーム更新に失敗しました。") from e


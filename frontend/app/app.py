import os
import gradio as gr
import requests
import pandas as pd
from typing import Tuple


def search_stories(query: str, page: int) -> Tuple[pd.DataFrame, int]:
    """
    Search stories from local API and return results as DataFrame
    """
    try:
        response = requests.post(
            url=os.environ.get("API_URL", "http://50.18.255.74:8600/search"),
            json={"query": query, "page": page},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

        # Convert response data to DataFrame
        data = response.json()["hits"]
        df = pd.DataFrame(data)

        # Reorder columns for better display
        columns = ["title", "author", "story_text", "created_at", "points"]
        df = df[columns]

        return df, page
    except requests.RequestException as e:
        print(e)
        return pd.DataFrame(), page


def next_page(query: str, current_page: int) -> Tuple[pd.DataFrame, int]:
    """
    Load next page of results
    """
    next_page = current_page + 1
    return search_stories(query, next_page)


# Create Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# Story Search")

    # Input components
    with gr.Row():
        query_input = gr.Textbox(
            label="Search Query", placeholder="Enter search terms..."
        )
        page_state = gr.State(value=0)

    # Search button
    search_btn = gr.Button("Search")

    # Results display
    results_df = gr.DataFrame(label="Search Results", interactive=False, wrap=True)

    # Next page button
    next_btn = gr.Button("Next Page")

    # Handle search button click
    search_btn.click(
        fn=search_stories,
        inputs=[query_input, page_state],
        outputs=[results_df, page_state],
    )

    # Handle next page button click
    next_btn.click(
        fn=next_page, inputs=[query_input, page_state], outputs=[results_df, page_state]
    )

if __name__ == "__main__":
    app.launch()

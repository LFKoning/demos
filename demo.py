import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    from itertools import combinations_with_replacement

    import marimo as mo
    import pandas as pd
    import altair as alt
    return alt, combinations_with_replacement, mo, pd


@app.cell
def _(mo):
    dice = mo.ui.slider(start=1, stop=10, label="Number of dice:")
    dice
    return (dice,)


@app.cell
def _(alt, combinations_with_replacement, dice, pd):
    combinations = combinations_with_replacement(range(1, 7), r=dice.value)
    probs = pd.DataFrame({"result": map(sum, combinations)}).value_counts(normalize=True).reset_index()
    alt.Chart(probs).mark_bar().encode(x="result", y="proportion")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

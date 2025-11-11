import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    option_1 = """
    Top level 1:
        w: 0.5

        Sub level 1.1:
            w: 0.3

            Indicator 1.1.A:
                w: 0.2
            Indicator 1.1.B:
                w: 0.8

        Sub level 1.2:
            w: 0.7

            Indicator 1.2.A:
                w: 1.0

    Top level 2:
        w: 0.5

        Indicator 2.A:
            w: 1.0
    """
    return


@app.cell
def _():
    option_2 = """
    structure:
        Top level 1:
            Sub level 1.1:
                Indicator 1.1.A
                Indicator 1.1.B
            Sub level 1.2:
                Indicator 1.2.A
        Top level 2:
            Indicator 2.A

    weights:
        Top level 1:     0.5
        Top level 2:     0.5

        Sub level 1.1:   0.3
        Sub level 1.2:   0.7

        Indicator 1.1.A: 0.2
        Indicator 1.1.B: 0.8

        Indicator 1.2.A: 1.0

        Indicator 2.A:   1.0
    """
    return


@app.cell
def _():
    option_3 = """
    Main:
        Top level 1: 0.5
        Top level 2: 0.5

    Top level 1:
        Sub level 1.1: 0.3
        Sub level 1.2: 0.7

    Sub level 1.1:
        Indicator 1.1.A: 0.2
        Indicator 1.1.B: 0.8

    Sub level 1.2:
        Indicator 1.2.A: 1.0

    Top level 2:
        Indicator 2.A: 1.0
    """
    return (option_3,)


@app.cell
def _():
    import yaml
    from typing import Self

    from pydantic import BaseModel
    return BaseModel, Self, yaml


@app.cell
def _(option_3, yaml):
    blueprint = yaml.safe_load(option_3)
    blueprint
    return (blueprint,)


@app.cell
def _():
    # Assume indicator scores have been built.
    indicators = {
        "Indicator 1.1.A": 1,
        "Indicator 1.1.B": 2,
        "Indicator 1.2.A": 3,
        "Indicator 2.A": 4,
    }
    return


@app.cell
def _(BaseModel, Self):
    class ModelItem(BaseModel):
        name: str
        weight: float | None = None
        children: list[Self] = []
    return (ModelItem,)


@app.cell
def _(ModelItem, blueprint):
    # Build the tree in a forward pass.
    mapping = {}


    for name, children in blueprint.items():
        if name not in mapping:
            item = ModelItem(name=name)
            mapping[name] = item
        else:
            item = mapping[name]

        for name, weight in children.items():
            child = ModelItem(name=name, weight=weight)
            if name not in mapping:
                mapping[name] = child
            item.children.append(child)

    return (mapping,)


@app.cell
def _(mapping):
    mapping["Main"].children[0].children[0].children
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

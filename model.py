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
    return (indicators,)


@app.cell
def _(BaseModel, Self):
    class ModelItem(BaseModel):
        name: str
        weight: float = 1.0
        value: float | None = None
        score: float | None = None

        children: list[Self] | None = None

        def resolve(self):
            if self.children:
                self.score = sum([child.resolve() for child in self.children])
                return self.score
            else:
                self.score = self.weight * self.value
                return self.score
    return (ModelItem,)


@app.cell
def _(ModelItem, blueprint, indicators):
    def make_items(name, weight=1.0):
        if name in blueprint:
            children = [
                make_items(name=name, weight=weight) for name, weight in blueprint[name].items()
            ]
            return ModelItem(name=name, weight=weight, children=children)

        elif name in indicators:
            return ModelItem(name=name, weight=weight, value=indicators[name])

    return (make_items,)


@app.cell
def _(make_items):
    main_item = make_items("Main")
    main_item.model_dump()
    return (main_item,)


@app.cell
def _(main_item):
    main_item.resolve()
    return


@app.cell
def _(main_item):
    main_item.model_dump()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

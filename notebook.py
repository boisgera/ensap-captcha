import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    from pathlib import Path
    return (Path,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    import PIL
    return PIL, np, plt


@app.cell
def _(PIL, Path):
    image_files = list(Path("captchas").glob("*.png"))
    image = PIL.Image.open(image_files[1])
    image
    return (image,)


@app.cell
def _():
    return


@app.cell
def _(image, np):
    array = np.array(image)
    array
    return (array,)


@app.cell
def _(array):
    array.shape, array.dtype
    return


@app.cell
def _(array):
    R, G, B, A = array[..., 0], array[..., 1], array[..., 2], array[..., 3]
    return A, B, G, R


@app.cell
def _(R, plt):
    plt.imshow(R, cmap="Reds")
    plt.gcf()
    return


@app.cell
def _(G, plt):
    plt.imshow(G, cmap="Greens")
    plt.gcf()
    return


@app.cell
def _(B, plt):
    plt.imshow(B, cmap="Blues")
    plt.gcf()
    return


@app.cell
def _(A, plt):
    plt.imshow(A, cmap="Greys")
    plt.gcf()
    return


@app.cell
def _(PIL, np):
    def to_greyscale(filename):
        output_name = str(filename).replace(".png", ".grey.png")
        array = np.array(PIL.Image.open(filename))
        alpha = 255 - array[..., 3]
        PIL.Image.fromarray(alpha).save(output_name)
    return (to_greyscale,)


@app.cell
def _(Path, to_greyscale):
    for image_name in Path("captchas").glob("*.png"):
        if ".grey" not in str(image_name):
            to_greyscale(image_name)
    return


if __name__ == "__main__":
    app.run()

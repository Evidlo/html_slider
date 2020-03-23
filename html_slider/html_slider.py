from pathlib import Path
import imageio
from shutil import rmtree
from itertools import product
import pkg_resources

def html_slider(x, imsize=300, output='out', labels=None):
    """Create slider html and image directory

    Args:
        x (ndarray): (..., m, n) array of images of size m x n.
            Leading axes are taken to be slider dimensions
        imsize (int): size of saved images
        output (str): output directory of images

    """

    output = Path(output)

    template_str = pkg_resources.resource_string(__name__, 'template.html').decode('utf8')
    slider_str = pkg_resources.resource_string(__name__, 'slider.html').decode('utf8')

    # compute slider sizes
    num_sliders = len(x.shape) - 2
    assert num_sliders >= 0, "array must be 3D or larger"
    slider_sizes = x.shape[:num_sliders]

    if labels is None:
        labels = [""] * num_sliders
    assert len(labels) == num_sliders, "Incorrect number of labels"

    # create slider html
    slider_html = []
    for n, (s, l) in enumerate(zip(slider_sizes, labels)):
        slider_html.append(slider_str.format(
            slider_num=n,
            slider_size=s - 1,
            slider_label=l
        ))
    slider_html = '\n'.join(slider_html)

    # save images to output dir
    if output.exists():
        rmtree(output)

    output.mkdir()

    # for index in np.ndindex(slider_sizes):
    slider_product = product(*[range(n) for n in slider_sizes])
    for index in slider_product:
        filename = ''.join(map(str, index)) + '.bmp'
        imageio.imwrite(output.joinpath(filename).as_posix(), x[index])

    html = template_str.format(
        output_dir=output,
        slider_html=slider_html,
        imsize=imsize
    )

    open(output.with_suffix('.html'), 'w').write(html)


def render_pandas(df, imsize=300, output='out', *, slider_cols, im_col):
    """Create slider html and image directory

    Args:
        df (pandas.DataFrame): dataframe of images
        imsize (int): size of saved images
        output (str): output directory of images
    """

    df = df.sort_values(slider_cols)
    output = Path(output)

    template_str = pkg_resources.resource_string(__name__, 'template.html').decode('utf8')
    slider_str = pkg_resources.resource_string(__name__, 'slider.html').decode('utf8')

    # compute slider sizes
    num_sliders = len(slider_cols)
    assert num_sliders >= 0, "slider_cols should be nonzero"
    slider_vals = product(*[df[sc].unique() for sc in slider_cols])
    slider_sizes = [len(df[sc].unique()) for sc in slider_cols]
    slider_indices = product(*[range(n) for n in slider_sizes])

    slider_vals_js = [df[sc].unique() for sc in slider_cols]
    slider_js = [list(df[sc].unique().astype(str)) for sc in slider_cols]

    # create slider html
    slider_html = []
    for n, (s, l) in enumerate(zip(slider_sizes, slider_cols)):
        slider_html.append(slider_str.format(
            slider_num=n,
            slider_size=s - 1,
            slider_label=l
        ))
    slider_html = '\n'.join(slider_html)

    # save images to output dir
    if output.exists():
        rmtree(output)

    output.mkdir()

    for index, vals in zip(slider_indices, slider_vals):
        filename = ''.join(map(str, index)) + '.bmp'
        query_string = ' and '.join(['{}=={}'.format(col, val) for col, val in zip(slider_cols, vals)])
        rows = df.query(query_string)
        if len(rows) > 0:
            img = rows.iloc[0][im_col]
        imageio.imwrite(output.joinpath(filename).as_posix(), img)

    html = template_str.format(
        output_dir=output,
        slider_html=slider_html,
        imsize=imsize,
        slider_js=slider_js
    )

    open(output.with_suffix('.html'), 'w').write(html)

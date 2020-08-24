import copy
import os
import pathlib
from typing import Any, Dict, List

import numpy as np  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore
import seaborn as sns  # type: ignore

from analysex.mapper.convert_to_matrix import convert_to_matrix
from analysex.mapper.plot_map import plot_geo_map


def plot_heatmap(
        assembly_map: List[List[Any]],
        data: Dict[str, float],
        filename: str = 'heatmap.png'
) -> None:
    matrix = copy.deepcopy(assembly_map)
    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            if matrix[i][j] in data:
                matrix[i][j] = data[matrix[i][j]]
            else:
                matrix[i][j] = 0.0

    vmin = min([column for row in matrix for column in row])
    vmax = max([column for row in matrix for column in row])

    matrix = pd.DataFrame(matrix)
    print(matrix.to_string())  # type: ignore

    mask = np.zeros_like(matrix, dtype=np.bool)
    mask[np.tril_indices_from(mask)] = True
    mask[np.diag_indices_from(mask)] = False

    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(
            matrix,
            vmin=vmin, vmax=vmax,
            center=0,
            mask=mask,
            cmap=sns.diverging_palette(220, 10, as_cmap=True),
            # square=True,
            annot=True,
            fmt='.2f',
            linewidths=.5,
        )
        ax.set_title(
            r'$Relative \ error \ 100\%\cdot\frac{Dragon5_{NFTOT}-Serpent2_{NFTOT}}{Serpent2_{NFTOT}}$',
            pad=20
        )
        ax.invert_yaxis()
        plt.savefig(filename, dpi=500, bbox_inches="tight")
        plt.show()


def plot_heatmap_label(
        assembly_map: List[List[Any]],
        data: Dict[str, float],
        title: str = '',
        filename: str = 'heatmap_label.png'
) -> None:
    matrix = copy.deepcopy(assembly_map)
    dmatrix = np.zeros_like(matrix, dtype=np.float)
    lmatrix = np.zeros_like(matrix, dtype=np.object)

    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            if matrix[i][j] in data:
                lmatrix[i][j] = f'{matrix[i][j]}\n{data[matrix[i][j]]:.2f}'
            else:
                lmatrix[i][j] = matrix[i][j]
    lmatrix[7][1] = 'CELL\nERR'  # for legend

    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            dmatrix[i][j] = data[matrix[i][j]] if matrix[i][j] in data else 0.0

    vmin = min([column for row in dmatrix for column in row])
    vmax = max([column for row in dmatrix for column in row])

    dmatrix = pd.DataFrame(dmatrix)
    print(dmatrix.to_string())
    lmatrix = pd.DataFrame(lmatrix)
    print(lmatrix.to_string())

    mask = np.zeros_like(matrix, dtype=np.bool)
    mask[np.tril_indices_from(mask)] = True
    mask[np.diag_indices_from(mask)] = False
    mask[7][1] = False  # for legend

    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(
            dmatrix,
            vmin=vmin, vmax=vmax,
            center=0,
            mask=mask,
            cmap=sns.diverging_palette(220, 10, as_cmap=True),
            # square=True,
            annot=lmatrix,
            annot_kws={"fontsize": 8},
            fmt='',
            linewidths=.5,
            xticklabels=False,
            yticklabels=False,
        )
        ax.set_title(
            '\n'.join([
                title,
                r'$Relative \ error \ 100\%\cdot\frac{Dragon5_{NFTOT}-Serpent2_{NFTOT}}{Serpent2_{NFTOT}}$'
            ]).strip(),
            pad=20
        )
        ax.invert_yaxis()

        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.show()


def plot_heatmap_label_2l_1l(
        assembly_map: List[List[Any]],
        data: Dict[str, float],
        data_1l: Dict[str, float],
        title: str = '',
        filename: str = 'heatmap_label.png'
) -> None:
    matrix = copy.deepcopy(assembly_map)
    dmatrix = np.zeros_like(matrix, dtype=np.float)
    lmatrix = np.zeros_like(matrix, dtype=np.object)

    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            if matrix[i][j] in data:
                lmatrix[i][j] = f'{matrix[i][j]}\n{data[matrix[i][j]]:.2f}\n{data_1l[matrix[i][j]]:.2f}'
            else:
                lmatrix[i][j] = matrix[i][j]
    lmatrix[7][1] = 'CELL\n2L RE\n1L RE'  # for legend

    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            dmatrix[i][j] = data[matrix[i][j]] if matrix[i][j] in data else 0.0

    vmin = min([column for row in dmatrix for column in row])
    vmax = max([column for row in dmatrix for column in row])

    dmatrix = pd.DataFrame(dmatrix)
    print(dmatrix.to_string())
    lmatrix = pd.DataFrame(lmatrix)
    print(lmatrix.to_string())

    mask = np.zeros_like(matrix, dtype=np.bool)
    mask[np.tril_indices_from(mask)] = True
    mask[np.diag_indices_from(mask)] = False
    mask[7][1] = False  # for legend

    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(
            dmatrix,
            vmin=vmin, vmax=vmax,
            center=0,
            mask=mask,
            cmap=sns.diverging_palette(220, 10, as_cmap=True),
            # square=True,
            annot=lmatrix,
            annot_kws={"fontsize": 8},
            fmt='',
            linewidths=.5,
            xticklabels=False,
            yticklabels=False,
        )
        ax.set_title(
            '\n'.join([
                title,
                r'$Relative \ error \ 100\%\cdot\frac{Dragon5_{NFTOT}-Serpent2_{NFTOT}}{Serpent2_{NFTOT}}$'
            ]).strip(),
            pad=20
        )
        ax.invert_yaxis()

        plt.savefig(filename, dpi=300, bbox_inches="tight")

        plt.gcf().set_size_inches(11.69, 8.27)
        plt.savefig(filename.replace('.png', '.pdf'), bbox_inches="tight")
        plt.show()


def plot_table(
        assembly_map: List[List[Any]],
        data: Dict[str, float],
        filename: str = 'table.png',
        label: str = '',
        title: str = ''
) -> None:
    map = copy.deepcopy(assembly_map)
    matrix = np.zeros_like(map, dtype=object)

    for i, row in enumerate(map):
        for j, column in enumerate(row):
            if map[i][j] in data:
                matrix[i][j] = (map[i][j], str(data[map[i][j]]))
            else:
                matrix[i][j] = map[i][j]

    plot_geo_map(matrix, filename=filename, label=label, title=title)


def plot_table_2l_1l(
        assembly_map: List[List[Any]],
        data_2l: Dict[str, float],
        data_1l: Dict[str, float],
        filename: str = 'table.png',
        label: str = '',
        title: str = ''
) -> None:
    map = copy.deepcopy(assembly_map)
    matrix = np.zeros_like(map, dtype=object)

    for i, row in enumerate(map):
        for j, column in enumerate(row):
            if map[i][j] in data_2l:
                matrix[i][j] = (map[i][j], str(data_2l[map[i][j]]), str(data_1l[map[i][j]]))
            else:
                matrix[i][j] = map[i][j]

    plot_geo_map(matrix, filename=filename, label=label, title=title)


if __name__ == '__main__':
    os.chdir(pathlib.Path(__file__).resolve().parent.parent.parent)

    assembly_map = """
    TI C0201 C0301     TG  C0501  C0601     TG   C0801 C0901
       C0202 C0302  C0402  C0502  C0602  C0702   C0802 C0902
             C0303  C0403  C0503  C0603  C0703   C0803 C0903
                       TG  C0504  C0604     TG   C0804 C0904
                           C0505  C0605  C0705   C0805 C0905
                                     TG  C0706   C0806 C0906
                                         C0707   C0807 C0907
                                                 C0808 C0908
                                                       C0909
                                                            
    """

    map = convert_to_matrix(assembly_map, debug=True)
    for location in [('first', 'Zero'), ('peak', 'Peak'), ('last', 'Max')]:
        for type in [('fission', 'f'), ('capture', 'c')]:
            with open(f'comp_error_{location[0]}_{type[0]}_2L.csv') as file:
                df = pd.read_csv(file, index_col=0)
                datas_2l = df.to_dict()
            with open(f'comp_error_{location[0]}_{type[0]}_1L.csv') as file:
                df = pd.read_csv(file, index_col=0)
                datas_1l = df.to_dict()
                for key in datas_2l.keys():
                    data_2l = datas_2l[key]
                    data_1l = datas_1l[key]
                    plot_table_2l_1l(map, data_2l, data_1l,
                                     filename=f'table_{key.lower()}_{location[0]}_{type[0]}.png',
                                     title=f'Assembly {key.upper()}\n {location[1]} Burnup\n {type[0].capitalize()} Reaction Map',
                                     label='''\
                            Cell Name
                            2L Relative Error
                            1L Relative Error''')
                    # plot_heatmap(map, data_2l, filename=f'hmap_{key.lower()}_{location[0]}_{type[0]}_2l.png)
                    plot_heatmap_label(
                        map, data_2l,
                        filename=f'hmap_assbly_{key.lower()}_{location[0]}_{type[0]}_2l.png',
                        title=f'$Assembly \ {key.upper()} \ {location[0].capitalize()} \ {type[0].capitalize()}$'
                    )
                    plot_heatmap_label_2l_1l(
                        map, data_2l, data_1l,
                        filename=f'hmap_assbly_{key.lower()}_{location[0]}_{type[0]}_2l_1l.png',
                        title=f'$Assembly \ {key.upper()} \ ({location[1].capitalize()} \ Burnup) \ {type[0].capitalize()} \ Reaction \ Map$'
                    )

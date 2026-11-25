#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 11:29:40 2022
@author: Alexander Mikhailov
"""
from econcan.funcs import combine_can, get_blueprint
from econcan.models.cobb_douglas import transform_cobb_douglas
from econcan.visualization.cobb_douglas import plot_cobb_douglas_3d


def main(year_base: int = 2012) -> None:
    # =========================================================================
    # Project V. Cobb--Douglas for Canada
    # =========================================================================
    # =========================================================================
    # First Figure: Exact Correspondence with 'note_incomplete_th05_2014_07_10.docx'
    # =========================================================================
    ARCHIVE_IDS = get_blueprint(year_base)
    df = combine_can(ARCHIVE_IDS)
    plot_cobb_douglas_3d(
        *df.pipe(transform_cobb_douglas, year_base=year_base),
        get_fig_map(year_base),
    )
    df.pipe(plot_cobb_douglas_3d)


if __name__ == "__main__":
    main()

from plotnine import theme_gray, theme, element_line, element_rect, element_text, element_blank, element_line

class theme_msand(theme_gray):
    """
    Personalized msand theme for plotnine.

    Parameters
    ----------
    base_size : int, optional
        Base font size. All text sizes are a scaled versions of
        the base font size. Default is 11.
    base_family : str, optional
        Base font family.
    """

    def __init__(self, base_size=11, base_family=None):
        # msand colours
        black = "#18191A"
        light_grey = "#999999"
        dark_grey = "#545454"
        sand = "#F1C761"
        white = "#FFFFFF"
        strip = "#2C2C2C"

        # Starts with theme_grey and then modify some parts
        theme_gray.__init__(self, base_size, base_family)
        self += theme(

            # Base Inherited Elements
            line=element_line(colour=dark_grey),
            rect=element_rect(fill=light_grey, colour=light_grey, linetype='solid'),
            text=element_text(family=base_family, face="plain",
                              colour=black),

            # Panel
            panel_background=element_rect(fill=white, color='None'),
            panel_border=element_rect(color=dark_grey),
            panel_grid_major=element_line(color=dark_grey, size = 0.2),
            panel_grid_minor=element_line(color=dark_grey, size = 0.1),

            # Legend
            legend_background=element_blank(),
            legend_key=element_rect(fill=white, color='None'),
            legend_box_margin=25,
            legend_position="bottom",

            # Strip (Used with multiple panels)
            strip_background=element_rect(fill=strip, color=dark_grey),
            strip_text=element_text(color=white),

            # Plot
            plot_title=element_text(colour=sand, size=base_size*1.5),
            plot_background=element_rect(fill=white, colour=white)


        )


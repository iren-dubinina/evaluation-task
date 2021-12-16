from matplotlib.patches import Rectangle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import os


class PlotsDrawer:
    """
        This class is used to compare two columns in the dataframe
    """

    def read_df(self, filename, first_label, second_label):
        """
            This method is used to read json files (as a pandas framework)
            and returns dataframe for comparison
        """
        return pd.read_json(filename)[[first_label, second_label]]

    def save_plot(self, file_path):
        """
            This method is used to save current plot by file_path
            If the file by file_path exists, this method will replace it
            Returns True if successfull
        """
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)

            plt.savefig(file_path)
            plt.clf()
            return True
        except:
            return False

    def draw_plots(self, filename, first_label, second_label, plots_folder="plots", colors=["purple", "lightblue"]):
        """
            This method:
                - reads json file with data
                - creates plots
                - returns paths to these plots
        """
        plt.ioff()
        matplotlib.style.use('ggplot')

        paths = []
        eval_df = self.read_df(filename, first_label, second_label)
        plot_path_template = f"{plots_folder}/{first_label}_{second_label}"

        if not os.path.isdir(plots_folder):
            os.mkdir(plots_folder)

        # Hist plot
        # Create legend for hist
        handles = [Rectangle((0, 0), 1, 1, color=c, ec="k") for c in colors]
        labels = [first_label, second_label]
        plt.legend(handles, labels)

        plt.hist(eval_df, color=colors)
        plot_path = f"{plot_path_template}_hist.png"
        if self.save_plot(plot_path):
            paths.append(plot_path)

        # KDE plot
        eval_df.plot.kde()
        plot_path = f"{plot_path_template}_kde.png"
        if self.save_plot(plot_path):
            paths.append(plot_path)

        # Heatmap of the first and second column
        heatmap = pd.crosstab(eval_df[first_label], eval_df[second_label])
        sns.heatmap(heatmap, annot=True, cmap="Blues")
        plot_path = f"{plot_path_template}_heatmap.png"
        if self.save_plot(plot_path):
            paths.append(plot_path)

        return paths

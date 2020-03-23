{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys\n",
    "import pandas as pd\n",
    "\n",
    "def countPlot(counts, stat='HR'):\n",
    "    \n",
    "    #Expects a dataframe with stats in different columns e.g. HR, or FDR\n",
    "    \n",
    "    #Calculate mean and std\n",
    "    mean_counts = counts.groupby(by=['landing_pad', 'condition']).mean().reset_index()\n",
    "    std_counts = counts.groupby(by=['landing_pad', 'condition']).std().reset_index()\n",
    "\n",
    "    ##Get labels\n",
    "    labels = mean_counts.landing_pad.unique()\n",
    "    \n",
    "    #Get means\n",
    "    control_mean_HR = mean_counts[mean_counts.condition.eq('control')][stat]\n",
    "    experiment_mean_HR = mean_counts[mean_counts.condition.eq('experiment')][stat]\n",
    "    \n",
    "    #Get standard deviations\n",
    "    control_std_HR = std_counts[mean_counts.condition.eq('control')][stat]\n",
    "    experiment_std_HR = std_counts[mean_counts.condition.eq('experiment')][stat]\n",
    "    \n",
    "    #Generate two colour bar plot\n",
    "    x = np.arange(len(labels))  # the label locations\n",
    "    width = 0.35  # the width of the bars\n",
    "\n",
    "    fig, ax = plt.subplots()\n",
    "    rects1 = ax.bar(x - width/2, control_mean_HR, width, label='control', yerr=control_std_HR, color='lightgrey')\n",
    "    rects2 = ax.bar(x + width/2, experiment_mean_HR, width, label='experiment', yerr=experiment_std_HR, color='green')\n",
    "\n",
    "    # Add some text for labels, title and custom x-axis tick labels, etc.\n",
    "    ax.set_ylabel(stat+' (%)')\n",
    "    #ax.set_title(\"mCherry -> Halo HitRate for different GFP&Spy Fusion Architectures\")\n",
    "    ax.set_xticks(x)\n",
    "    ax.set_xticklabels(labels)\n",
    "    ax.legend()\n",
    "\n",
    "    fig.tight_layout()\n",
    "\n",
    "    plt.show()\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "FACS_env",
   "language": "python",
   "name": "facs_env"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

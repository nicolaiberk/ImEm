# To lead or to follow?
#### Mainstream parties’ strategies and radical right success in Germany[^1].

## Summary:

The literature provides different expectations about the relationship between the emphasis of an issue through established parties, the vote share of the party 'owning' this issue (i.e. the party being associated with it), and the importance of an issue among the general public.

This project sets out to provide a new measure of the emphasis of immigration through German mainstream parties. Additionally, this data will be aggregated monthly and merged with data on public salience (from [Google Trends](https://trends.google.com/trends/?geo=DE)), and performance of the German radical right party AfD (from [PollOfPolls](https://www.politico.eu/europe-poll-of-polls/)). Lastly, the project will analyse some data using time-series regression, in order to disentangle the relationship between mainstream parties' issue emphasis of immigration, the issue's salience, and the AfD's vote share.


### The following documents are available so far:

0.  A [short theoretical introduction](https://github.com/samunico/ImEm/blob/master/00_Introduction_and_analytical_strategy.pdf) to the project that formulates some hypotheses to be tested and describes the output to be produced.
1. The code used to scrape the [links](https://github.com/samunico/ImEm/blob/master/01_LinkScraper.py);
2. The code used to scrape the [actual press releases](https://github.com/samunico/ImEm/blob/master/02_ReleaseScraper.py).
3. [Code](https://github.com/samunico/ImEm/blob/master/03_Preprocessing.py) pre-processing the text.
4. A [notebook](https://github.com/samunico/ImEm/blob/master/04_HandCoding.ipynb) showing how the training and test set for the classifier were coded.
5. A [notebook](https://github.com/samunico/ImEm/blob/master/05_Classifier.ipynb) used to train the classifier.
6. A [notebook](https://github.com/samunico/ImEm/blob/master/06_PrepareVariables.ipynb) preparing the variables for time-series estimation.
7. <span style="color:grey">The code analyzing the data to test the initially formulated hypotheses will follow soon.</span>
8. <span style="color:grey">A short conclusion about the findings.</span>

### Additionally, the collected data is provided [here](https://www.dropbox.com/sh/87o5u709h97i4t1/AAAhTJsndUEdH4KJ9FPooF6la?dl=0):

* One dataset of the speeches including the coding
* One dataset of the aggregated monthly share of mainstream parties' press releases, merged with data on the [Google searches about immigration](https://trends.google.com/trends/explore?date=all&geo=DE&q=%2Fm%2F0cbx95), as well as the [the monthly polling of the AfD vote share, based on poll of polls](https://www.politico.eu/europe-poll-of-polls/germany/).


[^1]: Special thanks to Damian Trilling who taught me the practical skills applied here in his [Big Data and Automated Content Analysis course](https://github.com/damian0604/bdaca)
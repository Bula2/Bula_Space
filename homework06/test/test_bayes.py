import csv
import pathlib

import bayes
import hackernews


def test_classification_single_words():
    x_train = [
        hackernews.clean(s).lower() for s in "The quick brown fox jumps over the lazy dog".split()
    ]
    y_train = ["NOT_ANIMAL"] * 3 + ["ANIMAL"] + ["NOT_ANIMAL"] * 4 + ["ANIMAL"]

    model = bayes.NaiveBayesClassifier()
    model.fit(x_train, y_train)

    assert model.score(x_train, y_train) == 1


def test_classification_massages_dataset():
    with (pathlib.Path(__file__).parent.parent / "data/SMSSpamCollection").open() as file:
        dataset = list(csv.reader(file, delimiter="\t"))
    msgs, targets = [], []
    for target, msg in dataset:
        msgs.append(msg)
        targets.append(target)

    msgs = [hackernews.clean(msg).lower() for msg in msgs]
    msgs_train, targets_train, msgs_test, targets_test = (
        msgs[:3900],
        targets[:3900],
        msgs[3900:],
        targets[3900:],
    )

    model = bayes.NaiveBayesClassifier()
    model.fit(msgs_train, targets_train)

    assert model.score(msgs_test, targets_test) > 0.95

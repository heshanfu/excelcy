import os
import shutil
from unittest import TestCase
from excelcy import DataTrainer
from spacy.cli import download


class BaseTestCase(TestCase):
    test_data_path = None  # type: str

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        cls.setup_class()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()
        cls.teardown_class()

    @classmethod
    def setup_class(cls):
        # set path
        current_path = os.path.dirname(os.path.abspath(__file__))
        cls.test_data_path = os.path.join(current_path, 'data')

        # download the model
        download('en')

    @classmethod
    def teardown_class(cls):
        pass

    @classmethod
    def get_test_data_path(cls, fs_path: str):
        return os.path.join(cls.test_data_path, fs_path)

    def assert_ents(self, data_path: str, train: bool = True, options: dict = None, tests: dict = None):
        data_trainer = DataTrainer(data_path=data_path, options=options)
        if train:
            data_trainer.train(auto_save=True)
        nlp = data_trainer.nlp
        for train_id, data_train in data_trainer.data_train.items():
            doc = nlp(data_train.get('text'))
            ents = set([(ent.text, ent.label_) for ent in doc.ents])
            rows = data_train.get('rows', {})
            erows = set([(row.get('subtext'), row.get('entity')) for _, row in rows.items()])

            # verify based on data
            assert erows <= ents

            # verify if test given
            test = (tests or {}).get(train_id, set())
            assert test <= ents
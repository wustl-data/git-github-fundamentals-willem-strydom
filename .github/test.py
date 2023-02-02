import os
from pathlib import Path
from importlib.util import find_spec
import datetime
import random
from unittest import mock


def test_module_exists():
    assert Path("fake_records.py").exists()


def test_faker_installed():
    assert find_spec("faker")


def test_generate():
    import fake_records

    df = fake_records.generate()
    assert len(df) == 1000
    assert {
        "First Name",
        "Last Name",
        "Birthday",
        "Email",
        "Phone Number",
    } == set(df.columns)


def test_data_folder_ignored():
    from git import Repo

    r = Repo(".")
    assert r.ignored("data")


def test_save():

    import pandas as pd
    import fake_records

    df = pd.DataFrame({"a": [1]})
    if not os.path.exists("data"):
        os.mkdir("data")
    fake_records.save(df)
    assert os.path.exists("data/fake_records.csv")
    os.remove("data/fake_records.csv")
    os.rmdir("data")


def test_load(tmp_path):
    import fake_records
    import pandas as pd

    df = pd.DataFrame(
        {
            "First Name": ["A"],
            "Last Name": ["B"],
            "Birthday": [pd.Timestamp(datetime.date(2000, 1, 1))],
            "Phone Number": ["555-555-5555"],
        },
        index=pd.Index(["example@example.com"], name="Email"),
    )
    df.to_csv(tmp_path / "test.csv")
    pd.testing.assert_frame_equal(fake_records.load(tmp_path / "test.csv"), df)


def test_assign_salaries():
    import fake_records
    import pandas as pd

    df = pd.DataFrame({"a": [1 for _ in range(1000)]})
    df = fake_records.assign_salaries(df)
    df["Salary"].min() >= 20000
    df["Salary"].max() <= 100000
    assert len(df.columns) == 2


def test_over_50k():
    import fake_records
    import pandas as pd

    df = pd.DataFrame({"Salary": [49999, 50000, 50001]})
    salaries = fake_records.over_50k(df)["Salary"]
    assert all(salaries > 50000)


def test_normalize():
    import fake_records
    import pandas as pd

    s = pd.Series([random.randint(0, 1000) for _ in range(1000000)])
    s_out = fake_records.normalize(s)
    assert s_out.mean() < 1 and s_out.mean() > -1
    assert s_out.std() > 0.9 and s_out.std() < 1.1


def test_normalize_salaries(mocker):
    import fake_records
    import pandas as pd

    normalized_spy = mocker.spy(fake_records, "normalize")
    assign_salaries_spy = mocker.spy(fake_records, "assign_salaries")

    df = pd.DataFrame({"Person": list(range(1000000))})
    df = fake_records.assign_normalized_salaries(df)
    assert df["Salary"].mean() < 1 and df["Salary"].mean() > -1
    assert df["Salary"].std() > 0.9 and df["Salary"].std() < 1.1
    assert len(df.columns) == 2
    normalized_spy.assert_called_once()
    assign_salaries_spy.assert_called_once()
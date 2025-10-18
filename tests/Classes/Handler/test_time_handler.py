import unittest.mock

from Classes.Handler.TimeHandler import TimeHandler, Task, datetime


class TestTask(unittest.TestCase):
    def test_from_dict(self):
        data: dict = {
            "time": "21:00",
            "endpoint": "brightness/set/50"
        }
        task: Task = Task.from_dict(data)

        self.assertTrue(task.time == datetime(year=1970, month=1, day=1, hour=21, minute=0))
        self.assertTrue(task.endpoint == "brightness/set/50")


class TestTimeHandler(unittest.TestCase):
    @unittest.mock.patch("time.sleep", return_value=None)
    @unittest.mock.patch.object(TimeHandler, "_request")
    @unittest.mock.patch("Classes.Handler.TimeHandler.datetime")
    def test_run(self, mock_datetime_datetime, mock_time_handler___request, _):
        tasks: list[dict] = [
            {
                "time": "21:00",
                "endpoint": "brightness/set/50"
            }
        ]

        mocked_dates: list[datetime] = [
            datetime(year=2000, month=1, day=1, hour=20, minute=50),
            datetime(year=2000, month=1, day=1, hour=21, minute=10),
            datetime(year=2000, month=1, day=2, hour=20, minute=50),
            datetime(year=2000, month=1, day=2, hour=21, minute=55)
        ]
        mock_datetime_datetime.now.side_effect = mocked_dates
        mock_datetime_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

        handler = TimeHandler(tasks)

        self.assertTrue([x.__dict__ for x in handler._tasks] == [{
            "time": datetime(year=1970, month=1, day=1, hour=21, minute=0),
            "endpoint": "brightness/set/50"
        }])

        self.called: int = 0

        def _run_once() -> bool:
            if self.called == len(mocked_dates) - 1:
                return False
            self.called += 1
            return True

        handler.run(_run_once)

        self.assertEqual([unittest.mock.call("brightness/set/50")] * 2,
                         mock_time_handler___request.call_args_list)

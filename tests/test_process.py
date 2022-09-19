import io
import pytest
from headj.process import run_headj, JSONProcessingError


class TestRunHeadj:
    """ """

    @staticmethod
    def run_run_headj(s: str, *args, **kwargs) -> str:
        infile = io.StringIO(s)
        output = io.StringIO()
        run_headj(
            infile=infile,
            output=output,
            *args,
            keep_output_open=True,
            show_stack_trace=True,
            **kwargs
        )
        return output.getvalue()

    def test_no_input(self):
        """
        poetry run headj /dev/null
        # No Output
        """
        with pytest.raises(StopIteration):
            o = self.run_run_headj("")
            assert o == ""

    def test_list_no_args(self):
        """
        poetry run headj <<- JSON
        [1,2,3,4,5]
        JSON
        # Output: [1, 2, 3, 4, 5]
        """
        o = self.run_run_headj("[1,2,3,4,5]")
        assert o == "[1, 2, 3, 4, 5]"

    def test_list_1_count(self):
        """
        poetry run headj -c 1 <<- JSON
        [1,2,3,4,5]
        JSON
        # Output: [1]
        """
        o = self.run_run_headj("[1,2,3,4,5]", count=1)
        assert o == "[1]"

    def test_list_1_count_2_skip(self):
        """
        poetry run headj -c 1 -s 2 <<- JSON
        [1,2,3,4,5]
        JSON
        # Output: [3]
        """
        o = self.run_run_headj("[1,2,3,4,5]", count=1, skip=2)
        assert o == "[3]"

    def test_list_2_count_2_skip(self):
        """
        poetry run headj -c 2 -s 2 <<- JSON
        [1,2,3,4,5]
        JSON
        # Output: [3, 4]
        """
        o = self.run_run_headj("[1,2,3,4,5]", count=2, skip=2)
        assert o == "[3, 4]"

    def test_object_1_key_context(self):
        """
        # Keys: ['foo']
        poetry run headj -k 'foo' <<- JSON
        {"foo":[1,2,3,4,5]}
        JSON
        # Output: [1, 2, 3, 4, 5]
        """
        o = self.run_run_headj('{"foo":[1,2,3,4,5]}', keys=["foo"], in_context=True)
        assert o == '{"foo": [1, 2, 3, 4, 5]}'

    def test_object_1_key(self):
        """
        # Keys: ['foo']
        poetry run headj -k 'foo' <<- JSON
        {"foo":[1,2,3,4,5]}
        JSON
        # Output: [1, 2, 3, 4, 5]
        """
        o = self.run_run_headj('{"foo":[1,2,3,4,5]}', keys=["foo"])
        assert o == "[1, 2, 3, 4, 5]"

    def test_object_2_keys_2_count_2_skip_context_format(self):
        """
        poetry run headj -k 'foo.bar' -c 2 -s 2 <<- JSON
        {"foo":{"bar":[1,2,3,4,5]}}
        JSON
        # Output: [3, 4]
        """
        o = self.run_run_headj(
            '{"foo":{"bar":[1,2,3,4,5]}}',
            keys=["foo", "bar"],
            count=2,
            skip=2,
            in_context=True,
            format_json=True,
        )
        assert (
            o
            == '{\n     "foo": {\n          "bar": [\n               3,\n'
            + "               4\n          ]\n     }\n}"
        )

    def test_object_2_keys_2_count_2_skip_context(self):
        """
        poetry run headj -k 'foo.bar' -c 2 -s 2 <<- JSON
        {"foo":{"bar":[1,2,3,4,5]}}
        JSON
        # Output: [3, 4]
        """
        o = self.run_run_headj(
            '{"foo":{"bar":[1,2,3,4,5]}}',
            keys=["foo", "bar"],
            count=2,
            skip=2,
            in_context=True,
        )
        assert o == '{"foo": {"bar": [3, 4]}}'

    def test_object_2_keys_2_count_2_skip(self):
        """
        poetry run headj -k 'foo.bar' -c 2 -s 2 <<- JSON
        {"foo":{"bar":[1,2,3,4,5]}}
        JSON
        # Output: [3, 4]
        """
        o = self.run_run_headj(
            '{"foo":{"bar":[1,2,3,4,5]}}', keys=["foo", "bar"], count=2, skip=2
        )
        assert o == "[3, 4]"

    def test_object_1_key_2_count_2_skip_context(self):
        """
        poetry run headj -k 'foo' -c 2 -s 2 <<- JSON
        {"foo":[1,2,3,4,5]}
        JSON
        # Output: [3, 4]
        """
        o = self.run_run_headj(
            '{"foo":[1,2,3,4,5]}', keys=["foo"], count=2, skip=2, in_context=True
        )
        assert o == '{"foo": [3, 4]}'

    def test_object_1_key_2_count_2_skip(self):
        """
        poetry run headj -k 'foo' -c 2 -s 2 <<- JSON
        {"foo":[1,2,3,4,5]}
        JSON
        # Output: [3, 4]
        """
        o = self.run_run_headj('{"foo":[1,2,3,4,5]}', keys=["foo"], count=2, skip=2)
        assert o == "[3, 4]"

    def test_no_input_with_key(self):
        """
        poetry run headj -k 'foo' /dev/null
        # Error: cannot unpack non-iterable NoneType object
        """
        with pytest.raises(StopIteration):
            _ = self.run_run_headj("", keys=["foo"])

    def test_incorect_first_key(self):
        """poetry run headj -k 'fooo.bar' -c 2 -s 2 <<- JSON
        {"foo":{
        "bar":[1,2,3,4,5]}
        }
        JSON
        # Error: Could not find key "fooo" in object "<TransientStreamingJSONObject: TRANSIENT, DONE>".
        """
        with pytest.raises(JSONProcessingError):
            _ = self.run_run_headj(
                """
                {"foo":{
                "bar":[1,2,3,4,5]}
                }
                """,
                keys=["fooo", "bar"],
                count=2,
                skip=2,
            )

    def test_incorrect_key(self):
        """
        poetry run headj -k 'foo' -c 2 -s 2 <<- JSON
        {"bar":[1,2,3,4,5]}
        JSON
        # Error: Could not find key "foo" in object "<TransientStreamingJSONObject: TRANSIENT, DONE>".
        """
        with pytest.raises(JSONProcessingError):
            _ = self.run_run_headj('{"bar":[1,2,3,4,5]}', keys=["foo"], count=2, skip=2)

    def test_array_with_key(self):
        """
        poetry run headj -k 'foo' <<- JSON
        [1,2,3,4,5]
        JSON
        # Error: Could not look up key "foo" in non-dictionary-object '<TransientStreamingJSONList:  #TRANSIENT, STREAMING>'.
        """
        with pytest.raises(JSONProcessingError):
            _ = self.run_run_headj("[1,2,3,4,5]", keys=["foo"])

    def test_incorrect_second_key(self):
        """
        poetry run headj -k 'foo.barz' -c 2 -s 2 <<- JSON
        {"foo":{"bar":[1,2,3,4,5]}}
        JSON
        # Error: Could not find key "barz" in object "<TransientStreamingJSONObject: TRANSIENT, DONE>".
        """
        with pytest.raises(JSONProcessingError):
            _ = self.run_run_headj(
                '{"foo":{"bar":[1,2,3,4,5]}}', keys=["foo", "barz"], count=2, skip=2
            )

    def test_incorrect_first_key_compact(self):
        """
        poetry run headj -k 'fooo.bar' -c 2 -s 2 <<- JSON
        {"foo":{"bar":[1,2,3,4,5]}}
        JSON
        # Error: Could not find key "fooo" in object "<TransientStreamingJSONObject: TRANSIENT, DONE>".
        """
        with pytest.raises(JSONProcessingError):
            _ = self.run_run_headj(
                '{"foo":{"bar":[1,2,3,4,5]}}', keys=["fooo", "bar"], count=2, skip=2
            )

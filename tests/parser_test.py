from nose.tools import *

from jsonselectjs import parse, parse_selector, JsonSelectError

def test_Selectors():
    eq_([4, [{'id': "foo"}]], parse(".foo"))
    eq_([8, [{'id': " foo "}]], parse('." foo "'))
    eq_([21, [{'a': 0, 'b': 1, 'id': "foo", 'pf': ":nth-last-child", 'type': "string"}]], parse("string.foo:last-child"))
    eq_([15, [{'id': "xxx@yyy", 'type': "string"}]], parse("string.xxx\\@yyy"))
    with assert_raises(JsonSelectError) as context:
        parse(" ")
    eq_("selector expected in ' '", context.exception.message)

    with assert_raises(JsonSelectError) as context:
        parse("")
    eq_("selector expected", context.exception.message)


def test_parseSelector():
    eq_([4, {'id': 'foo'}], parse_selector('.foo .bar', 0, {}))


def test_Combinators():
   eq_([9, [{'id': "foo"}, {'id': "bar"}]],
       parse(".foo .bar"))
   eq_([23, [",", [{'id': "foo", 'type': "string"}], [{'id': "foo", 'type': "number"}]]],
       parse("string.foo , number.foo"))
   eq_([24, [{'type': "string"}, ">", {'id': "foo"}, {'id': "bar", 'type': "number"}]],
       parse("string > .foo number.bar"))
   eq_([32, [",", [{'type': "string"}, ">", {'id': "foo"}, {'id': "bar", 'type': "number"}], [{'type': "object"}]]],
       parse("string > .foo number.bar, object"))
   eq_([
         60,
         [
           ",",
           [{'type': "string"}, ">", {'id': "foo"}, {'id': "bar", 'type': "number"}],
           [{'type': "object"}],
           [{'type': "string"}],
           [{'id': "baz bing"}],
           [{'pc': ":root"}]
         ]
       ],
       parse("string > .foo number.bar, object, string, .\"baz bing\", :root"))
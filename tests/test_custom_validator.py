from validr import Invalid, SchemaParser, validator


def test_custom_validator():

    @validator(string=False)
    def choice_validator(value, *choices):
        try:
            if value in choices:
                return value
        except:
            pass
        raise Invalid('invalid choice')

    sp = SchemaParser(validators={'choice': choice_validator})
    for value in 'ABCD':
        assert sp.parse('choice("A","B","C","D")')(value) == value
    assert sp.parse('choice&optional')(None) is None

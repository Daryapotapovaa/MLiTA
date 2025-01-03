from app.terms import Equal, Var, Not



def test_str():
    assert str(Equal(Var('A'), Var('B'))) == 'A = B'


def test_str_with_not():
    assert str(Equal(Var('A'), Not(Var('B')))) == 'A = !B'


def test_repr():
    assert repr(Equal(Var('A'), Var('B'))) == "Equal(Var('A'), Var('B'))"


def test_humanize():
    assert Equal(Var('A'), Var('B')).humanize() == 'A эквивалентно B'


def test_complex_humanize():
    eq = Equal(Equal(Var('A'), Var('B')), Equal(Var('C'), Var('D')))
    assert eq.humanize() == '(A эквивалентно B) эквивалентно (C эквивалентно D)'


def test_not_humanize():
    eq = Equal(Not(Var('A')), Var('B'))
    assert eq.humanize() == 'не A эквивалентно B'


def test_to_implication_view():
    assert (
        str(Equal(Var('A'), Var('B')).to_implication_view())
        == '!((A > B) > !(B > A))'
    )

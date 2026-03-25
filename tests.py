import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points_raises():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)


def test_add_choice_assigns_incremental_ids():
    question = Question(title='q1')

    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')

    assert [c1.id, c2.id, c3.id] == [1, 2, 3]


def test_add_choice_with_empty_text_raises():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')


def test_add_choice_with_text_longer_than_100_raises():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)


def test_remove_choice_by_id_removes_only_target_choice():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')

    question.remove_choice_by_id(c1.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == c2.id
    assert question.choices[0].text == 'b'


def test_remove_choice_by_invalid_id_raises():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)


def test_remove_all_choices_clears_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert question.choices == []


def test_set_correct_choices_marks_selected_ids_as_correct():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')

    question.set_correct_choices([c1.id, c3.id])

    assert c1.is_correct is True
    assert c2.is_correct is False
    assert c3.is_correct is True


def test_set_correct_choices_with_invalid_id_raises():
    question = Question(title='q1')
    c1 = question.add_choice('a')

    with pytest.raises(Exception):
        question.set_correct_choices([c1.id, 999])


def test_correct_selected_choices_returns_only_correct_selected_ids():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('a', is_correct=True)
    c2 = question.add_choice('b', is_correct=False)
    c3 = question.add_choice('c', is_correct=True)

    result = question.correct_selected_choices([c1.id, c2.id])

    assert result == [c1.id]

@pytest.fixture
def multiple_choice_question():
    question = Question(title='Capital of France', max_selections=2)
    c1 = question.add_choice('Paris', is_correct=True)
    c2 = question.add_choice('Lyon', is_correct=False)
    c3 = question.add_choice('Marseille', is_correct=False)
    c4 = question.add_choice('Nice', is_correct=False)
    return question, c1, c2, c3, c4


def test_fixture_question_has_expected_structure(multiple_choice_question):
    question, c1, c2, c3, c4 = multiple_choice_question

    assert question.title == 'Capital of France'
    assert question.max_selections == 2
    assert len(question.choices) == 4
    assert c1.is_correct is True
    assert [c.id for c in question.choices] == [1, 2, 3, 4]


def test_fixture_correct_selected_choices_uses_reused_question(multiple_choice_question):
    question, c1, c2, c3, c4 = multiple_choice_question

    result = question.correct_selected_choices([c1.id, c2.id])

    assert result == [c1.id]
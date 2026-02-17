import pytest
from model import Question, Choice

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
    

# ---

#1
def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    
    assert len(question.choices) == 2
    assert question.choices[0].text == 'a'
    assert question.choices[1].text == 'b'
    
    assert question.choices[0].is_correct == False
    assert question.choices[1].is_correct == True

#2
def test_remove_choice_by_id():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    
    question.remove_choice_by_id(1)
    
    assert len(question.choices) == 1
    assert question.choices[0].text == 'b'

#3
def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

#4
def test_select_correct_choices():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', True)
    
    selected = question.select_choices([choice1.id, choice3.id])
    
    assert selected == [choice1.id, choice3.id]

#5
def test_set_correct_choices():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', False)
    
    question.set_correct_choices([choice1.id, choice3.id])
    
    assert [True, False, True] == [choice1.is_correct, choice2.is_correct, choice3.is_correct]

#6
def test_get_invalid_id():
    question = Question(title='q1')
    question.add_choice('a', False)
    
    with pytest.raises(Exception):
        question._choice_by_id('invalid_id')
     
#7
def test_remove_invalid_id():
    question = Question(title='q1')
    question.add_choice('a', False)
    
    with pytest.raises(Exception):
        question.remove_choice_by_id('2')
        
#8
def test_error_max_selections():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', False)
    
    with pytest.raises(Exception) as e:
        question.select_choices([choice1.id, choice2.id, choice3.id])
    
    assert str(e.value) == 'Cannot select more than 2 choices'
    
#9
def test_error_long_choice_text():
    with pytest.raises(Exception) as e:
        Choice(0, "abc" * 300)
    
    assert str(e.value) == 'Text cannot be longer than 100 characters'
    
#10
def test_error_empty_text():
    with pytest.raises(Exception) as e:
        Choice(0, text="")
    
    assert str(e.value) == 'Text cannot be empty'
    
#11
def test_error_too_much_points_in_question():
    with pytest.raises(Exception) as e:
        Question(title="q1", points=101)
    
    assert str(e.value) == 'Points must be between 1 and 100'
    
#---

@pytest.fixture
def question_with_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', False)
    return question

def test_add_choice_fixture(question_with_choices):
    question_with_choices.add_choice('d', True)
    
    assert len(question_with_choices.choices) == 4
    assert question_with_choices.choices[2].text == 'c'
    assert question_with_choices.choices[3].is_correct
    
def test_set_correct_fixture(question_with_choices):
    question_with_choices.set_correct_choices([1, 2])
    
    assert len(question_with_choices.choices) == 3
    assert question_with_choices.choices[0].is_correct
    assert question_with_choices.choices[1].is_correct

def test_remove_all_fixture(question_with_choices):
    assert len(question_with_choices.choices) == 3
    
    question_with_choices.remove_all_choices()
    
    assert len(question_with_choices.choices) == 0
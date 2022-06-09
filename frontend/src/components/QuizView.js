import React, { Component } from 'react';
import $ from 'jquery';
import { Link } from "react-router-dom";
import '../stylesheets/QuizView.css';

const questionsPerPlay = 5;

class QuizView extends Component {
  constructor(props) {
    super();
    this.state = {
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      categories: [],
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false,
      playerName: '',
    };
  }

  componentDidMount() {
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({ categories: result.categories });
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again');
        return;
      },
    });
  }

  selectCategory = ({ type, id = 0 }) => {
    this.setState({ quizCategory: { type, id } }, this.getNextQuestion);
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  getNextQuestion = () => {
    const previousQuestions = [...this.state.previousQuestions];
    if (this.state.currentQuestion.id) {
      previousQuestions.push(this.state.currentQuestion.id);
    }

    $.ajax({
      url: '/quizzes', //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: this.state.quizCategory,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false : true,
        }, () => {
          if (this.state.forceEnd) this.submitToLeaderBoard();
        });
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again');
        return;
      },
    });
  };

  submitToLeaderBoard = () => {
    $.ajax({
      url: '/leaderboard', //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        name: this.state.playerName,
        score: this.state.numCorrect,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          numCorrect: 0,
          playerName: '',
        });
        return;
      },
      error: (error) => {
        alert('Unable to submit score. Please try your request again');
        return;
      }
    });
  }

  submitPlayerName = (event) => {
    const name = document.getElementById('player-name').value;
    this.setState({ playerName: name });
  }

  submitGuess = (event) => {
    event.preventDefault();
    let evaluate = this.evaluateAnswer();
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true,
    });
  };

  restartGame = () => {
    this.setState({
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false,
    });
  };

  renderPrePlay() {
    return ( 
    <div className='quiz-play-holder'>
        {this.state.playerName ? (<> <div className='choose-header'>Choose Category</div>
        <div className='category-holder'>
          <div className='play-category' onClick={this.selectCategory}>
            ALL
          </div>
          {this.state.categories.map(cateogry => {
            return (
              <div
                key={cateogry.id}
                value={cateogry.id}
                className="play-category"
                onClick={() => this.selectCategory(cateogry)}
              >
                {cateogry.type}
              </div>
            );
          })}
        </div> </>) : (
          <div className='player-name-holder'>
            <div className='player-name-header'>Enter your name to play</div>
            <div className='player-name-input'>
              <input id='player-name' type='text' name='playerName' />
              <button className='player-btn' onClick={this.submitPlayerName}>Submit</button>
            </div>
          </div>
        )}
      </div>
      ) 
  }

  renderFinalScore() {
    return (
      <div className='quiz-play-holder'>
        <div className='final-header'>
          Your Final Score is {this.state.numCorrect}
          <p>
						<Link to="leaderboard">
							See where you rank in the leaderboard.{" "}
						</Link>{" "}
					</p>
        </div>
        <div className='play-again button' onClick={this.restartGame}>
          Play Again?
        </div>
      </div>
    );
  }

  evaluateAnswer = () => {
    const formatGuess = this.state.guess
      // eslint-disable-next-line
      .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, '')
      .toLowerCase();
    const answerArray = this.state.currentQuestion.answer
      .toLowerCase()
      .split(' ');
    return answerArray.every((el) => formatGuess.includes(el));
  };

  renderCorrectAnswer() {
    let evaluate = this.evaluateAnswer();
    return (
      <div className='quiz-play-holder'>
        <div className='quiz-question'>
          {this.state.currentQuestion.question}
        </div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>
          {evaluate ? 'You were correct!' : 'You were incorrect'}
        </div>
        <div className='quiz-answer'>{this.state.currentQuestion.answer}</div>
        <div className='next-question button' onClick={this.getNextQuestion}>
          {' '}
          Next Question{' '}
        </div>
      </div>
    );
  }

  renderPlay() {
    return this.state.previousQuestions.length === questionsPerPlay ||
      this.state.forceEnd ? (
      this.renderFinalScore()
    ) : this.state.showAnswer ? (
      this.renderCorrectAnswer()
    ) : (
      <div className='quiz-play-holder'>
        <div className='quiz-question'>
          {this.state.currentQuestion.question}
        </div>
        <form onSubmit={this.submitGuess}>
          <input type='text' name='guess' onChange={this.handleChange} />
          <input
            className='submit-guess button'
            type='submit'
            value='Submit Answer'
          />
        </form>
      </div>
    );
  }

  render() {
    return this.state.quizCategory ? this.renderPlay() : this.renderPrePlay();
  }
}

export default QuizView;

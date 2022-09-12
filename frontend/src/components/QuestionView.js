import React, { Component } from "react";
import "../stylesheets/App.css";
import Question from "./Question";
import Search from "./Search";
import $ from "jquery";
import { Bars } from "react-loader-spinner";
import art from "../assets/art.svg";
import science from "../assets/science.svg";
import sports from "../assets/sports.svg";
import geography from "../assets/geography.svg";
import history from "../assets/history.svg";
import entertainment from "../assets/entertainment.svg";

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: null,
      loading: true,
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `https://general-trivia-api.herokuapp.com/questions?page=${this.state.page}`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
          loading: false,
        });
        return;
      },
      error: (error) => {
        alert("Unable to load questions. Please try your request again");
        return;
      },
    });
  };

  selectPage(num) {
    window.scrollTo(0, 10);
    this.setState({ page: num }, () => this.getQuestions());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? "active" : ""}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (id) => {
    $.ajax({
      url: `https://general-trivia-api.herokuapp.com/categories/${id}/questions`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
          loading: false,
        });
        return;
      },
      error: (error) => {
        alert("Unable to load questions. Please try your request again");
        return;
      },
    });
  };

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `https://general-trivia-api.herokuapp.com/questions`, //TODO: update request URL
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({ searchTerm: searchTerm }),
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
          loading: false,
        });
        return;
      },
      error: (error) => {
        alert("Unable to load questions. Please try your request again");
        return;
      },
    });
  };

  questionAction = (id) => (action) => {
    if (action === "DELETE") {
      if (window.confirm("are you sure you want to delete the question?")) {
        $.ajax({
          url: `https://general-trivia-api.herokuapp.com/questions/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert("Unable to load questions. Please try your request again");
            return;
          },
        });
      }
    }
  };

  getImage = (category) => {
    switch (category) {
      case "Art":
        return art;
      case "Entertainment":
        return entertainment;
      case "Geography":
        return geography;
      case "History":
        return history;
      case "Science":
        return science;
      case "Sports":
        return sports;
      default:
        return null;
    }
  };

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul className="question-category">
            {this.state.categories.map((category) => (
              <li
                className="category-item"
                key={category.id}
                onClick={() => {
                  this.getByCategory(category.id);
                }}
              >
                {category.type}
                <img
                  className="category"
                  alt={`${category.type}`}
                  src={this.getImage(category.type)}
                />
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch} />
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.loading ? (
            <div className="flex-center">
              <Bars color="#ffb703" height={80} width={80} />
            </div>
          ) : (
            this.state.questions.map((q, ind) => (
              <Question
                key={q.id}
                question={q.question}
                answer={q.answer}
                category={
                  this.state.categories.filter(
                    (c) => c.id === Number(q.category)
                  )[0].type
                }
                difficulty={q.difficulty}
                questionAction={this.questionAction(q.id)}
                getImage={this.getImage}
              />
            ))
          )}

          <div className="pagination-menu">{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;

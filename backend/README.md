# Backend - Trivia Game API

## Introduction
This API allows any frontend application to run a trivia game based on the questions provided.

## Getting Started
This API is not deployed yet. You will have to run it locally by using the steps provided in this [README.md file](./Readme.md). <br/>
**BASE URL**: `http://localhost:5000`

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: bad request
- 404: resource not found
- 405: method not allowed
- 422: unprocessable
- 500: internal server error

### Endpoints 
The API has the following endpoints:
### Categories
- `GET /categories`: returns a list of all categories

#### Query Parameters
This endpoint takes no query parameters.

#### Request Body
This endpoint takes no request body.

#### Sample Request
`curl http://localhost:5000/categories`

#### Sample Response
```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true,
  "total_categories": 6
}
```

### `GET /categories/{category_id}/questions`
This returns a list of questions for a given category.

#### Query Parameters
This endpoint takes the following query parameters:
- `category_id`: the id of the category

#### Request Body
This endpoint takes no request body.

#### Sample Request
`curl http://localhost:5000/categories/1/questions`

#### Sample Response
- `questions`: array - All questions within the specified category. <br>
- `totalQuestions`: int - Total number of questions within specified category. <br> 
```
{
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "Geography",
      "difficulty": "easy"
    },
    {
      "id": 2,
      "question": "What is the capital of Germany?",
      "answer": "Berlin",
      "category": "Geography",
      "difficulty": "easy"
    },
    {
      "id": 3,
      "question": "What is the capital of Italy?",
      "answer": "Rome",
      "category": "Geography",
      "difficulty": "easy"
    }
  ]
  "success": true,
  "total_questions": 3
}
```

### Questions

### `GET /questions`
This returns a paginated list of questions. Each page contains 10 questions.

#### Query Parameters
- `page`: int - The page number to return.

#### Request Body
This endpoint takes no request body.

#### Sample Request
`curl http://localhost:5000/questions?page=1`

#### Sample Response
- `questions`: array - Fetched questions. <br>
- `totalQuestions`: int - Total number of questions in the database. <br>

```
{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "categories" : {
    "1": "Science",
    "2", "Art",
    "3": "History"
   },
  "totalQuestions": 2
}
```

### `POST /questions`
This endpoint allows you to add a new question to the database. It requires the following:
- `question`: string - The question text.
- `answer`: string - The correct answer.
- `category`: int - The category id.
- `difficulty`: string - The difficulty level of the question.

#### Query Parameters
This endpoint takes no query parameters.

#### Request Body
This endpoint takes the following request body:
```
{
  "question": "What is the capital of France?",
  "answer": "Paris",
  "category": "Geography",
  "difficulty": "easy"
}
```

#### Sample Request
`curl -X POST -H "Content-Type: application/json" -d '{"question": "What is the capital of France?", "answer": "Paris", "category": "Geography", "difficulty": "easy"}' http://localhost:5000/questions`

#### Sample Response
```
{
  "success": true,
  "message": "Question added successfully"
}
```

### `POST /questions` (Search)
This endpoint allows you to search for questions based on a search term which is case insensitive. It requires the following:
- `searchTerm`: string - The search term.

#### Query Parameters
This endpoint takes no query parameters.

#### Request Body
This endpoint takes the following request body:
```
{
  "searchTerm": "What is the capital of France?"
}
```
#### Sample Request
`curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "What is the capital of France?"}' http://localhost:5000/questions`

#### Sample Response
```
{
  "questions": [
    {
      "answer": "Paris",
      "category": "Geography",
      "difficulty": "easy",
      "id": 1,
      "question": "What is the capital of France?"
    }
  ]
  "success": true,
  "total_questions": 1
  "current_Category": "Geography"
}
```

### `DELETE /questions/{question_id}`
This endpoint allows you to delete a question from the database.

#### Query Parameters
This endpoint takes the following query parameter:
- `question_id`: int - The id of the question to delete.

#### Request Body
This endpoint takes no request body.

#### Sample Request
`curl -X DELETE -H "Content-Type: application/json" http://localhost:5000/questions/1`

#### Sample Response
```
{
  "success": true,
  "message": "Question deleted successfully"
}
```

### Quizzes

### `POST /quizzes`
This returns a random question from the database within a specified category or from a random category if none is specified. It accepts an array of previous questions to ensure that a question that has been chosen before is not chosen again. If there are no other questions to left, it returns null.

#### Query Parameters
This endpoint takes no query parameters.

#### Request Body
This endpoint takes the following request body:
- `previous_questions`: array <small> (required) </small> - Contains ids of previously chosen questions. <br>
- `quiz_category`: object <small> (optional) </small> - Current category. <br>
```
{
  "previous_questions": [
    1,
    2,
    3
  ],
  "quiz_category": {
    "id": 3,
    "type": "History"
  }
}
```

#### Sample Request
`curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 2, 3], "quiz_category": '{"id":3, "type": "History"}'}' http://localhost:5000/quizzes`

#### Sample Response
`question`: object|null - randomly chosen question. <br>
```
{
  "question": {
    "category": "Geography",
    "correct_answer": "Paris",
    "difficulty": "easy",
    "id": 1,
    "question": "What is the capital of France?"
  },
  "success": true
}
```

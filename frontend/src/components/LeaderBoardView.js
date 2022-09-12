import React, { Component } from "react";
import { Link } from "react-router-dom";
import $ from "jquery";
import "../stylesheets/LeaderboardView.css";
import { Bars } from  'react-loader-spinner';

class LeaderboardView extends Component {
	constructor() {
		super();
		this.state = {
			results: [],
			page: 1,
			totalResults: 0,
			loading: true,
		};
	}

	componentDidMount() {
		this.getResults();
	}

	getResults = () => {
		$.ajax({
			url: `https://general-trivia-api.herokuapp.com/leaderboard?page=${this.state.page}`,
			type: "GET",
			success: (result) => {
				this.setState({
					results: result.results,
					totalResults: result.totalResults,
					loading: false,
				});
				return;
			},
			error: (error) => {
				alert("Unable to load scores. Please try your request again");
				return;
			},
		});
	};

	selectPage(num) {
		this.setState({ page: num }, () => this.getResults());
	}

	createPagination() {
		let pageNumbers = [];
		let maxPage = Math.ceil(this.state.totalResults / 10);
		for (let i = 1; i <= maxPage; i++) {
			pageNumbers.push(
				<span
					key={i}
					className={`page-num pointer-cursor ${
						i === this.state.page ? "active" : ""
					}`}
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

	render() {
		return (
			<div className="leaderboard-view">
				{this.state.loading ? <div className='flex-center'><Bars color="#ffb703" height={80} width={80} /></div> : this.state.results.length ? (
					<>
					<h1>Leaderboard</h1>
					<table>
						<thead>
							<tr>
								<th> Player</th>
								<th> Score</th>
							</tr>
						</thead>
						
						<tbody>
						{this.state.results.map((result, index) => (
							<tr key={index}>
								<td> {result.player} </td>
								<td> {result.score} </td>
							</tr>
						))}
						</tbody>	
					</table>
					</>
				) : (
					<p>
						There are no scores to display.
						<Link to="play">Play the trivia game here. </Link>
					</p>
				)}

				<div className="pagination-menu">{this.createPagination()}</div>
			</div>
		);
	}
}

export default LeaderboardView;
import React, { Component, PropTypes } from 'react';

export default class PoolEventForm extends Component {
  static propTypes = {
    gameshow: PropTypes.object.isRequired,
    createEvent: PropTypes.func.isRequired,
  };

  state = {
    title: null,
    date: null,
    date_performed: null,
    choices: null,
    matches_team: false,
  };

  bind(name) {
    return (e) => {
      this.setState({[name]: e.target.value});
    };
  }

  onSubmit = (e) => {
    e.preventDefault();
    this.props.createEvent(this.state);
  };

  render() {
    const { gameshow } = this.props;
    return (
      <form onSubmit={this.onSubmit}>
        <input placeholder="Title"
               onChange={this.bind('title')}
               required />
        <input placeholder="Date"
               onChange={this.bind('date')}
               required />
        <input placeholder="Date performed"
               onChange={this.bind('date_performed')}
               required />
        <input placeholder="Number of choices"
               onChange={this.bind('choices')}
               required />
        <label>
          <input onChange={this.bind('matches_team')}
                 type="checkbox" />
          Match team?
        </label>
        <button type="submit">Submit</button>
      </form>
    );
  }
}

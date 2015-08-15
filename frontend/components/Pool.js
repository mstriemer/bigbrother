import React, { Component, PropTypes } from 'react';
import PoolEventForm from './PoolEventForm';

function formatEvent(event) {
  let { id, choices, title } = event;
  let choicesText = choices === 1 ? 'choice' : 'choices';
  return <li key={id}>{title} ({choices} {choicesText})</li>;
}

export default class Pool extends Component {
  static propTypes = {
    gameshow: PropTypes.object.isRequired,
    events: PropTypes.array.isRequired,
    createEvent: PropTypes.func.isRequired,
  };

  render() {
    const { gameshow, events, createEvent } = this.props;
    return (
      <div className="pool">
        <nav className="nav">
          <h1>{gameshow.title}</h1>
        </nav>
        <PoolEventForm gameshow={gameshow} createEvent={createEvent} />
        <ul>
          {events.map(formatEvent)}
        </ul>
      </div>
    );
  }
}

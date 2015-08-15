import React, { Component } from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'redux/react';
import Pool from '../components/Pool';
import * as PoolActions from '../actions/PoolActions';

@connect(state => ({
  gameshow: state.gameshow,
  events: state.events,
}))
export default class PoolApp extends Component {
  render() {
    const { gameshow, events, dispatch } = this.props;
    return (
      <Pool gameshow={gameshow} events={events}
            {...bindActionCreators(PoolActions, dispatch)} />
    );
  }
}

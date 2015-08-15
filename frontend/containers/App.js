import React, { Component } from 'react';
import PoolApp from './PoolApp';
import { createRedux } from 'redux';
import { Provider } from 'redux/react';
import * as stores from '../stores';

const redux = createRedux(stores);
let gameshow = {
    title: 'Big Brother 17',
    slug: 'bb-17',
}

export default class App extends Component {
  render() {
    return (
      <Provider redux={redux}>
        {() => <PoolApp gameshow={gameshow} />}
      </Provider>
    );
  }
}

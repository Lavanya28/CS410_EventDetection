import React, { Component } from 'react';

import Header from '../Header/';
import Navigation from '../Navigation/';

class App extends Component {
  render() {
    return (
      <div
        className="App"
      >
        <Header />
        <Navigation />
      </div>
    );
  }
}

export default App;


import React, { Component } from 'react';
import { Segment } from 'semantic-ui-react'
import './styles.scss';

class Canvas extends Component {
  render() {
    return (
      <Segment raised className="Navigation">
        <img src="plots/fash.png" alt="plot" />
      </Segment>
    );
  }

}
export default Canvas;

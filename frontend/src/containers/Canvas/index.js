import React, { Component } from 'react';
import { Segment } from 'semantic-ui-react'
import './styles.scss';

class Canvas extends Component {
  render() {
    const {
      path,
      title,
    } = this.props;

    console.log(path)

    return (
      <Segment raised className="Navigation">
        <div className="Canvas-title-container">
          <div className="Canvas-title">{title}</div>
        </div>
        <img className="Canvas-image" key={path} src={path} alt={path} />
      </Segment>
    );
  }

}
export default Canvas;

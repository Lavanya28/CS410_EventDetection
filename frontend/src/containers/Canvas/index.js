import React, { Component } from 'react';
import { Segment,Label } from 'semantic-ui-react'
import './styles.scss';

class Canvas extends Component {
  render() {
    const {
      path,
      title,
      hashtags,
      selection,
    } = this.props;
    console.log(hashtags);
    console.log(typeof hashtags);

    const spikeView = (
      <div>
        <div className="Canvas-title-container">
          <div className="Canvas-title">{title}</div>
        </div>
        <img key={path} src={path} alt={path} />
      </div>
    );

    const eventView = (
      <div className="Canvas-event">
        {hashtags.map((hashtag, idx) => (
          <div key={idx} className="Canvas-hashtag">
          	<Label className="eventLabel" as='a' tag size="small">
       			{hashtag}
      		</Label>
            
          </div>
        ))}
      </div>
    );

    const topicView = (
      <div className="Canvas-event">
        <img className="Canvas-image1" src="topic_graph.jpg" />
        <img className="Canvas-image2" src="topics.jpg" />
      </div>
    );

    let view = spikeView;
    if (selection === "events") {
      view = eventView;
    } else if (selection === "topics") {
      view = topicView;
    }

    return (
      <Segment raised className="Navigation">
        {view}
      </Segment>
    );
  }

}
export default Canvas;

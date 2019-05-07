import React, { Component } from 'react';

import api from '../../api';

class Navigation extends Component {
  constructor(props) {
    super(props);

    this.state = {
      hashtags: [],
    }
  }

  getHashtags = () => {
    api.getHashtags()
      .then(response => {
        this.setState({ hashtags: response.data });
      });
  };

  render() {
    const { hashtags } = this.state;

    return (
      <div
        className="Navigation"
      >
        <div className="Navigation-buttons">
          <button
            type="button"
            onClick={this.getHashtags}
          >
            Top trending hashtags
          </button>
          <button
            type="button"
          >
            Top trending word
          </button>
          <button
            type="button"
          >
            Top trending word-pairs
          </button>
        </div>
        <div className="Navigation-options">
          {hashtags.map((hashtag, idx) => (
            <div id={idx}>
              {hashtag[0]}
            </div>
          ))}
        </div>
      </div>
    );
  }
}

export default Navigation;

